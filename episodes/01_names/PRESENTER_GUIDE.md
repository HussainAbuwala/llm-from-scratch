# Episode 01 coding · What is happening and how to present it

The notebook is the main screen. It builds a character-level name generator
using counting, then measures how well it predicts held-out name spellings.
You write or reveal a small block, run it, point to the result, and explain what
the result tells us. The finished file is `episode_01.ipynb`; `episode_01.html`
is the same executed lesson for browser reading.

The implementation has already run successfully from a fresh kernel. Values
below come from `outputs/results.json` and the saved notebook outputs. Rebuild
after changing the experiment and update these notes if its results change.

## Your preparation

1. Open the completed notebook and read through its outputs once.
2. Select the project's `.venv` kernel. Restart and run all cells before recording.
3. Make a recording copy in the same folder, restart its kernel, and clear outputs.
4. Keep the setup/import cell and chart helpers prepared. They are setup, not the lesson.
5. Practice explaining the counting, normalization, generation, and evaluation
   functions. Those are the blocks worth building slowly on screen.
6. Show the saved final samples for a brief cold open, then return to section 1.
   Identify them as outputs from the finished model you are about to build.

There are 12 notebook sections, but they need not be equal-length video chapters.
Record in the five blocks below and edit out repetitive typing and long scrolling.
The timing suggestions are rehearsal estimates, not a required runtime.

| Recording block | Notebook sections | Approximate time | Stop when the viewer can explain… |
|---|---|---:|---|
| Data into training examples | 1–3 | 7–9 min | What one example, one token, and one prediction mean |
| The first working generator | 4–6 | 10–12 min | How counts turn into a generated name |
| Measurement and the zero problem | 7–9 | 9–11 min | What NLL measures and why an unseen pair breaks it |
| An experiment that changes behavior | 10 | 5–7 min | Why validation chooses smoothing |
| Results and the next limitation | 11–12 | 5–7 min | What was learned and what one-character context misses |

## 1. Load and inspect the names

The file contains **32,033 lines**. We validate that every line is a nonempty
lowercase ASCII spelling. We remove repeated spellings and sort them, leaving
**29,494 unique names**. There are **2,539 duplicate lines**, and name lengths
range from **2 to 15** characters.

Explain the project choice: each spelling is one equally weighted example.
We are learning spelling patterns, not the population frequency of each name.
Removing duplicates also prevents an identical spelling from appearing in both
training and evaluation. Sorting first gives the seeded shuffle a stable input.

The checksum verifies the supplied file is the pinned dataset. You can keep
that line prepared and describe it briefly as a reproducibility check.
The histogram shows the actual distribution of name lengths.

Suggested explanation: “We have enough names to learn patterns, but the raw
material is simple: one string per line.”

## 2. Split before training

We copy the list and shuffle it using a dedicated `random.Random(42)` generator.
Whole names are assigned to three groups:

| Split | Names | Predicted transitions, including END |
|---|---:|---:|
| Training | 23,595 | 169,134 |
| Validation | 2,949 | 21,141 |
| Test | 2,950 | 21,053 |

Training supplies every learned count. Validation will choose k. Test loss is
computed after that choice is fixed. Assertions check that no spelling overlaps.
The independent random generator means generating more samples cannot change
the split. None of these steps optimizes the model yet.

## 3. Give the table meaningful addresses

`make_vocabulary` discovers the **26 letters in training only**. The row list is
START followed by the letters. The column list is the letters followed by END.
The resulting table is **27 × 27**, or 729 allowed count cells.

This is a subtle implementation detail to call out explicitly: row and column
indices are separate addresses. For example, `a` has row index 1 and column
index 0. They refer to the same character in different axes. START is never a
target, and END never supplies a next prediction.

We audit validation and test for unknown characters. Both have zero affected
names. This audit does not add held-out letters to the vocabulary or change
the split. On another dataset, the explicit error asks us to design an unknown
token policy; no evaluation names are silently discarded.

`transitions(name)` surrounds the characters with boundaries and zips the list
with its one-position-shifted version. For `anna`, the pairs are:

```text
START → a → n → n → a → END
```

There are five predictions for four letters. Pause on the printed example and
show how one pair maps to a specific table cell.

## 4. Training is counting

`count_bigrams` creates independent zero-filled rows. For each training name,
it extracts the pairs and increments `counts[row_id[current]][next_id[target]]`.
Nothing from validation or test enters this function during real-data training.
There is no optimizer, backpropagation, or repeated training epoch here.

Three checks account for the data: all counts sum to **169,134**; the START row
totals **23,595**; and the END column totals **23,595**. Each name starts once
and ends once, and there is no transition joining separate names.

The chart shows the whole count table. Its color is **log(1 + count)** so rare
pairs remain visible; that transform is used only to draw the chart. Training
retains the original integer counts. The printed top counts are easier to read
precisely than the heatmap.

## 5. Normalization completes the model

`normalize` divides every entry by its row total. Every resulting row sums to 1.
These rows are the conditional distributions the generator will use.

For the real data, the `a` row contains **25,663** transitions:

```text
P(END | a) = 5,215 / 25,663 ≈ 0.2032
P(n   | a) = 4,080 / 25,663 ≈ 0.1590
P(r   | a) = 2,394 / 25,663 ≈ 0.0933
```

Show the probability bars and connect the largest bar to the corresponding
count. Explain that the complete probability table is the trained model.
An entirely empty row is an error for this unsmoothed function; smoothing can
later give such a row a uniform distribution. Our training-derived vocabulary
has observed outgoing evidence for every letter, including terminal letters.

## 6. Generation repeatedly uses one row

`generate` starts with the current token set to START and an empty output list.
On each iteration it reads the current row. Greedy decoding selects the column
with maximum probability. Sampling uses `random.choices` to choose a token
with those probabilities as weights. END finishes the name; otherwise we
append the character and look up its row for the next iteration.

The row/column distinction matters here: the sampled column index is not
reused as the next row index. The code converts through the token itself.

Both modes stop after at most 24 generated characters. The returned boolean
distinguishes an actual END prediction from a length cap. The cap prevents
runaway execution; it is not evidence that the model learned when to stop.
Greedy ties follow the fixed column order.

The real model's greedy output is just **`a`**. That is a useful failure:
choosing the largest probability at each step can give an unhelpfully short
result. Greedy is a local decision rule, not a search over complete names.

## 7. Evaluation asks about the supplied answer

`evaluate` walks through actual names, looks up each true next token's
probability, accumulates `-math.log(p)`, and divides by the total number of
predictions. It does not call the generator and does not change any counts.

The denominator includes END and combines all predictions across the corpus.
We do not average the per-name averages: a longer name contributes more
prediction tasks. Natural logarithms make the unit **nats per prediction**.

If any observed target has probability zero, the corresponding loss is
infinite. No small epsilon disguises that failure. In the actual run,
unsmoothed training NLL is **2.452920** and validation NLL is **infinite**,
with **8 zero-probability validation predictions**.

Now take one minute to reuse the functions on `anna` and `ava`. The printed
toy table matches the theory. Scoring `ana` gives a complete-path probability
of **0.0625** and average NLL **0.693147**. Multiplication is used only for
this short teaching check; full-corpus evaluation accumulates log penalties.

Suggested explanation: “The dataset changed, but this known answer tells us
that our code still implements the arithmetic we learned.”

## 8. Establish baselines

The uniform model assigns 1/27 to each allowed next outcome, so its NLL is
ln(27), approximately **3.295837**. The unigram model sums the training table
down the columns and normalizes those global target frequencies. It uses the
same distribution after every current token, so it ignores context.

Both include END as a predicted outcome and exclude START. The validation
unigram NLL is **2.823959**. The unsmoothed bigram still has infinite validation
NLL; its use of context has not protected it from assigning impossible events.

## 9. Repair overconfident zeroes with smoothing

Use the toy name `avna` to isolate the problem: `v → n` was never observed,
even though both letters are known. Its unsmoothed score is infinite.

`smooth` adds k to every allowed count cell and then calls `normalize`.
With k = 1, the toy `v` row changes from `[1, 0, 0, 0]` to pseudo-counts
`[2, 1, 1, 1]`, then probabilities `[0.4, 0.2, 0.2, 0.2]`.
The function creates a new table; it does not overwrite observed counts.

Explain that smoothing reallocates probability. It does not create evidence
that the unseen pair actually appeared, and it cannot represent new letters.

## 10. Choose a setting with validation evidence

We test k values 0, 0.001, 0.01, 0.03, 0.1, 0.3, 1, 3, 10, and 100.
For each one, the counts stay fixed while a new probability table is formed.
Training and validation loss are then recomputed.

The best candidate is **k = 0.3**, with validation NLL **2.456622**. The
difference from k = 1 (**2.456749**) is small. Do not present 0.3 as a magic
constant or a meaningful universal win over 1. The experiment demonstrates
the selection process on this particular split and grid.

The chart has a full view and a zoomed view with explicitly different y-axis
ranges. Infinity at k = 0 is labeled rather than plotted at a made-up height.
Training loss increases with smoothing; excessive smoothing hurts validation
too. Huge k = 1e9 approaches the uniform baseline, checking the denominator.

## 11. Show the behavior honestly

The final 100 samples are the first results from seed 2026; they are not filtered.
The list begins `ann`, `aiootlostomia`, `jorole`, `vi`, and `kamifi`.
Some outputs are short or awkward, and some match training names. Each match
is labeled. “Not in training” does not imply a previously nonexistent name.

Add-k also gives START → END a small nonzero probability. That can produce an
empty output, which the implementation reports as an empty string. It is not
silently resampled. Truncation is explicitly reported as CAP.
The final recorded scope omits the constructed loop demonstration and per-name
diagnostics. Greedy output and the prefix comparison supply the limitation examples.

Finally, compare prefixes `an` and `marian`. Both end in `n`, so they use the
identical row. This is the clearest bridge to longer context: the limitation
is visible in the line of code that chooses a row.

## 12. Report the result and stop tuning

The selected k is fixed before this section. The original training counts
remain unchanged. All three final models score the same **21,053 test
predictions**, including END:

| Model | Test NLL |
|---|---:|
| Uniform | 3.295837 |
| Unigram | 2.818510 |
| Smoothed bigram, k = 0.3 | 2.460499 |

This establishes that the smoothed contextual model predicts these held-out
spellings better under our metric. It does not establish human-like name
quality or understanding. The samples and the context demonstration show
what the loss comparison alone cannot tell us.

Close with what viewers can now do: load data, train a count model, generate
from it, measure predictions, and use validation to choose a setting.
Their next question is how predictions would change if the model remembered
more than the last character.

## What the verification covers

Twelve focused tests check the actual functions extracted from `lesson.py`:
the theory count table and boundaries; the exact held-out probability;
infinite-loss handling and its repair; smoothing normalization and immutable
counts; prediction-weighted NLL; unknown-character rejection; immutable
evaluation; correct row/column conversion during generation; END and cap
semantics; reproducible weighted sampling; invalid input errors; and toy
baselines. A fresh-kernel notebook run checks the complete data and chart flow.
