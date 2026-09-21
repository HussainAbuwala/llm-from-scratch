# Bridge video · Upload preparation

## Recommended title

Our Language Model’s Next Chapter: From Counts to Weights

Alternative titles:

- Connecting the Dots: From Counts to Weights | LLM From Scratch
- Bigrams, Trigrams… What Comes Next? | LLM From Scratch
- Our Language Model Gets a New Learning Method | From Counts to Weights

Place between Episode 02B and Episode 03A in the series playlist. Label this
as a bridge rather than Episode 03 or an extra theory/build pair.

## Description — ready to copy

We've built bigram and trigram language models, generated names, and measured what happens when we give a count-based model more context. Before the next lesson, let's connect what we've learned to where we're going.

This bridge explains why we started with counting, what sparse evidence means, and why our next step is learning how adjustable weights produce probabilities. We use a small cup-and-mug example to separate three ideas: pooling evidence through shorter histories, combining predictions with interpolation, and learning useful relationships between different inputs.

The cup/mug illustration uses word tokens. Our implemented models and the next bigram lesson still use character tokens.

What comes next:
• Episode 03: bigram weights and softmax
• Episodes 04–06: gradients, autograd, then rebuilding the bigram in PyTorch
• Episode 07: embeddings and a small neural network

The learned bigram is a familiar task for understanding the training method. We are not claiming that weights alone solve sparse evidence or guarantee a better bigram.

Backoff and interpolation already reuse evidence from shorter histories. Our coding experiment did not test those methods, so it does not show that they are insufficient. We're now taking the route toward learned representations and, eventually, a small Transformer. First, we'll learn the training mechanism on the familiar bigram task.

Chapters:
00:00 Our language model's next chapter
01:03 What bigrams and trigrams taught us
01:51 More context, sparser evidence
02:33 Why exact matches keep related evidence separate
04:45 How longer and shorter count rows coexist
06:28 Backoff: choosing an existing row
08:34 Interpolation: combining predictions
10:30 What interpolation does not learn
11:34 Can learning about cups help with mugs?
12:52 Weights and the next steps in the series

This episode's learning notes and recording materials:
https://github.com/HussainAbuwala/llm-from-scratch/tree/main/episodes/02_bridge

Download the editable Excalidraw canvas:
https://github.com/HussainAbuwala/llm-from-scratch/blob/main/canvas/bridge_02_to_03.excalidraw

Series code and materials:
https://github.com/HussainAbuwala/llm-from-scratch

Previous coding lesson — notebook and results:
https://github.com/HussainAbuwala/llm-from-scratch/blob/main/episodes/02_trigrams/README.md

The roadmap:
https://github.com/HussainAbuwala/llm-from-scratch/blob/main/SERIES_PLAN.md

References:
Jurafsky & Martin, Speech and Language Processing, Chapter 3:
https://web.stanford.edu/~jurafsky/slp3/3.pdf

Bengio et al., A Neural Probabilistic Language Model (2003):
https://www.jmlr.org/papers/v3/bengio03a.html

#LLMFromScratch #MachineLearning #LanguageModels

## Tags

LLM from scratch, language models, bigram model, trigram model, n gram language model, count based language model, backoff, interpolation, data sparsity, neural language model, neural network weights, machine learning, natural language processing, The Unplanned Stack

## Thumbnail alternatives

[Side-by-side comparison](thumbnails/bridge-02-to-03-options.jpg)

| Option | Headline | Image | Angle |
|---|---|---|---|
| A — recommended | NEXT CHAPTER | [Download JPG](thumbnails/bridge-02-to-03.jpg) | Direct bridge from count tables to adjustable weights |
| B | GIVE IT A DIAL | [Download JPG](thumbnails/bridge-02-to-03-sharing.jpg) | Playful introduction to adjustable weights |
| C | CONNECT THE DOTS | [Download JPG](thumbnails/bridge-02-to-03-roadmap.jpg) | Connect previous lessons with the next stage |

All three are 1280 × 720 JPGs under 2 MB. A narrow navy Count strip transitions
into the warm cream-and-plum Learn theme, with the existing local font.
See [the stage theme guide](SERIES_VISUAL_THEMES.md) for Count, Learn and Attend palettes. These are illustrative diagrams, not experimental outputs.
The comparison sheet is for review, not upload. No selection is assumed.

Suggested pair: recommended title + thumbnail A. B adds a playful adjustable-model metaphor; C emphasizes connecting the lessons. These are editorial alternatives,
not claims of measured click-through performance.

Rebuild from repository root:

```bash
.venv/bin/python youtube/build_bridge_thumbnail.py
```

## Recording and publishing notes

- Recording inspected: `~/Movies/llm-series/episode-bridge-02-03.mp4`.
  Duration: 927.633333 seconds (15:27.633), 1920 × 1080, 30 fps.
- Chapters above use observed canvas transitions in the recording, rounded down
  to whole seconds. They are visual topic navigation points, not verified
  word-level narration boundaries. Zooms within a frame are not new chapters.
- Frames 8 and 9 are grouped under “What interpolation does not learn.”
- Transition detection: `youtube/chapters.py`; each topic heading was inspected
  on extracted frames, with spot checks one second after the chosen transitions.
  No transcript or full spoken-content audit was performed.
- Add the actual previous-video and next-video links when available. Do not
  invent video URLs. The description currently links to existing repository paths.
- Category: Education. Language: English. Use the existing series playlist.
- Audience: General software education; not made for kids.
- Suggested initial visibility: Private for review. License: Standard YouTube License.
- Optional end screen: link the previous trigram coding video and the series playlist.
- Review captions for bigram, trigram, NLL, backoff, interpolation, weights,
  embeddings, autograd and PyTorch.
- The bridge repository links above target the main branch; verify them after pushing.
- This package does not upload, publish, schedule or post a comment.

## Optional pinned comment — draft

What feels clear now, and what still feels confusing about the move from counting to learning weights? The next lesson returns to bigrams so we can focus on the learning mechanism itself.
