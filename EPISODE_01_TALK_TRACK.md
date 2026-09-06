# Episode 1 Talk Track

Status: Detailed development reference. The recorded version uses
[`canvas/episode_01_presenter.excalidraw`](canvas/episode_01_presenter.excalidraw)
and [`canvas/EPISODE_01_PRESENTER_GUIDE.md`](canvas/EPISODE_01_PRESENTER_GUIDE.md).

Canvas: `canvas/episode_01_bigram.excalidraw` (24 scenes)
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

- **Mechanical scenes** — 07 to 09 and 11 to 20. Arithmetic on screen.
  Say the numbers precisely and slowly; work them on camera. Precision is the
  product here.
- **Conceptual scenes** — 01 to 06, 10, 13, and 21 to 24. Conviction, not
  precision. Bullets only, improvise the wording, let yourself be informal.

Getting these backwards is the main way this episode goes wrong: rehearsed
delivery of the ideas, and hand-wavy delivery of the numbers.

**One take per scene**, not one take per video. 24 short takes are recoverable.

---

## 01 · Cold open

What is on screen: the complete toy training corpus and four sequences that its
probability table can produce. Nothing is presented as code output yet.

- **SAY:** "Today we will make every number in a real language model small enough to check by hand. In the next video, we will implement the same concepts on a larger dataset."
- **DRAW:** Take the pen and circle the broken one — **not** the good ones.
- **BRIDGE:** "That sounds almost useless. It is also the smallest thing that is honestly a language model."

**Why circle the failure.** Three reasons, and they compound:

1. The viewer has already spotted it. Showcasing the successes while ignoring the
   obvious dud makes you look like you are selling; pointing at it first makes you
   the person who noticed.
2. It states the honest claim in the first fifteen seconds — this works, and it
   also produces garbage — which is the tone the whole series runs on.
3. It is a seed you harvest in scene 22. Trained on `anna` and `ava`, every
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

## 03 · What "vocabulary" means

- **SAY:** "The vocabulary is the set of token types. It is not the names — the names are the data. The vocabulary is what the model is allowed to emit."
- **DRAW:** Sweep across the three panels left to right as you name them: characters, words, subword pieces.
- **NUMBERS:** The worked vocabulary has three ordinary characters: `a`, `n`, `v`. Including `<END>`, there are four allowed next-token outcomes. `<START>` is a context, not an outcome.
- **BRIDGE:** "Ours is characters. So now every one of them needs a number."

**Keep this to 30–45 seconds.** It is a definition scene, not a tokenization
lecture — the whole point is to stop "vocabulary" meaning "the words I know", and
to show the definition survives the tokens changing. Do not get drawn into how BPE
works; that is episode 13 and the panel says so.

The everyday meaning of the word points the wrong way, and it would be *correct*
for a word-level model, which is what makes it worth 40 seconds rather than a
throwaway line.

## 04 · Vocabulary and integer IDs

- **SAY:** "The model never sees a letter. Integers are row and column numbers, and that is the only reason they exist."
- **THEN:** Point at `"anna" → [2, 3, 3, 2]`. "That is what actually gets handed to the model. Letters only exist when we read the file and when we print the result."
- **DRAW:** Draw the arrow from each character to its id.
- **WATCH FOR:** Say explicitly that the vocabulary is the *characters*, not the names. The names are the data; the vocabulary is the alphabet they are built from. Everyday English means the opposite by "vocabulary", so the word points the wrong way for a beginner — and it is a word-level model where the vocabulary really would be the words.
- **BRIDGE:** "Two of these tokens aren't characters at all."

Expand the abbreviations out loud the first time — `stoi` is **s**tring **to**
**i**nt, `itos` is **i**nt **to** **s**tring. They are conventional names you will
keep meeting, and they stop looking arbitrary the moment you hear what they stand
for. One goes in, one comes out: `stoi` to build the table from text, `itos` to
turn a generated number back into a printable name.

Mention the training-split-only vocabulary rule, briefly. It matters in the build video.

## 05 · Boundaries

- **SAY:** "Without `<END>`, the model can only ever answer *what comes next* — it can never say *that's the whole name*."
- **THEN:** "P(anna) would really mean P(anything starting with anna). Annabelle included. There'd be no way to say the name ended there."
- **ALSO SAY:** "`<START>` is where generation begins. Without it the model could only ever continue text — it could never start any."
- **DRAW:** Underline `<START>` green, `<END>` red as you assign each its job.
- **BRIDGE:** "Now we can turn this into the only thing the model actually learns from."

The generation-side motivation for `<START>` is the concrete one and is easy to
leave implicit. Say it here: the model always needs a current token, and on the
first step there is nothing to condition on unless you invent one. That is also
why the matrix is asymmetric in scene 08 — `<START>` is somewhere you can be,
never somewhere you can arrive.

## 06 · The sliding window

- **SAY:** "Training data isn't text. It's ordered pairs. Each pair is a bigram — bi meaning two — which is where the model gets its name."
- **WATCH FOR:** A bigram model does not look at two tokens of context. It counts *pairs*, and one half of each pair is the thing being predicted, so the context is one token. An n-gram model has context length n−1 — which is why the trigram in scene 23 gives you two characters of history, not three.
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

## 11 · Generate one example  ·  *mechanical*

- **SAY:** "Generation is not a new model. It is repeated lookup and sampling from the fixed table we just trained."
- **DRAW:** Trace `<START> → a → n → a → <END>` one token at a time. At each arrow, point back to the exact probability row that supplied the number.
- **NUMBERS:** 1.00, 0.25, 0.50, 0.50. Output: `ana`.
- **BRIDGE:** "Those numbers describe the choices. They do not tell us how to choose."

This is the explicit post-training generation walkthrough. Pause at `a`: `<END>`
is the largest value, but sampling can still select `n` with probability 0.25.

## 12 · Greedy versus sampling

- **SAY:** "Greedy and sampling query the same table. Only the selection rule changes."
- **DRAW:** Trace greedy on the left, then the sampled path on the right.
- **NUMBERS:** Greedy produces `a` because `P(END|a)=0.50` is the row maximum. Sampling can produce `ana` by taking the 0.25 `a→n` branch.
- **BRIDGE:** "A generated word can look convincing. That still does not tell us whether the model is good."

Mention the maximum-length guard once. It is an implementation requirement for
the next video, not another decoding lesson.

## 13 · Lucky, or good?

- **SAY:** "Is the model good, or did I get lucky and pick the one I liked?"
- **DRAW:** Circle `ana`, then cross out the weaker toy-table samples one by one.
- **BRIDGE:** "We need one number I cannot flatter myself with."

This is the hinge of the episode. Let the pause sit before you answer it.

## 14 · The answer key

- **SAY:** "During generation there is no correct answer. During evaluation, the held-out text supplies one."
- **DRAW:** Highlight the true-target column, then the bar for row 2.
- **NUMBERS:** Exact toy-table values: `<START>→a` 1.00, `a→n` 0.25, `n→a` 0.50, `a→END` 0.50.
- **BRIDGE:** "Evaluation never changes the model. We are taking a measurement."

## 15 · Why the probabilities multiply  ·  *mechanical*

- **SAY:** "Each multiplication takes a fraction of whatever survived the step before."
- **DRAW:** Walk down the funnel writing each survivor count.
- **NUMBERS:** 16 → ×1.00 → 16 → ×0.25 → 4 → ×0.50 → 2 → ×0.50 → 1. So P(`ana`) = 1/16 = 0.0625.
- **BRIDGE:** "Now do that for a thousand tokens instead of four."

Name the chain rule once. Don't dwell.

## 16 · Logarithms, and why we need them  ·  *mechanical*

- **SAY:** "The problem comes first: multiply a thousand small numbers and your computer rounds it to zero."
- **DRAW:** Write `10³ = 1000` then the log underneath it.
- **NUMBERS:** ln 1.00 = 0, ln 0.25 ≈ −1.39, ln 0.50 ≈ −0.69 twice. Sum ≈ −2.77. And ln(0.0625) ≈ −2.77 — the same number.
- **BRIDGE:** "Probabilities are at most 1, so their logs are never positive. Which is awkward for a score."

Do the addition on camera. The two −2.77s matching is the moment logs stop being scary.

## 17 · Negative log-likelihood  ·  *mechanical*

- **SAY:** "Negate each log probability, add the penalties, then divide by four. That gives the model's average surprise per transition."
- **DRAW:** Work down the four exact transitions, then perform the final division.
- **NUMBERS:** 0.000 + 1.386 + 0.693 + 0.693 = 2.772. Divide by 4: average NLL = 0.693 nats per transition.
- **BRIDGE:** "Now we have a number. But a number is meaningless until we compare it with something."

## 18 · Lower than what?  ·  *mechanical*

- **SAY:** "An average NLL of 0.693 means nothing on its own."
- **DRAW:** Draw the two arrows left to right as you build up the comparison.
- **NUMBERS:** Uniform NLL 1.386; unigram NLL 1.158; bigram NLL 0.693, all evaluated on `ana` with the toy training corpus.
- **BRIDGE:** "For this example, one character of context helped. Now we have to confront the zeros that counting creates."

The coding episode will recompute these baselines on the larger dataset. The
concept and comparison remain; the values should change.

## 19 · The zero  ·  *mechanical*

- **SAY:** "Both characters are known. The model assigns zero only because this particular ordered pair never appeared."
- **DRAW:** Circle `v→n`, then the zero probability, then the infinite penalty.
- **NUMBERS:** `v` row = [1,0,0,0] over [a,n,v,END]. `P(n|v)=0`. `P(avna)=0`.
- **BRIDGE:** "We need to reserve a little probability for transitions absent from a tiny sample."

Use `v→n` because it comes directly from the same `{anna, ava}` table. No new
character or second hidden corpus is introduced.

## 20 · Add-k smoothing  ·  *mechanical*

- **SAY:** "Add one to every allowed cell, not only to the cell that caused trouble."
- **DRAW:** Add the four pseudo-counts, update the total, then normalize.
- **NUMBERS:** [1,0,0,0] → [2,1,1,1], total 5 → [0.40,0.20,0.20,0.20]. `P(n|v)` rises from 0 to 0.20; `P(a|v)` falls from 1.00 to 0.40.
- **BRIDGE:** "The model now handles unseen pairs, but it still remembers only one character."

State the practical coding rule without adding another frame: make `k`
configurable and compare choices on validation data. Smoothing cannot create a
token that is missing from the vocabulary.

## 21 · Limitation 1: it forgets

- **SAY:** "Twenty characters of context and two characters of context are the same thing to this model."
- **DRAW:** Draw all four arrows into the single row, one at a time, deliberately.
- **BRIDGE:** "It cannot know how it got to `a`."

The repetition of drawing four arrows into one box is the argument. Don't shortcut it.

## 22 · Limitation 2: locally fine, globally nonsense

- **SAY:** "Every adjacent pair in that word was observed in training. The whole word is still garbage."
- **DRAW:** Check off each pair in `annnnavannava` against the learned list.
- **BRIDGE:** "Local correctness does not compose into global coherence."

## 23 · The obvious fix, and why it fails

- **SAY:** "Fine — remember two characters. Now count the rows you need."
- **DRAW:** Write each number as you say it. Let the last one land.
- **NUMBERS:** 30 → 900 → 27,000 → and for ten characters, about 590 trillion.
- **BRIDGE:** "Almost all of those rows would be empty. More context makes the table sparser and the zeros worse."

## 24 · Next: implement the same concepts

- **SAY:** "How can a model use more context, and share what it learns between similar contexts, without storing a number for every possible history?"
- **DRAW:** Underline "generalise" and "compress".
- **BRIDGE:** "Before replacing counting, the next video implements this complete count-based model on a larger names dataset. The concepts stay the same; the numbers become real."

Do not promise that the coding episode reproduces the toy values. Its checks
are structural: pair extraction is correct, probability rows sum to one,
generation follows the lookup loop, evaluation uses held-out targets, and
smoothing removes zero-probability transitions.

---

## Rehearsal

Do one pass out loud with the canvas open and nothing else, timing yourself per
scene. Anything under 30 seconds is probably being read. Anything over 2 minutes
has two scenes' worth of content in it and should be split.

The canvas is now four scenes shorter and keeps one numerical example throughout.
Budget roughly 30–35 minutes. If rehearsal passes 35, shorten the vocabulary
comparison and the context-growth bridge before cutting the mechanical trace.
