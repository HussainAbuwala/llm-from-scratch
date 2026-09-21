# Bridge learning notes

## Purpose and prerequisites

Prerequisites: a bigram uses one context character; a trigram uses two; counts
become conditional probabilities; generation repeatedly samples; lower held-out
NLL means better probabilities for that evaluation set. No new mathematics is
required here. This bridge explains our teaching choices rather than proving
neural models superior to n-grams.

## Why this order?

Counting made a complete model inspectable before introducing calculus.
Increasing context changed one variable and exposed the evidence tradeoff.
Next we separate three learning tasks: representing an adjustable model,
calculating useful adjustments, and automating the calculation. Only then do we
build the embeddings/MLP model that shares learned components across contexts.
PyTorch arrives after the hand-built autograd engine. Attention and the small
Transformer follow. This sequence is a project teaching choice, not a required
historical or mathematical order.

Episode 03 introduces one-hot inputs, weights, scores (logits), softmax and the
connection between cross-entropy and our existing NLL. Episode 04 explains
updates through derivatives and gradients; Episode 05 builds autograd. Treat
these as a connected arc. This bridge does not promise to teach all of training
in the next video or settle its final length.

## The root issue: how evidence is organized

Sparse data is a symptom of representing each exact context with a separate
probability row. In the plain table, an observation updates the matching row;
it does not teach a relationship between different context tokens. More data
can help, but the number of possible combinations grows quickly with length.
This is a limitation of the model's representation and sharing structure, not
an arithmetic defect in counting. Changing the optimizer alone cannot fix it.

Frames 4–9 use an **imagined word-level example**, not our character dataset:

- Suppose `a cup of tea` is common but `a mug of` is rare. Separate exact rows
  do not infer useful cup/mug similarity from their other uses in the corpus.
- Backing off through `mug of` to `of` can reuse observations after `cup of`.
  It also pools observations after `bag of`, losing the container distinction.
  We do not claim every fallback must reach `of`; the example shows what is
  sacrificed when that much shortening is necessary.
- Interpolation retains long-context contributions. It does not discard all
  specificity. However, mixing exact suffix models alone does not learn a
  representation linking cup with mug; their rare long rows remain data-poor.
- A learned representation and shared network can potentially use patterns from
  cup to inform mug while retaining mug in the input. Training must establish
  useful similarity elsewhere; no model can infer an unseen token's behavior
  from nothing. Similarity may be imperfect, task-dependent, or unhelpful.

No illustrative phrase is a measured count or guaranteed model completion.
The diagram illustrates a possible transfer mechanism, not an experiment.
Our Episode 07 implementation will learn character, not word, representations.

This comparison concerns the exact-suffix approaches introduced in Episode 02.
Class-based n-grams and other structured count methods can also share beyond
suffix matching. Interpolation coefficients may themselves be learned. Therefore
“counts cannot share” and “only neural models learn” are both misleading.
The distinction we need is **fixed exact-context/suffix grouping versus learned
representations feeding a shared prediction function**, not counts versus magic.
Our chosen curriculum explores the latter; it does not exhaust the former.

## Does backoff already share learning?

Yes, in the sense of pooling/reusing evidence. For example, histories `an` and
`vn` both have suffix `n`. The shorter-context row collects evidence regardless
of which character preceded that `n`. A fallback can consult it, and an
interpolated model combines distributions from different context lengths.
That is a meaningful form of sharing; it is not exclusive to neural networks.

Our Episode 02 theory used a simplified whole-row fallback for an absent
context. Formal backoff smoothing also handles probability allocation for unseen
continuations and is more careful than that toy rule. Interpolation combines
normalized distributions with nonnegative weights summing to one. Neither needs
a full implementation in this short bridge. [Jurafsky and Martin, Chapter 3](https://web.stanford.edu/~jurafsky/slp3/3.pdf).

## Why explore another method?

We have not established that backoff or interpolation is insufficient for our
names dataset. The coding experiment compared add-k models only. A claim of
superiority would require an appropriate held-out comparison.

The next route is motivated by the series endpoint and the kind of structure
we want to learn. An embedding represents an input with learned numbers; a
shared network combines those representations. Inputs need not be identical
suffixes for a shared parameter update to influence their predictions. Useful
similarity is learned through the training objective; it is not a guarantee of
human-like meaning or correct generalization. Our eventual character model
learns character representations, not word meanings. [Bengio et al. (2003)](https://www.jmlr.org/papers/v3/bengio03a.html).

These approaches can also be combined; this is not a universal either/or choice.
We are choosing a bounded route to understand a small Transformer, not exhausting
all classical language-model improvements first.

## What weights do—and do not—buy us

Weights are adjustable parameters. For the next unrestricted one-hot bigram
model, each context character selects its own row of scores. Softmax converts
those scores to probabilities. Merely replacing each count row with a weight
row does not introduce learned sharing across different input rows.

For an observed row with counts c_j, total N and predicted probabilities p_j,
its unsmoothed training objective is -sum_j c_j log(p_j). Over the probability
simplex this is minimized at p_j = c_j/N. Thus the learned bigram can target the
same empirical distribution as counting. Finite softmax scores are strictly
positive, so exact zero-probability outcomes are approached as a limit, rather
than attained with finite scores. This is our mathematical check, not spoken
bridge material. Smoothing, regularization and incomplete optimization change
the comparison. Do not promise to reproduce the smoothed baseline automatically.

The value of the next lesson is learning the optimization mechanism on a familiar
task. Embeddings and the MLP in Episode 07 introduce the planned richer sharing.

## Experiment shown on frame 3

Reuses [Episode 02's verified validation results](../02_trigrams/README.md).
Context characters 1/2/3/4/5; validation NLL 2.456622 / 2.233214 / 2.126903 /
2.196154 / 2.386382 nats per prediction. Each point uses its validation-selected
k from the tested grid: 0.3 / 0.3 / 0.1 / 0.1 / 0.1. These are jointly selected
context/smoothing results, not a fixed-k causal comparison. All points use the
same 21,141 validation targets, character vocabulary, split and END convention.
START padding is not scored. No new experiment or test-set claim is introduced.

## Simplifications and limits

- “Sharing” is a broad teaching word. Distinguish suffix pooling from learned
  representations; neither guarantees useful transfer.
- The shared-model picture illustrates common computation, not a particular
  implemented architecture or measured prediction.
- “Adjust to reduce loss” states an optimization aim. Neither every update nor
  held-out performance is guaranteed to improve.
- A Transformer endpoint here means a small decoder-only model trained at laptop
  scale, not a ChatGPT-level assistant. Post-training and serving remain out of scope.

## Understanding check

1. Does our curve prove backoff cannot help? **No. We did not test it.**
2. What can `an` and `vn` share in a shorter-history model? **The suffix `n` row.**
3. Does a bigram weight table automatically share across input rows? **No.**
4. Why revisit bigrams? **Keep the task familiar while learning a new mechanism.**
5. What remains the same? **Next-token probabilities, repeated generation, and
   held-out evaluation.**
6. When does the planned richer sharing arrive? **Embeddings and the MLP, Episode 07.**

## Source and correctness notes

Established methods: n-gram estimation, backoff/interpolation, learned distributed
representations. Primary/authoritative links above were checked September 21,
2026. Our curriculum order, wording and eleven-frame format are editorial choices.
The row-optimum calculation and diagrams are our explanations. Review explicitly
checked bigram/trigram terminology, evidence scope, sharing claims, and the
separation between Episode 03's weight table and Episode 07's shared model.

## Closing teaching sequence (frames 8–11)

Frame 8 lists the suffix rows consulted for `a mug of`. The existing `a cup of`
row is not directly consulted; its observations contribute indirectly via `of`.
Frame 9 shows that the pooled row lacks container attribution. The original
training data and longer-context rows still retain that information.

Frame 10 uses one mug query and paired illustrative training examples (drinking
from cups/mugs and pouring tea into each). These belong to a hypothetical larger
training dataset, not the exact counting toy. It asks: can cup-related experience
help with the mug query, while mug still influences the answer? Interpolation
already preserves some specificity through longer rows; the additional goal is
learning useful relationships between different inputs. This is a future goal,
not a measured effect in the toy corpus or a claim of automatic generalization.

Frame 11 combines the motivation for adjustable weights and the three enablers:
weights (Episode 03: bigram weights and softmax), a training method (Episodes
04–06: gradients, autograd, PyTorch), and a structure that reuses weights
(Episode 07: embeddings and the MLP). Future concepts are named only to locate
them in the curriculum. No knowledge of those concepts is assumed here.
Weights make predictions adjustable; shared structure allows updates to affect
multiple inputs; training decides how to adjust the numbers. Counts are also
learned statistics. Neither weights alone nor sharing guarantees improvement.

Understanding checks:

- Is `a cup of` absent? **No; it exists but isn't a suffix of the mug query.**
- Is cup evidence completely excluded? **No; it reaches the pooled `of` row.**
- Does that row retain the container behind each count? **No. Longer rows do.**
- Does interpolation ignore mug completely? **No; longer rows still contribute.**
- Does the next weight table already solve sharing? **No; it teaches training
  on the familiar task before building richer models.**

## Exact counting and interpolation toy (frames 5–7)

This is a separate constructed corpus, not measured names data or the earlier
common/rare hypothetical: `a cup of tea`, `a mug of coffee`, `a bag of rice`.
Only final-word observations are displayed. For each context length, each
observation is counted once in its matching row. The long rows coexist with
the pooled `of` row, whose counts are tea=1, coffee=1, rice=1. These are three
observations viewed by three models, not nine independent examples.

The missing-row fallback uses `a mug of` immediately because it exists. Query
`the mug of` has no exact row but finds `mug of`. Both give coffee probability
1 in this tiny unsmoothed toy. This is empirical certainty, not certainty about
language. No row is created, removed, or modified while predicting. Query `a glass of`
finds neither `a glass of` nor `glass of` in the fixed training data and therefore
uses `of`: tea, coffee and rice each get probability 1/3. Only this third query
demonstrates losing the container information entirely. Glass is supplied in the
query; it is not an added training observation or a learned-similarity claim.

For interpolation query `a mug of`, both longer rows assign coffee probability
1. The `of` row assigns 1/3 each to tea, coffee and rice. Equal mixture weights
1/3 yield tea=1/9, coffee=7/9, rice=1/9. The weights sum to one and the resulting
distribution sums to one. Other outcomes have zero probability in this toy.
No smoothing is needed to define these particular rows; this is not a complete
zero-probability remedy or a claim that the chosen mixture improves evaluation.

Check: the shorter row exists regardless of which query uses it. Training
creates the estimates; backoff/interpolation governs prediction from them.
