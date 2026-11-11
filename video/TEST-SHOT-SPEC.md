# MiniMax H3 test shots — edit plan (per George's video standard)

This is a PIPELINE PROOF, not a publishable Wahala episode. Nothing here uploads
anywhere. Its job is to answer one question with evidence: can Nosana's MiniMax H3
lane turn our real Wahala stills into usable motion, at what cost and quality,
compared with the Kaggle Wan lane George already tested?

## Diagnosis
- Type/purpose: engine test, 2 shots x ~5s. Audience: George (decision), then the
  NOSvember Build Log (proof material).
- Emotion/tone: Wahala warm cinematic — tungsten light, deep shadows, teal/amber.
- Key message: a phone-first builder with no GPU animated a real drama still on
  decentralized compute, with the cost printed next to the clip.

## Overall strategy
Image-to-video, first frame pinned to the real episode still. H3 generates motion
AND a soundtrack in one pass (32 kHz stereo). Turbo LoRA settings from the official
template README: 8 steps, cfg 1.0 for I2V. Output 1344x768, 124 frames, 24 fps.

## The shots
- **Test A (safe, object):** `test-assets/shot-01.webp` — the phone lighting up on
  the repair bench (Ep1 hook frame, no face).
  Prompt: "Slow push-in toward the phone as its screen flickers on in the dark
  kiosk, warm bulb swaying almost imperceptibly, dust in the light, cables still,
  cinematic, photorealistic, no camera cuts, no text."
- **Test B (the money test, face):** `test-assets/shot-02.webp` — Tunde holding the
  phone to his ear, eyes wide (Ep1 escalation frame).
  Prompt: "The man's hand trembles slightly as he listens, his breathing quickens,
  eyes dart once toward the door then back, jaw tightens, the warm bulb light
  flickers once, everything else still, cinematic photorealistic performance,
  no camera cuts, no lip movement, no text."
  Face performance is where AI video lanes fail; B is the verdict shot.

## Honest limits, stated before the run
- H3 output is landscape 1344x768. Wahala publishes vertical 1080x1920. A pinned
  vertical first frame will be adapted by the model; expect reframing. If the
  output cannot be cropped to vertical without wrecking the shot, that is a real
  finding against H3 for Shorts, and it goes in the Build Log writeup as-is.
- The 32GB variant needs a Blackwell GPU (RTX 5090 market, $0.500/h base) because
  of its nvfp4 text encoder. First start downloads 44-55 GB of weights before
  ComfyUI opens, so the first session is mostly download time. Budget the test
  at 2h of 5090 time (~$1.00 base) inside the 2h deployment timeout.
- H3 generates its own audio. For drama use the audio is a reference only; the
  series' real sound stays TTS narration + sound design in the drama-layer edit.

## After the run (verification, mandatory)
- ffprobe both outputs (resolution, fps, duration, audio stream present).
- Extract frames at 0s / 2.5s / 5s for A and B; check face identity holds in B
  (same man, no morphing), hand/phone stay coherent, no text artifacts.
- Record in RECEIPTS.md: deployment id, market, wall-clock from deploy to first
  frame, total billed time, cost, and the verdict per shot (usable / insert-only /
  fail) with the frame extracts saved under `video/results/`.
- Decision rule: H3 joins the Wahala lane only if Test B's face holds. Otherwise
  the lane stays Kaggle Wan and H3 is documented as tested-and-rejected, which is
  still a valid Build Log proof point.
