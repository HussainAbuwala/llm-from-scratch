# Episode 03A — YouTube upload package

## Recommended title

EP 03A — From Counts to Weights: Softmax and Loss Explained

Alternative titles:

- EP 03A — How Weights Become Predictions: Softmax Step by Step
- EP 03A — A Better Prediction Can Make Your Model Worse

## Description (paste-ready)

How do adjustable weights become next-character probabilities—and how do we measure whether a change actually helps?

In this theory episode of Building an LLM From Scratch, we return to anna and ava. We replace the count table with adjustable scores, start every weight at zero, apply softmax to each row, and calculate the loss for all nine training predictions—including END.

Then we try two changes by hand: ln 2 improves the overall training loss, while ln 100 pushes too far. A higher probability for one target does not necessarily mean a better model overall.

Along the way:
• Count-based fitting versus weight-based training
• Why softmax turns scores into a probability distribution
• Negative log-likelihood and average loss per prediction
• Why score differences matter and how to calculate softmax stably
• How generation feeds sampled characters back into the model

This episode explains the forward calculation and measures chosen weight changes. We are not using gradients to select those changes yet. Our bigram still has independent rows; embeddings and shared representations arrive later.

Final edited recording canvas (download and open in Excalidraw):
https://github.com/HussainAbuwala/llm-from-scratch/blob/main/canvas/episode_03_final.excalidraw

Theory reference and worked calculations:
https://github.com/HussainAbuwala/llm-from-scratch/blob/main/EPISODE_03_THEORY.md

Exercises and learning companion:
https://github.com/HussainAbuwala/llm-from-scratch/tree/main/episodes/03_weights

Full series repository:
https://github.com/HussainAbuwala/llm-from-scratch

Chapters:
00:00 From counts to adjustable weights
08:50 Score rows, softmax and individual prediction loss
17:26 Average loss and trying weight changes
23:04 Score differences, stability and generation

Next: the Episode 03 coding companion. Episode 04 introduces gradients—how to choose weight adjustments automatically.

#LLMFromScratch #MachineLearning #Softmax

## Tags

LLM from scratch, softmax explained, weights and logits, bigram language model, negative log likelihood, cross entropy loss, training loss, next token prediction, language model from scratch, softmax numerical stability, machine learning fundamentals, neural network fundamentals

## Thumbnail alternatives

A (recommended): `thumbnails/episode-03a-turn-the-weights.jpg` — TURN THE WEIGHTS. Shows the episode's central action and measured loss improvement.

B: `thumbnails/episode-03a-scores-to-chances.jpg` — SCORES TO CHANCES. Leads with softmax and the concrete 20/20/20/40 distribution.

C: `thumbnails/episode-03a-too-confident.jpg` — TOO CONFIDENT? Leads with the overshoot: ln 100 worsens average loss.

All are 1280 × 720 JPGs in the cream/plum Learn palette. `thumbnails/episode-03a-options.jpg` is a review sheet, not an upload thumbnail. Rebuild with `.venv/bin/python youtube/build_episode_03a_thumbnails.py`.

## Upload settings and editorial notes

- Channel: The Unplanned Stack
- Playlist: Building an LLM From Scratch
- Category: Education; language: English
- Audience: general software education, not made for kids
- Review privately before publishing; no upload or publication was performed here.
- Review automatic captions for softmax, logit, NLL, natural logarithm, anna, ava, START and END.
- Chapter times use the next whole second after actual clip boundaries. Topics were verified from recording stills, not a full transcript; these are broad navigation markers.
- Repository links target main. Commit and push availability must be checked before publication; this task only commits locally.
- The final recording canvas has 19 frames. The 20-frame generated rehearsal presentation remains a separate preparation artifact.

## Pinned comment draft

Why does raising the END score to ln 2 help, while raising it to ln 100 makes the overall loss worse? Try explaining it using the other targets after a.

Worked arithmetic and exercises: https://github.com/HussainAbuwala/llm-from-scratch/tree/main/episodes/03_weights
