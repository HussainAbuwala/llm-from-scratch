# Episode 03B · Preparation review

Prepared September 30, 2026; recorded release prepared October 1.
Status: recorded and packaged, not yet published. Earlier checks below describe preparation. 03A publication confirmed by the presenter.

## Delivered

- 28-cell notebook (13 code cells), executed in a fresh Jupyter kernel.
- HTML reading copy and reproducible percent-cell source/builder.
- Setup/learning guide, coding presenter walkthrough, exercises and answers.
- Seven coding integration checks alongside the ten existing theory checks.

## Verified results

| Toy setting | Training NLL (nats/prediction) |
|---|---:|
| All-zero scores | 1.386294 |
| Chosen a→END score ln(2) | 1.331437 |
| Chosen a→END score ln(100) | 1.806672 |

Each uses anna/ava, character tokens, START reset per name, END included, and
nine predictions. Values match the independent 03A arithmetic verifier.

The optional real-data extension uses the bundled dataset with its SHA-256
check, sorted unique spellings, seed-42 shuffle, original 80/10/10 split, and
training-only vocabulary/counts. Fixed add-one count probabilities and
constructed log(C+1) weights both give validation NLL **2.456749** across
**21,141 predictions** from **2,949 validation names**, using **23,595 training
names**. No hyperparameter selection or test loss is included.

## Checks performed

- Fresh-kernel execution of every cell, with saved outputs and HTML export.
- All 17 unittest checks passed: boundaries, target indexing, hand arithmetic,
  prediction-weighted loss, softmax stability, count equivalence, sampling ID
  translation, empty END outputs, CAP labeling, and notebook/source agreement.
- `git diff --check` passed.

Initial sandbox execution could not bind Jupyter's local ports; the authorized
run outside that restriction succeeded. No dependencies were installed.

## Scope and recording notes

Established theory and source references remain in EPISODE_03_THEORY.md.
Direct score-row lookup is the required route; one-hot/matrix derivations remain
optional theory references. There is no optimizer, parameter sharing, or longer
context. Hand-chosen changes and count-derived scores are explicitly labeled.
All generated samples are shown in order; seeds are fixed and caps are labeled.

Rehearse pacing and editor font size before recording. The 25–35 minute guide
is a target, not an observed duration. Video chapters, thumbnails, and upload
metadata are future release work once the recording is available.

## October 1 · Visible NumPy operations

Added labeled input/target arrays, stored and gathered score tables, softmax
intermediates and shapes, paired target indices, selected probabilities, and
loss arrays. An optional two-row example illustrates keepdims and broadcasting
without changing the model. Re-executed the notebook in a fresh kernel; all
17 tests and whitespace checks passed.

Section 6 now presents separate softmax-then-log and direct log-softmax
demonstrations using the same scores and target. Outputs show the infinite
versus finite (2000) loss explicitly. Fresh-kernel execution and all 17 tests pass.

## October 1 · Recorded release

The user-edited notebook is preserved byte-for-byte (26 cells, 12 code cells).
The optional real-data extension and extended closing notes were removed by the
presenter. `lesson.py` now matches the notebook; the HTML reading copy was
exported from that notebook. Its generation example remains supplemental to
the recording, which closes after the weight comparison.

A temporary copy executed successfully in a fresh kernel. All 16 remaining
theory/coding checks passed; the removed real-data extension's integration test
was removed with that lesson section. See ../../youtube/EPISODE_03B_RELEASE.md
for video verification, assets, and notebook preservation hash.
