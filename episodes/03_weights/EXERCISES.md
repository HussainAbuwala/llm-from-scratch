# Episode 03 · Understanding checks

Use input order `[START,a,n,v]` and output order `[a,n,v,END]` throughout.
Try these before opening [the answers](ANSWERS.md). Calculators are welcome;
explain what each number means.

1. For current input `v`, which score row do we look up? Is one-hot encoding required?
2. For input `a`, W has row `[−2,0,1,3]`. What are the logits? Must they add to one?
3. Apply softmax to `[0,ln 3,0,0]`. What is the probability of END?
4. Why can we not just divide four zero scores by their sum? How does softmax repair this?
5. Which transformation preserves softmax: adding 7 to every score, or
   multiplying every score by 7? Explain using the exponential ratios.
6. For the probabilities in question 3, score the observed target `n` using
   NLL. Which probability do you select, and why?
7. How many predictions do `anna` and `ava` contribute? If their average losses
   are 1.2 and 1.5 respectively, what is the combined per-prediction loss?
8. In our chosen `[0,0,0,ln 2]` a row, why does increasing the END logit also
   change the probability of n? Why can the full training loss increase?
9. Optional extension (outside the recording route): construct logits that reproduce the add-one a count row. Did you run an
   optimizer to obtain them? Why add one before taking logarithms?
10. Updating only W[a,END] changes which input rows' predicted distributions?
    What does that imply about learned similarity in this model?
11. Given logits `[1000,1000,1000,1000+ln 2]`, show the maximum-subtracted
    logits and their exponentials. Why does this prevent exponential overflow?
12. Explain how the source of the next input differs during evaluation and
    generation. What is the difference between END and reaching a length cap?

Challenge: under the add-one constructed model, score the complete held-out
name `ana`, including END. Identify all four selected rows and target columns.
Compare to the original unsmoothed bigram path only after labeling smoothing.

Teach-back: explain the whole `a→END` calculation in two minutes without using
the words “understands,” “magic,” or “the optimizer figures it out.”
