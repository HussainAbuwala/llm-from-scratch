# Episode 03B · Recording walkthrough

Historical rehearsal plan. The finished recording skips the optional real-data
extension and generation walkthrough; see the release metadata for its chapters.

Target 25–35 minutes, adjusted after rehearsal. Use the executed notebook as a
reference, then restart the kernel and clear outputs in a recording copy.
Record sections 1–8 and 10 as the core route; section 9 is an optional extension.
Keep the theory's existing PRESENTER_GUIDE.md for 03A.

## Opening · 1 minute

“In the theory video, we turned scores into probabilities and measured two
chosen changes. Today we will build that exact path in NumPy. By the end we can
score and sample from the model. Next episode we learn how to choose updates.”

## Block 1 · Addresses and predictions · 6 minutes

Sections 1–3. Introduce arrays as tables. Point to a's two different IDs.
Trace START→a and a→END. Count five predictions for anna and four for ava.
Show W's (4,4) shape and gathered scores' (9,4) shape. Repeated a inputs select
the same parameter row; gathering does not create nine independent sets of weights.
Pause check: “Which axis lists possible next tokens?”

## Block 2 · Probabilities and loss · 8 minutes

Sections 4–6. Explain subtraction, exponentiation, row sums, then broadcasting.
Do not start with one-hot encoding or matrix multiplication. Show the target
index arrays selecting nine cells. Read one loss, total them, divide by nine.
Then demonstrate the underflowed probability and finite log-softmax loss of 2000.
Pause check: “Why not average the two names' average losses equally?”

## Block 3 · Chosen changes and generation · 8 minutes

Sections 7–8. Ask for a prediction before revealing log(100). Compare the whole
loss, not just the END column. Say explicitly that no optimizer ran. Trace the
sampling loop, including output-token-to-input-row translation, empty samples,
and the difference between END and CAP. Display all samples without selecting favorites.
Pause check: “During scoring, who supplies the previous character? During sampling?”

## Optional block · Real names · 5–7 minutes

Section 9. Reuse the earlier dataset and split. Explain np.add.at as accumulating
repeated table addresses. State that log(C+1) constructs the existing add-one
model in score space. Show the matching validation losses and denominator.
This demonstrates equivalence, not a quality gain or a new training algorithm.
Skip this block if the core lesson needs more room; no later cell depends on it.

## Closing · 1 minute

“We now have adjustable numbers, a prediction rule, a loss, and a sampler.
A bigger weight was not always better. Episode 04 asks how a small change affects
the loss, and uses derivatives to choose a direction.”

Before recording: run all tests and the notebook in a fresh kernel, rehearse
the index explanation, enlarge the editor font, and keep expected losses nearby.
Chapters and upload metadata should follow the actual recording timeline.

## NumPy presentation cues

Show x and y before W[x]. Compare the printed (4,4) stored table with the
(9,4) gathered rows. Explain that array-of-indices lookup is NumPy behavior.
In section 4, follow row maxima → shifted scores → exponentials → row totals
→ probabilities. Use the optional two-row example to make broadcasting visible
when all-zero rows obscure it. In section 5, read the two index arrays together
and point to one selected cell before showing all nine selected probabilities.
These extra inspection outputs can extend the original rehearsal estimate.
