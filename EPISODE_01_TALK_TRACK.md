# Episode 1 Talk Track

Canvas: `canvas/episode_01_bigram.excalidraw` (27 scenes)
Theory: [EPISODE_01_THEORY.md](EPISODE_01_THEORY.md) · Plan: [EPISODE_01_VIDEO_PLAN.md](EPISODE_01_VIDEO_PLAN.md)

## How to use this

**Do not read the canvas aloud.** Whatever is on screen, the viewer has already
read it — people read several times faster than you speak. If your voice is
saying the same words, you are dead air with a face on it. The canvas is the
skeleton; your voice is the muscle.

**Do not write a full script either.** Read scripts sound read, and this series'
whole credibility rests on you sounding like someone working something out.

What you want is four things per scene, which is what this file gives you:

| Field | What it is |
|---|---|
| **SAY** | The one sentence that must land. Everything else can be improvised. |
| **DRAW** | What you annotate live. Every scene has one — this is the format. |
| **NUMBERS** | Exact values to state. Read these; do not recall them. |
| **BRIDGE** | The sentence that creates the need for the next scene. |

**Episode 1 has two kinds of scene and they want opposite treatment:**

- **Mechanical scenes** — 07 to 09, 15 to 18, 20 to 22. Arithmetic on screen.
  Say the numbers precisely and slowly; work them on camera. Precision is the
  product here.
- **Conceptual scenes** — 01 to 06, 10 to 14, 19, 23 to 27. Conviction, not
  precision. Bullets only, improvise the wording, let yourself be informal.

Getting these backwards is the main way this episode goes wrong: rehearsed
delivery of the ideas, and hand-wavy delivery of the numbers.

**One take per scene**, not one take per video. 27 short takes are recoverable.

---

## 01 · Cold open

> **The four names here are illustrative, not real output** — the program does not
> exist yet. That is a deliberate choice and it is fine; illustrative examples are
> normal throughout this episode. The only thing worth watching is framing: the
> `$ python bigram.py` line makes it read as a run that happened rather than as an
> example. Either say "roughly what it will produce" on camera, or drop that one
> line from the scene. Swap in real samples later if you happen to have them.

What is on screen: `$ python bigram.py` — the program you build in the follow-up
video — and four names it generated. Three look plausible; `annnava` is broken.

- **SAY:** "These came out of a program with no neural network, no attention, and a memory of exactly one character."
- **DRAW:** Take the pen and circle the broken one — **not** the good ones.
- **BRIDGE:** "That sounds almost useless. It is also the smallest thing that is honestly a language model."

**Why circle the failure.** Three reasons, and they compound:

1. The viewer has already spotted it. Showcasing the successes while ignoring the
   obvious dud makes you look like you are selling; pointing at it first makes you
   the person who noticed.
2. It states the honest claim in the first fifteen seconds — this works, and it
   also produces garbage — which is the tone the whole series runs on.
3. It is a seed you harvest in scene 25. Trained on `anna` and `ava`, every
   adjacent pair in `annnava` was genuinely observed: `a→n`, `n→n`, `n→a`,
   `a→v`, `v→a`. Every neighbouring step is legitimate and the whole word is
   still nonsense. Circling it here and calling back to it later makes the
   episode feel built rather than listed.

Pick your real failure sample with that callback in mind — you want one whose
adjacent pairs all check out.

## 02 · What a language model outputs

- **SAY:** "A language model does not output text. It outputs a number for every token that could come next."
- **DRAW:** Trace the loop arrow; tick the bars as you name them.
- **NUMBERS:** n 0.25, v 0.25, END 0.50 — and they add to 1.
- **BRIDGE:** "Predicting and choosing are two different jobs. We'll do the choosing two different ways later."

## 03 · Make the problem tiny

- **SAY:** "Tokens are characters and context is one character — both are deliberate simplifications, and both get replaced later in the series."
- **DRAW:** Split `anna` into the four cards with your pen.
- **BRIDGE:** "First it has to become numbers."

## 04 · Vocabulary and integer IDs

- **SAY:** "The model never sees a letter. Integers are row and column numbers, and that is the only reason they exist."
- **DRAW:** Draw the arrow from each character to its id.
- **BRIDGE:** "Two of these tokens aren't characters at all."

Mention the training-split-only vocabulary rule, briefly. It matters in the build video.

## 05 · Boundaries

- **SAY:** "`<END>` is not decoration. Without it the model never predicts stopping, so it isn't describing names — it's describing endless streams of letters."
- **ALSO SAY:** "`<START>` is where generation begins. Without it the model could only ever continue text — it could never start any."
- **DRAW:** Underline `<START>` green, `<END>` red as you assign each its job.
- **BRIDGE:** "Now we can turn this into the only thing the model actually learns from."

The generation-side motivation for `<START>` is the concrete one and is easy to
leave implicit. Say it here: the model always needs a current token, and on the
first step there is nothing to condition on unless you invent one. That is also
why the matrix is asymmetric in scene 08 — `<START>` is somewhere you can be,
never somewhere you can arrive.

## 06 · The sliding window

- **SAY:** "Training data isn't text. It's ordered pairs."
- **DRAW:** Slide the window down, ticking off each pair on the right as you go. Five moves, five ticks.
- **NUMBERS:** A four-letter name gives five transitions.
- **BRIDGE:** "`a → n` and `n → a` are different observations. Never merge them."

Slow down here. This is the scene where a beginner either gets it or is lost for the next twenty minutes.

## 07 · Counting  ·  *mechanical*

- **SAY:** "Training, for this model, is counting. There is no optimiser and no second pass."
- **DRAW:** Tally each transition into the merged list as you say it.
- **NUMBERS:** `<START>→a` 2, `a→n` 1, `a→v` 1, `a→<END>` 2, `n→n` 1, `n→a` 1, `v→a` 1. Out of `a`: four observations.
- **BRIDGE:** "Four observations out of `a`. Hold that number."

## 08 · The count matrix  ·  *mechanical*

- **SAY:** "`<START>` is a row but never a column. `<END>` is a column but never a row."
- **DRAW:** Write the 2 into the `<START>→a` cell yourself. Shade the `a` row.
- **NUMBERS:** Row `a` = [0, 1, 1, 2]. Matrix is (V+1) × (V+1).
- **BRIDGE:** "Every cell in here is a transition that is at least possible. That matters in about ten minutes."

## 09 · Counts → probabilities  ·  *mechanical*

- **SAY:** "Counts are not probabilities. Divide every count by the row total."
- **DRAW:** Write `÷ 4` and the four results. Then count the tickets out loud.
- **NUMBERS:** [0, 1, 1, 2] ÷ 4 = 0.00, 0.25, 0.25, 0.50. Adds to 1.00. `<END>` owns two of four tickets.
- **BRIDGE:** "Say the phrase 'maximum-likelihood estimate' and move on. We come back to it."

## 10 · What the model IS

- **SAY:** "This is the finished model. There is nothing else, and no network is hiding behind it."
- **DRAW:** Box the three artefacts, then underline `P(next | current)`.
- **BRIDGE:** "Saving this model means saving a table of numbers. So — can it write anything?"

## 11 · Greedy decoding

- **SAY:** "Greedy picks the best next token, which is not the same as the best sequence."
- **DRAW:** Start your pen on `<START>` and say "this is the seed" before tracing. Then circle the loop when it repeats.
- **BRIDGE:** "It never takes a lower-probability exit, even when that exit is the only sane move."

Say the illustration is constructed. Do not imply it came out of the run.

## 12 · Sampling

- **SAY:** "Treat the probabilities as odds, not as a ranking."
- **DRAW:** Count out the 60/30/10 ticket strip.
- **NUMBERS:** 60, 30, 10 out of 100.
- **BRIDGE:** "Greedy shows you one path through the model. Sampling shows you the model."

## 13 · Lucky, or good?

- **SAY:** "Is the model good, or did I get lucky and pick the one I liked?"
- **DRAW:** Circle `marin`, then cross out the failures one by one.
- **BRIDGE:** "We need one number I cannot flatter myself with."

This is the hinge of the episode. Let the pause sit before you answer it.

## 14 · The answer key

- **SAY:** "During generation there is no correct answer. During evaluation, the held-out text supplies one."
- **DRAW:** Highlight the true-target column, then the bar for row 2.
- **NUMBERS:** Illustrative — say so. Row 2: greedy would have said `<END>`; we record the 0.25 it gave to `n`.
- **BRIDGE:** "Evaluation never changes the model. We are taking a measurement."

## 15 · Why the probabilities multiply  ·  *mechanical*

- **SAY:** "Each multiplication takes a fraction of whatever survived the step before."
- **DRAW:** Walk down the funnel writing each survivor count.
- **NUMBERS:** 100 → ×0.80 → 80 → ×0.50 → 40 → ×0.25 → 10 → ×0.40 → 4. So P = 0.04.
- **BRIDGE:** "Now do that for a thousand tokens instead of four."

Name the chain rule once. Don't dwell.

## 16 · Logarithms, and why we need them  ·  *mechanical*

- **SAY:** "The problem comes first: multiply a thousand small numbers and your computer rounds it to zero."
- **DRAW:** Write `10³ = 1000` then the log underneath it.
- **NUMBERS:** ln 0.80 ≈ −0.22, ln 0.50 ≈ −0.69, ln 0.25 ≈ −1.39, ln 0.40 ≈ −0.92. Sum ≈ −3.22. And ln(0.04) ≈ −3.22 — the same number.
- **BRIDGE:** "Probabilities are at most 1, so their logs are never positive. Which is awkward for a score."

Do the addition on camera. The two −3.22s matching is the moment logs stop being scary.

## 17 · Negative log-likelihood  ·  *mechanical*

- **SAY:** "Flip the sign and you have a loss where lower is better — and every optimiser we meet from episode 3 pushes numbers down."
- **DRAW:** Read the surprise table row by row.
- **NUMBERS:** 100% → 0.00; 50% → 0.69; 10% → 2.30; 1% → 4.61.
- **BRIDGE:** "Total penalty grows with the amount of text, so divide by the number of transitions."

## 18 · Lower than what?  ·  *mechanical*

- **SAY:** "An average NLL of 2.4 means nothing on its own."
- **DRAW:** Draw the two arrows left to right as you build up the comparison.
- **NUMBERS:** Uniform = ln(V+1); for V=26 that is ln(27) ≈ 3.30. Bigram must beat unigram or one character of context bought nothing.
- **BRIDGE:** "Same number, two names you'll see everywhere: cross-entropy and perplexity."

This scene did not exist in your first draft and it is the most useful one in the episode. Don't rush it.

## 19 · What counting already did

- **SAY:** "Dividing counts by row totals isn't just reasonable — it's the exact minimiser of the loss we just defined."
- **DRAW:** Arrow from the left box to the right box as you say "episode 3 will crawl there with gradients."
- **BRIDGE:** "Which gives us the answer key for the next model. If the network doesn't reach roughly this number, the training code is broken."

The single most important sentence in the whole series. Say it twice, differently.

## 20 · The zero

- **SAY:** "Zero is a very strong claim. It says `a → x` is impossible, on the evidence of a few hundred names."
- **DRAW:** Circle the 0, then the 0.00 under it, then write `∞`.
- **NUMBERS:** One zero anywhere makes the whole product zero. −log(0) is undefined, not large.
- **BRIDGE:** "So the fix has to deliberately move away from the maximum-likelihood estimate."

## 21 · Add-k smoothing  ·  *mechanical*

- **SAY:** "The `k × A` in the denominator is not optional — we added k to A cells, so the total grew by k times A."
- **DRAW:** Write +1 into each cell, then the new total, then each new probability.
- **NUMBERS:** [1,1,2,0] → [2,2,3,1], total 8 → 0.250, 0.250, 0.375, 0.125. `P(<END>|a)` fell from 0.500 to 0.375.
- **BRIDGE:** "Nothing is free. Probability given to the unseen is taken from the seen."

## 22 · k is a dial, and it costs you  ·  *mechanical*

- **SAY:** "Smoothing makes the training loss worse, on purpose. k = 0 is unbeatable on training data by construction."
- **DRAW:** Draw both curves yourself, training first, then validation. Mark where you'd pick k.
- **BRIDGE:** "The setting that makes training loss lowest is not the setting that generalises best. That's the whole field in one line."

## 23 · Two different problems

- **SAY:** "Smoothing changes a belief: from 'unseen means impossible' to 'unseen means unlikely'."
- **DRAW:** Tick the green panel, cross the red one.
- **BRIDGE:** "An unknown character is a tokenizer problem, and we'll fix it much later."

## 24 · Limitation 1: it forgets

- **SAY:** "Twenty characters of context and two characters of context are the same thing to this model."
- **DRAW:** Draw all four arrows into the single row, one at a time, deliberately.
- **BRIDGE:** "It cannot know how it got to `a`."

The repetition of drawing four arrows into one box is the argument. Don't shortcut it.

## 25 · Limitation 2: locally fine, globally nonsense

- **SAY:** "Every adjacent pair in that word was observed in training. The whole word is still garbage."
- **DRAW:** Check off each pair in `annnnavannava` against the learned list.
- **BRIDGE:** "Local correctness does not compose into global coherence."

## 26 · The obvious fix, and why it fails

- **SAY:** "Fine — remember two characters. Now count the rows you need."
- **DRAW:** Write each number as you say it. Let the last one land.
- **NUMBERS:** 30 → 900 → 27,000 → and for ten characters, about 590 trillion.
- **BRIDGE:** "Almost all of those rows would be empty. More context makes the table sparser and the zeros worse."

## 27 · The question for episode 2

- **SAY:** "How can a model use more context, and share what it learns between similar contexts, without storing a number for every possible history?"
- **DRAW:** Underline "generalise" and "compress".
- **BRIDGE:** Stop. Do not answer it.

---

## Rehearsal

Do one pass out loud with the canvas open and nothing else, timing yourself per
scene. Anything under 30 seconds is probably being read. Anything over 2 minutes
has two scenes' worth of content in it and should be split.

Episode 0 ran 11:20 against a 7–9 minute plan. Expect the same stretch here —
so budget for 40 minutes, and if it lands there, that is fine. This one is
allowed to be long.
