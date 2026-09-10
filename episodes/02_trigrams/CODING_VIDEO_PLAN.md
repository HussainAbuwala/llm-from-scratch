# Episode 02 · Coding companion scope

The [theory video](../../EPISODE_02_THEORY.md) establishes the mechanism with
hand-worked examples: more specific rows divide evidence; unseen combinations
need a probability policy; smoothing and shorter histories have limits.

This coding video implements those ideas and tests their consequences. It
must not describe the experiment as proof that longer context always hurts,
or tune the demonstration until it matches a predetermined narrative.

## Suggested sequence

1. Reproduce the original `anna` / `ava` windows and probabilities in `lab.py`.
   Match P(ana)=1/16 for the bigram, zero for the unsmoothed trigram, and 1/75
   for the k=1 trigram. Then show the exact denominator of four predictions.
2. Implement generalized windows with m START pads, one END, and reset per name.
3. Store observed counts in a sparse dictionary. Show that a missing target
   and a missing row are different cases at k=0. Compute smoothing on demand;
   evaluation and generation never add to training counts.
4. Load the same bundled names data and seed-42 split as Episode 01. Vocabulary
   comes from training; verify evaluation targets are supported.
5. Implement NLL and generation, including END in evaluation and marking capped
   samples. Separate random generation from evaluation on supplied histories.
6. Compare context lengths 1–5. Select k for each model from the declared grid
   using validation; show the candidate values and matching prediction counts.
7. Compare training and validation curves, observed rows, singleton rows, and
   held-out occurrences of unseen contexts. Separate unsmoothed training fit
   from selected-k training fit. Show unfiltered generated samples with labels.
8. Explain the result within this dataset, split, and add-k family. More context
   may improve predictions before sparse estimates outweigh the benefit.
9. After choices are frozen, add the series' final test evaluation for release.
   The current lab report does not score test. Do not imply that step is already
   implemented or completed.

## Existing experiment evidence

[The lab README](README.md) contains the measured table, commands, and metric
conventions. [study_results.json](outputs/study_results.json) preserves all
candidate sweeps and the first 12 samples per model. These results were removed
from the theory canvas; they remain available for this coding video.

The existing `lab.py` is a working reference implementation and validation lab,
not yet a completed recording notebook or full release build. The dataset has
29,494 deduplicated names, split 23,595 / 2,949 / 2,950. All validation candidates
score 21,141 predictions. The held-out test split stays reserved.

## Shorter histories

Backoff and interpolation are brief theory concepts. The main experiment
currently implements add-k only. Implementing a lower-order mixture would be
an optional, separately labeled extension, with its weight selected on
validation and all probability rows checked for normalization. Do not present
it as already included in the saved experiment results.

## Opening bridge

“In the theory video, we saw how the same observations split into smaller
groups as context grows. Now we'll build that mechanism and measure it on
thousands of names. Does the extra detail help more than the sparse evidence
hurts? Let's find out.”
