# YouTube Metadata — Video 0: Series Introduction

Everything needed to upload. Copy-paste blocks are marked.

> **Chapters are measured from the actual recording** (`llm-2026-08-17
> 09-02-34.mp4`, 11:20), not from the plan. Derived by frame-differencing the
> canvas region to find the Excalidraw scene transitions, then reading the frame
> heading at each one — see `youtube/chapters.py` to redo this for later
> episodes. All ten satisfy YouTube's rules: first at `00:00`, ten chapters,
> minimum gap 39s.

---

## 1. Title

**Recommended:**

```
I Can't Explain an LLM. So I'm Building One From Scratch.
```

56 characters. It carries the confession *and* the searchable phrase
("building an LLM from scratch"), and it sets up a series rather than a one-off.

Pair it with **thumbnail `07_excalidraw_llm`** (the drawing of the machine). Title
and thumbnail should say *different* things: the title makes the confession, and
the thumbnail answers the question it raises by opening the box. Pairing this
title with `01_cant_explain` or `05_blackbox` wastes the thumbnail on the same
four words.

**Alternative pairings**

| Thumbnail | Title |
|---|---|
| `04_notebook` | `I Can't Explain an LLM. So I'm Building One From Scratch.` |
| `01_cant_explain` | `Building an LLM From Scratch: Counting to GPT in 14 Episodes` |
| `02_counting_gpt` | `Before You Learn Transformers, Build This (LLM From Scratch, Ep 0)` |

Avoid: "Episode 0" or "Ep 0" at the *front* of the title. It reads as "nothing
has happened yet" to anyone who hasn't subscribed. The episode number is already
on the thumbnail chip and in the playlist.

---

## 2. Description

Copy from here to the end of the block:

```
I use LLMs every day. If you asked me to explain how one actually works, I couldn't.

So I'm building one from scratch — starting with a model so small you can check it with a pencil, and ending with a small GPT, written by us, trained on a laptop, that generates text. No API keys, no black boxes, no "trust me, it works".

I'm learning this as I go. That means you'll watch me check the papers, get things wrong, and fix them on camera. If that sounds like a strange way to teach, I think it's the honest one.

This first video is the plan: what we're building, the 14 episodes it takes, and the maths that shows up along the way (and when).

── THE PLAN ──────────────────────

Part 1 · COUNT (pure Python)
  01  The smallest language model
  02  Trigrams and the sparsity wall

Part 2 · LEARN (NumPy, then PyTorch)
  03  From counts to weights
  04  Gradients, by hand
  05  Autograd from scratch
  06  Enter PyTorch
  07  Embeddings and the MLP model
  08  Making training actually work

Part 3 · ATTEND (PyTorch)
  09  Why fixed context breaks
  10  Self-attention from scratch
  11  Multi-head attention and the block
  12  Build the GPT
  13  Tokenization for real (BPE)
  14  Train it. Make it talk.

Every episode ships twice: a theory video where I work one example by hand, and a build video where I write the code and the two numbers have to match on screen.

── WHAT YOU NEED ─────────────────

Python you'd call "okay" — loops, dicts, functions. Arithmetic. That's the floor.
No machine-learning background. No PyTorch. No maths degree. No GPU until episode 12, and free Colab covers that.

Every mathematical idea gets introduced from zero, in the episode that needs it. If a symbol is on screen, I've already said what it means.

── WHAT I'M NOT PROMISING ────────

This will not produce ChatGPT. The final model will be small and it will say strange things. It won't be fast and it won't be production code. What it will be is a language model where I can point at any line and tell you why it's there.

── EVERYTHING IS FREE ────────────

Theory write-ups, code, tests, and the actual Excalidraw canvas from each video:
https://github.com/HussainAbuwala/llm-from-scratch

── CHAPTERS ──────────────────────

00:00 I can't explain one
01:34 The only idea in the whole series
03:16 Using vs understanding
04:09 The four moves
05:53 All 14 episodes
06:40 Theory video + build video
07:19 The maths, just in time
08:30 What you need (and what I'm not promising)
09:47 What you get
10:37 Next: the smallest language model

── SOURCES THIS SERIES LEANS ON ──

Jurafsky & Martin, Speech and Language Processing — https://web.stanford.edu/~jurafsky/slp3/
Bengio et al. (2003), A Neural Probabilistic Language Model — https://www.jmlr.org/papers/v3/bengio03a.html
Vaswani et al. (2017), Attention Is All You Need — https://arxiv.org/abs/1706.03762
Karpathy, Neural Networks: Zero to Hero — https://github.com/karpathy/nn-zero-to-hero

Episode 1 is next: a language model with no neural network, no attention, and a memory of exactly one character. It still learns real structure from text — and it fails in ways that explain why everything after it exists.

#llm #machinelearning #fromscratch
```

Notes on the above:

- The GitHub link **404s until you push** — the remote exists but has no commits.
  Push before publishing, or the most valuable line in the description is dead.
- Only the first ~150 characters show before "...more", so the confession is
  deliberately in sentence one.
- Three hashtags maximum are displayed above the title. More than three and
  YouTube shows none.

---

## 3. Tags

Paste into the Tags field (500-character limit; this is ~340):

```
llm from scratch, build an llm, how llms work, language model tutorial, bigram model, transformer from scratch, gpt from scratch, machine learning for programmers, neural network from scratch, pytorch tutorial, attention mechanism explained, tokenization, next token prediction, andrej karpathy inspired, deep learning fundamentals, learn ml by building
```

---

## 4. Upload settings

| Field | Value |
|---|---|
| Visibility | Public (or schedule — see §8) |
| Category | Science & Technology |
| Language | English |
| Made for kids | **No** |
| Age restriction | No |
| Altered content disclosure | **No** — no synthetic media of real people |
| Comments | On, "hold potentially inappropriate for review" |
| Playlist | Create **"Building an LLM From Scratch"** and add this as item 1 |
| License | Standard YouTube License |
| Allow embedding | Yes |
| Shorts remixing | Allow video and audio remixing |

Playlist description:

```
Building a language model from nothing: counting, then gradients, then attention, then a small GPT — with the theory worked by hand and the code written on screen. Every episode has a theory video and a build video.
```

---

## 5. Thumbnail

Seven at `youtube/thumbnails/`, in three families.

**Drawn in Excalidraw** — the most coherent option, and the recommended one.

| File | Hook | |
|---|---|---|
| `07_excalidraw_llm.png` | "what's actually inside?" over a drawing of the machine — prompt in, layers of connected units in a cut-open box, next-token probabilities out | **recommended** |

Built by `canvas/build_thumbnail_ep0.py` as a genuine `.excalidraw` scene, on the
`#f9d6a7` peach sampled from your channel banner, so thumbnail, banner and canvas
share one ground. It is also the only option that *argues* the series: the black
box is open and you can see the parts.

For the upload, open `canvas/thumbnail_ep0.excalidraw`, select the frame and use
**Export image → PNG, "only selected"** — that gives authentic Excalidraw strokes
and the real Excalifont at 1600×900. The checked-in PNG is a Pillow-rendered
stand-in, close but not identical.

The other six, all 1280×720, in two families.

**Hand-drawn** — marker on graph paper, the same visual language as the
Excalidraw canvas the video is presented on. Recommended: it can't be mistaken
for a template, and it tells the truth about what the video looks like.

| File | Hook | Pair with |
|---|---|---|
| `04_notebook.png` | Promise — hand-lettered title, sketched staircase **(recommended)** | The recommended title |
| `05_blackbox.png` | Curiosity — "i can't explain this" + a drawn black box | A scope-focused title |
| `06_sticky.png` | Curiosity — whiteboard and sticky notes | Either |

**Flat vector** — bolder and higher contrast, but more conventional:

| File | Hook | Pair with |
|---|---|---|
| `01_cant_explain.png` | Curiosity — the admission | A scope-focused title |
| `02_counting_gpt.png` | Promise — the arc as coloured blocks | The recommended title |
| `03_no_api_keys.png` | Provocation — struck-through API call | Either |

**Recommended pair:** `07_excalidraw_llm.png` + *"I Can't Explain an LLM. So I'm
Building One From Scratch."* The title makes the confession; the thumbnail answers
it by opening the box. Neither repeats the other, and the peach ground matches the
channel banner.

Next best: `04_notebook.png` with the same title — same logic, less specific
image.

If you'd rather lead with `05_blackbox.png`, switch the title to
*"Building an LLM From Scratch: Counting to GPT in 14 Episodes"* — otherwise the
thumbnail and title say the same four words.

The `_guide` versions mark where your cutout goes. To composite it:

```bash
.venv/bin/python youtube/build_thumbnails.py --face ~/Desktop/cutout.png
```

A transparent-background PNG works best — export a cutout from Preview
(Instant Alpha) or `photos.google.com`. The script scales it to fill the
reserved box anchored to the bottom, so a head-and-shoulders crop sits correctly.

Before uploading, view the thumbnail at 20% zoom. If the words aren't readable
there, they aren't readable in the feed, which is where the decision happens.

Test the alternatives properly: YouTube's built-in **Test & Compare** runs up to
three thumbnails on the same video and picks the winner on watch time. Upload all
three rather than guessing.

---

## 6. Pinned comment

```
I'm learning this as I build it, so if you spot something I've got wrong, say so — corrections go in the next video, with credit.

Everything is free and in the description: theory write-ups, code, tests, and the Excalidraw canvas from this video.

Episode 1 is a language model with no neural network that remembers exactly one character. It's stranger and more useful than it sounds.
```

---

## 7. End screen and cards

- **End screen** (last 20 seconds): subscribe element + "latest upload". Until
  episode 1 exists, point the video element at the playlist.
- **Card** at ~03:30, when the 14 episodes come on screen: link the playlist.
- Do **not** put an end screen over the closing beat — the generated names are
  the hook for episode 1. Leave that shot clean and add the end screen after it.

---

## 8. Publishing

Best day for a developer-audience series intro is **Tuesday–Thursday, 14:00–16:00
UTC** — it catches US morning and European evening.

Publish episode 0 and episode 1 close together, ideally within a week. A series
intro with nothing to click through to converts far worse than one that hands the
viewer the first real episode immediately.

---

## 9. Shorts to cut from this video

Extract after the long-form is live, each with a link to the full video:

1. **"The only idea in LLMs"** (scene 02, ~50s) — the next-token loop, start to
   finish. The most self-contained idea in the video.
2. **"I can use one, I can't explain one"** (scene 03, ~30s) — the confession.
   Strongest hook, weakest information; good for reach.
3. **"The maths you actually need"** (scene 07, ~45s) — the just-in-time timeline.
   Answers the single most common reason people don't start.

Vertical crop: your canvas frames are 16:9, so a Short needs the canvas centred
with the face bubble moved to the top third. Re-record these against a zoomed
frame rather than cropping the 16:9 master.

---

## 10. Pre-publish checklist

- [ ] Chapter timestamps corrected against the finished cut
- [ ] Repo pushed, and the README link in the description opens
- [ ] Thumbnail checked at 20% zoom
- [ ] All three thumbnails uploaded to Test & Compare
- [ ] Playlist created and video added
- [ ] Description's first 150 characters read well truncated
- [ ] Watched the first 30 seconds on a phone, with sound
- [ ] Captions: let YouTube auto-generate, then fix "bigram", "NLL", "PyTorch",
      "Excalidraw", and your own name
