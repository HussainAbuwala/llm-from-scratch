# Episode 02 — Trigrams and the sparsity wall

Status: Recorded theory reference · finalized September 10, 2026.

Audience materials: [theory companion guide (PDF)](docs/episode-02-theory.pdf),
[guide source](docs/episode-02-theory.md), and
[29-frame canvas (PDF)](docs/episode-02-canvas.pdf).

Use [the editable theory canvas](canvas/episode_02_trigrams.excalidraw) and
[the frame-by-frame presenter guide](canvas/EPISODE_02_CANVAS_GUIDE.md) for
recording. [The offline theory reader](canvas/episode_02_theory.html) follows the
same frames. Speaker notes are hidden by default.

## The promise of this video

By the end, viewers can explain how an extra context token changes a count
model, why fixed data can become sparse as context grows, how that affects
predictions, and which practical responses can help.

The theory uses hand-worked examples and diagrams. **The real-data experiment,
Python implementation, parameter sweeps, output samples, and measured validation
curves belong to the separate coding video.** See the
[coding-video plan](episodes/02_trigrams/CODING_VIDEO_PLAN.md).

Prerequisites: Episode 01's counts, conditional probabilities, NLL, generation,
and smoothing. No Python syntax, calculus, or matrix operations are needed on
camera. The presenter guide supplies narration and pointing cues; this document
is the fuller explanation, with properly formatted mathematics.

**Opening line:** “Our first model remembered one character. What changes if
we let it remember two—and why can't we keep adding memory to a count table
without thinking about the data?”

**Central claim:** Longer context can distinguish useful patterns. With a fixed
dataset, it can also leave each pattern supported by fewer observations.
There is no universal context length at which counting suddenly fails.

## 1. Change the question the model can ask

An $n$-gram model uses the previous $n-1$ tokens to predict one next token. A bigram
uses one; a trigram uses two. Count normalization estimates the conditional
probabilities; add-k smoothing assigns pseudocounts. Backoff and interpolation
can use shorter histories when longer histories have weak evidence. These are
established methods, described in [Jurafsky and Martin, Chapter 3](https://web.stanford.edu/~jurafsky/slp3/3.pdf).

Our project uses characters. Therefore a trigram prediction looks like:

```text
context        target
(a, n)      -> n
```

The **three** in trigram counts the two context tokens plus the target. It does
not mean predicting three characters, or looking back three characters.

The bigram model asks $P(\text{next} \mid n)$. It has to use that same row after `an` and
`nn`. The trigram asks $P(\text{next} \mid a,n)$ or $P(\text{next} \mid n,n)$. Those can be different.

The extra context separates the shared row:

```text
Bigram                           Trigram
                                 (a,n) -> its own distribution
n -> one distribution     =>
                                 (n,n) -> its own distribution
```

More context gives the model a way to distinguish situations. It does not
supply extra observations of those situations.

## 2. Keep the old names; change the windows

We reuse the training names `anna` and `ava`. Write S for START and E for END.
Our boundary convention supplies two START tokens as initial context, then
predicts every character and exactly one END:

```text
S S a n n a E
S S a v a E
```

These are the complete training examples:

| Name | Context | Target |
|---|---|---|
| anna | (S,S) | a |
| anna | (S,a) | n |
| anna | (a,n) | n |
| anna | (n,n) | a |
| anna | (n,a) | E |
| ava | (S,S) | a |
| ava | (S,a) | v |
| ava | (a,v) | a |
| ava | (v,a) | E |

There are still **nine predictions**: five from `anna`, four from `ava`.
Padding is input, never a target. Reset the context at each name; never count
a transition from the end of one name into the beginning of another.

## 3. Build every row by hand

Let $C(h,t)$ be the count of target $t$ after context $h$. The row total,
$C(h)$, is the sum of those counts over all allowed targets:

$$
C(h) = \sum_{t \in \mathcal{V}_{\text{out}}} C(h,t)
$$

Here, $\mathcal{V}_{\text{out}}$ means the set of allowed next-token outcomes.
For an observed row, divide each target count by that row total:

$$
P(t \mid h) = \frac{C(h,t)}{C(h)}
$$

Read $P(t \mid h)$ as “the probability of token $t$, given context $h$.”

Our outcome vocabulary is `[a, n, v, E]`. START is not an outcome.

| Context | a | n | v | E | Row total |
|---|---:|---:|---:|---:|---:|
| (S,S) | 2 | 0 | 0 | 0 | 2 |
| (S,a) | 0 | 1 | 1 | 0 | 2 |
| (a,n) | 0 | 1 | 0 | 0 | 1 |
| (n,n) | 1 | 0 | 0 | 0 | 1 |
| (n,a) | 0 | 0 | 0 | 1 | 1 |
| (a,v) | 1 | 0 | 0 | 0 | 1 |
| (v,a) | 0 | 0 | 0 | 1 | 1 |

Notice why $P(n \mid S,a) = \frac{1}{2}$ while
$P(n \mid a,n) = 1$. The denominators describe different groups of observations.

### Follow generation

Start at `(S,S)`. It must generate `a`. Now use `(S,a)`; it chooses `n` or `v`
with equal probability. Thereafter each reached row has one observed outcome.
Consequently the unsmoothed toy trigram produces only `anna` and `ava`:

$$
\begin{aligned}
P(\text{anna}) &= 1 \times \frac{1}{2} \times 1 \times 1 \times 1 = \frac{1}{2} \\
P(\text{ava}) &= 1 \times \frac{1}{2} \times 1 \times 1 = \frac{1}{2}
\end{aligned}
$$

These outputs look convincing because they are exactly the training names.
That is not evidence that the model handles unseen names well. This particular
corpus creates memorization; trigrams do not inherently generate only training
examples on every corpus.

### Follow evaluation on ana

Evaluation uses the actual preceding characters of the supplied name. It does
not sample a continuation and score that instead.

| Context | Observed target | Probability |
|---|---|---:|
| `(S,S)` | `a` | $1$ |
| `(S,a)` | `n` | $\frac{1}{2}$ |
| `(a,n)` | `a` | $0$ |
| `(n,a)` | `E` | $1$ |

$$
P(\text{ana}) = 1 \times \frac{1}{2} \times 0 \times 1 = 0
$$

Episode 01's bigram gave `ana` probability $\frac{1}{16}$ and NLL $0.693147$ nats per
prediction. Our trigram gives it zero probability and infinite NLL. Its extra
context separated `an` from `nn`, exposing the fact that training contained
no `an -> a` example.

This is an illustrative held-out spelling, not statistical evidence about the
best model order. The larger experiment will supply a broader comparison.

## 4. Two different kinds of missing evidence

Do not confuse these cases:

| Query | What training contains | Unsmoothed result |
|---|---|---|
| $P(a \mid a,n)$ | The context `(a,n)` exists; its only target was `n` | $\frac{0}{1} = 0$ |
| $P(a \mid v,n)$ | No prediction ever used context `(v,n)` | $\frac{0}{0}$; row unspecified |

For an unseen context, maximum likelihood provides no preferred distribution:
that row had no effect on training likelihood. A program returning an all-zero
row would not produce a normalized probability distribution.

An unspecified row needs a policy before the model can assign probabilities
there. This is different from a known row assigning zero to one target: that
zero genuinely makes a complete path's NLL infinite. Smoothing supplies a
normalized distribution for both cases.

### Add-k, worked all the way through

With $K$ allowed outcomes and smoothing amount $k > 0$:

$$
P_k(t \mid h) = \frac{C(h,t) + k}{C(h) + kK}
$$

The subscript $k$ identifies the smoothing amount. Read this as “the probability
of token $t$, given context $h$, with smoothing amount $k$.” The denominator
adds $k$ once for each of the $K$ possible outcomes.

For our toy, $K = 4$. Set $k = 1$:

$$
\begin{aligned}
P_1(a \mid a,n) &= \frac{0+1}{1+4} = \frac{1}{5} \\
P_1(a \mid v,n) &= \frac{0+1}{0+4} = \frac{1}{4}
\end{aligned}
$$

Every entirely unseen row becomes uniform, for **any positive $k$**. Increasing
$k$ cannot extract a preference from zero observations.

Now score `ana` again, including the changed probabilities at every step:

$$
P_1(\text{ana}) = \frac{3}{6} \times \frac{2}{6} \times \frac{1}{5} \times \frac{2}{5} = \frac{1}{75}
$$

$$
\operatorname{NLL} = -\frac{\ln(1/75)}{4} \approx 1.079372
\quad \text{nats per prediction}
$$

Smoothing fixes the zero, but it also takes probability away from observed
outcomes. You cannot change only the failing step and leave all other rows
unsmoothed. These are exact toy probabilities; the displayed NLL is rounded.

An unknown character is a third issue. Smoothing over `[a,n,v,E]` cannot create
a probability for `z`. Unknown tokens require a separate vocabulary policy.

## 5. Derive the sparsity wall

### More specific questions use smaller groups of observations

Return to `anna` and `ava`. The bigram's `n` row pools two observations:
one `n` followed by `n`, and one `n` followed by `a`. The trigram splits them:

| Model | Question | Matching observations | Unsmoothed estimate |
|---|---|---|---|
| Bigram | What follows `n`? | `n` once, `a` once | One-half each |
| Trigram | What follows `an`? | `n` once | $P(n\mid a,n)=1$ |
| Trigram | What follows `nn`? | `a` once | $P(a\mid n,n)=1$ |

**Say:** “The estimate became 100%, but it is based on one matching example.
That is what happened in our training sample; it does not prove a universal
rule about names.”

The extra detail can be useful. But in our held-out `ana` example, `a` follows
`an`, so the unsmoothed trigram fails on that continuation. This illustrates
what sparse evidence can do; it does not establish that trigrams are generally
worse than bigrams.

### Continue beyond trigrams: a separate controlled example

For this demonstration only, replace the training corpus with four constructed
strings. Do not combine these counts with the original toy table:

```text
anna    enna    inna    onna
```

Each has four letters and contributes five predictions including END. There
are **20 training observations**, regardless of context length.

Focus on predictions of the last `a`. A two-character context pools four
observations into one row. A three-character context separates them:

| Two-character context | Count | Three-character context | Count |
|---|---:|---|---:|
| `(n,n)` followed by `a` | 4 | `(a,n,n)` followed by `a` | 1 |
| | | `(e,n,n)` followed by `a` | 1 |
| | | `(i,n,n)` followed by `a` | 1 |
| | | `(o,n,n)` followed by `a` | 1 |

Both model orders currently assign probability one to `a` in these rows. So
**splitting evidence does not automatically change a prediction or make it
wrong**. It makes each longer-context estimate depend on fewer observations.
Each of these new rows is a **singleton**: its total training count is one.

Now ask a local prediction question after a supplied prefix ending in `nnn`:

- The trigram uses `(n,n)`, which has four observations, all followed by `a`.
- The 4-gram uses `(n,n,n)`, which has no observations. Its raw count estimate
  is unspecified.

This is a comparison of next-token queries on a supplied history, not a claim
that either unsmoothed model generated the prefix `nnn`. Every character is
known; it is the combination that is missing. Here the four-string vocabulary
has five ordinary characters (`a,e,i,n,o`); plus END gives six outcomes.
With positive add-k smoothing, the unseen row would be uniform over those six
outcomes. We do not reuse the original toy's four-outcome denominator here.

**Say:** “Longer context is asking a more specific question. The answer may be
useful, but the data must contain enough matching examples to estimate it.”

### Why the number of possible rows grows so quickly

Use the alphabet `a`, `n`, `v` for the counting illustration. Ignore boundaries
first. One position gives three choices. Two positions give:

```text
aa   an   av
na   nn   nv
va   vn   vv
```

There are $3\times3=3^2=9$ pairs. Three positions give
$3\times3\times3=3^3=27$ possibilities. Each added position multiplies the
number of ordinary-character contexts by the alphabet size.

In general, $A$ ordinary characters and $m$ context positions give $A^m$
ordinary-character contexts. This counts possibilities, not a claim that they
are equally likely or that all appear in natural data.

Include valid START prefixes next. For 26 characters and two context positions:

$$
R_2 = \underbrace{1}_{(S,S)} + \underbrace{26}_{(S,\text{letter})}
+ \underbrace{26^2}_{(\text{letter},\text{letter})} = 703
$$

START only appears at the beginning; `(a,S)` is invalid. END is a predicted
outcome, never part of a context. Under these conventions:

$$
R_m = 1 + A + A^2 + \cdots + A^m
$$

Each row has $A+1$ next-token outcomes, including END:

$$
\text{Possible cells} = R_m(A+1)
$$

| Context characters | Model order | Possible rows, $A=26$ | Possible cells |
|---|---|---:|---:|
| 1 | bigram | 27 | 729 |
| 2 | trigram | 703 | 18,981 |
| 3 | 4-gram | 18,279 | 493,533 |
| 4 | 5-gram | 475,255 | 12,831,885 |
| 5 | 6-gram | 12,356,631 | 333,629,037 |

These numbers are **calculated capacities**, not measurements from the names
experiment. A sparse implementation need not allocate these cells.

The observation count, meanwhile, remains:

$$
N_{\text{train}} = \sum_{\text{name in training}}
\bigl(\operatorname{length}(\text{name})+1\bigr)
$$

Read the sum aloud as “for each name, its number of letters plus one END.”
The original two-name corpus contributes nine observations. The separate
four-string illustration contributes twenty. Extra START pads add no targets.

**The sparsity wall is a relationship between context detail and available
data.** Possible rows multiply; many contexts receive little or no evidence.
Observed rows need not increase at every step, and held-out loss need not worsen
at every step. The practical question is how well a chosen model predicts new
data.

### Would a sparse dictionary solve this?

It solves the storage part: keep only observed counts. A missing target entry
means zero count; an absent context has total zero. Smoothed probabilities can
be calculated when needed, using the full allowed outcome vocabulary.

It does not supply missing observations. The model can fit comfortably in
memory and still lack evidence for many queries. **Saving the space occupied
by an empty row does not teach us what belongs in that row.**

## 6. What can we do about sparse evidence?

Present these as practical responses with limits, not guaranteed fixes:

| Response | What it helps with | What it does not guarantee |
|---|---|---|
| Collect more representative data | More matching observations for useful contexts | Coverage of every long context |
| Use a shorter context | Pool more observations into each row | Preserve every useful distinction |
| Smooth the probabilities | Avoid zero probabilities for known outcomes | Learn a preference from an entirely empty row |
| Consult shorter histories | Reuse evidence available at lower model orders | Find the best fallback or mixture without evaluation |
| Learn shared representations | Let related patterns inform one another through shared parameters | Generalize well without sufficient data and suitable training |

Choose context lengths and smoothing choices using held-out validation data.
Repeated copies of the same examples do not provide new independent evidence.
Add-k is our transparent teaching method; stronger classical smoothing methods
exist. Empirical method comparisons are discussed by
[Chen and Goodman (1996)](https://aclanthology.org/P96-1041/).

## 7. Shorter histories are still useful

**Keep this in the theory video, briefly.** It answers the natural question:
“Can we reuse the information we already had in the bigram?” There is no need
for a full implementation or a survey of smoothing algorithms.

Return explicitly to the original training corpus: **`anna` and `ava`**.

### Backoff: use a shorter-history rule when needed

The context `(v,n)` has no observations. But its suffix `n` has two: one `n`
and one `a`. A simple, fully defined rule for this illustration is:

> Use the observed trigram row when it exists. If the entire context is unseen,
> use the bigram row for its last token. If that row is also unseen, use a
> uniform fallback over the allowed outcomes.

For the missing `(v,n)` row, this gives one-half to `n`, one-half to `a`, and
zero to `v` and END. It is a normalized distribution, but **this simple
whole-row fallback still permits zero probabilities**. For example, the known
`(a,n)` row would still assign zero to `a`. It is not a complete zero-probability
solution or an implementation of Katz backoff. More sophisticated backoff
methods discount and reallocate probability carefully.

### Interpolation: combine longer and shorter histories

Instead of choosing one row, mix two defined probability distributions:

$$
P_{\text{mix}}(t\mid a,b)
= \lambda P_{\text{tri}}(t\mid a,b)
+ (1-\lambda)P_{\text{bi}}(t\mid b)
$$

$\lambda$ is the weight given to the trigram, between zero and one. If both
rows sum to one, their weighted mixture also sums to one. This retains specific
context while using broader evidence.

For one optional worked number, smooth both original toy models with $k=1$
and mix equally:

$$
P_{\text{tri}}(a\mid a,n)=\frac{1}{5},
\qquad P_{\text{bi}}(a\mid n)=\frac{1+1}{2+4}=\frac{1}{3}
$$

$$
P_{\text{mix}}(a\mid a,n)
=\frac{1}{2}\times\frac{1}{5}+\frac{1}{2}\times\frac{1}{3}=\frac{4}{15}
$$

That is more probability for the problematic continuation than the smoothed
trigram alone gives it. It is not proof of a better whole-model held-out score.
The weight one-half is a teaching choice, not an experimentally selected optimum.
Both component rows must exist; mixing an undefined distribution is not valid.

**Recording emphasis:** backoff consults a shorter history by a rule;
interpolation combines histories by weights. These are established responses
within n-gram modeling, described in
[Jurafsky and Martin, “N-gram Language Models”](https://web.stanford.edu/~jurafsky/slp3/3.pdf).
A short explanation and one visual per method are enough.

## 8. What the coding video will test; where the series goes

**Closing narration:** “We can now predict the tradeoff: extra context may
capture useful patterns, while sparse rows may weaken our estimates. In the
coding video, we'll build these tables on a larger names dataset and measure
which effect wins. We won't assume that more context always helps—or always
hurts.”

The coding video implements counts, on-demand smoothing, generation, and
consistent NLL evaluation; then compares context lengths and smoothing amounts.
It checks training fit, held-out predictions, singleton rows, and unseen contexts.
It tests the practical consequences of our explanation; one experiment does not
prove a universal ranking of model orders or smoothing methods. The primary
planned sweep remains add-k; backoff/interpolation are optional extensions.

After that companion build, Episode 03 learns the familiar bigram task using
weights and softmax. It introduces learning parameters; an unconstrained bigram
weight matrix alone does not solve longer-context sparsity. Embeddings and the
MLP arrive in Episode 07, where learned representations allow parameter sharing
across contexts. This motivation is central to
[Bengio et al. (2003)](https://jmlr.org/papers/v3/bengio03a.html).

Our endpoint remains a small decoder-only Transformer we implement, train at
laptop scale, and use to generate text. We move past counting as a curriculum
choice, not because classical models become useless after trigrams.

## Presenter appendix — details to keep off the main path

### Possible cells versus independent probabilities

A naive array with $(A+1)^m$ context slots also includes invalid START
placements. The valid-row formula excludes those. With $K$ outcomes in a
normalized row, choosing $K-1$ valid probabilities fixes the last as one minus
their sum. Thus “cells” and “independent parameters” are different counts.
This precision is useful for questions, but unnecessary for the main explanation
of sparse evidence; it has no dedicated recording frame.

### Evidence standard and correctness review

**Established material:** conditional count estimates, n-gram histories,
smoothing, backoff/interpolation, and learned representation sharing. The linked
textbook and papers supply the foundations. References rechecked September 10,
2026; the Stanford chapter is the August 19, 2026 draft.

**Pedagogical simplifications:** character tokens, tiny constructed corpora,
add-k, and a whole-row fallback example. None is claimed to be a competitive
modeling recipe. Distinguish the two-name model, the four-string evidence
illustration, and the 26-character capacity calculation every time data changes.

**Engineering choices:** separate START/END, one END target per name, repeated
START padding, and storage of observed counts only. These preserve the same
prediction denominator when context length changes.

**Correctness gates before recording:** reproduce both toy corpora's counts,
path probabilities, NLL, normalization, interpolation and fallback examples;
verify the capacity arithmetic; render and inspect every frame. Exact results
are checked by `episodes/02_trigrams/test_lesson_material.py` together with the
existing `test_lab.py`. The review record is
[EPISODE_02_REVIEW.md](EPISODE_02_REVIEW.md).

**Quick understanding check:** explain why 100% from one observation is not
proof of a general rule; distinguish an unseen target from an unseen row;
explain why sparse storage adds no evidence; and name a response with its limit.
No experiment or coding exercise is required before recording the theory.
