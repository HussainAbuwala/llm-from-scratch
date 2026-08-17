# Series Plan: Building an LLM From Scratch

Status: Working plan · decided 2026-08-17

This is the single source of truth for scope. The roadmap canvas
(`canvas/series_intro.excalidraw`, scene 05) is generated to match it — if the
plan changes, change it here and regenerate.

## Endpoint

The series ends with a **small decoder-only Transformer, written by us, trained
on a laptop, generating text**. Approximately 14 episodes.

Post-training (instruction tuning, LoRA, RLHF/DPO) and inference engineering
(KV cache, quantisation, serving) are explicitly **out of scope**. They are
named on camera as "not in this series" so the promise stays keepable. If the
series works, they become a second series rather than an ever-growing first one.

## Code stack progression

| Episodes | Stack | Reason |
|---|---|---|
| 1–2 | Pure Python: dicts, lists, loops | Nothing between the viewer and the arithmetic |
| 3–4 | NumPy | Matrices become necessary, not decorative |
| 5 | Pure Python again | An autograd engine has to be hand-built to be believed |
| 6–14 | PyTorch | Introduced once the viewer already knows what it is doing for them |

PyTorch arrives as *relief* in episode 6, after the viewer has hand-written the
thing PyTorch replaces. That ordering is the pedagogical point, not an
implementation detail.

## Episode list

Each episode ships as **two videos**: a theory video (canvas, worked by hand)
and a build video (editor, tests, real output).

### Part 1 · Count — pure Python

| # | Episode | Core content | New maths |
|---|---|---|---|
| 01 | The smallest language model | Char bigram by counting; boundaries; NLL; baselines; sampling; add-k smoothing | Probability, conditional probability, logs |
| 02 | Trigrams and the sparsity wall | Longer count-based context; combinatorial blow-up; why counting ends here | Counting/combinatorics |

### Part 2 · Learn — NumPy, then PyTorch

| # | Episode | Core content | New maths |
|---|---|---|---|
| 03 | From counts to weights | One-hot inputs, a weight matrix, logits, softmax; same bigram task, learned | Vectors, matrix multiply, softmax, cross-entropy |
| 04 | Gradients, by hand | Derivatives from first principles; chain rule; gradient descent on a two-parameter toy | Derivatives, chain rule |
| 05 | Autograd from scratch | A scalar `Value` class; forward graph; backward pass; verify against numeric gradients | Computational graphs |
| 06 | Enter PyTorch | Tensors, `.backward()`, optimisers; rebuild episode 3 in ~20 lines; confirm it matches episode 1's loss | — |
| 07 | Embeddings and the MLP model | Bengio 2003; a context window of several characters; hidden layer; learned representations | Embedding as lookup, non-linearity |
| 08 | Making training actually work | Initialisation, normalisation, learning-rate finding, train/val curves, overfitting | Variance intuition |

### Part 3 · Attend — PyTorch

| # | Episode | Core content | New maths |
|---|---|---|---|
| 09 | Why fixed context breaks | Fixed windows waste capacity; the need to look back selectively | — |
| 10 | Self-attention from scratch | Queries, keys, values; scaled dot product; causal masking; one head by hand | Dot product as similarity |
| 11 | Multi-head attention and the block | Several heads; residual connections; layer norm; feed-forward | — |
| 12 | Build the GPT | Full decoder-only stack; positional embeddings; parameter count | — |
| 13 | Tokenization for real | Bytes, BPE, merges; why "strawberry" is hard; retrain with a real tokenizer | — |
| 14 | Train it. Make it talk. | Training at laptop scale; checkpoints; temperature, top-k, top-p; final evaluation against episode 1's baselines | — |

## Continuity devices

Three things recur deliberately across episodes so the series feels like one
build rather than fourteen tutorials:

1. **The same metric.** Average NLL, in nats, from episode 1 to episode 14. Every
   model is compared against the uniform and unigram baselines established in
   episode 1. The number goes down over the series, on camera.
2. **The same canvas language.** Character cards, probability bars, count
   matrices, and the surprise chart are reused and evolved, not redrawn.
3. **The same honesty rule.** The hand-worked number in the theory video and the
   printed number in the build video must match on screen.

## Definition of done for an episode

- Theory document exists and follows `RESEARCH_STANDARD.md`.
- Canvas generated and proofread.
- Code runs from a clean checkout, with tests that would fail if the concept
  were implemented wrongly.
- At least one honest failure is shown.
- The episode's loss is reported next to the previous episode's loss.
