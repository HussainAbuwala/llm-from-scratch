# Episode 03 · Answer key

1. Look up the v row. Its index is 3 in our input order, but no one-hot vector
   is required. The index is an address, not a score multiplier.
2. The logits are `[−2,0,1,3]`. They are real-valued scores; there is no
   sum-to-one requirement before softmax.
3. Exponentials `[1,3,1,1]`, total 6, probabilities `[1/6,1/2,1/6,1/6]`.
   END gets 1/6, not 1/2: keep the output order visible.
4. Dividing raw zeros by their zero total is undefined. Softmax exponentiates
   first: every exponential is 1, so dividing each by 4 works.
5. A common addition preserves it: the factor exp(7) cancels. Multiplication
   changes score differences and generally changes the distribution (equal
   scores are a special case where it does not).
6. The actual target is n, so select its probability 1/2. Its loss is
   `−ln(1/2)=ln 2≈0.693147` nats. No target one-hot vector is needed.
7. Five and four predictions, nine total. `(5×1.2+4×1.5)/9=4/3≈1.333333`.
   An equal average of the two name averages would use the wrong weighting.
8. All outcomes share a normalization denominator. Raising END increases that
   denominator while n's numerator stays fixed. END is not the only observed
   target, so losses on n and v may outweigh gains on END.
9. Counts `[0,1,1,2]` become `[1,2,2,3]` after adding one. Choose
   `[ln 1,ln 2,ln 2,ln 3]`. Softmax returns `[1,2,2,3]/8`. These are constructed
   weights, not optimizer output. Adding one avoids ln(0). Optional detail: finite logits give positive probabilities;
   the exact unsmoothed zero is a limiting case. Floating-point underflow is
   a numerical effect, not an exception to the mathematical statement.
10. Only the a row's distribution changes, though all four output probabilities
    in that row change. Predictions for START, n and v are unchanged. This
    unrestricted table has no learned representation sharing across input rows.
11. `[-ln 2,-ln 2,-ln 2,0]`, then `[1/2,1/2,1/2,1]`, with total 5/2.
    The resulting probabilities are `[1/5,1/5,1/5,2/5]`. Every shifted score is at most zero, so no exponential exceeds one.
    Optional: computing log probabilities directly also avoids log of an underflowed zero.
12. Evaluation uses the real previous character from each supplied name;
    generation uses the previous sampled character. END is an explicit model
    outcome. A cap stops the procedure without claiming that END was predicted.

Challenge: START→a is 3/6; a→n is 2/8; n→a is 2/6; a→END is 3/8.
The product is 1/64 and average NLL is ln(64)/4≈1.039721 nats per prediction.
The Episode 01 unsmoothed bigram gave 1/16 and ln(16)/4≈0.693147.
The change here is add-one smoothing; constructing logits preserves each
smoothed count distribution exactly.

Teach-back example: “For current a, look up
the a row, `[0,0,0,ln 2]`. Exponentiating gives `[1,1,1,2]`; dividing by five
gives the probabilities. The data says END came next, so we score 2/5.
Negative log of 2/5 is about 0.916291 nats. That computes a prediction and a
loss; choosing a useful update is the next problem.”
