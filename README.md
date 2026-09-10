# Building an LLM From Scratch

This repository follows a language model from count tables to a small
decoder-only Transformer. Each concept is introduced with the smallest example
that can be inspected by hand, then implemented on a larger dataset.

## Episode 01 — The smallest language model

Episode 01 builds a character bigram model from the training names `anna` and
`ava`. It covers token boundaries, counts, normalization, generation, held-out
evaluation, negative log-likelihood, baselines, smoothing, and the limits of
one-character context.

- [Technical handout (PDF)](docs/episode-01-theory.pdf)
- [Editable presenter canvas](canvas/episode_01_presenter.excalidraw)
- [Presenter canvas, one frame per page (PDF)](docs/episode-01-canvas.pdf)
- [Presenter guide](canvas/EPISODE_01_PRESENTER_GUIDE.md)
- [YouTube upload metadata](youtube/EPISODE_01_METADATA.md)
- [Coding notebook: build a name generator](episodes/01_names/episode_01.ipynb)
- [Coding setup and verified results](episodes/01_names/README.md)
- [Short code companion guide](episodes/01_names/CODE_GUIDE.md)
- [Coding presenter walkthrough](episodes/01_names/PRESENTER_GUIDE.md)

The worked model uses rows `[START, a, n, v]` and next-token outcomes
`[a, n, v, END]`. The complete held-out path `ana` has probability `1/16`, or
`0.0625`, and average NLL `0.693147` nats per prediction.

## Episode 02 — Trigrams and the sparsity wall

Episode 02A theory materials and a separate coding companion:

- [Theory companion guide (PDF)](docs/episode-02-theory.pdf)
- [Canvas: one frame per page (PDF)](docs/episode-02-canvas.pdf)
- [YouTube release metadata](youtube/EPISODE_02A_METADATA.md)

- [Theory reference: worked arithmetic, sparsity, and practical responses](EPISODE_02_THEORY.md)
- [Theory presentation: 29 frames](canvas/episode_02_theory.html)
- [Presenter guide: narration, cues, and timing](canvas/EPISODE_02_CANVAS_GUIDE.md)
- [Editable trigram canvas](canvas/episode_02_trigrams.excalidraw)
- [Pure-Python lab and verified validation results](episodes/02_trigrams/README.md)
- [Coding-video plan](episodes/02_trigrams/CODING_VIDEO_PLAN.md)
- [Understanding checks](episodes/02_trigrams/EXERCISES.md)
- [Separate answer key](episodes/02_trigrams/ANSWERS.md)

The theory explains the mechanism with hand-counted examples, then introduces
smoothing, backoff, interpolation, and representation sharing. The separate
coding video measures the tradeoff on Episode 01's data. Its current lab reports
validation results; the test set remains reserved for the coding release.

## Repository map

- `docs/` — audience handouts and reproducible PDF sources
- `canvas/` — Excalidraw files, generators, and presenter notes
- `youtube/` — titles, descriptions, chapters, and thumbnail assets
- `EPISODE_01_THEORY.md` — detailed development reference
- `SERIES_PLAN.md` — scope and sequence for the full series

See [RESEARCH_STANDARD.md](RESEARCH_STANDARD.md) for the evidence and citation
policy used throughout the series.
