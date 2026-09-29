# Episode 03A · Presenter guide

20 frames · 2106 scripted words · 32 minutes of rehearsal allocations including pointing, arithmetic and pauses.
These are preparation timings, not final chapters or a runtime cap. Expand the worked
steps naturally; do not rush the softmax motivation or the four-target loss.

Read [the theory](../../EPISODE_03_THEORY.md) first. Open
[the presentation](../../canvas/episode_03_theory.html) for rehearsal.
Arrow keys move between frames; Speaker notes reveals this script; Present
hides controls and notes; Escape restores controls. Save an annotation copy
of the Excalidraw canvas before drawing on it.

## Recording blocks

1. Frames 1–6: task, count-versus-weight workflow, initial table, lookup and softmax motivation.
2. Frames 7–11: all-row softmax, every target in both names, and the overall average.
3. Frames 12–16: chosen ln 2 improvement, ln 100 overshoot, update loop and numerical stability.
4. Frames 17–20: model limits, generation, understanding checks and the next lesson.

Frames 4–11 evaluate the all-zero initial weights; no update occurs during that
walkthrough. Frames 12–13 are hand-set adjustments, not optimizer output.
Every reported full training NLL uses the same 9 targets from anna/ava, including
END. The gradient rule for choosing updates remains Episode 04.

One-hot notation, matrix multiplication, and constructing weights from smoothed
counts are in [optional notes](OPTIONAL_MATH.md), outside the main recording route.

## 01 · From counting to adjustable weights

Rehearsal start 0:00 · 65 seconds

Last time, we saw that longer count-based contexts can leave us with less evidence for each exact situation. Backoff and interpolation remain useful ways to reuse evidence; we did not rule them out. Our next route is toward models that learn shared patterns. To understand those models, we first need adjustable weights and a way to measure their predictions. Today we keep the familiar character bigram task and replace count rows with score rows. We will turn those scores into probabilities and see whether a chosen change improves the loss. This weight table does not yet share learned patterns across different inputs. That comes later. Today we are learning the pieces we will need.

**Visual cue:** Briefly reconnect to the bridge without reteaching sparsity. Point to the middle box as today’s scope and the right box as a later step.

**Basis:** Bridge learning notes and SERIES_PLAN.md; the add-k experiment does not rule out backoff or interpolation.

## 02 · Keep the training examples

Rehearsal start 1:05 · 80 seconds

Nothing about the data changes. Anna gives us five predictions: its four characters and END. Ava gives us four. Write the start transition for each name separately. There is no transition connecting the two names. Our current input can be START, a, n or v. Our next output can be a, n, v or END. These are two ordered lists. They have the same length here, but START and END have different jobs.

**Visual cue:** Count five targets, then four. Point to the input and output lists separately.

**Basis:** Project example; see EPISODE_03_THEORY.md.

## 03 · Two ways to fit the same bigram task

Rehearsal start 2:25 · 130 seconds

Both approaches begin with the same training transitions. On the left, count what followed each input, optionally smooth the counts, and normalize each row. That directly gives a fitted count model. On the right, initialize adjustable scores, look up the input row, apply softmax, and measure the observed targets using NLL. A training method then updates weights from training loss and repeats. Today we inspect the initial model and try two changes by hand; Episode Four supplies the gradient rule. Validation remains separate: it chooses k for our count experiment and can choose training settings or checkpoints for the weight model. Test data stays for final evaluation. We are not claiming the weight model is automatically better.

**Visual cue:** Trace each column top to bottom. The right-hand feedback loop updates weights, not the training data.

**Basis:** Project worked example; authoritative references in EPISODE_03_THEORY.md.

## 04 · Start with all weights at zero

Rehearsal start 4:35 · 80 seconds

This is our initial weight table. Every entry is zero. The rows identify the current input: START, a, n or v. The columns identify possible next tokens: a, n, v or END. A weight is a stored adjustable number. When we read a row for a prediction, those output scores are called logits. We only need the term once: logits means scores before softmax. Zero initialization is a transparent choice for this independent-row model, not a rule for all neural networks.

**Visual cue:** Read the input and output labels. Distinguish zero scores from zero probabilities.

**Basis:** Project example; see EPISODE_03_THEORY.md.

## 05 · Each input has its own score row

Rehearsal start 5:55 · 90 seconds

We do not need to pick a as the first training input. Each possible input already has its own score row. We can apply softmax to all four rows independently, producing four probability distributions. Then each training transition tells us which row to read and which actual target probability to score. Anna starts with START followed by a, so that observation uses the START row and the a column. Some rows are used more often than others: START twice, a four times, n twice and v once across our two names. That gives nine predictions, not four row losses. Computing softmax after looking up each input row would give the same predictions; for this walkthrough we normalize the whole table row by row first.

**Visual cue:** Point to the four input labels on the previous frame. Preview START followed by a as the first scored transition; every repeated transition counts.

**Basis:** Episode 03 theory reference and linked softmax-regression sources.

## 06 · Softmax: scores into probabilities

Rehearsal start 7:25 · 160 seconds

Our old counts were nonnegative and an observed row had a positive total, so dividing by that total worked. Scores have no such restriction. Our all-zero starting row would give zero divided by zero. Negative scores could also produce invalid negative probabilities. We need a rule that accepts any finite real scores, gives a normalized distribution, and favors larger scores. Softmax first applies the exponential, then divides by the total. The exponential is positive even for negative scores, and increases smoothly as the score grows. That smooth response will be useful when we learn gradients. This is a useful standard choice, not the only possible probability rule. Softmax names the whole two-step transformation; it does not change weights or sample a token. The graph shows one slice of softmax, not a single universal graph of this multi-input function. Keep the a, n and v scores at zero and vary only END’s score. END’s probability is exponential of its score divided by three plus that exponential. It forms an S-shaped curve: near zero probability for very low scores, a steeper middle, and flattening toward one for very high scores. At score zero all four outcomes have one quarter probability. At natural log three END has half the probability, because its exponential amount three matches the other three ones combined. For finite scores the probability never reaches exactly zero or one mathematically. The three other probabilities decrease as END increases so the row keeps summing to one. The smooth response makes gradients possible later; it does not guarantee useful predictions. Softmax does not train the weights or sample a token.

**Visual cue:** Read the motivation and two steps on the left, then trace the curve from low to high. Explicitly hold the other three scores at zero. At END score zero all four probabilities are 25%; 50% occurs at ln 3, not zero.

**Basis:** Episode 03 theory reference and linked softmax-regression sources.

## 07 · Apply softmax independently to every row

Rehearsal start 10:05 · 110 seconds

Exponential zero equals one. We must be able to predict from START, a, n and v. Every row currently contains four zeros. For each row independently, exponentiate to four ones, obtain a row total of four, then divide by four. We now have a complete probability table: every entry is one quarter. There are four distributions, each summing to one. The whole matrix is not one distribution. Code can compute these operations in a batch, but the normalization remains separate for each row.

**Visual cue:** Read all four rows across, including each row’s own denominator.

**Basis:** Project worked example; authoritative references in EPISODE_03_THEORY.md.

## 08 · How do we score one prediction?

Rehearsal start 11:55 · 110 seconds

We need a number that rewards assigning higher probability to what actually happened. The negative natural log gives us the same loss as Episode One. For START followed by a, read the a probability in the START row: one quarter. Natural log one quarter is negative one point three eight six; the minus sign makes loss positive one point three eight six. Since every row is uniform, all nine targets will have this same loss. We will show each one. For a whole name, sequence probabilities multiply, so their negative logs add. To report a per-prediction average, divide by the number of targets, including END.

**Visual cue:** First select the target probability, then apply the loss rule. Distinguish one target from a whole name.

**Basis:** Project worked example; authoritative references in EPISODE_03_THEORY.md.

## 09 · Score every transition in anna

Rehearsal start 13:45 · 110 seconds

Now score anna using the actual preceding character at every position. Read each row and select the actual next token. All selected probabilities are one quarter in this initial model, so each contributes negative log one quarter, or log four. There are 5 targets including END. Add the losses to get 5 times log four for this name. We have evaluated the weights, not updated them. The model does not sample its own history while evaluating this supplied name.

**Visual cue:** Trace every line and count the END target. Do not skip repeated transitions: each is a separate observation.

**Basis:** Project worked example; authoritative references in EPISODE_03_THEORY.md.

## 10 · Score every transition in ava

Rehearsal start 15:35 · 110 seconds

Now score ava using the actual preceding character at every position. Read each row and select the actual next token. All selected probabilities are one quarter in this initial model, so each contributes negative log one quarter, or log four. There are 4 targets including END. Add the losses to get 4 times log four for this name. We have evaluated the weights, not updated them. The model does not sample its own history while evaluating this supplied name.

**Visual cue:** Trace every line and count the END target. Do not skip repeated transitions: each is a separate observation.

**Basis:** Project worked example; authoritative references in EPISODE_03_THEORY.md.

## 11 · Combine all nine prediction losses

Rehearsal start 17:25 · 120 seconds

Anna contributes five losses and ava contributes four. Add all nine, then divide by nine. Anna has total five times log four; ava has total four times log four. Together the total is nine times log four, about twelve point four seven seven nats. Dividing by nine gives log four, about one point three eight six two nine four nats per prediction. It equals the individual loss only because every target had the same probability here. In general the losses differ. We do not average the two name totals, and we do not give equal weight to per-name averages of unequal-length names. This completes evaluation of the starting model.

**Visual cue:** Follow the five-plus-four count through numerator and denominator. No weight update has occurred.

**Basis:** Project worked example; authoritative references in EPISODE_03_THEORY.md.

## 12 · Suppose we try one weight change

Rehearsal start 19:25 · 110 seconds

Suppose we try natural log two for the a-to-END weight. We picked it so exponential natural log two equals two. The a row is now zero, zero, zero, log two; softmax gives one fifth, one fifth, one fifth and two fifths. We do not need to repeat all nine predictions. The five predictions with other input rows are unchanged. The four targets after a are n, END, v, END. Scoring all nine with the same rule lowers average training NLL from one point three eight six two nine four to one point three three one four three seven. This is a measured result of a hand-set change, not a claim we already know how to train automatically.

**Visual cue:** Highlight only the a-to-END weight. Show the changed row and compare the two full-data losses.

**Basis:** Project worked example; authoritative references in EPISODE_03_THEORY.md.

## 13 · Push too far: one success, overall failure

Rehearsal start 21:15 · 110 seconds

Let us make END much more likely: use natural log one hundred. The row becomes one, one, one, one hundred divided by one hundred and three. END now has about ninety-seven percent probability and a tiny loss. That looks impressive if we show only END. But n and v each get less than one percent and a loss over four point six. Averaged over all nine training targets, the loss rises to one point eight zero seven. A change can help one observation while making the full model worse. We need a method that considers the objective we actually care about.

**Visual cue:** Start with the good END score, then reveal n/v cost and total failure. Pause on the red panel.

**Basis:** Project example; see EPISODE_03_THEORY.md.

## 14 · What did we actually do?

Rehearsal start 23:05 · 70 seconds

Separate these steps. First choose weights and compute predictions. Second, use observed targets to calculate the loss. Third, change a weight and repeat. We just performed that loop by choosing the changes ourselves. Neither softmax nor cross-entropy updates a parameter on its own. They give us a prediction and a number to evaluate. The missing piece is a systematic way to decide which change to try. That is the motivation for the gradient lesson, not a mysterious step we hide inside today’s model.

**Visual cue:** Ask which step softmax performs, and which step is still hand-directed.

**Basis:** Project example; see EPISODE_03_THEORY.md.

## 15 · Only score differences matter

Rehearsal start 24:15 · 80 seconds

Compare our chosen row with the same row plus one thousand. Every exponential gets multiplied by exponential one thousand, and that common factor cancels in the ratio. The probabilities stay the same. This also means the absolute value of a logit is not its probability. But multiplying every score by two is different: the final exponential becomes four instead of two, so the distribution changes. Addition and multiplication do different things here.

**Visual cue:** Show the common factor cancellation on an annotation copy. Distinguish shift from scale.

**Basis:** Project example; see EPISODE_03_THEORY.md.

## 16 · Make the calculation stable

Rehearsal start 25:35 · 100 seconds

The previous frame shifted all scores by a thousand without changing their probabilities mathematically. But exponential one thousand is too big for ordinary computer arithmetic. We can prevent that overflow by subtracting the largest score before exponentiating. A common shift preserves the probabilities. For our original a row, subtract natural log two to get negative log two three times and zero. Their exponentials are one half, one half, one half and one. Divide by their total, two and a half, to recover one fifth, one fifth, one fifth and two fifths. The maximum shifted score is zero, so no exponential exceeds one. Very tiny amounts can still underflow; computing log probabilities directly is an implementation detail in the reference and coding companion.

**Visual cue:** Point back to common-shift invariance. Read the last row as positive amounts, not probabilities yet.

**Basis:** Episode 03 theory reference and linked softmax-regression sources.

## 17 · What has not changed yet?

Rehearsal start 27:15 · 85 seconds

We changed how the model produces probabilities, but it still sees only one character. The first and last a in anna select the same row. Updating that row does not change predictions after n or v. There is no learned relationship between different input characters yet. The point of this lesson is to understand adjustable scores and measure their predictions, not to claim better generalization or solve sparse context. Later we will build richer models that share structure. The exact distinction between finite softmax probabilities and unsmoothed zeros is an optional reference detail, not needed for today’s main route.

**Visual cue:** Return to the two a occurrences in anna and point out that both use the same row.

**Basis:** Project example; see EPISODE_03_THEORY.md.

## 18 · Generation uses the same loop

Rehearsal start 28:40 · 75 seconds

Generation starts at START. Select its row and compute probabilities, then sample a token. END means stop. Otherwise append the character and use it as the next input. Repeat. During loss evaluation, the data supplies the correct previous character at every step. During generation, our sample supplies it. Those are different ways of feeding the same prediction rule. A length cap is still just a safety cap, not a predicted END. With finite scores, START can also assign positive probability to END immediately, so an empty result is possible.

**Visual cue:** Trace the feedback arrow in words, and contrast it with the fixed training pairs.

**Basis:** Project example; see EPISODE_03_THEORY.md.

## 19 · Check your understanding

Rehearsal start 29:55 · 90 seconds

Try three questions. If the input is n, which weight row gets used? If every selected score is zero, what distribution do we get? And if increasing the END score helps an END example, must it improve the whole training loss? Pause and explain your answers. For input n, we look up the n row. Four zero scores give four equal probabilities. And no: our overshoot example damaged the other observed targets enough to increase the total loss. If those answers make sense, we have the forward computation and the objective in place.

**Visual cue:** Pause after each question; answers are in these notes, not on the audience slide.

**Basis:** Project example; see EPISODE_03_THEORY.md.

## 20 · Next: how should a weight change?

Rehearsal start 31:25 · 65 seconds

We can now start with a character, look up its scores, turn them into probabilities, and score the target using the same loss as before. We also saw that a larger weight is not automatically a better model. Next we will study how a small change in a number changes the loss, using derivatives and then gradients. We fully evaluated the initial weights and measured two chosen changes. The theory reference includes our arithmetic, limitations and authoritative sources. The coding companion will let us inspect the same operations with NumPy before the later lessons automate the training machinery.

**Visual cue:** Close with the question, not a claim of a newly trained superior model.

**Basis:** Reading links in EPISODE_03_THEORY.md; project curriculum in SERIES_PLAN.md.

## Rehearsal checkpoints

Can you select the a row without saying “the computer understands a”? Can you
explain why zero logits are uniform? Can you score n as well as END after the
same input a? Can you distinguish a hand-set weight from one fitted by an
optimizer? Use the [exercises](EXERCISES.md) and [answers](ANSWERS.md).

The theory reference contains sources and optional details on row-optimum
limits, independent parameters, batches, and the exact held-out ana path.
The canvas is the spoken route, not the whole reference.
