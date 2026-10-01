# Episode 03B — YouTube upload package

## Recommended title

EP 03B — Build Softmax and Loss from Scratch in NumPy

Alternative titles:

- EP 03B — Why Your Loss Becomes Infinity (and How Log-Softmax Fixes It)
- EP 03B — From Weights to Probabilities: A Language Model in NumPy

## Description (paste-ready)

Let's turn the theory from Episode 03A into code—and inspect the arrays along the way.

In this episode of Building an LLM From Scratch, we use NumPy to implement the forward calculation of a tiny character bigram model. Starting with anna and ava, we map tokens to IDs, gather score rows from a weight table, apply softmax, and calculate the loss across all nine next-token predictions, including END.

We also examine a numerical trap: even after preventing overflow, a tiny probability can round to zero and produce infinite loss. We work through log-softmax to calculate the same objective without losing the target's log probability.

Finally, we change one weight by hand. A modest increase in the END score after a improves the loss; pushing it too far makes the overall loss worse.

What we cover:
• Input and target IDs, boundaries, and prediction pairs
• NumPy indexing, array shapes, and row-wise softmax
• Target selection and average negative log-likelihood
• Underflow: why a positive probability can become zero on a computer
• Log-softmax and a finite loss calculation
• Comparing three manually chosen weight settings

This episode builds and evaluates the prediction machinery. We are not using gradients to train the weights yet, and we are not claiming an improvement over the earlier count model. Episode 04 introduces derivatives and gradients so we can start choosing updates systematically.

Notebook (includes a generation example for further exploration):
https://github.com/HussainAbuwala/llm-from-scratch/blob/main/episodes/03_weights/episode_03.ipynb

Setup and code guide:
https://github.com/HussainAbuwala/llm-from-scratch/blob/main/episodes/03_weights/CODE_GUIDE.md

Theory reference:
https://github.com/HussainAbuwala/llm-from-scratch/blob/main/EPISODE_03_THEORY.md

Full series repository:
https://github.com/HussainAbuwala/llm-from-scratch

Chapters:
00:00 From theory to NumPy
03:00 Token addresses and vocabulary
05:00 Build input-target pairs
08:00 Inspect arrays and look up score rows
09:00 Softmax: scores to probabilities
11:00 Select targets and calculate loss
13:43 Underflow and log-softmax
17:43 Work through the log-softmax calculation
22:43 Change a weight and compare losses
24:43 Recap and the next episode

#LLMFromScratch #NumPy #MachineLearning

## Tags

LLM from scratch, NumPy tutorial, softmax from scratch, log softmax explained, numerical underflow, negative log likelihood, cross entropy loss, bigram language model, weights and probabilities, Python machine learning, NumPy indexing, neural network fundamentals, language model tutorial

## Thumbnail alternatives

All three are 1280 × 720 JPG, under 2 MB, using the cream/plum Learn palette.

- A — `thumbnails/episode-03b-build-it-in-numpy.jpg`: BUILD IT IN NUMPY. Recommended for continuity and a clear coding-episode promise.
- B — `thumbnails/episode-03b-why-loss-explodes.jpg`: WHY LOSS EXPLODES. Focuses on the concrete infinity-versus-2000 demonstration.
- C — `thumbnails/episode-03b-one-weight-three-losses.jpg`: ONE WEIGHT. THREE LOSSES. Focuses on the helpful change and overshoot.

`thumbnails/episode-03b-options.jpg` is a comparison sheet, not an upload thumbnail.
Rebuild: `.venv/bin/python youtube/build_episode_03b_thumbnails.py`.

## Upload notes

- Channel: The Unplanned Stack; playlist: Building an LLM From Scratch.
- Category: Education; language: English; audience: general software education, not made for kids.
- No upload or publication performed in this release task.
- Review automatic captions for NumPy, softmax, log-softmax, underflow, NLL, anna, ava, START and END.
- Chapters are approximate visual navigation anchors checked against recording stills, not transcript-derived first mentions. The join is at 12:43.333; the second clip begins with an average-loss recap.
- The recorded closing follows the weight comparison. The preserved notebook also contains generation code; the larger-data count-equivalence extension was removed by the presenter and is not advertised here.
- Repository links target main. This task commits locally; push the commit before relying on new public links.

## Pinned comment draft

Why can increasing the probability of END make the overall loss worse? Look at all four targets that follow a in anna and ava.

Notebook and exercises: https://github.com/HussainAbuwala/llm-from-scratch/tree/main/episodes/03_weights
