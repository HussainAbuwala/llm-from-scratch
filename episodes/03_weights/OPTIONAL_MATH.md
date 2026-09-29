# Optional mathematics for Episode 03

These derivations are not prerequisites for this episode. The main lesson uses
direct row lookup. Matrix multiplication returns in Episode 07 when it combines
learned features.

## Optional reference · One-hot encoding and matrix multiplication

A vector is an ordered list of numbers. The position matters. Under our input
order, the one-hot encoding of `a` is

\[
x_a=[0,1,0,0].
\]

Only the coordinate for `a` is 1. The others are 0. This encoding identifies
the input; it does not say that `a` is more similar to `n` than to `v`.
An integer ID could also select a row in code. One-hot notation lets us see why
that lookup is a matrix multiplication.

Let \(W\) be a 4×4 table of adjustable numbers. Row means current input;
column means possible next token. A weight is a parameter stored in this table.
The output scores for an input are called **logits**.

### Work through the matrix multiplication

**Yes, `xW` is matrix multiplication.** Here a 1×4 row vector multiplies
a 4×4 matrix and produces another 1×4 row vector. Each output number comes
from multiplying the input row by one column of W, then adding the products.

Use the **same weight matrix we already introduced**: all entries are zero
except the a-to-END score, ln 2. No new example is needed.

```text
                         W
                    a  n  v  END
                  ┌──────────────┐
                  │ 0  0  0   0  │ START
  [0, 1, 0, 0]  × │ 0  0  0 ln 2 │ a
                  │ 0  0  0   0  │ n
                  │ 0  0  0   0  │ v
                  └──────────────┘
```

Match the input's four entries with one column at a time. Multiply matching
entries, then add the products:

```text
Output a:   0×0 + 1×0    + 0×0 + 0×0 = 0
Output n:   0×0 + 1×0    + 0×0 + 0×0 = 0
Output v:   0×0 + 1×0    + 0×0 + 0×0 = 0
Output END: 0×0 + 1×ln 2 + 0×0 + 0×0 = ln 2

Result: [0, 0, 0, ln 2]
```

The END column makes the selection visible: the input's 1 multiplies the
entry in the a row, ln 2. Every other input coordinate is 0. The result is a
**new vector with exactly the same entries as the a row**, not the character
`a` itself. These are four scores; probabilities come later.

The expression below groups the same calculation by whole rows:

```text
xW = 0×W_START + 1×W_a + 0×W_n + 0×W_v
```

Each `W_a` or `W_n` means an **entire row of four numbers**. Multiplying a
row by a scalar multiplies every entry. Adding rows adds corresponding entries:

```text
0 × [0, 0, 0, 0]    = [0, 0, 0, 0]
1 × [0, 0, 0, ln 2] = [0, 0, 0, ln 2]
0 × [0, 0, 0, 0]    = [0, 0, 0, 0]
0 × [0, 0, 0, 0]    = [0, 0, 0, 0]
                       ────────────────
Add by position:       [0, 0, 0, ln 2]
```

“Row times each column” and “weighted sum of whole rows” describe the same
matrix multiplication. One-hot input keeps exactly one row: multiplying the
other rows by zero would remove their contributions even if they contained
nonzero weights. An arbitrary input vector could combine multiple rows.

The multiplication selects the `a` row. More generally,
\(z_j=\sum_i x_iW_{ij}\). A 1×4 input times a 4×4 matrix gives a 1×4 score
vector. A batch of B inputs gives `(B,4) @ (4,4) -> (B,4)`; each example still
has its own output distribution. NumPy's `@` means matrix multiplication;
`*` means elementwise multiplication. [NumPy matrix multiplication documentation](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html).

We omit a separate bias because each input already has an unrestricted row.
A common output bias could be absorbed into every row without increasing the
set of distributions this model can represent. Our orientation is a project
convention; sources using column vectors transpose the corresponding shapes.


## Optional reference · Target one-hot and cross-entropy

The one-hot **target** under the output order is \(y=[0,0,0,1]\).
Cross-entropy \(-\sum_j y_j\log p_j\) keeps only the target term, so this is
exactly the per-prediction NLL from Episode 01. Input one-hot chooses the row;
target one-hot chooses the probability we score. They serve different purposes.
[Dive into Deep Learning, §4.1.2](https://d2l.ai/chapter_linear-classification/softmax-regression.html).


## Optional reference · Constructing weights from count probabilities

For any strictly positive normalized row q, choose \(z_j=\ln q_j\). Then
softmax returns q because its denominator is \(\sum_jq_j=1\). Equivalently,
for positive add-k smoothing, choose logits \(\ln(c_j+k)\): exponentiating
returns the pseudo-counts, and softmax divides by their total.

This is an exact **construction from counts**, not evidence of an optimizer
learning the weights. For k=1 our four rows give the familiar bigram distribution:
`START: [3,1,1,1]/6`, `a: [1,2,2,3]/8`, `n: [2,2,1,1]/6`,
`v: [2,1,1,1]/5`. On `ana`, the path probability is
\((1/2)(1/4)(1/3)(3/8)=1/64\), with average NLL
\(\ln64/4\approx1.039721\). The old **unsmoothed** count model gave 1/16
and 0.693147. The difference is smoothing, not a failure of the representation.

### Optional presenter detail: exact zeros and the best possible fit

Unsmoothed count rows contain exact zeros. Finite softmax logits cannot produce
those zeros mathematically; they can approach them as score differences grow.
For each observed row, let empirical frequencies be q. Its average training
loss decomposes as \(H(q)+D_{KL}(q\Vert p)\), minimized over probability
distributions at p=q. For rows containing zeros, this is an infimum for finite
softmax parameters, approached in a limit. An unobserved row has no data term
to determine it. This optional presenter explanation does not require an
on-camera derivative. [Dive into Deep Learning, cross-entropy and its minimum](https://d2l.ai/chapter_linear-classification/softmax-regression.html).

There are 16 stored numbers but 12 independent probability degrees of freedom:
each of four normalized rows has three, and a constant logit shift per row has
no effect. Neither this parameter count nor changing from counts to scores
creates extra context or learned sharing across distinct rows.
