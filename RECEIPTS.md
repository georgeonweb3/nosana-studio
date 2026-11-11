# Receipts

Every live run gets an entry here before the next run starts. Empty means not run
yet — this file never describes a result that has not happened.

## Pre-flight checks (done 2026-11-11, no account needed)
- All 4 job definitions validate locally (`python3 studio.py validate`):
  whisper (VRAM req 5120MB), flux (12288MB), qwen (9216MB), h3-video (30720MB).
- Container images exist: `nosana/comfyui:2.0.11` and `ollama/ollama:0.35.1`
  confirmed on Docker Hub (HTTP 200). Whisper image is Nosana's own supported
  template image on the HF Spaces registry.
- GPU market addresses + base prices snapshotted live from
  `api.nosana.com/markets/prices` into `markets-selected.json`:
  RTX 3090 $0.192/h, RTX 5090 $0.500/h (before network fee).

## Live runs
(none yet — gated on the Nosana account sign-in and credits)
