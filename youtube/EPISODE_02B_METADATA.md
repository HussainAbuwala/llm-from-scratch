# EP 02B - YouTube release package

## Recommended title

EP 02B — Build a Trigram Language Model in Python

Alternative titles:

- EP 02B — More Context, Better Predictions? Let's Test It in Python
- EP 02B — Trigrams, Smoothing, and Sparsity: A Python Experiment

## Description

Build a trigram language model in Python, then give it even more context and measure what changes.

In this coding episode of Building an LLM From Scratch, we turn the theory into working code: context windows, sparse count dictionaries, on-demand smoothing, negative log-likelihood, and character-by-character name generation. We start with anna and ava, then compare models with one to five context characters on the same names dataset used in Episode 01.

Does extra context improve predictions, or leave each row with too little evidence? We compare training and validation loss, inspect rare and unseen contexts, choose settings using validation, and report the fixed models on test.

Run the complete notebook (code, charts, and saved outputs):
https://github.com/HussainAbuwala/llm-from-scratch/blob/main/episodes/02_trigrams/episode_02.ipynb

Code companion guide - setup and explanations:
https://github.com/HussainAbuwala/llm-from-scratch/blob/main/episodes/02_trigrams/CODE_GUIDE.md

Download or clone the whole repository so the notebook can find its dataset and chart helpers:
https://github.com/HussainAbuwala/llm-from-scratch

Episode 02A theory companion (PDF):
https://github.com/HussainAbuwala/llm-from-scratch/blob/main/docs/episode-02-theory.pdf

Theory canvas - all 29 frames (PDF):
https://github.com/HussainAbuwala/llm-from-scratch/blob/main/docs/episode-02-canvas.pdf

Chapters:
00:00 From the theory to Python: setup and context windows
05:00 Sparse counts and smoothed probabilities
12:47 From toy samples to the larger dataset
14:47 Comparing context lengths and choosing smoothing
18:47 Reading training and validation loss
22:47 Sparse evidence: rare and unseen contexts
26:47 Final test comparison and takeaways

What you'll build:
• A count-based model with arbitrary context length
• Probabilities computed from sparse counts without creating unseen training rows
• Name evaluation and weighted sampling with explicit END handling
• A validation comparison across context lengths and smoothing values
• Charts showing prediction loss and the evidence behind each context

A trigram uses two previous characters to predict one next token. Three context characters make a 4-gram. Our experiment goes beyond trigrams to test the tradeoff discussed in theory.

Among the tested settings, validation selected three context characters with k = 0.1. Its test NLL is 2.129940 nats per prediction, compared with 2.460499 for the bigram baseline. Both use the same 21,053 test predictions, including END. These results describe this dataset, split, and add-k model family; they do not establish a universal best context length.

The test split is the same one previously reported in Episode 01. It is excluded from this episode's training and model selection, but it is not a newly collected independent dataset. Backoff and interpolation are theory topics; this coding comparison evaluates add-k models.

The model uses Python's standard library. Jupyter presents the notebook and Matplotlib draws the charts. Basic Python knowledge and the Episode 01 bigram concepts are helpful.

Dataset credit: names.txt from Andrej Karpathy's makemore repository. The dataset license and pinned source information are preserved in our repository. We use 29,494 unique name spellings, each equally weighted.
https://github.com/karpathy/makemore

Next in the series: learn bigram probabilities using weights and softmax.

#Python #LLMFromScratch #MachineLearning

## Tags

trigram language model, LLM from scratch, Python language model, n gram model, bigram, context length, data sparsity, add k smoothing, Laplace smoothing, negative log likelihood, next token prediction, name generator, machine learning from scratch, Jupyter notebook, validation loss, overfitting

## Selected thumbnail

`thumbnails/episode-02b-lets-code-trigram.jpg` - LET'S CODE A TRIGRAM

Selected by the user. Supporting tagline removed. 1280 x 720 JPG with the series' navy background. Not uploaded automatically.

## Prepared upload settings

- Channel: The Unplanned Stack
- Playlist: Building an LLM From Scratch, if available
- Category: Education
- Language: English
- Audience: General software education; not made for kids
- Visibility: Private for review; this task did not upload, publish, or schedule the video
- License: Standard YouTube License
- Chapters: Use the supplied recording-based markers
- Captions: Review automatic captions for trigram, n-gram, NLL, pseudocount, START, and END
- Thumbnail: use the selected LET'S CODE A TRIGRAM image

## Suggested pinned comment (prepared, not posted)

Try the notebook and compare one, two, and three context characters. Can you explain why a longer context can have fewer matching observations, even though the dataset is unchanged?

Notebook: https://github.com/HussainAbuwala/llm-from-scratch/blob/main/episodes/02_trigrams/episode_02.ipynb
Code guide: https://github.com/HussainAbuwala/llm-from-scratch/blob/main/episodes/02_trigrams/CODE_GUIDE.md

Use training and validation for exploration. Keep the test report for fixed choices rather than tuning against it.

## Editorial notes - not part of the description

Two recordings joined in numeric order without cuts or added transitions. Duration is approximately 30:30. The export uses a regular 30 fps H.264 timeline to repair source frame-timing irregularities; audio is AAC stereo at 48 kHz.

Chapter markers are grounded in sampled recording frames: 05:00 was checked directly; 12:47 is the second-part boundary; later markers correspond to part-2 offsets 02:00, 06:00, 10:00, and 14:00. They are navigation points within the observed topics, not word-level transcript timings or first-appearance claims.

The notebook follows the recorded 11-section structure and closing recap. Report saving runs during the build, outside the presentation. It includes k = 0 in the declared grid; the five raw validation scores are infinite and do not change the positive-k selections. All 50 candidate results remain in the JSON report.
