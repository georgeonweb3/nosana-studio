# First-run runbook — the exact sequence once account + credits land

Prereqs (blockers, in order): Nosana Deploy account signed in, credits on the
account (free Builder's Challenge claim or a small top-up), `NOSANA_API_KEY`
exported in the shell that runs studio.py. Dashboard route also works for every
step below: paste the job definition, pick the same market, deploy.

Each run gets a RECEIPTS.md entry BEFORE the next one starts: deployment id,
market, start/stop, billed time, cost, output files, verdict. No receipts, no
claims — that is the whole point of this repo.

## Run 1 — Whisper (proof: transcription accuracy)
1. `python3 studio.py deploy whisper` (RTX 3090 market)
2. Open the service URL (Gradio :7860), upload `audio/narration-ep01-shot02.mp3`.
3. Save the transcript to `results/whisper-ep01-shot02.txt`.
4. Score it against `audio/narration-ep01-shot02.ground-truth.txt` (the manifest's
   real narration line) — count word errors, write the number in RECEIPTS.md.
5. Stop the deployment. Note billed minutes.

## Run 2 — FLUX images (proof: a usable storyboard still)
1. `python3 studio.py deploy flux` (RTX 3090 market)
2. In ComfyUI (:8188), run the FLUX workflow with this fixed prompt:
   "A lone man waiting at a dark Lagos bus stop at night, one hand raised to flag
   a bus that is not coming, warm sodium streetlight, deep shadows, muted teal and
   amber, cinematic digital painting, vertical composition, no text, no watermark"
   (This is the Ep3 'The Man Who Waits' key visual — a real asset if it lands.)
3. Save the best output to `results/flux-man-who-waits.png`.
4. Stop the deployment. Note billed minutes and cost.

## Run 3 — Qwen LLM endpoint (proof: an agent-grade endpoint)
1. `python3 studio.py deploy qwen` (RTX 3090 market)
2. Wait for the health check (/api/tags returns 200), then run three fixed prompts
   (in `results/qwen-prompts.md` once written): a summarisation, a JSON extraction,
   and a code fix. Save raw responses + response times.
3. The proof number: tokens/sec or seconds-per-response per prompt, in RECEIPTS.md.
4. Stop the deployment.

## Run 4 — MiniMax H3 video (proof: motion verdict)
Follow `video/TEST-SHOT-SPEC.md` exactly. RTX 5090 market, 2h timeout.
Test A (phone still) first, then Test B (Tunde face still). Verify frames before
calling anything a success.

## After all four
- Update README status with the real numbers.
- Draft the Build Log Reddit post and the Creation Challenge explainer FROM the
  receipts (hook first, one worked example, one quantified proof point each,
  per the submission standard). Nothing is submitted on drafts alone; George
  approves each before it goes out.
