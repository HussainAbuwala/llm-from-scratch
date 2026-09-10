# Episode 02 · Understanding checks

Use [the theory reference](../../EPISODE_02_THEORY.md) as a reference only after your
first attempt. Write predictions before running code. Keep
[the answer key](ANSWERS.md) closed until you have tried each question.

## A. Work it out on paper

1. A trigram model is given the prefix `ann`. What is its context? What would a
   bigram use? How many tokens will either predict next?
2. List every trigram context/target pair from `ava`, including boundaries.
   Explain why there are four predictions rather than five or six.
3. Train on `anna` and `ava`. Compute P(n given S,a), P(n given a,n), and
   P(a given n,n). Explain each denominator.
4. Compute the unsmoothed trigram probabilities of `anna`, `ava`, and `ana`.
   Explain why plausible samples can conceal a generalization failure.
5. Contrast P(a given a,n) with P(a given v,n) without smoothing. Which is
   zero, and which has an unspecified row? Why can't an all-zero row be sampled?
6. Apply k=1 to every toy row. Compute P(ana) and its average NLL, including END.
   Check against the answer key; running the lab is optional.
7. Suppose k=0.01 instead. What probability does the unseen context (v,n)
   assign to each of the four outcomes? Does a smaller k express more confidence
   in one of those outcomes?
8. Derive the number of valid trigram context rows for 26 characters, given
   separate START and END. Explain why it is neither 26² nor 27².
9. Two names have 4 and 8 predictions with total negative-log penalties of
   6 and 20. What is the corpus NLL? Why is averaging the two per-name NLLs wrong
   for our metric?

## B. Coding-video exercises — optional during theory preparation

10. Write `my_windows(name, context_size)` without looking at `windows`.
    It must work for a one-character name and a context longer than the name.
    Check `ava` against your paper result; verify that no target is START.
11. Run the real-data experiment. Which context length wins on validation?
    Which model has the most training contexts observed only once? Explain why
    it can fit training better while predicting held-out names worse.
12. In a scratch copy, keep all counts fixed and change k to 1,000,000,000.
    Predict the validation NLL before evaluating. Does the limit depend on
    context length?
13. Train on only `anna` and `ava`, and try to score `zoe`. Explain why add-k
    does not solve this problem. What explicit policy would a broader system need?
14. Inspect the first 12 samples per model in the saved report. Identify any
    training matches or capped samples. Explain why neither “looks like a name”
    nor “not in training” proves that the model learned a good distribution.

## C. Optional extension and teach-back

15. Mix the k=1 trigram and bigram toy distributions with equal weights.
    Compute P_mix(a given a,n), and prove that the full mixture sums to one.
    If you implement it, use validation to choose its weight; don't tune on test.
16. Give a two-minute explanation containing: one benefit of extra context,
    one failure from the toy, one example of splitting evidence, one mitigation, and
    the actual scope of Episode 03.

For theory recording, focus on the hand-worked checks in 2–9 and complete 16
without claiming
that all n-grams stop working after trigrams or that a weight matrix alone
solves sparse longer contexts. If one item is difficult, revisit that section
rather than memorizing its answer.
