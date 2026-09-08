# EP 01B · YouTube release package

## Title

EP 01B — Build a Bigram Language Model in Python

## Thumbnail choices

Recommended first: `thumbnails/episode-01b-lets-code-bigram.jpg`

Updated choices explicitly communicate coding a bigram language model:

- **LET’S CODE A BIGRAM LANGUAGE MODEL** — recommended; Python code and generated names reinforce the hands-on build.
- **BIGRAM LANGUAGE MODEL IN PYTHON** — `thumbnails/episode-01b-bigram-in-python.jpg`; larger model-name headline with a LET’S CODE badge.

Prompts: `EPISODE_01B_THUMBNAIL_CODING_PROMPTS.md`.

Earlier concepts below are retained as drafts; the updated choices above are clearer about the topic and coding format.

1. **COUNTS → NEW NAMES** — the strongest match for this episode's mechanism;
   complements the title instead of repeating it.
2. **29,494 NAMES IN** — emphasizes the jump from the two-name theory example
   to the larger coding dataset.
3. **ONE LETTER AT A TIME** — emphasizes the bigram model's defining mechanism
   and limitation.

The earlier `LET'S CODE A LANGUAGE MODEL` concept remains in the repository as
an unused draft. It is not recommended because the phrase could apply to every
future coding video in the series.

## Description

Build a character-level language model in pure Python, then use it to generate names and measure its predictions on unseen data.

This is the coding companion to EP 01A. We take the bigram model from the theory video and implement it in a Jupyter notebook, using 29,494 unique name spellings. We build the count table, turn counts into probabilities, compare greedy decoding with weighted sampling, calculate negative log-likelihood, and choose add-k smoothing using validation data.

Run the notebook:
https://github.com/HussainAbuwala/llm-from-scratch/blob/main/episodes/01_names/episode_01.ipynb

Download or clone the whole repository so the notebook can find its dataset and chart helpers:
https://github.com/HussainAbuwala/llm-from-scratch

Code companion: setup, key functions, expected results, and common questions:
https://github.com/HussainAbuwala/llm-from-scratch/blob/main/episodes/01_names/CODE_GUIDE.md

Watch the theory episode first:
https://www.youtube.com/watch?v=YV30EDncrY4

Theory handout (PDF):
https://github.com/HussainAbuwala/llm-from-scratch/blob/main/docs/episode-01-theory.pdf

Chapters:
00:00 Names, data splits, and character tokens
10:21 Counting, probabilities, and generation
16:45 Inspecting samples, evaluation, and smoothing
25:44 Choosing k, model limits, and final test

What you'll build:
• A character bigram model trained by counting
• Greedy and weighted-sampling name generation
• Training, validation, and test evaluation
• Uniform and unigram baselines
• An experiment to select smoothing strength

The model uses Python lists, dictionaries, math, and random. Jupyter presents the code and Matplotlib draws the charts. Basic Python knowledge is helpful.

Final test NLL (lower is better): uniform 3.295837; unigram 2.818510; smoothed bigram 2.460499. All three use the same 21,053 test predictions, including END. Smoothing k = 0.3 was selected on validation data.

Dataset credit: names.txt from Andrej Karpathy's makemore repository, with its MIT license preserved in our repo. The upstream README attributes the data to US Social Security name data.
https://github.com/karpathy/makemore

Next in the series: give the model more context and explore the limits of counting.

#Python #MachineLearning #LLMFromScratch

## Tags

LLM from scratch, language model in Python, bigram model, character language model, Python tutorial, Jupyter notebook, name generator, machine learning from scratch, next token prediction, negative log likelihood, NLL, add k smoothing, weighted sampling, random choices, n gram model

## Upload settings

- Visibility: Private. Do not publish or schedule.
- Channel: The Unplanned Stack
- Playlist: Building an LLM From Scratch, if available in the channel picker
- Category: Education
- Video language: English
- Audience: Not made for kids (general software education)
- License: Standard YouTube License
- Paid promotion: No
- Altered/synthetic realistic content: No; ordinary recorded instruction, with an illustrated thumbnail
- Automatic chapters: Off; four supplied chapters follow the verified source-part boundaries
- Captions: Review YouTube-generated captions after processing; no transcript was supplied
- Thumbnail: choose one of the two updated 1280 × 720 alternatives above

## Suggested pinned comment (prepared, not posted)

Run the notebook and try a different sampling seed or smoothing strength. Which outputs surprised you most?

Notebook: https://github.com/HussainAbuwala/llm-from-scratch/blob/main/episodes/01_names/episode_01.ipynb
Code guide: https://github.com/HussainAbuwala/llm-from-scratch/blob/main/episodes/01_names/CODE_GUIDE.md

## Editorial notes

The four input recordings are joined in numeric order without content cuts or
added transitions. Chapters follow their boundaries rather than guessed
fine-grained speech timings. Speech loudness is adjusted for the upload.
The final 1080p H.264 export uses CRF 18 and a regular 30 fps timeline to
correct timestamp irregularities detected at a recording boundary.

The notebook is the primary companion artifact. A short Markdown guide handles
setup and common questions; the existing theory PDF remains the mathematical
reference, so a second overlapping theory PDF is unnecessary.
