# Nosana Studio — a phone-first GPU job pack for solo AI builders

**Hook:** One public repo of ready-to-run Nosana job definitions that lets a solo builder with no GPU — working from a phone — transcribe audio, generate images and video, and serve an LLM on decentralized GPU compute, paying cents per job instead of renting a cloud box.

## Status (honest, updated as receipts land)
- Scaffold: 2026-11-11. Job definitions vendored from the official `nosana-ci/pipeline-templates` repo (see `jobs/`, each file is the upstream template, unmodified).
- NOT yet deployed. First live run is gated on two blockers, in order:
  1. A Nosana Deploy account (deploy.nosana.com — Google login or Solana wallet).
  2. Credits: claim free Builder's Challenge credits (nosana.com/builders-credits — email + this repo's GitHub link, airdropped twice daily), or a small top-up (card / USDC / NOS).
- First-run receipts (deployment IDs, GPU market, runtime, cost, outputs) go in `RECEIPTS.md` the moment a job actually runs. Nothing in this repo claims a result that has not happened.

## The pack (v1)
| Job | Template image | GPU need | What it does for a solo builder |
|---|---|---|---|
| `jobs/whisper.json` | `registry.hf.space/openai-whisper` (Gradio :7860) | any, 3090 fine | Whisper large transcription for content, interviews, voice notes — the job local phones/VMs do painfully slowly on CPU |
| `jobs/comfyui-flux.json` | `nosana/comfyui:2.0.11` (:8188) | 3090 / 24GB | FLUX.1 image generation for storyboards, thumbnails, character art |
| `jobs/minimax-h3-i2v-32gb.json` | `nosana/comfyui:2.0.11` (:8188) | 32GB+ market | MiniMax H3 image-to-video — animating stills into short drama/content clips |
| `jobs/qwen-9b.json` | `ollama/ollama` (:11434) | 3090 / 24GB | Qwen3.5-9B served as an OpenAI-compatible endpoint an AI agent can call |

Live base prices checked 2026-11-11 via the public Nosana markets API (before network fee): RTX 3060 $0.048/h, RTX 3090 $0.192/h, RTX 5080 $0.200/h, RTX 4090 $0.385/h, RTX 5090 $0.500/h. A one-hour 3090 test session costs roughly twenty cents at base rate.

## Why this exists
The builder behind this works from an Android phone (Termux) and a small cloud VM with no GPU. Kaggle's free 30h/week is the current GPU lifeline for video work and it is rationed, queued and session-based. Nosana is pay-per-second, template-driven and needs no local Docker build for v1 — the dashboard or CLI posts a job definition and a host GPU runs it.

## Entries this feeds (each written separately, per-programme)
- NOSvember Creation Challenge (explainer) — deadline Nov 22, 2026.
- NOSvember Build Log ($500+ pool in $NOS + GPU credits) — Reddit post, deadline Nov 30, 2026.
- Nosana Grants ($5K–$50K, rolling, ~2-week review) — only after live receipts exist.
