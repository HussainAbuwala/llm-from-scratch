# Episode 02 · Answer key

Attempt [the exercises](EXERCISES.md) first. These explanations are checkpoints,
not a narration script to memorize.

1. Trigram: `(n,n)`; bigram: `n`. Both predict one next token. Trigram means
   two context tokens plus the target.
2. `(S,S)->a`, `(S,a)->v`, `(a,v)->a`, `(v,a)->E`. The two START tokens
   supply context. Only the three characters and END are targets.
3. 1/2, 1, and 1. `(S,a)` has two observations, one n and one v. `(a,n)`
   has one observation, n; `(n,n)` has one observation, a.
4. 1/2, 1/2, and 0. The first two routes have one fair branch and otherwise
   deterministic transitions. `ana` requires the unseen target a in row `(a,n)`.
   The toy generates training names perfectly but rules out this held-out name.
5. P(a given a,n)=0/1=0. P(a given v,n)=0/0 is unspecified by training.
   An all-zero row sums to zero, so it isn't a probability distribution. The
   lab returns `None` for an unspecified row at k=0 and records it separately.
6. `(3/6) × (2/6) × (1/5) × (2/5) = 1/75`.
   Average NLL is `ln(75)/4 = 1.079372`. Every row must be smoothed, not just
   the row that previously gave zero probability.
7. 1/4 for every outcome: k/(4k)=1/4. Changing positive k cannot distinguish
   outcomes that all have zero evidence in that row.
8. `1 + 26 + 26² = 703`. One all-START context, 26 `(S,character)` contexts,
   and 676 ordinary-character pairs. `26²` misses initial contexts; `27²`
   includes invalid `(character,S)` contexts. Multiply 703 by 27 outcomes to
   obtain 18,981 possible cells. This counts potential rows, not observed rows.
9. `(6+20)/(4+8) = 26/12 = 2.166667`. Averaging per-name NLLs gives
   `(6/4+20/8)/2 = 2`, which weights the two names equally instead of giving
   each prediction equal weight.
10. One approach maintains a rolling tuple rather than slicing padded tokens:

    ```python
    def my_windows(name, context_size):
        if context_size < 1:
            raise ValueError("Use at least one context token")
        context = ("<START>",) * context_size
        for target in [*name, "<END>"]:
            yield context, target
            context = (*context[1:], target)
    ```

    Its final unused context may include END; it emits no further prediction.
    A one-character name still emits two predictions for any positive size.
11. Context length 3 wins among tested candidates, with validation NLL
    2.126903. Length 5 has 21,379 singleton rows. More specific rows separate
    training observations; the held-out distribution may require continuations
    poorly represented in those smaller groups. The table's 2,746 unseen-context
    predictions at length 5 supply additional evidence of sparsity.
12. All rows approach uniform over 27 outcomes, so NLL approaches
    `ln(27) = 3.295837`, regardless of context length. At a finite huge k the
    result is very close, not algebraically equal for every observed row.
13. `z`, `o`, and `e` aren't in the toy vocabulary. Add-k only redistributes
    mass among existing outcomes. A larger system needs an explicit unknown-token
    policy or a vocabulary scheme such as bytes; silently skipping targets
    corrupts the score.
14. Use the actual saved `first_12_samples` entries; `in_training` and `ended`
    answer the factual parts. Novel strings may be implausible, and training
    matches may reflect memorization. Twelve samples are a small illustration,
    not a generalization estimate. Capped strings are unfinished outputs.
15. `P_tri(a|a,n)=1/5`, `P_bi(a|n)=2/6=1/3`; their equal-weight mixture
    assigns `1/10 + 1/6 = 4/15`. Summing across targets gives
    `(1/2 × 1) + (1/2 × 1) = 1`. Both component rows must be normalized and
    defined. Interpolation with unspecified raw MLE rows needs another policy.
16. A valid teach-back: the extra token distinguishes `an` from `nn`. That
    improves training fit but gives `ana` zero probability in our tiny model.
    In the separate four-string example, a shared nn row with four observations
    splits into ann, enn, inn, and onn rows with one observation each. Smoothing and shorter-history
    methods can help. Episode 03 learns the familiar bigram task with weights
    and softmax; embeddings and the MLP come in Episode 07.
