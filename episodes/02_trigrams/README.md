# Episode 02 · Coding companion and experiment

Start with [the theory reference](../../EPISODE_02_THEORY.md). It develops the
intuition, works through the arithmetic, and links the authoritative readings.
For a visual route, open [the 29-frame theory presentation](../../canvas/episode_02_theory.html)
or [the editable Excalidraw canvas](../../canvas/episode_02_trigrams.excalidraw).
Then attempt [the exercises](EXERCISES.md); [the answers](ANSWERS.md) are separate.

The experiment below belongs to the separate **coding video**. It is not
required for presenting the theory. See [the coding-video plan](CODING_VIDEO_PLAN.md)
and [the theory presenter guide](../../canvas/EPISODE_02_CANVAS_GUIDE.md).

## Run the lab

From the repository root, with Python 3.11 or newer:

```bash
# First: verify the anna / ava arithmetic.
python3 episodes/02_trigrams/lab.py --toy

# Second: compare longer contexts on the real names dataset.
python3 episodes/02_trigrams/lab.py --experiment

# Optional: save a new report without replacing the reference.
python3 episodes/02_trigrams/lab.py --experiment --output /tmp/episode-02-study.json

# Check the concepts implemented by the lab.
python3 -m unittest discover -s episodes/02_trigrams -p 'test_*.py' -v
```

The repository's `.venv/bin/python` also works. No packages or downloads are
needed: the model, experiment, and tests use the Python standard library and
Episode 01's bundled dataset. Verified with Python 3.14.2.

## Read the code in this order

| Function | Question to answer before moving on |
|---|---|
| `windows` | Why does each name produce length+1 targets, even with five START pads? |
| `CountModel.__init__` | What do the outer tuple key and inner target key represent? |
| `probability` | What changes between a zero count in an observed row and an absent row? |
| `evaluate` | Why do we feed in real history and include END in the denominator? |
| `generate` | How does the context shift after a sampled token? |
| `experiment` | Which decisions use validation, and what remains reserved? |

Try writing `windows` yourself before opening its implementation. It is the
main change from the previous episode. Generalizing from two context tokens
to m tokens is a loop/indexing change; it does not change the learning objective.

## Verified validation experiment

The same 29,494 unique names as Episode 01; split sizes 23,595 / 2,949 / 2,950
using shuffle seed 42. Training defines 26 ordinary characters and 27 next-token
outcomes. Every row below scores the same **21,141 validation predictions**.
NLL is total negative natural-log probability divided by all predicted
characters plus one END per name. START padding is not scored.

| Context characters | Selected k | Training NLL | Validation NLL ↓ | Observed rows | Rows seen once | Validation predictions with unseen context |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 0.3 | 2.453138 | 2.456622 | 27 | 0 | 0 |
| 2 | 0.3 | 2.197541 | 2.233214 | 592 | 57 | 8 |
| 3 | 0.1 | 1.924842 | 2.126903 | 5,402 | 1,197 | 176 |
| 4 | 0.1 | 1.762922 | 2.196154 | 20,067 | 8,581 | 1,153 |
| 5 | 0.1 | 1.750099 | 2.386382 | 36,171 | 21,379 | 2,746 |

“Rows seen once” means total training evidence for the context equals one,
not that the row has only one distinct next-token type. “Unseen context” counts
prediction occurrences, not distinct contexts. Positive smoothing makes those
predictions scoreable, but does not make their contexts observed.

Each model selects k from `[0.001, 0.01, 0.03, 0.1, 0.3, 1, 3, 10, 100]` using
validation only. These are the best of the tested candidates. The report also
contains unsmoothed training/evaluation diagnostics and all validation sweeps.
The test set was not scored. Do not compare this table's validation numbers
against Episode 01's **test** number 2.460499.

What the measurements support:

- Trigrams improve substantially over bigrams on this split.
- Three characters of context give the lowest validation loss in this grid.
- Four and five characters improve selected-k training fit while validation
  loss rises; the unseen-context and singleton counts expose thinning evidence.
- This experiment measures plain add-k count models. It does not establish the
  limit of backoff, interpolation, or other classical smoothing methods.

## Inspect generation without cherry-picking

[The saved JSON report](outputs/study_results.json) includes the first 12
samples from each model, with seed 2026. `ended: false` means the 24-step cap
was reached, not that the model predicted END. `in_training` identifies exact
training spellings. Empty strings are allowed because smoothed start rows can
predict END. Samples illustrate behavior; use held-out loss for the numerical
comparison. Exact random samples may depend on Python version.

## What is ready

- A theory reference, 29-frame recording canvas, and presenter narration.
- A runnable lab reproducing the toy arithmetic and comparing contexts 1–5.
- Exercises, a separate answer key, twelve passing concept/material tests, and saved
  numerical evidence with dataset checksum and runtime details.

The theory has its own recording sequence above. The coding notebook and full
coding release remain a later step, including the series' final test evaluation
after choices are frozen.
