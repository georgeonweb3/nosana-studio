#!/usr/bin/env python3
"""Nosana Studio runner — validate and deploy the job pack on Nosana.

Stdlib only. No dependencies, runs anywhere Python 3 does (including Termux).

Commands:
  python3 studio.py validate            Local structural validation of every job
                                        definition in jobs/. No network, no account.
                                        This checks OUR files are well formed; it
                                        does NOT claim a deployment happened.
  python3 studio.py markets             Print the GPU markets we use, from the
                                        live snapshot in markets-selected.json.
  python3 studio.py deploy <job>        Create a real deployment through the
                                        Nosana API. Needs NOSANA_API_KEY in the
                                        environment (from deploy.nosana.com ->
                                        Account). <job> is one of: whisper, flux,
                                        qwen, h3-video.
  python3 studio.py status <id>         Poll a deployment by id.

Costs: deployments bill prepaid Nosana credits per second at the market rate.
Live base rates are snapshotted in markets-selected.json (checked 2026-11-11).
"""
import json
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
API = "https://api.nosana.com"

# job name -> (file, market address, timeout seconds, note)
# Market addresses verified live 2026-11-11 via GET api.nosana.com/markets/prices.
MARKET_3090 = "CA5pMpqkYFKtme7K31pNB1s62X2SdhEv1nN9RdxKCpuQ"   # NVIDIA 3090, $0.192/h base
MARKET_5090 = "6Xt8hgVLLL2PSHC9NtJP8E8oTdA5ZJc95hZEnHcdqKqb"   # NVIDIA 5090, $0.500/h base
JOBS = {
    "whisper":  ("jobs/whisper.json", MARKET_3090, 3600,
                 "Whisper ASR service (Gradio :7860) for transcription jobs"),
    "flux":     ("jobs/comfyui-flux.json", MARKET_3090, 3600,
                 "ComfyUI + FLUX.1 image generation (:8188)"),
    "qwen":     ("jobs/qwen-9b.json", MARKET_3090, 3600,
                 "Qwen3.5-9B via Ollama, OpenAI-compatible endpoint (:11434)"),
    "h3-video": ("jobs/minimax-h3-i2v-32gb.json", MARKET_5090, 7200,
                 "MiniMax H3 image-to-video in ComfyUI (:8188). Needs a Blackwell "
                 "GPU (5090) for the nvfp4 text encoder; first start downloads "
                 "44-55 GB of weights, hence the 2h timeout."),
}


def load_job(name):
    path = os.path.join(ROOT, JOBS[name][0])
    with open(path) as f:
        return json.load(f)


def validate():
    ok = True
    for name in JOBS:
        job = load_job(name)
        problems = []
        if job.get("version") != "0.1":
            problems.append("version is not 0.1")
        if job.get("type") != "container":
            problems.append("type is not container")
        ops = job.get("ops") or []
        if not ops:
            problems.append("no ops")
        for op in ops:
            args = op.get("args", {})
            if not args.get("image"):
                problems.append(f"op {op.get('id')} has no image")
            if "expose" not in args and "exposedPorts" not in str(args):
                problems.append(f"op {op.get('id')} exposes no port")
        req = (job.get("meta", {}).get("system_requirements") or {})
        print(f"{name:9s} ops={len(ops)} vram_req={req.get('vram_total_mb', '-')}MB "
              f"images={[op['args'].get('image') for op in ops]} "
              f"{'OK' if not problems else 'PROBLEMS: ' + '; '.join(problems)}")
        ok = ok and not problems
    print("validate:", "all job definitions well formed" if ok else "FAILED")
    return 0 if ok else 1


def api(path, body=None):
    key = os.environ.get("NOSANA_API_KEY")
    if not key:
        sys.exit("NOSANA_API_KEY is not set. Get it at deploy.nosana.com -> Account "
                 "after signing in, then export it. It is a secret: never commit it.")
    req = urllib.request.Request(
        API + path,
        method="POST" if body is not None else "GET",
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def deploy(name):
    if name not in JOBS:
        sys.exit(f"unknown job {name!r}; choose from {sorted(JOBS)}")
    _, market, timeout, note = JOBS[name]
    body = {
        "name": f"nosana-studio-{name}",
        "market": market,
        "timeout": timeout,
        "replicas": 1,
        "strategy": "SIMPLE",
        "job_definition": load_job(name),
    }
    print(f"Creating deployment: {note}")
    print(f"Market {market}  timeout {timeout}s  (bills credits per second while running)")
    result = api("/deployments/create", body)
    print(json.dumps(result, indent=1))
    print("Record the deployment id, start time and market in RECEIPTS.md.")
    return 0


def status(deployment_id):
    result = api(f"/deployments/{deployment_id}")
    print(json.dumps(result, indent=1))
    return 0


def markets():
    with open(os.path.join(ROOT, "markets-selected.json")) as f:
        for row in json.load(f):
            print(f"{row['name']:45s} ${row['usd_reward_per_hour']:.3f}/h  {row['address']}")
    print("(base reward per hour before network fee; snapshot 2026-11-11, "
          "refresh: curl https://api.nosana.com/markets/prices)")
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "validate"
    if cmd == "validate":
        sys.exit(validate())
    if cmd == "markets":
        sys.exit(markets())
    if cmd == "deploy" and len(sys.argv) == 3:
        sys.exit(deploy(sys.argv[2]))
    if cmd == "status" and len(sys.argv) == 3:
        sys.exit(status(sys.argv[2]))
    print(__doc__)
    sys.exit(2)
