# Episode 02 · Theory presenter guide

Recording sequence: **29 frames**, approximately **26 minutes**
including pauses. Timing is a rehearsal estimate, not a promised video length.
The sources frame can be held silently as an end card.

Open [the theory canvas](episode_02_trigrams.excalidraw) in Excalidraw. Select a
frame and use Shift+2 to zoom to it; advance left to right. For annotations,
save a copy named `episode_02_trigrams.RECORDING.excalidraw` before drawing.

[The offline theory reader](episode_02_theory.html) follows the same sequence.
Speaker notes are hidden by default. “Speaker notes” reveals narration for
rehearsal; “Present” hides controls and notes. Arrow keys advance; Escape exits
presentation mode. The reader is an SVG approximation; Excalidraw supplies the
original editable rendering. The old `episode_02_study.html` link opens this
same updated presentation.

## Audience release copies

[Theory companion guide (PDF)](../docs/episode-02-theory.pdf) ·
[Canvas PDF: all 29 frames](../docs/episode-02-canvas.pdf).
The recorded video is about 43:44; timings below remain rehearsal estimates.

## Recording route

| Frames | Theory section | Purpose |
|---|---|---|
| 01–10 | 1–3 | Context, boundaries, every anna window, counts and normalization |
| 11–15 | 3–4 | Generation, ana failure, missing evidence and smoothing |
| 16–22 | 5 | Evidence splitting beyond trigrams, capacity and sparse storage |
| 23 | 6 | Practical responses and their limits |
| 24–25 | 7 | Shorter histories: backoff and interpolation |
| 26–29 | 8 | Shared representations, recap, coding handoff and references |

The full real-data experiment stays in the coding video: no measured loss curves,
smoothing sweeps, generated batches, or empirical winning context appear here.
Frame 21 contains mathematical capacities only. Keep the phrases “can” and
“may” when discussing generalization; theory does not predict a universal
point at which performance must worsen.

## Three context switches to say out loud

1. Frames 01–16: `anna`, `ava`; four next-token outcomes.
2. Frames 17–18: separate constructed corpus `anna`, `enna`, `inna`, `onna`;
   twenty predictions and six next-token outcomes. The supplied `nnn` query
   is not a claimed generated sample.
3. Frames 19–21: capacity calculations, first with three letters, then 26.
   These are not training datasets or experiment results. Frame 24 explicitly
   returns to the original two-name toy.

Keep the K−1 free-parameter detail in the theory document's appendix. It is
not needed in the spoken path. Frame 25's arithmetic can be shortened aloud;
retain the distinction between fallback and weighted combination.

## Frame-by-frame narration

### 01 · One more character of memory.

Suggested start 00:00 · about 55 seconds

**Say:** Our first model remembered one character. Today we give it two. Both models still predict one next token: trigram means two context tokens plus the target. We will build a tiny table by hand, see what the extra context buys us, and see why the data matters as we keep extending that context.

**Point / cue:** Point to one blue card, then two; keep the green question mark as the same task.

### 02 · Split one row into two questions.

Suggested start 00:55 · about 55 seconds

**Say:** In anna, n is followed once by n and once by a. The bigram merges those observations into one row. The trigram can distinguish an from nn. That is a useful new capability. But notice that each more specific row now has only one observation behind it.

**Point / cue:** Trace the shared n row into the two context rows. Do not say either estimate is a universal rule.

### 03 · Two START pads. One END target.

Suggested start 01:50 · about 45 seconds

**Say:** S means START, and E means END. Two START pads supply the first context. We predict the four letters of anna, then END: five predictions. We reset before ava, which adds four more. Padding does not add prediction targets.

**Point / cue:** Count the five targets after the two pads.

### 04 · Slide the window: anna, step 1 of 5.

Suggested start 02:35 · about 20 seconds

**Say:** Our first context is START, START. The observed next character is a. Add one to that context's a count.

**Point / cue:** Point to the blue window, then the green target, then count plus one.

### 05 · Slide the window: anna, step 2 of 5.

Suggested start 02:55 · about 20 seconds

**Say:** Slide one place. The context is now START, a. The observed target is n. This is a new row.

**Point / cue:** Move attention one card to the right.

### 06 · Slide the window: anna, step 3 of 5.

Suggested start 03:15 · about 20 seconds

**Say:** Now a, n predicts the next n. This is the observation that will matter when we later try to score ana.

**Point / cue:** Emphasize that the target is the second n.

### 07 · Slide the window: anna, step 4 of 5.

Suggested start 03:35 · about 20 seconds

**Say:** Now n, n is followed by a. The trigram keeps this evidence separate from the preceding a, n row.

**Point / cue:** Contrast the blue pair with the preceding frame.

### 08 · Slide the window: anna, step 5 of 5.

Suggested start 03:55 · about 20 seconds

**Say:** Finally n, a is followed by END. We count that target and stop; we do not produce a new training window after END.

**Point / cue:** Point to E, then pause before moving to the combined table.

### 09 · Add ava. Combine identical observations.

Suggested start 04:15 · about 70 seconds

**Say:** Ava adds four windows. The initial START, START to a observation repeats, so that cell becomes two. START, a gains a v alongside its n. The a, v and v, a rows are new. Seven context rows now hold all nine observations. Read each cell as a count, not yet a probability.

**Point / cue:** Read the S,a row aloud, then check the total count is nine.

### 10 · Divide each row by its own total.

Suggested start 05:25 · about 55 seconds

**Say:** Normalize within each row. START, a has two observations, one n and one v, giving one-half each. The a, n row has one observation, an n, giving probability one to n. Different rows have different denominators because they represent different groups of evidence.

**Point / cue:** Follow count to row total to fraction.

### 11 · Follow both possible generation paths.

Suggested start 06:20 · about 60 seconds

**Say:** Generation begins at START, START, so a is forced. At START, a, choose n or v with equal probability. Taking n has already written an; the remaining targets are n, a, END. Taking v has written av; the remaining targets are a, END. Each complete name therefore has probability one-half. This particular unsmoothed toy table only generates its training names.

**Point / cue:** Trace both branches. The targets written on each right-hand box come after its branch token.

### 12 · Now ask it to score ana.

Suggested start 07:20 · about 70 seconds

**Say:** Now evaluate the supplied name ana. We follow its real characters, not a sample. The third prediction asks for a after a, n. That row only saw n, so it assigns a zero. Multiplying the path gives zero probability and infinite NLL. The old bigram assigned this name one-sixteenth. The toy shows a possible generalization failure, not that every trigram is worse.

**Point / cue:** Stop at the red third box before multiplying the path.

### 13 · An empty cell is not an unseen row.

Suggested start 08:30 · about 65 seconds

**Say:** Two things can be missing. In a, n, the row exists, but its a cell is zero: zero divided by one is zero. For v, n, the entire row is unseen: zero divided by zero gives no defined distribution. An all-zero row would not sum to one. We need a policy for the missing evidence.

**Point / cue:** Read the two denominators separately. Do not call zero over zero a probability of zero.

### 14 · Smoothing gives every outcome a ticket.

Suggested start 09:35 · about 70 seconds

**Say:** Add-one smoothing adds one pseudo-count to every allowed outcome, not just to zeros. The observed a, n row has one real ticket plus four added tickets; a gets one out of five. The unseen v, n row has only the four added tickets, so it becomes uniform. Pseudo-counts are a modeling convention, not extra training observations.

**Point / cue:** Count the five left tickets and four right tickets. State the original toy has four outcomes.

### 15 · Recompute the whole path after smoothing.

Suggested start 10:45 · about 60 seconds

**Say:** After smoothing, recompute every step. Ana gets three-sixths, times two-sixths, times one-fifth, times two-fifths: one-seventy-fifth. Its average NLL is about 1.079372 nats per prediction, divided by four including END. Smoothing fixes the zero but also redistributes probability away from observed outcomes.

**Point / cue:** Point through all four factors. Read the displayed decimal as approximately.

### 16 · 100% can rest on one observation.

Suggested start 11:45 · about 60 seconds

**Say:** Let's name the evidence issue. The bigram had two matching observations after n. The trigram separates them into two rows with one observation each. Both new rows look completely certain. But one hundred percent from one example says what happened in the sample, not what must happen in the population. Whether the extra distinction is useful depends on the data we want to predict.

**Point / cue:** Contrast the evidence counts before and after splitting.

### 17 · What if we add a third context token?

Suggested start 12:45 · about 80 seconds

**Say:** For this next demonstration, replace the corpus with four constructed strings: anna, enna, inna, onna. Do not mix these counts with the original toy. A two-character context n, n pools four observations, all followed by a. With three context characters, we split that row into ann, enn, inn, and onn, each seen once. The probabilities are still one for a here; nothing became wrong automatically. What decreased is the support for each estimate. The corpus still supplies twenty predictions.

**Point / cue:** Read the new corpus before touching the rows. Call a row with total count one a singleton.

### 18 · A longer query can have no matching row.

Suggested start 14:05 · about 65 seconds

**Say:** Stay with those four strings. Suppose a supplied history ends in nnn, and we ask for the next token. The trigram uses its last two tokens, nn, and has four observations. The 4-gram uses all three, nnn, and has none. This is a local query, not a generated sample. The letters are known; their longer combination is unseen. A more specific question can need a distribution that counting has never estimated.

**Point / cue:** Point to the supplied three tokens, then compare suffix lengths. Do not reuse the original four-outcome smoothing denominator; this corpus has six outcomes.

### 19 · Each extra position multiplies possibilities.

Suggested start 15:10 · about 55 seconds

**Say:** For the counting calculation, use just a, n, v and temporarily ignore boundaries. One position has three choices. For every first letter, the second has three choices, giving nine pairs. A third position multiplies by three again. In general, A choices in each of m positions gives A to the power m. We count possible combinations, not equally likely events.

**Point / cue:** Scan one row of pairs, then all three rows; show the third-position multiplication.

### 20 · Include the valid START contexts.

Suggested start 16:05 · about 65 seconds

**Say:** Now calculate capacity for 26 ordinary letters. Valid two-token contexts are START, START; START plus one letter; or two letters. That is one plus twenty-six plus six hundred seventy-six, or seven hundred three rows. Each row has twenty-seven outcomes, because END is a target and START is not. The full table would contain eighteen thousand nine hundred eighty-one cells.

**Point / cue:** Point to the three valid context families, then multiply rows by outcomes.

### 21 · Possible rows multiply. Data does not.

Suggested start 17:10 · about 60 seconds

**Say:** Increasing context length makes the possible row count grow quickly. These are capacity calculations, not measured experimental results. The training observation count does not grow with the context: each original toy name still supplies its letters plus one END, nine in total. We create more possible groups for the same evidence. Some longer rows may stay well supported; others are singletons or absent.

**Point / cue:** Contrast the growing left column with the fixed nine on the right.

### 22 · Sparse storage saves space, not evidence.

Suggested start 18:10 · about 60 seconds

**Say:** We do not have to allocate every possible cell. Sparse storage keeps only observed counts. Missing entries can act as zero counts in the smoothing formula, calculated when needed. That saves space, but it adds no observations. A model can be small enough to store and still lack evidence for many contexts.

**Point / cue:** Point to the observed blue cells, then distinguish storage from evidence.

### 23 · Three immediate responses, each with a limit.

Suggested start 19:10 · about 80 seconds

**Say:** There are several responses. More representative data can provide more matching examples, though not every long context will be covered. A shorter context pools evidence but may lose useful distinctions. Smoothing prevents zeros for known outcomes but cannot discover a preference in an empty row. These are tools with different tradeoffs. We use held-out validation to choose settings; we do not assume any one choice always wins.

**Point / cue:** Read the benefit and limitation of each column together.

### 24 · Backoff: consult a shorter history.

Suggested start 20:30 · about 80 seconds

**Say:** Return to anna and ava. The unseen v, n context has a suffix we do know: n. A simple rule is to use an observed trigram row, otherwise use the bigram for its last token, with a normalized further fallback if necessary. Here that gives half to n and half to a. This whole-row fallback is only an introductory example. It still leaves zero probabilities: in a known a, n row, a remains zero. Formal backoff smoothing has more careful probability allocation.

**Point / cue:** Trace v,n to n. Say explicitly that missing-row fallback does not fix every missing target.

### 25 · Interpolation: let both histories contribute.

Suggested start 21:50 · about 65 seconds

**Say:** Interpolation combines the rows instead of choosing only one. Both toy models here use add-one smoothing. For a after a, n, the trigram gives one-fifth and the bigram gives one-third. Equal weights give four-fifteenths. The full mixture remains normalized because its component distributions are normalized and its weights sum to one. This helps this one continuation; it is not proof that the whole model has a better score. One-half is just our teaching weight.

**Point / cue:** Read the two component probabilities; optionally omit the arithmetic aloud and emphasize combining evidence.

### 26 · Learn to share information across contexts.

Suggested start 22:55 · about 60 seconds

**Say:** Later we will learn shared representations so that related contexts can inform one another through shared parameters. Episode 03 first learns a familiar bigram table with weights and softmax; it introduces parameter learning, not the full sparsity solution. Embeddings and the MLP arrive in Episode 07. They also need suitable data and training. We are building toward our small decoder-only Transformer step by step.

**Point / cue:** Follow the series progression; do not skip the coding companion in the next frame's handoff.

### 27 · The tradeoff is context versus evidence.

Suggested start 23:55 · about 60 seconds

**Say:** The tradeoff is not that more context is bad. More context distinguishes situations, but each more specific row can use only a subset of the observations available to its suffix. That can expose useful patterns or leave unreliable estimates and missing rows. We can gather evidence, pool it, smooth, or share information. A model's apparent certainty needs to be read alongside the evidence behind it.

**Point / cue:** Summarize one benefit, one risk, and one response.

### 28 · Next: build it and test the tradeoff.

Suggested start 24:55 · about 50 seconds

**Say:** In the coding companion, we will implement these models on the larger names dataset. We will compare training and held-out loss and inspect rare and unseen contexts. Does more context help, and when does it stop helping for those choices? We will measure that rather than build the conclusion into the experiment. Theory explains a mechanism; the experiment tests its practical consequences.

**Point / cue:** Finish on the question. Do not disclose the measured best context or curve here.

### 29 · The foundations behind this episode.

Suggested start 25:45 · about 15 seconds

**Say:** The methods come from established n-gram literature and neural language-model research. The examples and presentation sequence are ours. Full references are in the companion theory document.

**Point / cue:** Use as an end card; do not read URLs aloud.

## Evidence and correctness

All hand-worked examples and capacities are checked by
`episodes/02_trigrams/test_lesson_material.py`; the original lab tests remain in
place. See [the correctness review](../EPISODE_02_REVIEW.md) for verification
and limits. No new real-data experiment is required for this theory revision.

Primary and authoritative references: [Jurafsky and Martin, Chapter 3](https://web.stanford.edu/~jurafsky/slp3/3.pdf),
[Chen and Goodman (1996)](https://aclanthology.org/P96-1041/), and
[Bengio et al. (2003)](https://jmlr.org/papers/v3/bengio03a.html).
See [the theory reference](../EPISODE_02_THEORY.md) for equations and source scope.

## Regenerate

From the repository root, run `python3 canvas/build_episode_02.py`.
This overwrites the generated canvas, reader, and this presenter guide. Edit
narration and scene content in the builder before regenerating; keep recording
annotations in a separate copy.
