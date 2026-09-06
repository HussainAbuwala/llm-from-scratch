# Episode 1 — presenter guide

Open `episode_01_presenter.excalidraw` for the theory recording. The older
`episode_01_bigram.excalidraw` remains the detailed reference canvas.

This canvas contains staged reveal frames, not one new subject per frame.
The ten count frames and five generation frames are continuous demonstrations.
Advance as you explain each step; do not spend a minute on every frame.

## Recording

- Use the frame names in numerical order. Select a frame and zoom to selection
  (Shift+2 in the current setup). Cut navigation between frames from the recording.
- All calculations are already staged. You can present without drawing or editing
  objects live. Optional circles or underlines are enough; do not read every label.
- Work from a duplicate if adding annotations. The generator overwrites this
  presenter canvas and these notes when rerun.
- The region x=1240–1600, y=650–900 is clear in every frame for a small face bubble.
  Keep the bubble entirely inside that region, or hide it for full-screen diagrams.
- Important content uses 30–94 px text; chapter/footer labels use 24–28 px.
  Record a short sample and check actual phone playback before the full session.
- Rehearse once with these notes on a separate screen. Timings are guidance;
  pause for viewer predictions and speak the fractions slowly.
- Mathematical examples are deliberate worked paths. Do not call them random
  recorded runs or a representative test benchmark.

## Teaching conventions

Tokens are characters plus START and END. START is a context only; END is an
outcome only. The compact table has row labels [START,a,n,v] and column labels
[a,n,v,END]. Numeric indexing belongs in the coding video, with separate maps
if using this compact table. START→END remains an allowed outcome; smoothing
can therefore generate an empty name. Mention that if it appears in code.

The shown NLL averages predictions including END. The `ana` path is held out
from counts but hand-selected for explanation. Add-one comparisons smooth every
row. Tune k on validation data; final test data does not choose k.

The following build video should first reproduce this exact toy example, then
use the larger dataset. Chapter 2 is trigrams; Chapter 3 is learned bigram weights.

## Sources

- Jurafsky and Martin, n-gram language models:
  https://web.stanford.edu/~jurafsky/slp3/3.pdf
- Karpathy, makemore (educational reference):
  https://github.com/karpathy/makemore

## Frame cues

### 01 · Two names. A new possibility.

Approximate start: 00:00 · 60 seconds

These are the only two names our model has seen: anna and ava. This tiny table can produce ana. It can also produce this awkward string. Today we build the table, follow its choices, and calculate how well it predicts.

**Present:** Point to the training names, then ana, then the awkward example. These are possible paths, not claimed recorded program outputs.

### 02 · Predict chances. Then choose.

Approximate start: 01:00 · 70 seconds

Our model assigns a probability to each possible next token. A separate rule chooses one. Today a token is one character, plus special boundary tokens. This is not yet a neural network or a modern LLM.

**Present:** Trace context → probabilities → choice. The numbers are a preview; counting will explain them.

### 03 · Give each name a beginning and an end.

Approximate start: 02:10 · 90 seconds

We split anna into character tokens. START selects the first-character distribution. END is a target: the model must learn when to stop. Our ordinary vocabulary is a, n, v; allowed predictions are a, n, v, END. START is only a context here.

**Present:** Point to both boundaries. Explain START and END are each one special token.

### 04 · Turn adjacent pairs into counts.

Approximate start: 03:40 · 55 seconds

Each training pair has a current token and the next token we observed. Bigram means two tokens in the pair, but only one token of context. Rows are current tokens; columns are next tokens.

**Present:** Explain the empty matrix before advancing.

### 05 · Count 1 of 9:  START → a

Approximate start: 04:35 · 18 seconds

In anna, a follows START. Add one to row START, column a. The count is now 1.

**Present:** The next frame advances the window and updates one cell. Pause before revealing the final a→END count.

### 06 · Count 2 of 9:  a → n

Approximate start: 04:53 · 18 seconds

In anna, n follows a. Add one to row a, column n. The count is now 1.

**Present:** The next frame advances the window and updates one cell. Pause before revealing the final a→END count.

### 07 · Count 3 of 9:  n → n

Approximate start: 05:11 · 18 seconds

In anna, n follows n. Add one to row n, column n. The count is now 1.

**Present:** The next frame advances the window and updates one cell. Pause before revealing the final a→END count.

### 08 · Count 4 of 9:  n → a

Approximate start: 05:29 · 18 seconds

In anna, a follows n. Add one to row n, column a. The count is now 1.

**Present:** The next frame advances the window and updates one cell. Pause before revealing the final a→END count.

### 09 · Count 5 of 9:  a → END

Approximate start: 05:47 · 18 seconds

In anna, END follows a. Add one to row a, column END. The count is now 1.

**Present:** The next frame advances the window and updates one cell. Pause before revealing the final a→END count.

### 10 · Count 6 of 9:  START → a

Approximate start: 06:05 · 18 seconds

In ava, a follows START. Add one to row START, column a. The count is now 2.

**Present:** The next frame advances the window and updates one cell. Pause before revealing the final a→END count.

### 11 · Count 7 of 9:  a → v

Approximate start: 06:23 · 18 seconds

In ava, v follows a. Add one to row a, column v. The count is now 1.

**Present:** The next frame advances the window and updates one cell. Pause before revealing the final a→END count.

### 12 · Count 8 of 9:  v → a

Approximate start: 06:41 · 18 seconds

In ava, a follows v. Add one to row v, column a. The count is now 1.

**Present:** The next frame advances the window and updates one cell. Pause before revealing the final a→END count.

### 13 · Count 9 of 9:  a → END

Approximate start: 06:59 · 18 seconds

In ava, END follows a. Add one to row a, column END. The count is now 2.

**Present:** The next frame advances the window and updates one cell. Pause before revealing the final a→END count.

### 14 · What followed a?

Approximate start: 07:17 · 60 seconds

Across the two names, a has four outgoing observations. One n, one v, two ENDs. Ask how often a ended a name before revealing the probabilities.

**Present:** Count all four tickets. The two END tickets are two observations of the same outcome.

### 15 · Divide by the row total.

Approximate start: 08:17 · 80 seconds

Each probability is its count divided by four. A zero, one quarter, one quarter, and one half. They sum to one. Normalization preserves the proportions.

**Present:** Trace counts to fractions to probabilities. Read the denominator out loud.

### 16 · Training is finished.

Approximate start: 09:37 · 55 seconds

Do the same normalization for every row. This probability table, its token labels, and the boundary rules are the finished model. Counting and normalization fitted it; there is no hidden neural network.

**Present:** Read one entry from the n row so the later generation step is familiar.

### 17 · Begin at START.

Approximate start: 10:32 · 35 seconds

We will follow one possible sampling path. Sampling means drawing according to the probabilities: imagine the four tickets from the a row, selecting one at random, then replacing it before the next draw. It is selected for explanation; the path is not predetermined by the table.

**Present:** Advance once per choice; the table stays fixed. At a, explain that END is more likely but n remains possible.

### 18 · Choose a from the START row.

Approximate start: 11:07 · 35 seconds

Look up START. Select a with probability 1.00. The selected token becomes the next current token.

**Present:** Advance once per choice; the table stays fixed. At a, explain that END is more likely but n remains possible.

### 19 · Choose n from the a row.

Approximate start: 11:42 · 35 seconds

Look up a. Select n with probability 0.25. The selected token becomes the next current token.

**Present:** Advance once per choice; the table stays fixed. At a, explain that END is more likely but n remains possible.

### 20 · Choose a from the n row.

Approximate start: 12:17 · 35 seconds

Look up n. Select a with probability 0.50. The selected token becomes the next current token.

**Present:** Advance once per choice; the table stays fixed. At a, explain that END is more likely but n remains possible.

### 21 · Choose END from the a row.

Approximate start: 12:52 · 35 seconds

Look up a. Select END with probability 0.50. END stops generation; the printed name is ana.

**Present:** Advance once per choice; the table stays fixed. At a, explain that END is more likely but n remains possible.

### 22 · Greedy takes the largest probability.

Approximate start: 13:27 · 70 seconds

From START we get a. At a, END has probability one half, the largest. Greedy therefore produces a. Sampling can take the quarter-probability branch to n. Neither rule retrains the model. Code will use a maximum-length guard and mark truncation.

**Present:** Ask what greedy chooses after a before pointing at END.

### 23 · A nice sample is not a score.

Approximate start: 14:37 · 50 seconds

A single nice output can be cherry-picked. We need to measure probabilities on text that did not contribute to training. Ana is a preselected worked evaluation example, not a benchmark proving quality.

**Present:** Pause at the question before advancing.

### 24 · This time, the text supplies the targets.

Approximate start: 15:27 · 80 seconds

Training used anna and ava. We score the separate example ana. We do not sample here. At each position, look up the probability of the actual next token, using the actual preceding token. This is four predictions including END.

**Present:** Point to training versus held-out labels, then read all four probabilities.

### 25 · Every step must happen.

Approximate start: 16:47 · 65 seconds

The whole sequence requires all four conditional choices, so we multiply. This is the chain rule of probability with our one-token context assumption. We are not assuming the successive characters are independent.

**Present:** Point to each arrow and read its probability.

### 26 · A one-in-sixteen path.

Approximate start: 17:52 · 55 seconds

If we independently sample many times, this exact complete name occurs with probability one sixteenth. Out of sixteen attempts, the expected number is one, not a guarantee of exactly one. Each factor keeps a fraction of the remaining matching paths.

**Present:** Walk through expected matching counts from left to right.

### 27 · Long products become tiny.

Approximate start: 18:47 · 45 seconds

A thousand factors of one tenth gives ten to the minus one thousand. Ordinary floating-point arithmetic cannot store that tiny result. We need to accumulate evidence without multiplying it into zero.

**Present:** Let the exponent land; introduce the next frame as a tool for this problem.

### 28 · A logarithm asks for the exponent.

Approximate start: 19:32 · 85 seconds

Ten cubed is one thousand, so log base ten of one thousand is three. We use natural log, ln, with base e about 2.718. The useful rule is log of a product equals the sum of the logs. No calculus is needed here.

**Present:** Read the top equation forwards and the second backwards.

### 29 · Turn each probability into a log.

Approximate start: 20:57 · 80 seconds

The logs are zero, minus 1.386, minus 0.693, and minus 0.693. Adding gives minus 2.773 after rounding; this equals the log of one sixteenth. We sum logs directly, rather than forming a tiny product first.

**Present:** Use the same rows throughout. Only the right-hand column changes or the average appears.

### 30 · Negate: unlikely targets cost more.

Approximate start: 22:17 · 65 seconds

For positive probabilities at most one, logs are non-positive. Negating gives a nonnegative penalty. High probability on the actual target gives a small penalty; low probability gives a large penalty.

**Present:** Use the same rows throughout. Only the right-hand column changes or the average appears.

### 31 · Average over all four predictions.

Approximate start: 23:22 · 80 seconds

Add the negative log penalties and divide by four predictions, including END. The result is 0.693 nats per prediction. Nats means we used natural logs. For a dataset, sum all transition penalties and divide by all transitions, not by the number of names.

**Present:** Use the same rows throughout. Only the right-hand column changes or the average appears.

### 32 · Lower than what?

Approximate start: 24:42 · 100 seconds

Uniform gives each of our four allowed outcomes one quarter. Unigram uses overall training target frequencies and ignores the current character: a four, n two, v one, END two, nine in total. The bigram uses context. All three score the same held-out ana with the same vocabulary and END convention. One character of context helped on this example; we need more held-out data to judge generalization.

**Present:** Read the unigram counts before the score. Do not claim these numbers establish real-world quality.

### 33 · Known characters. An unseen pair.

Approximate start: 26:22 · 75 seconds

Here is a constructed stress example: avna. V and n are known characters, but v followed by n never appeared in training. One zero makes the complete path probability zero. As probability approaches zero, negative log loss grows without bound. This is an unseen pair, not an unknown token.

**Present:** Ask what one zero does to the product. Then point to the zero cell.

### 34 · Add one to every allowed outcome.

Approximate start: 27:37 · 70 seconds

Add one pseudo-count to all four allowed outcomes, not just the troublesome n cell. The v row changes from one, zero, zero, zero to two, one, one, one. Total five. Apply this same rule to every row when building the smoothed model.

**Present:** Trace all four columns. The denominator changes because every cell received one.

### 35 · Normalize again. Probability moves.

Approximate start: 28:47 · 70 seconds

Divide by five: point four, point two, point two, point two. The unseen v to n now gets a chance. That chance comes from observed v to a, which falls from one to point four. Smoothing redistributes probability; it cannot add a missing token to the vocabulary.

**Present:** Trace all four columns. The denominator changes because every cell received one.

### 36 · One is a choice. We can add k.

Approximate start: 29:57 · 55 seconds

Instead of adding one, we can add a smaller positive value k to every allowed cell. The denominator increases by four k because there are four outcomes in each row. Zero means the original unsmoothed table. We will compare choices on validation data in the build video.

**Present:** Point to k in the numerator and four k in the denominator. Explain both before reading the expression.

### 37 · A safer guess can score worse.

Approximate start: 30:52 · 75 seconds

The original ana score was point 693. With add one applied to every row, it becomes about 1.040: worse. Meanwhile the previously zero-probability avna path becomes possible. Smoothing is protection against limited evidence, not a guaranteed improvement on every example. In code we will compare smoothing strengths on validation data; the test set is saved for final evaluation.

**Present:** Explicitly say the whole table is smoothed for this comparison.

### 38 · Different histories. The same last character.

Approximate start: 32:07 · 70 seconds

The history could be a, ana, or ava. Each ends in a, so each queries exactly the same row. This model has no way to use how it got there. Giving it more examples does not change its one-character memory.

**Present:** Trace all three histories into the same row.

### 39 · Every pair fits. The whole string can fail.

Approximate start: 33:17 · 65 seconds

Return to the awkward opening example annnava. Every neighboring transition, including boundaries, is supported by the training table. That local support does not ensure a convincing complete name. It has no additional knowledge that the whole sequence should look like a name.

**Present:** Point out the repeated n→n transition and the familiar a→v transition.

### 40 · First, make the code prove it.

Approximate start: 34:22 · 60 seconds

Today we counted, normalized, generated, and scored. Next video: code this exact tiny example and verify the same numbers, then run the pipeline on a larger names dataset. Chapter two tries two-character context. Chapter three changes from counts to weights; richer shared representations come later.

**Present:** End on the concrete coding promise. No new combinatorics lesson here.

Estimated spoken sequence: 35 minutes 22 seconds, before additional pauses.
