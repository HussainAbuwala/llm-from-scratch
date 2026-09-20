# Episode 02B - Learn it, then record it

The notebook is the main screen: [episode_02.ipynb](episode_02.ipynb).
Start by reading [CODE_GUIDE.md](CODE_GUIDE.md), then run one section at a time.
This guide supplies the speaking route, checkpoints, and likely questions.

## The promise

> In the theory video, we saw how longer contexts divide the same evidence into
> smaller groups. Now we'll build that model, generate names, and measure when
> the extra detail helps on our dataset.

This episode builds on Episode 01B. Reuse the familiar ideas of next-token
probabilities, weighted sampling, and NLL; spend more time on tuple contexts,
sparse storage, and fair comparisons. The key change is the history used to
address a probability row.

## Prepare the recording

1. Read the executed outputs, then restart and Run All once in the project `.venv`.
2. Create `episode_02.RECORDING.ipynb` **in this same directory**; that suffix is ignored by Git.
3. Clear outputs in the recording copy. Keep setup and plot helpers prepared.
4. Reveal or type the model functions in small blocks. Do not narrate imports or plot styling line by line.
5. State explicitly when switching from anna/ava to the real dataset.
6. Pause the recording during the grid computation if needed; show the complete result, not edited candidates.
7. Use the report for numerical reference. Suggested durations below are rehearsal estimates, not chapter timestamps.

The notebook has 11 sections but fits into five recording blocks. At this stage
we are preparing the lesson, not an upload; final video chapters must come from
the actual recording.

| Block | Sections | Suggested time | Viewer should be able to explain |
|---|---|---:|---|
| Build and score the toy model | 1-4 | 10-12 min | Tuple windows, sparse counts, smoothing, and evaluation |
| Generate from the toy model | 5 | 4-5 min | How predictions feed back into context |
| Run a fair comparison | 6-8 | 8-10 min | Fixed data, declared candidates, validation selection |
| Inspect what changed | 9-10 | 7-9 min | Loss curves, sparsity denominators, unfiltered samples |
| Freeze and report | 11 | 4-5 min | The role and limits of the final test set |

## 1-2. From one character to a tuple

Show the original anna and ava, then the windows function. Trace the first
window of anna: `(START, START) -> a`. Explain that slice endpoints exclude
`index`, so the slice contains the preceding m tokens and the target is at index.

The loop advances one token, not three. `yield` lets a caller loop through one
window at a time. For a list-like view of the result, use `list(windows(...))`.

Point at the nine-observation total for all five context lengths. More padding
fills missing history but adds no prediction targets. Every name resets START.

**Ask yourself:** if I use a 4-gram, what is `context_size`? Answer: 3.

## 3. Store evidence and query it

Read `CountModel` in two passes. `__init__` learns vocabulary from the provided
training names, then counts each context-target pair. `self` keeps all the data
for one model together. It is ordinary Python organization, not a neural network.

A tuple such as `('a', 'n')` addresses the outer dictionary. Its Counter maps
targets to counts. There are seven observed rows and nine total observations.
The row total is the denominator's real evidence term.

Then explain `probability`. This is where count lookup and add-k meet. The
function accepts a context, target, and k. It returns one probability on demand;
it does not construct or store an entire dense probability table.

**Python detail worth explaining:** training uses bracket access to add a row;
prediction uses `.get()` to avoid creating a row. With a defaultdict, accidentally
using brackets during evaluation could make the model appear to have observed
contexts it only encountered in evaluation.

## 4. Evaluation is following a supplied path

Run the three ana comparisons. Expected path probabilities are 1/16 for raw
bigram, zero for raw trigram, and 1/75 for add-one trigram. Smoothed trigram NLL
is about 1.079372, averaged over four predictions including END.

Do not compare that single example with the real-data average. Its purpose is
to verify that our implementation reproduces the hand calculation.

Explain the separate missing counters in `evaluate`. A zero target in a seen
row and an entirely absent row both prevent finite raw evaluation, but their
causes differ. Infinity is a failure marker for the latter; `0/0` is not zero.

Use `avna` briefly to show both cases together, then show that add-one smoothing
makes the path scoreable. The final assertion verifies that evaluation did not
insert the unseen context into the stored training counts.

For multiple names, sum loss over all targets before dividing. Otherwise a
short name and a long name could receive equal weight regardless of target count.

## 5. Generation feeds its own predictions back

Evaluation takes the actual token. Generation samples a token using the same
probability function. Start at START padding, sample, append the token, shift
history, repeat. Point to `(*context[1:], target)` as the memory update.

Without smoothing, this toy can only produce anna or ava. Smoothing allows
other paths. Label the first 12 outputs per smoothing setting and keep every one.

The 24-step cap is a program limit. END is a model decision. An empty generated
string means END was sampled from the initial row; do not silently remove it.

## 6. Keep the data comparison fair

Reuse the exact Episode 01 checksum, deduplication, sort, seed-42 shuffle, and
whole-name split. No new download and no frequency weighting.

| Split | Names | Predictions including END |
|---|---:|---:|
| Training | 23,595 | 169,134 |
| Validation | 2,949 | 21,141 |
| Test | 2,950 | 21,053 |

The training set defines 26 letters plus END. Held-out character checks audit
compatibility; they do not expand the vocabulary, discard examples, or train
the model. Resetting a sampling seed must not change the split.

## 7-8. Declare choices, then measure

Show context lengths 1-5 and the ten k candidates, including 0, before the loop.
The experiment already existed during theory preparation; don't present this
as a surprise or as a new preregistered claim.

Every model gets the same 169,134 training targets. Every validation setting
scores the same 21,141 targets. We choose k independently for each context,
then choose the context using validation loss. Test has no role in this decision.

Keep the 50 candidate scores in the saved evidence. The printed summary shows
k = 0 and the winner per context. Here all five unsmoothed validation losses are
infinite because of zero-count targets or missing contexts, so none wins.
The smoothing chart shows positive k on a log axis and k = 0 in a separate table.
The minimum is among tested candidates, not a continuous global optimum.

## 9. Read loss and evidence together

First read the loss chart:

- Gray dashed: raw training fit at k = 0.
- Blue: training fit using each model's selected k.
- Orange: validation using that same selected k.

In the verified run, validation improves from one to two to three context
characters, then rises at four and five. Selected-k training loss continues
to decrease. Say **three context characters / 4-gram**, not trigram.

The right panel holds k fixed. Use it to check whether the qualitative pattern
is merely an artifact of selecting different k values for different contexts.
Do not read every point aloud; refer back to the complete grid as evidence.

Then read the sparsity chart. At m = 5, 21,379 of 36,171 observed rows are
singletons, and 2,746 of 21,141 validation prediction occurrences require
unseen contexts. These are different denominators. They are associated with
the generalization pattern, not a controlled proof of the sole causal factor.

The next cell finds a real missing context in validation and prints its raw
and smoothed target probabilities. It connects the aggregate plot to one lookup.
All allowed outcomes get 1/27 in that empty row; k cannot choose a preference.

## 10. Samples are illustrations, not the leaderboard

Show each model's first 12 outputs with the same seed and selected k. Keep the
training-spelling label, END/CAP status, and any empty output visible.

An exact training spelling is not automatically a defect, and a novel spelling
is not automatically good. Likelihood on held-out data answers a different
question from whether a few samples look plausible.

## 11. Freeze, test, and close

The selection file is written before test scoring. The declared validation
winner remains the chosen model even if a test ranking differs. Training counts
stay fixed; we do not add validation names before this comparison.

This test split was already used for the Episode 01 report. Be transparent:
it is excluded from fitting and selection here but is not a newly collected
independent dataset. Re-running unchanged code does not reset that history.

Read the final numbers from `outputs/coding_results.json` or the README's final
table. The m = 1 result should reproduce Episode 01's approximately 2.460499.
Compare test to test, not test to the validation figure 2.456622.

Close with:

> We gave a count model more context without giving it more training evidence.
> Some extra detail helped. At longer contexts, many rows were rare or missing,
> and our plain add-k model predicted held-out names less well. Next we learn
> probabilities using weights and softmax, before later introducing shared representations.

## Scope guardrails

- Backoff and interpolation were theory concepts; they are not implemented or evaluated in this add-k sweep.
- This does not establish a universal best context or a limit on all classical language models.
- A bigram weight matrix alone does not solve sparsity; shared embeddings and the MLP arrive later.
- The final video duration, chapters, thumbnail, and upload metadata should be prepared after recording.

## Recorded release

The final recording is about 30:30. The release notebook follows its 11-section
structure and closing recap; reporting utilities run only during the build.
[Upload metadata and chapter markers](../../youtube/EPISODE_02B_METADATA.md)
are based on the recording; rehearsal estimates above are not upload timestamps.
