# Episode 03A · Preparation review

Prepared September 28, 2026. Scope: theory learning and rehearsal materials.

## Prepared

- [Theory reference](EPISODE_03_THEORY.md), with prerequisites, established
  concepts, project choices, limitations, authoritative sources and worked math.
- [20-frame presentation](canvas/episode_03_theory.html) and
  [editable canvas](canvas/episode_03_weights.excalidraw).
- [Presenter script](episodes/03_weights/PRESENTER_GUIDE.md): 2,106 scripted
  words; approximately 32 minutes allocated for narration, pointing, pauses
  and working the arithmetic. Rehearsal determines actual runtime.
- [Twelve understanding checks](episodes/03_weights/EXERCISES.md), a challenge,
  and a [separate answer key](episodes/03_weights/ANSWERS.md).
- [NumPy verifier](episodes/03_weights/verify_theory.py) and ten concept tests.

## Correctness decisions

1. Input rows `[START,a,n,v]` differ from output columns `[a,n,v,END]`.
   The current character selects a row by lookup; the actual target selects
   the probability scored by NLL. One-hot notation is optional reference material.
2. The toy corpus contributes 9 targets, including two END targets. Aggregate
   NLL weights predictions equally, not names equally.
3. Chosen weights and count-derived weights are explicitly labeled. There is
   no claim that an optimizer produced them or that this is a new benchmark.
4. The helpful change yields full training NLL **1.331437** from **1.386294**.
   The overshoot yields **1.806672**, despite its low individual END loss.
5. Softmax normalizes each output row. It does not sample a token. A common
   score shift preserves probabilities; scaling generally changes them.
6. Maximum subtraction handles ordinary exponential overflow; log-softmax
   avoids taking the logarithm of an underflowed probability. Mathematical
   positivity is distinguished from floating-point behavior.
7. Log pseudo-counts reproduce positive add-k probabilities. Finite logits
   cannot exactly reproduce the zeros of an unsmoothed count row.
8. The unrestricted bigram rows remain independent. Longer context and richer
   learned sharing are not benefits established by this lesson. Gradients
   remain Episode 04; embeddings and the MLP remain Episode 07.

## Verification

- Ten concept tests passed using the existing Python 3.14.2 / NumPy 2.5.3
  environment. They check boundaries, counts, one-hot selection, per-row
  softmax, shift/scale behavior, stable loss under underflow, target selection,
  helpful and harmful changes, prediction weighting, add-k equivalence, the
  held-out ana path, and independence across input rows.
- All 22 frames generated successfully with element-bound checks. Text-width
  checks using the local renderer's actual fonts found no fitting warnings.
- The original 22 frames were rendered at 1200×675 and visually inspected.
  The revised single matrix-multiplication frame was rendered at the same size
  and inspected separately. Text-width checks pass, with no clipping observed.
  These are local approximations, not exports from the full Excalidraw renderer.
- The HTML embeds the series font and uses no external runtime dependencies.
  Live browser verification remains outstanding: the sandbox disallowed
  starting a local HTTP server and the browser URL policy rejected `file:`.

Reproduce the mathematical checks:

```bash
.venv/bin/python -m unittest discover -s episodes/03_weights -p 'test_*.py' -v
.venv/bin/python episodes/03_weights/verify_theory.py
.venv/bin/python canvas/build_episode_03.py
```

## Production boundary

Ready for learning and rehearsal. This is the theory-first preparation requested
by the presenter, not a claim that the complete two-video episode has shipped.
The full 03B notebook, release PDFs, recorded chapter timestamps, thumbnails and
upload metadata remain future production work. The existing Episode 01 notebook
has unrelated local edits and was not modified by this preparation.

Sources were checked against the author-published *Dive into Deep Learning*
softmax-regression chapter, Stanford CS231n notes, and official NumPy matmul
documentation. Links and concept attribution are in the theory reference.

## September 29 · Complete initial-model walkthrough

The recording route now compares count fitting and weight training side by side
(frame 3), starts from all 16 weights at zero (frame 4), and introduces logits
briefly as the selected scores. Frames 7–9 show softmax on one row and then all
four rows independently. Frames 10–13 select the actual target probability,
list every anna/ava transition with its loss, and calculate the average over all
nine targets. No update is claimed during that initial evaluation.

Frames 14–15 show the chosen ln 2 improvement and ln 100 overshoot without
repeating the full evaluation. The update method is deferred to Episode 04.
The standalone logits and count-equivalence frames were removed. Constructing
weights from smoothed counts is preserved in OPTIONAL_MATH.md alongside the
one-hot and matrix derivations. Theory, script and recording-block ranges follow
the new route; the presentation remains 22 frames.

All 22 frames were rendered at 1200×675 and visually inspected in three proof
sheets. Text fitting checks pass. The nine displayed transitions were checked
against the verifier; the average uses 5+4 targets and total 9 ln 4. Existing
concept tests pass. Live browser behavior retains the earlier verification limit.

Frame 5 now describes row-wise normalization followed by transition-specific
scoring, rather than implying a is the first training input. Its revised frame
was rendered and visually checked; the theory and presenter narration match.

## Pacing revision

Removed the separate single-row softmax and uniform-bar frames (formerly 7–8).
The current sequence moves directly from motivation (6) to the full row-wise
calculation (7). Its narration explicitly states exp(0)=1. There are now 20
frames; the walkthrough ends at 11, chosen changes occupy 12–13, and recording
block ranges and entry-point documentation have been updated. Earlier frame
numbers in this review describe the preceding revision.

Frame 6 now combines the definition, motivation, two softmax operations, and
a plotted slice P(END)=exp(t)/(3+exp(t)) with the other three scores fixed at
zero. Its 25% starting point is marked; the narration distinguishes this slice
from a universal graph. Rendered and visually checked; text-width checks pass.

Frame 1 now briefly connects sparse-context motivation from the bridge to
adjustable weights and later learned sharing. The narration retains the
backoff/interpolation qualification and makes today’s independent-row scope
explicit. Regenerated with presenter notes and visually checked.
