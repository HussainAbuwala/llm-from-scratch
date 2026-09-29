# Episode 03 · From counts to weights

Theory preparation · September 28, 2026 · Part 2: Learn

## The promise

Take the bigram we already understand and give it adjustable scores. By the end,
the viewer can follow a character through a lookup in a weight table,
softmax, and the same negative log-likelihood used in Episode 01. They can change
a score and check whether the change helped the observed data.

This lesson prepares the prediction rule and objective. It does not derive an
automatic update rule. Episode 04 explains gradients; Episodes 05–06 develop
automatic differentiation and rebuild with PyTorch. The separate Episode 03B
build should use NumPy to inspect this forward computation and controlled weight
changes, clearly labeling any optimization demonstration and its limitations.

Read this reference first, then use the [presentation](canvas/episode_03_theory.html)
and [presenter script](episodes/03_weights/PRESENTER_GUIDE.md). Attempt the
[exercises](episodes/03_weights/EXERCISES.md) before reading the answers.

## Prerequisites and scope

Know what a character bigram predicts, how a count row becomes probabilities,
why END is scored, and why a small probability gives a large negative log loss.
No matrix algebra or derivatives are assumed. Use a labeled score table and
direct row lookup. One-hot encoding and matrix multiplication are optional notes.

Established concepts: adjustable scores, softmax regression,
categorical cross-entropy, and maximum likelihood. A one-layer softmax classifier
is enough here; calling it a deep neural network would be misleading.

Pedagogical simplifications: two training names, three ordinary characters,
one-character context, an unrestricted score row per input, no hidden layer,
and no separate bias. These make the arithmetic visible but do not introduce
learned similarity between different input characters. Counts are also fitted
from data; we are changing the parameterization and preparing an optimization
method, not introducing learning for the first time.

Project choices: direct row lookup, float64 NumPy verification,
zero scores as a transparent starting point, and deliberately chosen score
changes. Zero initialization is useful for this independent-row model; it is
not a recommendation for multilayer networks. Training remains `anna`, `ava`.
The name `ana` is a familiar held-out illustration, not a statistically reliable
validation set. Do not select our illustrative weights by its loss.

## Recording route and training comparison

Begin with the same data, then contrast the approaches side by side:

| Count-based bigram | Weight-based bigram |
|---|---|
| Count the training transitions | Initialize adjustable scores |
| Smooth if chosen and normalize each row | Look up input rows, apply softmax, calculate training NLL |
| Evaluate probabilities using NLL | Update weights from training loss and repeat |
| Use validation to choose k | Use validation to choose training settings or checkpoints |

The loss is the same. Counts fit the empirical rows directly; the weight route
introduces iterative updates. Validation does not supply weight gradients.
Test data remains excluded from fitting and selection.

The canvas first evaluates the **all-zero** weight table completely: softmax on
every row, all five anna targets, all four ava targets,
and the combined average. It then tries ln 2 and ln 100 by hand and compares
full training NLL without repeating the whole evaluation. The method for choosing
updates is the next lesson. Logits is a name for output scores, introduced
on the initial table rather than as a separate learning detour.

## 1. Keep the data and boundaries fixed

Input row order is **[START, a, n, v]**. Output column order is
**[a, n, v, END]**. Both lists happen to have length four; their meanings differ.
START is context only. END is predicted once and ends a name; it has no input row.

| Training name | Observed bigram transitions |
|---|---|
| anna | START→a, a→n, n→n, n→a, a→END |
| ava | START→a, a→v, v→a, a→END |

There are **9 predictions**: 7 characters plus 2 END targets. Reset to START
between names; never create a transition from one name into the next.

| Input / next | a | n | v | END | Total |
|---|---:|---:|---:|---:|---:|
| START | 2 | 0 | 0 | 0 | 2 |
| a | 0 | 1 | 1 | 2 | 4 |
| n | 1 | 1 | 0 | 0 | 2 |
| v | 1 | 0 | 0 | 0 | 1 |

This is the original unsmoothed bigram table. The new model will answer the same
four questions using a table of real-valued parameters.

## 2. Look up the current character’s scores

Keep the familiar row lookup. Let W be a table of adjustable scores, with
input rows `[START,a,n,v]` and output columns `[a,n,v,END]`.
Initialize every entry to zero. For input `a`, read its row: `[0,0,0,0]`. These four output scores are
called **logits**. Weights are stored parameters; logits are the scores used
for a particular prediction. In this simple model, the logits are a copied
weight row. In richer models, they are computed using many parameters.

For the full training walkthrough, apply softmax independently to all four
rows first. Then each observed transition selects its input row and actual
target column. START is used twice, a four times, n twice, and v once: nine
predictions, not four equally weighted row losses. The first anna transition
is START→a, not an input a. Looking up each row before applying softmax is
equivalent; it is an implementation choice.

In code, `scores = W[input_id]` is sufficient. The ID is an address into the
table, not a quantity to multiply by the weights. We can train this model
using that lookup directly. A one-hot vector multiplied by W is equivalent,
but is not required. The [optional derivation](episodes/03_weights/OPTIONAL_MATH.md)
retains the worked multiplication for interested readers. Episode 07 introduces
matrix multiplication where it combines learned features.

We omit a separate bias because each input already has an unrestricted score
row; a common output bias can be absorbed into those rows. This is a project
choice, not a claim that all models should omit biases.

## 3. Turn scores into a distribution

### Why this rule appears

In the count model, observed counts were nonnegative with a positive total.
Dividing by that total produced probabilities. Adjustable scores are different:
they may be negative, and an all-zero row has total zero. Simply dividing raw
scores by their sum is not a general probability rule.

We want to accept any finite real scores, produce probabilities adding to one,
and give larger scores larger probabilities. A smooth response to score changes
will also let us use gradients later. Softmax satisfies these aims. They motivate
it; they do not uniquely determine it. Other transformations are possible.

The exponential `exp(z)` means e raised to the score z, with e approximately
2.718. It is positive for every finite real input and strictly increasing.
For this episode, understand `exp(0)=1`, `exp(ln 2)=2`, and
`exp(−ln 2)=1/2`. Natural log and exponential undo each other. We deliberately
chose ln 2 so the worked arithmetic stays simple. It is not a special training
constant. Exponentiated scores are relative amounts, not observed counts.
Normalize them by dividing each by their sum, just as we normalized counts.

Larger score differences become larger probability ratios:
`p(END)/p(n) = exp(z_END − z_n)`. A gap of ln 2 means twice the probability.
This ratio fact is useful presenter intuition; deriving it is optional. A common
score shift cancels, and every probability shares the denominator, so raising
one score changes all probabilities in that row. Softmax does not update weights
or sample a token. It is not itself a guarantee of calibrated confidence.

For the spoken lesson, stop at the purpose, these two steps, the original
four-score calculation, and the common-shift stability trick. Derivatives,
log-softmax implementation, and deeper statistical derivations belong in later
lessons or optional notes. The softmax and stability sources below support the
standard construction; this teaching sequence is our choice.

### Read the S-shaped curve on frame 6

Softmax takes a vector, so it has no single universal one-input graph. The
canvas shows a slice: hold the a, n and v scores at zero and vary END's score t.
Then P(END) = exp(t) / (3 + exp(t)). This rises smoothly in an S shape,
approaching zero and one without reaching either for finite scores. At t=0,
P(END)=1/4; at t=ln 3, P(END)=1/2. The midpoint depends on the other scores.
Each of the other three probabilities is 1/(3+exp(t)), decreasing as END rises.
The graph illustrates competition and smooth change, not a new training run.

### The rule and worked example

Scores may be negative, need not sum to one, and are not probabilities.
Softmax exponentiates them and divides by their sum:

\[
p_j=\frac{e^{z_j}}{\sum_k e^{z_k}}.
\]

For finite real scores, each probability is positive and the row sums to one.
With multiple examples, normalize across outcomes separately for each example.
Softmax produces a distribution, not a sampled character. This is the standard
softmax-regression prediction rule. [Dive into Deep Learning, §4.1](https://d2l.ai/chapter_linear-classification/softmax-regression.html).

Start with the all-zero a row:

| Stage | a | n | v | END |
|---|---:|---:|---:|---:|
| Scores | 0 | 0 | 0 | 0 |
| Exponentials | 1 | 1 | 1 | 1 |
| Divide by row total 4 | 1/4 | 1/4 | 1/4 | 1/4 |

Apply those steps independently to each input row:

| Input | Scores | Exponentials | Row total | Probabilities |
|---|---|---|---:|---|
| START | [0,0,0,0] | [1,1,1,1] | 4 | [1/4,1/4,1/4,1/4] |
| a | [0,0,0,0] | [1,1,1,1] | 4 | [1/4,1/4,1/4,1/4] |
| n | [0,0,0,0] | [1,1,1,1] | 4 | [1/4,1/4,1/4,1/4] |
| v | [0,0,0,0] | [1,1,1,1] | 4 | [1/4,1/4,1/4,1/4] |

Each row sums to one. Normalizing all sixteen scores together would answer a
different question and would not give the required conditional distributions.

Zero is a score, not a ban: \(e^0=1\). With four zero logits, every output has
probability 1/4. A negative score also contributes positive mass. Raising one
score changes the denominator, so it changes the entire probability row.

Only differences matter: adding a constant to all four scores multiplies every
exponential by the same factor, which cancels. Multiplying scores by a constant
does not generally preserve the distribution. In our toy, doubling the scores
in the later `[0,0,0,ln 2]` example changes the exponential weights from `[1,1,1,2]` to `[1,1,1,4]`.

For numerical stability, subtract the maximum score before exponentiating:

\[
s_j=z_j-\max_k z_k,\qquad p_j=\frac{e^{s_j}}{\sum_k e^{s_k}}.
\]

The maximum shifted score is zero. This avoids exponential overflow for ordinary
finite inputs. Extreme negative differences can still underflow in floating
point. For the loss, compute log probabilities directly:
\(\log p_j=s_j-\log\sum_k e^{s_k}\), rather than taking `log` of an already
underflowed probability. [Stanford CS231n, numeric stability](https://cs231n.github.io/linear-classify/).

## 4. Use the same loss we already know

For the initial model, START→a has probability 1/4, so its loss is

\[
\ell=-\ln(1/4)=\ln4\approx1.386294\text{ nats}.
\]

Read the probability of the actual observed target and take its negative
natural log. For a categorical target, this is also called **cross-entropy
loss**. A target one-hot vector and sum over classes express the same calculation,
but are not needed in the main lesson. See [the optional notes](episodes/03_weights/OPTIONAL_MATH.md).
This is one prediction’s loss. Sum the individual losses to score a complete
name, then divide by its target count for the per-prediction average.
[Source: Dive into Deep Learning, §4.1.2](https://d2l.ai/chapter_linear-classification/softmax-regression.html).

Over all training transitions, use the token-weighted average

\[
L(W)=-\frac{1}{9}\sum_{t=1}^{9}\ln p_W(y_t\mid x_t).
\]

Do not divide by two names, or average two per-name averages equally. The names
contribute five and four predictions. Evaluation supplies the real preceding
character at every step; generation instead feeds back the sampled character.

### Complete initial evaluation: every target

| Name | Step | Input row | Actual target | Probability | Loss |
|---|---:|---|---|---:|---|
| anna | 1 | START | a | 1/4 | ln 4 |
| anna | 2 | a | n | 1/4 | ln 4 |
| anna | 3 | n | n | 1/4 | ln 4 |
| anna | 4 | n | a | 1/4 | ln 4 |
| anna | 5 | a | END | 1/4 | ln 4 |
| ava | 1 | START | a | 1/4 | ln 4 |
| ava | 2 | a | v | 1/4 | ln 4 |
| ava | 3 | v | a | 1/4 | ln 4 |
| ava | 4 | a | END | 1/4 | ln 4 |

Anna contributes total loss 5 ln 4; ava contributes 4 ln 4.
The combined total is 9 ln 4 ≈ 12.476649 nats. Divide by 9 targets:

\[
L=\frac{5\ln4+4\ln4}{9}=\ln4\approx1.386294.
\]

The average equals each individual loss only because all target probabilities
are equal in this starting model. No weights changed while we evaluated it.
An actual training step also chooses and applies an update.

## 5. An adjustment that helps—and one that fails

Start with **all 16 weights zero**. Every prediction has probability 1/4,
so both the training average and the held-out `ana` average are
\(\ln4\approx1.386294\). This is an initial model, not a trained result.

Change only \(W_{a,\mathrm{END}}\) from zero to \(\ln2\). Its score row
becomes `[0,0,0,ln 2]`, exponentials `[1,1,1,2]`, and probabilities
`[1/5,1/5,1/5,2/5]`. The other input rows stay uniform. The four training
targets after `a` are `n`, `END`, `v`, `END`. Their average loss changes from
1.386294 to

\[
L_a=\frac{2\ln5+2\ln(5/2)}4\approx1.262864.
\]

The other five predictions still cost ln 4 each, so the full training loss is

\[
L=\frac{5\ln4+2\ln5+2\ln(5/2)}9\approx1.331437.
\]

We chose a change, measured it, and found a smaller training loss. We have not
derived a rule that knows which weight to change or by how much.

Now set that same weight to **ln 100**, leaving everything else at zero.
The `a` row becomes `[1,1,1,100]/103`. An END target looks excellent:
\(-\ln(100/103)\approx0.029559\). But `n` and `v` each cost
\(\ln103\approx4.634729\). Full training loss rises to **1.806672**.

This is the honest failure: making one favored outcome extremely confident
can worsen the total objective. END follows `a` only twice in four training
observations. Score all observations, not just the one that looks good.
The reproducible [arithmetic check](episodes/03_weights/verify_theory.py)
prints these values; its tests check the hand-derived expressions.

## 6. What the new parameterization has not changed

This remains a one-character bigram. Every occurrence of a uses the same a row,
so the first and last a in anna have the same predicted distribution. Changing
that row does not change predictions after n or v. Richer shared representations
arrive in Episode 07. Positive loss is not automatically an error: one input can
have multiple observed continuations, and one probability row cannot assign
probability one to all of them.

Constructing weights from smoothed count probabilities, exact-zero caveats,
and the row-optimum argument are retained in [optional notes](episodes/03_weights/OPTIONAL_MATH.md),
outside the recording route. The main demonstration does not require smoothing.

## 7. Generate, and establish the next question

Begin at START. Select its weight row, apply softmax, sample a next token.
If it is END, stop. Otherwise append it and use that character as the next
input. A safety cap is not an END prediction. Softmax alone does not perform
sampling, and choosing the largest probability every time is a different
generation rule. Empty names remain possible for finite logits.

No new real-data experiment or test-set result is claimed in this theory
package. Toy losses specify the corpus and denominator above and should not
be compared to the 27-outcome names experiment's losses.

The final question is: **How do we know which changes will reduce the loss?**
Episode 04 answers using derivatives and gradients. This episode supplies the
function whose behavior those tools will study. Richer learned representations
and shared prediction machinery arrive in Episode 07.

## Sources and correctness review

Sources checked September 28, 2026. The examples, numbers, script, and curriculum
choices are our own; they instantiate established methods.

- [Dive into Deep Learning, softmax regression](https://d2l.ai/chapter_linear-classification/softmax-regression.html): softmax and categorical NLL.
- [Stanford CS231n, linear classification](https://cs231n.github.io/linear-classify/): score functions and stable softmax.
- [NumPy, matmul](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html): array shape and multiplication semantics.
- [Bridge learning notes](episodes/02_bridge/THEORY.md): project continuity and the independent-row limitation.

Review checklist: keep input/output orders visible; normalize each output row;
include END in loss; distinguish scores from probabilities, fitting from
prediction, constructed weights from optimized weights, and training fit from
generalization. Verify the equations with the included NumPy checks before
changing any displayed number. See [the preparation review](EPISODE_03_REVIEW.md)
for executed verification and remaining production work.
