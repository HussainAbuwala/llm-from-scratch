# Episode 1 Theory: The Smallest Language Model

Status: Learning draft

Research policy: [RESEARCH_STANDARD.md](RESEARCH_STANDARD.md)

## What this chapter is

In this episode we will build a character-level bigram language model. It will
read a collection of text examples, count which characters follow which other
characters, convert those counts into probabilities, and generate new text one
character at a time.

This is an established kind of language model, not a modern LLM and not yet a
neural network. We are using it because every part of the language-modeling
process remains small enough to inspect.

The established material in this chapter includes n-gram language modeling,
conditional probability, likelihood, negative log-likelihood, and smoothing.
Character tokens, a tiny line-based dataset, and our teaching order are
pedagogical choices. The examples and code organization are project choices.

By the end of the learning phase, we should be able to explain:

1. What a language model predicts.
2. What tokens, a vocabulary, and context mean.
3. How text becomes input-target transitions.
4. How counts become a probability table.
5. What the finished model actually contains.
6. How greedy decoding and sampling generate text.
7. How training, evaluation, and generation differ.
8. How likelihood, logarithms, and average NLL measure performance.
9. What baselines a loss number has to be compared against to mean anything.
10. Why smoothing helps with unseen transitions, and what it costs.
11. Why a bigram model cannot capture long-range structure.

## Prerequisites

### Python

- Strings and characters
- Lists and dictionaries
- For loops
- Functions
- Indexing
- Basic arithmetic

### Mathematics

- Counts and fractions
- A probability as a number between 0 and 1
- A probability distribution whose values add up to 1
- Multiplication

Logarithms are introduced from first principles in the evaluation section. No
calculus, linear algebra, neural-network knowledge, or PyTorch experience is
required yet.

## 1. What is a language model?

A language model assigns probabilities to possible token sequences. We can use
that ability one step at a time: given some context, it returns a probability
distribution over the next possible token.

Given:

~~~text
The cat sat on the
~~~

a word-level model might produce something conceptually like:

~~~text
mat       0.32
floor     0.19
chair     0.08
moon      0.0001
...
~~~

The output is not only one answer. It is a probability for every possible next
token. The probabilities communicate what the model considers more or less
plausible.

Generation repeatedly applies this process:

1. Produce next-token probabilities.
2. Choose one token.
3. Append it to the context.
4. Predict again.

This gives us the central idea of the series:

> A language model repeatedly predicts a probability distribution over the
> next token.

Modern autoregressive LLMs and our bigram model share this broad next-token
framework. They differ enormously in architecture, context length, data,
parameters, training method, and capability.

## 2. Tokens, vocabulary, and integer IDs

A computer needs a finite set of symbols. The units processed by a language
model are called **tokens**, and the complete set of token types the model
recognizes is its **vocabulary**.

Tokens can be:

- Characters: c, a, t
- Words: cat
- Pieces of words: un, plan, ned
- Raw bytes

For Episode 1, every distinct character is one token. The text cat contains
three tokens: c, a, and t.

Character tokenization is useful for the first model because:

- The vocabulary is small.
- Unseen words remain representable if their characters are in the vocabulary.
- We can inspect the complete probability table.

It is inefficient for serious language models because a single word may require
many prediction steps. We will build a better tokenizer later.

The model will not operate directly on character strings. We create two
mappings:

~~~text
character -> integer ID
integer ID -> character
~~~

For example:

~~~text
<START> = 0
<END>   = 1
a       = 2
n       = 3
v       = 4
~~~

Integer IDs let us use characters as row and column positions in a matrix.

## 3. Context and bigrams

The **context** is the information the model is allowed to use when predicting
the next token.

A modern Transformer may use thousands of earlier tokens. Our first model uses
exactly one previous character.

For the text hello, the adjacent pairs are:

~~~text
h -> e
e -> l
l -> l
l -> o
~~~

Each pair of consecutive tokens is a **bigram**. Bi means two. A bigram model
predicts the next token using only the current token:

~~~text
P(next character | previous character)
~~~

The vertical bar means “given.” Therefore:

~~~text
P(n | a)
~~~

means:

> The probability that the next character is n, given that the current
> character is a.

This is a simplifying assumption. The ideal target would use everything that
came before:

~~~text
P(next character | all previous characters)
~~~

Our model deliberately throws away all but the final character.

This simplification has an established name. Assuming that the next token
depends only on the last few tokens rather than the entire history is the
**Markov assumption**, and a bigram model is the first-order case: context
length one. "Bigram model", "2-gram model", and "first-order Markov model"
describe the same family of assumptions.

## 4. Boundaries and transitions

Suppose the dataset contains two independent examples:

~~~text
anna
ava
~~~

We add special boundary tokens:

~~~text
<START> a n n a <END>
<START> a v a <END>
~~~

The start token lets the model learn which characters commonly begin an
example. The end token lets it learn when to stop.

### Why the end token is not optional

The end token does more work than it appears to. Without it, the model would
never assign probability to *stopping*, so its probabilities would no longer
describe complete examples — only endless streams of characters. Two concrete
consequences:

- Generation would have no natural stopping rule. We would have to cut every
  sequence off at an arbitrary length and hope it looked finished.
- Evaluation would silently stop caring about length. A model that believes
  names never end would lose no points for that belief.

By treating `<END>` as an ordinary token that must be predicted like any other,
"this example is finished here" becomes something the model is scored on.

A **transition** is one token followed immediately by another. The arrow means
“was followed by.” We count adjacent, ordered pairs rather than merely counting
individual characters.

For anna:

~~~text
<START> -> a
a       -> n
n       -> n
n       -> a
a       -> <END>
~~~

For ava:

~~~text
<START> -> a
a       -> v
v       -> a
a       -> <END>
~~~

Combining identical transitions produces:

~~~text
<START> -> a       2
a       -> n       1
a       -> v       1
a       -> <END>   2
n       -> n       1
n       -> a       1
v       -> a       1
~~~

Direction matters. The transitions a -> n and n -> a are different.

Looking only at transitions out of a, there are four observations:

~~~text
a -> n       once
a -> v       once
a -> <END>   twice
~~~

These observations later become the probabilities 1/4, 1/4, and 2/4.

## 5. Training by counting

For this model, training means using the training examples to determine the
transition statistics:

~~~text
training examples
       ↓
extract adjacent transitions
       ↓
count each transition
       ↓
normalize each row
       ↓
probability table
~~~

There is no gradient descent, optimizer, or repeated loss-driven parameter
update. Counting and normalization finish the training process.

The count matrix has one row for each possible current token and one column for
each possible next token:

~~~text
                             next token
                          a   n   v  <END>
              <START>  [  2,  0,  0,   0 ]
current token a        [  0,  1,  1,   2 ]
              n        [  1,  1,  0,   0 ]
              v        [  1,  0,  0,   0 ]
~~~

Each cell answers:

> How many times did the column token follow the row token?

### The rows and columns are not the same set

This is easy to get wrong in code, so it is worth stating explicitly:

- `<START>` is a row but never a column. Nothing can be followed *by* the start
  of an example.
- `<END>` is a column but never a row. Nothing follows the end of an example.
- Every ordinary character is both a row and a column.

With V ordinary characters, the matrix is therefore (V + 1) rows by (V + 1)
columns, and every cell in it describes a transition that is at least possible.
That property matters in Section 11: when we add pseudo-counts, we want to
spread probability only across cells that could legitimately occur.

A common alternative design uses a single boundary token for both jobs —
Karpathy's *makemore* uses `.` — which makes the matrix square over one shared
vocabulary. We keep two tokens because the two jobs, "how examples begin" and
"when examples end", are easier to see separately. Both designs are correct.

## 6. Normalization and the finished model

Counts are not probabilities. To turn one row into a probability distribution,
divide every count by the total of that row.

For the row representing a:

~~~text
counts = [0, 1, 1, 2]
total  = 4

probabilities = [0/4, 1/4, 1/4, 2/4]
              = [0.00, 0.25, 0.25, 0.50]
~~~

Therefore:

~~~text
P(n | a)     = 0.25
P(v | a)     = 0.25
P(END | a)   = 0.50
~~~

A probability distribution must contain non-negative values that add up to 1.
Dividing every count by the same row total is **normalization**.

Normalization changes the scale but preserves relative proportions. END
occurred twice as often as n after a, so its normalized probability remains
twice as large.

In this section, normalization specifically means:

~~~text
probability =
transition count / total transitions from the current token
~~~

The word normalization has other meanings elsewhere in machine learning.

### What exactly is the finished model?

The finished count-based model consists conceptually of:

- The vocabulary and integer mappings
- The start and end token conventions
- A probability row for every possible current token

Its central artifact is:

~~~text
P(next token | current token)
~~~

The counts are the evidence used to construct the probability table. We may
keep them so that we can inspect the data or change smoothing, but generation
and evaluation query the probabilities.

Normalizing observed counts is the **maximum-likelihood estimate** for a basic
unsmoothed bigram model: it chooses row probabilities that make the observed
transitions as likely as possible under this model's assumptions.

That claim is stronger than it sounds, and it is the hinge between this episode
and the rest of the series. In Section 10 we define a loss: average negative
log-likelihood. For this model class, dividing counts by row totals is not
merely *a* reasonable way to produce probabilities — it is the exact minimizer
of that loss on the training data. No bigram table scores better on this
training set, and we obtained it in a single pass with no optimizer at all.

Hold on to that, because the next model will not have this luxury. A neural
network starts from random numbers and uses gradient descent to crawl, step by
step, toward a training loss that counting hands us for free. Watching it arrive
at roughly the same number is how we will know the machinery is working.

## 7. Training, evaluation, and generation

These are three distinct activities.

### Training

~~~text
training examples -> counts -> normalized probabilities
~~~

Training creates the model.

### Evaluation

~~~text
fixed model + evaluation examples -> numerical score
~~~

Evaluation measures the model without changing its counts or probabilities.
The score gives feedback to us. We might use it to choose a smoothing value,
collect different data, or design a better model.

The outer development loop is:

~~~text
train
  ↓
evaluate
  ↓
human examines the results
  ↓
change a design choice
  ↓
train a new model
~~~

There is no automatic evaluation-to-parameter feedback mechanism inside this
count-based model.

A neural model will be different during training:

~~~text
training example
  ↓
prediction
  ↓
loss
  ↓
gradients
  ↓
parameter update
  ↓
repeat
~~~

Even for a neural model, validation and test evaluation normally measure the
model without updating it.

### Generation

~~~text
fixed model + current token -> choose a next token -> repeat
~~~

During generation, no correct next token is supplied. The model is producing a
new sequence.

The mechanisms differ, but the objective is the same one: assign high
probability to the token that actually came next in each observed context.
Counting reaches the best possible value of that objective in closed form; a
neural network approaches it iteratively using gradients. Both are minimizing
average negative log-likelihood — one analytically, one numerically.

## 8. Training, validation, and test sets

To measure whether the model handles unseen examples, split the available
examples into separate groups.

### Training set

Used to create the transition counts and probability table.

### Validation set

Used to compare project choices, such as the smoothing strength. Validation
examples do not contribute to the transition counts.

### Test set

Used for a final measurement after the major choices are settled. Repeatedly
changing the model in response to test results gradually turns the test set into
another validation set, so the test set should be consulted sparingly.

If validation or test examples influence the counts, the model has already seen
the information on which we claim to evaluate it. This is **data leakage**.

For early demonstrations we may inspect training loss to verify that the
implementation works. Held-out validation and test loss are the evidence of
generalization.

### Where the vocabulary comes from

Splitting the data raises a question that is easy to skip past: which characters
are in the vocabulary?

Building the vocabulary from the entire dataset is convenient, but it leaks a
small amount of information out of validation and test — namely, which
characters exist at all. Building it from the training split alone is the honest
choice, and it immediately creates a second problem: a validation example may
contain a character the model has never seen and has no row, column, or ID for.

Our project choice for Episode 1:

1. Build the vocabulary from the training split only.
2. Check the validation and test splits for characters outside it, and report
   any we find rather than crashing or silently skipping them.
3. Use a dataset and split where that count is zero, so this episode is not
   complicated by the issue.

The general solutions — mapping unknown characters to a reserved `<UNK>` token,
or using byte-level tokens so that nothing can ever be out of vocabulary — are
real techniques we will need later. Naming the problem is enough for now.

## 9. Generating text

Generation starts at the start token:

1. Look up the probability row for the current token.
2. Choose one possible next token.
3. Append it to the output.
4. Make it the new current token.
5. Stop if END is selected; otherwise repeat.

There are different ways to make step 2.

### Greedy decoding

Greedy decoding always chooses the highest-probability next token.

Suppose the strongest transitions are:

~~~text
<START> -> a
a       -> n
n       -> a
~~~

Greedy decoding can become trapped in:

~~~text
anananan...
~~~

It always makes the best-looking immediate choice. It does not search for the
best complete sequence and never selects a lower-probability escape such as
a -> END.

Greedy decoding is deterministic, reproducible, and useful when variation is
undesirable.

### Sampling

Sampling treats the probabilities as chances:

~~~text
a: 60%
b: 30%
c: 10%
~~~

Across many draws, a should be selected approximately 60% of the time, b
approximately 30%, and c approximately 10%. This is weighted randomness, not
equal randomness.

Sampling produces variety and exposes the full learned distribution. A random
seed makes a particular run reproducible.

Neither greedy decoding nor sampling is universally correct. We will implement
both and compare their behavior. Temperature, top-k, and top-p are later
extensions rather than Episode 1 requirements.

### Generation needs a stopping guarantee

Nothing forces `<END>` to ever be selected. Greedy decoding can enter a cycle it
will never leave, and sampling can, with bad luck, continue for a long time.
Every real implementation therefore needs a maximum length, after which
generation halts and the output is marked as truncated.

A truncated sample is a finding about the model, not a bug to hide. When greedy
decoding hits the cap, that is the clearest possible evidence of the limitation
we discuss in Section 12.

## 10. Evaluation: how do we judge the model?

Generated examples are useful but subjective. A weak model might produce one
convincing example by chance, and a presenter could unintentionally cherry-pick
it.

Evaluation asks:

> How much probability did the model assign to the next tokens that actually
> occurred in held-out text?

### Where does the correct token come from?

The evaluation data supplies it. If an evaluation example is anna:

~~~text
<START> a n n a <END>
~~~

then the evaluation input-target pairs are:

~~~text
input       correct target
<START>  -> a
a        -> n
n        -> n
n        -> a
a        -> <END>
~~~

For the pair a -> n, the input is a and the correct target is n because n
actually appears next in the evaluation example.

Suppose the model predicts:

~~~text
n       25%   <- correct target
v       25%
<END>   50%
~~~

Greedy generation would select END, but evaluation records the 25% assigned to
the target n.

During generation there is no answer key. During evaluation, existing text
provides one.

### Combining transition probabilities

Suppose the evaluation example is ana and the model assigns:

~~~text
P(a | <START>) = 0.80
P(n | a)       = 0.50
P(a | n)       = 0.25
P(<END> | a)   = 0.40
~~~

For the complete sequence to occur, every transition must occur in order:

~~~text
P(ana) =
0.80 × 0.50 × 0.25 × 0.40
= 0.04
~~~

This is the probability of one complete path through the model.

An intuitive interpretation uses 100 generation attempts:

~~~text
100 attempts
  ↓ 80% choose a
80 attempts
  ↓ 50% choose n
40 attempts
  ↓ 25% choose a
10 attempts
  ↓ 40% choose END
4 attempts
~~~

Approximately 4 of 100 attempts follow exactly that path. Each multiplication
takes a fraction of the possibilities that survived the previous step.

The precise sequential probability rule is:

~~~text
P(A and then B) = P(A) × P(B | A)
~~~

We are not multiplying unrelated probabilities. Every factor is conditional on
the context available at that step.

This is the **chain rule of probability**. Applied to a whole sequence, it says
that the probability of the sequence is the product of each token's probability
given everything that came before it. Our bigram model is exactly the chain rule
plus the Markov assumption: we keep the product, but each factor is permitted to
look at only the single preceding token.

### A quick introduction to logarithms

A logarithm answers:

> What exponent produces this number?

For example:

~~~text
10³ = 1000
therefore
log base 10 of 1000 = 3
~~~

Machine learning commonly uses the natural logarithm, written ln, whose base is
the mathematical constant e, approximately 2.718. The choice of base changes
the scale of the score, not which model ranks better.

The scale has a name. With the natural logarithm the score is measured in
**nats**; with base 2 it is measured in **bits**. If you encounter "bits per
character" in a paper, that is this same quantity computed in base 2. Dividing a
nats figure by ln(2) ≈ 0.693 converts it to bits.

The important rule is:

~~~text
log(a × b × c) = log(a) + log(b) + log(c)
~~~

Multiplying hundreds or millions of probabilities creates extremely small
numbers that a computer may round to zero, called numerical underflow. Logs
replace that unstable product with a manageable sum.

For ana:

~~~text
ln(0.80) ≈ -0.22
ln(0.50) ≈ -0.69
ln(0.25) ≈ -1.39
ln(0.40) ≈ -0.92

sum ≈ -3.22
~~~

This equals:

~~~text
ln(0.80 × 0.50 × 0.25 × 0.40)
= ln(0.04)
≈ -3.22
~~~

Probabilities are between 0 and 1, so their natural logarithms are zero or
negative. We negate the log-likelihood to create a loss where smaller is
better:

~~~text
negative log-likelihood = -log-likelihood
~~~

The per-transition penalty can be understood as surprise:

~~~text
probability on correct target    negative log penalty
100%                             0.00
50%                              0.69
10%                              2.30
1%                               4.61
~~~

High probability on the correct target creates a small penalty. Low probability
creates a large penalty.

### Averaging across transitions and examples

Total NLL naturally grows with the amount of text. A model performing equally
well on 1,000 predictions accumulates approximately ten times the total penalty
it would accumulate on 100 predictions.

We therefore calculate:

~~~text
average NLL =
sum of negative log penalties for all correct transitions
----------------------------------------------------------
total number of evaluated transitions
~~~

This answers:

> On a typical next-token prediction, how surprised was the model?

For a line-based word dataset, transitions are constructed separately inside
each word. We do not create a transition from the end of one word into the
beginning of the next.

For:

~~~text
ana
bo
~~~

ana contributes four transitions and bo contributes three:

~~~text
<START> -> a     <START> -> b
a       -> n     b       -> o
n       -> a     o       -> <END>
a       -> <END>
~~~

The primary evaluation metric sums the seven penalties and divides by seven.
It therefore encompasses all evaluation words and gives each character
transition equal weight. Longer words contribute more transitions.

An equal average of per-word scores is possible, but it answers a different
question by giving short and long words the same weight.

Lower average NLL is better because the model assigned higher probability to
the correct next tokens on average.

### Lower than what? Baselines

An average NLL of 2.4 means nothing on its own. A loss value is interpretable
only next to a reference point, so we compute two deliberately unintelligent
models on the same evaluation data.

**Uniform baseline.** Ignore the data completely and give every allowed next
token the same probability. With V ordinary characters plus `<END>`, every
prediction is 1 / (V + 1) and the average NLL is exactly:

~~~text
ln(V + 1)
~~~

For V = 26 that is ln(27) ≈ 3.30. Any model that has learned anything at all
must beat this number.

**Unigram baseline.** Use each character's overall frequency and ignore the
context entirely: P(next token), with no conditioning. This is a genuinely
informative model — it knows that `a` is common and `q` is rare — and it is the
number our bigram model must beat in order to claim that *context* helped.

The comparison we actually care about is therefore three-way:

~~~text
uniform     knows nothing
unigram     knows which characters are common
bigram      knows which characters follow which
~~~

If the bigram model does not beat the unigram model on held-out data, then one
character of context bought us nothing, and we should understand why before
building anything larger.

### Two familiar names for this same number

Two terms will appear constantly in later episodes, and both refer to the
quantity we just built:

- Average NLL over a dataset is the **cross-entropy** between the data and the
  model, measured in nats. When we later call a library function named
  `cross_entropy`, it computes what we are computing by hand here.
- **Perplexity** is exp(average NLL). An average NLL of 2.30 is a perplexity of
  10, usually read as "the model was about as unsure as if it were choosing
  uniformly among 10 options."

We will not use perplexity as our metric in Episode 1, but it is the same
measurement wearing different clothes, and it is worth being able to recognize.

## 11. Smoothing and unseen transitions

Suppose x is already a known vocabulary character because it appears elsewhere
in the training set, but x never followed a. The row counts might be:

~~~text
next token    n   v  <END>  x
count         1   1    2    0
~~~

Without smoothing:

~~~text
P(n | a)     = 25%
P(v | a)     = 25%
P(END | a)   = 50%
P(x | a)     = 0%
~~~

If evaluation contains a -> x, that transition has zero probability. The
complete sequence probability becomes zero because the factors multiply. Its
negative log penalty is unbounded because log(0) approaches negative infinity.

Zero is usually too confident for limited data. Not observing a transition is
not proof that it is impossible.

### Add-one smoothing

Add-one, or Laplace, smoothing adds one pseudo-count to every allowed outcome
before normalization:

~~~text
original counts    [1, 1, 2, 0]
smoothed counts    [2, 2, 3, 1]
new total           8
~~~

The probabilities become:

~~~text
P(n | a)     = 2/8 = 25%
P(v | a)     = 2/8 = 25%
P(END | a)   = 3/8 = 37.5%
P(x | a)     = 1/8 = 12.5%
~~~

The pseudo-count does not claim that x appeared after a. It represents
uncertainty: reserve some probability for possibilities absent from a limited
sample.

Probability must still sum to 1, so smoothing redistributes probability mass.
Giving unseen transitions nonzero probability takes some probability away from
observed transitions.

### Add-k smoothing

Adding one may be aggressive. More generally:

~~~text
smoothed count = observed count + k
~~~

For k = 0.1:

~~~text
original counts    [1,   1,   2,   0]
smoothed counts    [1.1, 1.1, 2.1, 0.1]
new total           4.4
~~~

This reserves a smaller amount of probability for unseen transitions.
Validation NLL can help us compare candidate smoothing strengths. Evaluation
does not automatically change k; we choose it through the outer development
loop.

Written as a formula, with A standing for the number of allowed next tokens in a
row — the ordinary characters plus `<END>`, as established in Section 5:

~~~text
                       count(current -> next) + k
P(next | current)  =  ------------------------------
                        total(current) + k × A
~~~

The `k × A` term in the denominator is not optional. We added k to every one of
the A cells in the row, so the row total grew by exactly `k × A`. Forgetting it
is the most common way to end up with rows that do not sum to 1, and it is the
first thing to check when a probability table misbehaves.

### What k does at the extremes

Two limits make the parameter intuitive:

- **k = 0** is no smoothing. The table is the maximum-likelihood estimate,
  unseen transitions have probability zero, and the training NLL is as low as it
  can possibly be.
- **As k grows very large**, the observed counts become negligible beside the
  pseudo-counts, and every row approaches the uniform distribution. The model
  forgets the data.

So k is a dial between "trust the counts completely" and "trust the counts not
at all". Notice what that implies for our loss: **smoothing deliberately makes
the training NLL worse.** By construction, k = 0 is unbeatable on training data.
Smoothing is not an attempt to fit the training set better — it is an admission
that the training set is a limited sample of a larger world.

Held-out data is what exposes the trade-off:

~~~text
k          training NLL       validation NLL
0          lowest             infinite if any held-out transition was unseen
small      slightly higher    usually the best value
large      much higher        rises again, drifting toward ln(V + 1)
~~~

Sweeping k and plotting both curves is the single most informative experiment in
this episode. It is also the first appearance of a pattern that governs the
entire rest of the series: the setting that makes training loss lowest is not
the setting that generalizes best.

Add-k is the simplest smoothing method, not the best one. It is presented here
because it can be verified by hand in a single row.

### Unseen transition versus unseen token

An unseen transition means both characters are in the vocabulary, but that pair
was not observed:

~~~text
a and x are known
a -> x was unseen
~~~

Smoothing can help.

An unseen token means x is not in the vocabulary at all. The model has no row,
column, or ID for it. Smoothing cannot solve that separate vocabulary problem.

Smoothing replaces:

> Unseen means impossible.

with:

> Unseen means unlikely but possible.

More advanced n-gram methods use backoff, interpolation, Good-Turing estimates,
or Kneser-Ney smoothing. Those are established techniques but are outside the
implementation scope of Episode 1.

## 12. Why this model is limited

### It remembers only one character

After seeing:

~~~text
The cat sat on the ma
~~~

the model knows only that the current character is a. It cannot remember cat,
sat, or the rest of the sentence.

All histories ending in a use the same row:

~~~text
ma
pa
za
The cat sat on the ma
~~~

They all collapse into:

~~~text
P(next character | a)
~~~

The model cannot know how it reached a, where it is in the sequence, or whether
it has already repeated a pattern.

### Local plausibility is not global coherence

From anna and ava, the model observes:

~~~text
a -> n
n -> n
n -> a
a -> v
v -> a
a -> <END>
~~~

It may generate:

~~~text
annnnavannava
~~~

Every neighbouring transition may have occurred in training while the complete
result is not a sensible name. The model can make adjacent pairs plausible but
cannot ensure the whole sequence makes sense.

### It has no representation of meaning

The probability table stores local frequencies. It does not know that queen
and king are related, that cat is an animal, or that a sentence communicates an
idea.

### It cannot share learning between contexts

Learning that a -> n is common tells the model nothing about e -> n. Every row
is estimated separately. It cannot recognize that tokens or contexts behave
similarly.

Neural networks will introduce learned representations that allow patterns to
share information.

### Longer count-based context grows rapidly

A trigram model uses two previous characters and can distinguish ma from pa.
But the number of possible contexts grows quickly.

With a vocabulary of 30 characters:

~~~text
one-character contexts:    30
two-character contexts:    30 × 30 = 900
three-character contexts:  30 × 30 × 30 = 27,000
~~~

Most longer contexts may appear rarely or never, producing sparse tables and
many unseen transitions.

These limitations motivate the next question:

> How can a model use more context and share learning across similar patterns
> without storing a separate count for every possible sequence?

That leads toward learned representations, neural networks, and eventually
attention and Transformers.

## 13. What we will implement

The Episode 1 implementation will:

1. Load a small line-based dataset.
2. Split examples into training, validation, and test sets deterministically.
3. Discover the training vocabulary, and report any held-out characters that
   fall outside it.
4. Map characters to integer IDs and back.
5. Add start and end boundaries.
6. Count training bigrams in a matrix with the row/column shape from Section 5.
7. Apply configurable add-k smoothing over the allowed cells only.
8. Normalize every row into probabilities, and assert that each row sums to 1.
9. Generate with greedy decoding and sampling, both with a maximum length.
10. Calculate average NLL without updating the model.
11. Compute the uniform and unigram baselines on the same data.
12. Compare training and validation NLL, and sweep k to see both curves move.
13. Inspect per-word scores and generated failures.

We will first make the logic obvious, then make the implementation compact.

The uniform baseline doubles as a correctness test: a model built with an
enormous k should land almost exactly on ln(V + 1), and if it does not, the
smoothing denominator is wrong.

## Glossary

- **Add-k smoothing:** Adding a positive pseudo-count k to allowed outcomes
  before normalization.
- **Bigram:** A pair of consecutive tokens.
- **Bits and nats:** The units of a log-based score, using base 2 and base e
  respectively.
- **Chain rule of probability:** The probability of a sequence equals the product
  of each token's probability given everything before it.
- **Conditional probability:** The probability of an event given known context.
- **Context:** Earlier information available when predicting the next token.
- **Cross-entropy:** Average negative log-likelihood of data under a model; the
  same number our evaluation computes.
- **Data leakage:** Allowing evaluation information to influence training.
- **Evaluation:** Measuring a fixed model without updating it.
- **Generation:** Producing a new sequence by repeatedly choosing next tokens.
- **Greedy decoding:** Always selecting the highest-probability next token.
- **Likelihood:** The probability a model assigns to observed data.
- **Logarithm:** The inverse of exponentiation; used to convert products into
  sums.
- **Markov assumption:** Assuming the next token depends only on a limited
  amount of preceding context.
- **Maximum-likelihood estimate:** Parameter values that make observed data as
  likely as possible under a model's assumptions.
- **Negative log-likelihood:** A loss that penalizes low probability on correct
  outcomes; lower is better.
- **Normalization:** Rescaling counts into probabilities that sum to 1.
- **Out of vocabulary:** A token in held-out data that the model has no ID for.
- **Perplexity:** exp(average NLL); an alternative scale for the same score.
- **Probability distribution:** Non-negative values over possible outcomes that
  add up to 1.
- **Pseudo-count:** A value added before normalization to express uncertainty.
- **Sampling:** Randomly selecting an outcome according to its probability.
- **Target:** The actual next token supplied by training or evaluation data.
- **Token:** One unit processed by the model.
- **Training:** Using training data to determine model statistics or parameters.
- **Transition:** An ordered pair consisting of a current token and the token
  immediately following it.
- **Unigram model:** A model that predicts the next token from overall frequency
  alone, ignoring context; our main baseline.
- **Vocabulary:** The set of token types recognized by the model.

## Understanding checkpoints

We should be able to answer these without relying on memorized wording:

1. What does a language model output for a given context?
2. What are the vocabulary and context of our first model?
3. How does anna become input-target transitions?
4. Why do we add start and end tokens?
5. How do counts [1, 1, 2] become probabilities?
6. What files or values constitute the finished count-based model?
7. How do training, evaluation, and generation differ?
8. Where does the correct token come from during evaluation?
9. Why do probabilities along one complete sequence multiply?
10. What does a logarithm do, and why is it useful for many probabilities?
11. Why do we negate and average log-likelihood?
12. Does evaluation update this count-based model?
13. Why must validation examples be excluded from transition counts?
14. How do greedy decoding and sampling differ?
15. What problem does smoothing solve?
16. Why can smoothing help an unseen transition but not an unseen token?
17. Why can locally plausible bigrams form a globally implausible sequence?
18. What problem appears when a count-based model uses progressively longer
    context?
19. Why is `<START>` a row but not a column, and `<END>` a column but not a row?
20. Why must the smoothing denominator grow by k × A rather than staying the
    same?
21. Why does smoothing make training NLL worse, and why is that acceptable?
22. Is an average NLL of 2.4 good? What two baselines answer that question?
23. Why must the model be scored on predicting `<END>` at all?
24. In what sense did counting already solve the same problem a neural network
    will solve with gradient descent?

## Primary references

- Dan Jurafsky and James H. Martin, *Speech and Language Processing*, Chapter 3,
  “N-gram Language Models”:
  https://web.stanford.edu/~jurafsky/slp3/ed3book.pdf
- Yoshua Bengio, Réjean Ducharme, Pascal Vincent, and Christian Jauvin, “A
  Neural Probabilistic Language Model”:
  https://www.jmlr.org/papers/v3/bengio03a.html
- Andrej Karpathy, *makemore*:
  https://github.com/karpathy/makemore
- Andrej Karpathy, *Neural Networks: Zero to Hero*:
  https://github.com/karpathy/nn-zero-to-hero

These are supporting sources rather than scripts to copy. Our explanations,
examples, exercises, and implementation will be developed for this series.
