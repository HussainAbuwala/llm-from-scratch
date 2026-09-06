# Episode 01 YouTube package

## Recommended package

**Title**

I Built the Smallest Language Model (From Scratch) | LLM #1

**Thumbnail**

`thumbnails/episode-01-just-2-names.jpg`

The title promises the build and the thumbnail supplies the surprising detail:
the entire worked training corpus contains two names. Both are accurate, the
wording remains readable at feed size, and the native Excalidraw treatment
matches what viewers see in the video.

## Paste-ready description

What is the smallest thing that honestly counts as a language model?

In Episode 1 of Building an LLM From Scratch, we construct a character bigram
model entirely by hand. Starting with just `anna` and `ava`, we turn adjacent
character pairs into a probability table, generate a new name, evaluate held-out
text with negative log-likelihood, compare baselines, and fix unseen transitions
with smoothing.

Reference material:

Technical handout (PDF):
https://github.com/HussainAbuwala/llm-from-scratch/blob/main/docs/episode-01-theory.pdf

Editable Excalidraw canvas:
https://github.com/HussainAbuwala/llm-from-scratch/blob/main/canvas/episode_01_presenter.excalidraw

Canvas reading copy (PDF):
https://github.com/HussainAbuwala/llm-from-scratch/blob/main/docs/episode-01-canvas.pdf

Series repository:
https://github.com/HussainAbuwala/llm-from-scratch

Chapters:

00:00 The smallest language model
02:00 What the model predicts
03:15 Tokens, START and END
04:45 Training by counting pairs
10:45 Turning counts into probabilities
13:30 The finished probability table
14:45 Generating a name
19:45 Greedy vs sampling
23:30 Evaluation vs generation
26:30 Why sequence probabilities multiply
29:00 Why tiny numbers are a problem
30:15 What logarithms mean
32:15 Negative log-likelihood
34:15 Why average the NLL?
37:45 Uniform and unigram baselines
40:30 Smoothing unseen transitions
44:00 How to choose k
47:15 The bigram model's limitations
49:30 What we will code next

The next video implements this same pipeline in code and runs it on a larger
names dataset.

#LLM #MachineLearning #LanguageModels

## Alternate title and thumbnail tests

1. `thumbnails/episode-01-this-table-writes.jpg`
   
   **How Next-Token Prediction Actually Works | LLM From Scratch #1**

2. `thumbnails/episode-01-no-neural-network.jpg`
   
   **Before Transformers: The Simplest Language Model**

Use the recommended package first. If YouTube's Test & Compare is available,
test all three thumbnails against the recommended title before changing both
the title and thumbnail together. That makes the result easier to interpret.

## Tags

`language model, LLM from scratch, bigram model, n-gram model, next token prediction, negative log likelihood, NLL explained, add-k smoothing, greedy vs sampling, probability explained, machine learning from scratch, AI tutorial`

Tags are included mainly for spelling variants and topic clarity. The title,
thumbnail, and opening description carry the main discovery work.

## Upload settings

- Category: Education
- Language: English
- Audience: Not made for kids
- Playlist: Building an LLM From Scratch
- License: Standard YouTube License
- Comments: On
- Automatic chapters: Off, because the description supplies reviewed chapters
- Captions: Review YouTube's automatic captions after processing
- End screen: Link to the coding episode once it is published

## Pinned comment

The next episode turns every count, probability, and NLL calculation from this
video into code. Which part should I slow down on there: sampling, smoothing, or
evaluation?

Handout: https://github.com/HussainAbuwala/llm-from-scratch/blob/main/docs/episode-01-theory.pdf

Canvas: https://github.com/HussainAbuwala/llm-from-scratch/blob/main/canvas/episode_01_presenter.excalidraw
