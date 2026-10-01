# Episode 03B · Coding checks

Use a copy of the notebook. Answers are in CODING_ANSWERS.md.

1. Print the two arrays for `ava`. Explain why a has different input/output IDs.
2. Compute the initial total loss and denominator without running code.
3. Add 50 to every entry in the chosen-log2 table. Compare probabilities and loss.
4. Multiply that table by 2. Does the same invariance hold?
5. Print all nine individual losses for log2 and log100. Which predictions worsen?
6. Average per-name losses equally, then compare with the full prediction mean.
7. Make START almost certainly produce END. What should the sampler return?
8. Explain why a sample marked CAP is not evidence the model predicted END.
9. Optional: construct log(C + 0.5) and check equivalence to add-0.5 probabilities.
   Label it a construction check; do not choose settings based on held-out results.
10. Which code would have to change to make this a model that learns by gradients?
