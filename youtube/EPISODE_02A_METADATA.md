# EP 02A - YouTube release package

## Recommended title

EP 02A — Trigram Language Models and the Sparsity Problem

Alternative: EP 02A — Does More Context Make a Better Language Model?

## Description

What changes when a language model remembers two characters instead of one? We build a trigram model by hand, then explore why more context needs more evidence.

In this theory episode of Building an LLM From Scratch, we use tiny name examples to make every count and probability visible. We cover START padding, next-character generation, zero probabilities, add-k smoothing, the growth of context tables, sparse storage, backoff, and interpolation.

More context can capture useful patterns. But with the same training data, each more specific context has the same number or fewer matching examples than its shorter ending. We explain the tradeoff without assuming that longer context must always help or always hurt.

Download the theory companion guide (PDF):
https://github.com/HussainAbuwala/llm-from-scratch/blob/main/docs/episode-02-theory.pdf

Download the canvas - all 29 frames (PDF):
https://github.com/HussainAbuwala/llm-from-scratch/blob/main/docs/episode-02-canvas.pdf

Editable Excalidraw canvas (download and open in Excalidraw):
https://github.com/HussainAbuwala/llm-from-scratch/blob/main/canvas/episode_02_trigrams.excalidraw

Repository, exercises, and source files:
https://github.com/HussainAbuwala/llm-from-scratch

Watch the bigram theory episode first:
https://www.youtube.com/watch?v=YV30EDncrY4

Chapters:
00:00 From bigrams to trigrams: context, boundaries, and counts
08:44 Generation, missing evidence, and smoothing
16:16 Smoothing the full path and splitting evidence
23:53 Unseen longer contexts, table growth, and sparse storage
33:07 Practical responses, backoff, interpolation, and what comes next

The coding companion will implement the models on a larger names dataset and compare training loss, held-out loss, and rare or unseen contexts. This video focuses on the theory and hand-worked examples; no coding is required.

Foundations and further reading:
Jurafsky & Martin, Speech and Language Processing, Chapter 3:
https://web.stanford.edu/~jurafsky/slp3/3.pdf

Chen & Goodman (1996), An Empirical Study of Smoothing Techniques for Language Modeling:
https://aclanthology.org/P96-1041/

Bengio et al. (2003), A Neural Probabilistic Language Model:
https://jmlr.org/papers/v3/bengio03a.html

Educational inspiration and coding-dataset source: Andrej Karpathy's makemore:
https://github.com/karpathy/makemore

The methods come from established language-modeling literature; the tiny examples and teaching sequence are ours. The series builds toward a small decoder-only Transformer that we can implement and train ourselves.

#LLMFromScratch #LanguageModels #MachineLearning

## Tags

LLM from scratch, trigram language model, bigram model, n gram language model, language modeling, next token prediction, character language model, data sparsity, context length, add k smoothing, Laplace smoothing, backoff, interpolation, negative log likelihood, machine learning theory, name generation

## Thumbnail choices

A (recommended): `thumbnails/episode-02a-more-context.jpg` - MORE CONTEXT, BETTER?

B: `thumbnails/episode-02a-counts-run-out.jpg` - WHERE COUNTS RUN OUT

C: `thumbnails/episode-02a-one-more-letter.jpg` - ONE MORE LETTER

All are 1280 x 720 JPGs. See `EPISODE_02A_THUMBNAILS.md` for the comparison.

## Prepared upload settings

- Channel: The Unplanned Stack
- Playlist: Building an LLM From Scratch, if available
- Category: Education
- Language: English
- Audience: General software education; not made for kids
- Visibility: Leave private for review; no upload, publishing, or scheduling performed
- License: Standard YouTube License
- Chapters: Use the supplied verified source-part boundaries
- Captions: Review automatic captions after upload, especially n-gram, START, END, NLL, backoff, and interpolation
- No paid promotion or realistic synthetic scenes were added in this edit

## Suggested pinned comment (prepared, not posted)

More context gives us a more specific question, but do we have enough matching examples to answer it reliably?

Theory guide: https://github.com/HussainAbuwala/llm-from-scratch/blob/main/docs/episode-02-theory.pdf
Canvas PDF: https://github.com/HussainAbuwala/llm-from-scratch/blob/main/docs/episode-02-canvas.pdf

Try explaining the difference between a missing context row and a zero-count target inside a seen row. That distinction is the key to understanding our simple backoff rule.

## Editorial notes (do not paste into the description)

- Join parts 1-5 in numeric order. Remove [09:14.000, 09:18.000) from part 4 only.
- The final 0.133 seconds of part 4 is retained. No other content cuts or transitions were added.
- Export: 1920 x 1080, H.264, 30 fps, AAC stereo 48 kHz; duration about 43:43.6.
- Chapter markers use the five source-part boundaries, rounded down to seconds. Their subjects were checked against frames from each source part. These are not fine-grained transcript timings.
- The presenter guide's 26-minute estimate is a rehearsal estimate, not the recorded duration.
- Companion links target the repository's main branch. They become public only after this release commit is pushed. Preparing this package does not publish a YouTube video.
- The existing lab and validation results are included as development material; the Episode 02B notebook and final test evaluation are not represented as finished.
