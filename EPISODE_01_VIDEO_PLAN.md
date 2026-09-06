# Episode 1 Video Plan: The Smallest Language Model

Status: Detailed development reference

The recorded cut follows
[`canvas/episode_01_presenter.excalidraw`](canvas/episode_01_presenter.excalidraw)
and its presenter guide. This file preserves the longer planning rationale.

Series: Building an LLM From First Principles

Theory source: [EPISODE_01_THEORY.md](EPISODE_01_THEORY.md)

## 1. Episode purpose

Episode 1 is the theory episode. It should give the viewer a complete mental
model of a count-based language model before any implementation appears. The
following episode will code the same concepts on a larger names dataset.

The viewer should leave understanding this loop:

~~~text
text
  ↓
tokens
  ↓
context-target pairs
  ↓
next-token probabilities
  ↓
generation and evaluation
~~~

The worked model is a character-level count-based bigram trained on the tiny
corpus `{anna, ava}`. The held-out word `ana` provides one coherent path through
generation, likelihood, logarithms, NLL, and baselines.

The episode is not trying to make a useful assistant. It is trying to expose
the complete language-modeling framework in a form small enough to see.

## 2. Viewer promise

By the end of the episode, the viewer will:

- Understand a real, minimal language model without a neural network.
- Understand next-token prediction as a probability distribution.
- See how training text becomes transition counts.
- Convert counts into probabilities.
- Generate text using greedy decoding and weighted sampling.
- Evaluate the model on unseen examples using average NLL.
- Understand why smoothing is needed.
- See exactly why a one-character model is limited.
- Be ready to implement the same concepts on a realistic dataset in the next
  episode without expecting the toy values to remain the same.

The emotional promise is:

> You do not need to begin with a Transformer. We can make the central idea of
> language modeling visible with a small table and build upward from there.

## 3. Working title and packaging

### Recommended working title

**The Smallest Language Model, Explained by Hand**

### Alternative titles

- **Before GPT: Build the Smallest Language Model From Scratch**
- **How Language Models Begin: Predicting One Character at a Time**
- **Building an LLM From First Principles — Episode 1**

The first title has the clearest curiosity gap. The series and episode number
can appear in the thumbnail, description, and opening rather than consuming the
front of the title.

### Thumbnail direction

Use a clean composition with:

- Hussain on one side, looking toward the model.
- A tiny probability table or character path on the other.
- Generated text emerging from the table.
- Two to four words, such as **THE SMALLEST LM**.

Do not place equations, code, and a full Transformer diagram in the thumbnail.
The visual idea is “a surprisingly small machine generates text.”

## 4. Audience and assumed knowledge

Primary audience:

- Software engineers curious about LLM internals.
- AI users who want to move beyond API calls.
- Beginners with basic Python knowledge.
- Viewers intimidated by the mathematics of deep learning.

Assume:

- Basic Python syntax
- Basic arithmetic and fractions

Do not assume:

- Probability theory
- Logarithms
- Linear algebra
- PyTorch
- Neural networks
- Machine-learning terminology

Every required mathematical idea should be introduced immediately before it is
used.

## 5. Final artifact shown in the episode

The final artifact is the complete hand-worked model:

1. Training corpus `{anna, ava}`.
2. Vocabulary and integer mappings.
3. Every boundary-aware bigram transition.
4. The complete count matrix and normalized rows.
5. One sampled generation: `START → a → n → a → END`.
6. Held-out evaluation of `ana`, ending at average NLL `0.693`.
7. Uniform and unigram baselines computed on the same example.
8. One coherent unseen transition, `v → n`, repaired with smoothing.
9. The one-character-context failure that motivates later models.

The following coding episode scales this pipeline to a larger names dataset.
Its checks are conceptual and structural: extract the right pairs, normalize
rows, generate by repeated lookup, evaluate held-out targets, and smooth unseen
transitions. It should not reproduce the toy counts or loss values.

## 6. Narrative spine

The episode follows one question:

> What is the smallest machine that can learn patterns from text and generate
> something new?

The story develops through successive discoveries:

1. Show the tiny corpus and several sequences its table can produce.
2. Set the boundary: theory now, realistic implementation in the next video.
3. Define language modeling as next-token probabilities.
4. Reduce tokens to characters and context to one character.
5. Discover that learning can begin with counting.
6. Turn counts into probabilities.
7. Use the table to generate text.
8. Trace one complete generated example, then compare greedy decoding and sampling.
9. Ask how we can objectively judge the model.
10. Use held-out transitions, likelihood, logs, and average NLL.
11. Encounter zero probability and introduce smoothing.
12. Reveal that locally valid transitions can still create nonsense.
13. End with the problem that motivates a more capable model.

This creates a problem-solution chain rather than a list of definitions.

## 7. Proposed runtime and segment plan

Target runtime: approximately 28–33 minutes.

This is a guide rather than a hard timing constraint. Clarity takes priority,
but each section should earn its place by advancing the model.

| Time | Segment | What the viewer sees | Core takeaway |
|---|---|---|---|
| 0:00–1:00 | Cold open and boundary | `{anna, ava}`, possible toy samples, and “theory now; code next” | Every number will be inspectable before the implementation scales up |
| 1:00–3:20 | Language-model output | Current token enters; one probability row emerges | A language model predicts a distribution; choosing is separate |
| 3:20–6:00 | Tokens and boundaries | Character vocabulary, IDs, START and END | Text becomes finite symbols and examples gain learnable boundaries |
| 6:00–9:30 | Bigrams and counts | Sliding window over `anna`, merge with `ava`, then the matrix | Training for this model is counting ordered transitions |
| 9:30–11:30 | Normalize and freeze | `[0,1,1,2] / 4` and the finished model artifacts | Counts become `P(next | current)` |
| 11:30–14:00 | One complete generation | `START → a → n → a → END` with `1,.25,.5,.5` | Generation repeatedly queries the same fixed table |
| 14:00–15:30 | Greedy versus sampling | Greedy produces `a`; sampling can produce `ana` | The selection rule changes behavior, not the model |
| 15:30–17:00 | Lucky or good? | Several possible toy-table outputs | Samples are not objective evaluation |
| 17:00–20:00 | Evaluation and likelihood | Held-out `ana`, the same four probabilities, and the 16-attempt funnel | Held-out text supplies targets; path probabilities multiply |
| 20:00–23:30 | Logs and average NLL | Product becomes a sum; exact average NLL `0.693` | Logs stabilize calculation; NLL measures average surprise |
| 23:30–25:00 | Baselines | Uniform `1.386`, unigram `1.158`, bigram `0.693` | Context helped on the worked example |
| 25:00–27:30 | Zero and smoothing | Unseen `v→n`; `[1,0,0,0] → [2,1,1,1] / 5` | Smoothing replaces impossible with unlikely and redistributes mass |
| 27:30–30:30 | Limitations | Histories collapse; locally valid nonsense; context-table explosion | One-character memory cannot create global structure |
| 30:30–32:00 | Handoff | Larger dataset next, learned weights after that | Coding preserves concepts and invariants, not the toy numbers |

Scene-by-scene visuals are built in
`canvas/episode_01_bigram.excalidraw` (24 frames, numbered to match this order).

## 8. Detailed beat sheet

### Beat 1: Cold open

Show the complete toy corpus and several sequences its probability table can
produce. Do not use a terminal prompt or imply that the coding episode has
already happened.

~~~text
training:  anna, ava
samples:   a, ana, ava, annnava
~~~

Do not claim that every sample is impressive. Include at least one strange
result because failure becomes part of the lesson.

Suggested opening idea:

> Today we are going to understand the smallest honest language model using
> numbers we can verify by hand. In the next video, we will implement the same
> concepts on a larger dataset.

Use this as an intent, not final script wording.

### Beat 2: Personal series premise

On camera, briefly establish:

- LLMs are everywhere, but using them is different from understanding them.
- The series will build upward from the smallest understandable system.
- Hussain is learning deeply, checking the literature, and sharing that journey.
- Each episode will leave behind theory and runnable artifacts.

Keep this under one minute. The viewer clicked for the model, so return quickly
to the build.

### Beat 3: Define the task visually

Show:

~~~text
context: "a"

possible next characters:
n       25%
v       25%
<END>   50%
~~~

Then animate:

~~~text
current character
       ↓
probability distribution
       ↓
chosen next character
       ↓
new current character
~~~

Avoid discussing Transformers at this point. The viewer only needs the
next-token contract.

### Beat 4: Introduce the data and tokenization

Display a handful of dataset rows:

~~~text
anna
ava
~~~

Keep these as the only training examples in every hand calculation. `ana` is
reserved as held-out text. The larger names list belongs to the coding episode.

Zoom into one word and separate it into character cards. Show the vocabulary
mapping only after the character idea is clear.

Explain that line boundaries matter because every line represents an
independent example.

### Beat 5: Build transitions by hand

Use anna and ava as the hand-worked example.

Animate the boundary tokens:

~~~text
<START> a n n a <END>
~~~

Slide a two-token window across the sequence. Add one tally to the matching
matrix cell after each movement.

The most important visual distinction is:

~~~text
a -> n  is not the same as  n -> a
~~~

Only after the viewer understands the manual process should the code loop
appear.

### Beat 6: Reveal the count matrix

Show a small labeled matrix first. Then, if the actual vocabulary is larger,
switch to a heatmap.

Highlight one row:

~~~text
current token = a
~~~

Explain that this row contains every observed answer to:

> What followed a?

### Beat 7: Normalize one row

Use:

~~~text
[0, 1, 1, 2]
~~~

Show the total of four and divide every cell by four.

The four-ticket visual should reinforce the meaning:

~~~text
[n] [v] [END] [END]
~~~

The probability values are the share of tickets belonging to each outcome.

### Beat 8: Name the finished model

Pause before generation and make the artifact explicit:

~~~text
vocabulary + boundary convention + probability table
~~~

This prevents the viewer from waiting for a hidden neural network to appear.

### Beat 9: Generate one complete example

Immediately after declaring the table finished, trace:

~~~text
<START> -> a -> n -> a -> <END>
            1.00  0.25  0.50  0.50
~~~

At every step, point back to the probability row already trained. The sampled
output is `ana`. This is the explicit proof that generation is repeated lookup
and selection rather than a separate mechanism.

### Beat 10: Compare greedy and sampling

From the same table:

~~~text
greedy:    <START> -> a -> <END>              output: a
sampling:  <START> -> a -> n -> a -> <END>    output: ana
~~~

Greedy takes `END` because 0.50 is the maximum in the `a` row. Sampling can
take the 0.25 branch. Neither method changes the trained model.

### Beat 11: Introduce evaluation as a problem

Show one plausible output and ask:

> Is the model good, or did we just get lucky?

Then reveal multiple weaker samples. Explain that a single generated example is
not an objective comparison.

### Beat 12: Use evaluation text as the answer key

Hold out one word that did not create the counts.

Use `ana`. Its characters and transitions are covered by the training
vocabulary, but the complete word was not one of the two training examples.

Convert it into pairs and display the model's probability for the actual target
in each pair.

Keep generation and evaluation visually distinct:

~~~text
generation: no target is supplied
evaluation: the existing text supplies the target
~~~

### Beat 13: Explain multiplication with a funnel

Use the exact 16-attempt funnel:

~~~text
16 × 1.00 × 0.25 × 0.50 × 0.50 = 1
P("ana") = 0.0625
~~~

Describe each multiplication as taking a fraction of the attempts that survived
the previous transition.

### Beat 14: Introduce logs only when needed

First show the practical problem:

~~~text
0.1 × 0.1 × 0.1 × ... thousands of times
~~~

The number becomes too small for ordinary floating-point representation.

Then introduce the definition:

~~~text
10³ = 1000
log base 10 of 1000 = 3
~~~

Use:

~~~text
log(a × b) = log(a) + log(b)
~~~

Finally, introduce negative log-likelihood as a surprise penalty. Avoid
deriving calculus or information theory here.

For the same path:

~~~text
ln(1.00) + ln(0.25) + ln(0.50) + ln(0.50) ≈ -2.77
average NLL = 2.77 / 4 ≈ 0.693
~~~

### Beat 15: Average fairly

Compare two sets with equal per-transition quality but different lengths:

~~~text
100 transitions  -> total NLL 80  -> average 0.8
1000 transitions -> total NLL 800 -> average 0.8
~~~

State that our metric averages across every transition in every evaluation
word. Longer words contribute more transitions.

### Beat 16: Encounter zero and smooth it

Use an unseen transition where both characters are known:

~~~text
v -> n was never observed
P(n | v) = 0
~~~

Show how one zero makes the sequence likelihood zero and log(0) unusable.

Add a pseudo-count to every allowed outcome and normalize again:

~~~text
[1,0,0,0] -> [2,1,1,1]
total = 5
P(next | v) = [0.40,0.20,0.20,0.20]
~~~

Show the tradeoff: unseen transitions gain probability by taking probability
from the observed `v→a` transition.

Mention that unseen characters are a different vocabulary problem.

### Beat 17: Let the model fail honestly

Generate or construct a sequence whose adjacent transitions all exist but whose
whole structure is poor.

Then reveal why:

~~~text
long history ending in a
short history ending in a
            ↓
both use the same P(next | a)
~~~

The model has no way to distinguish those histories.

### Beat 18: Bridge to the next problem

End by expanding the context:

~~~text
one previous character
        ↓
two previous characters
        ↓
many previous tokens
~~~

Then show the combinatorial growth of count tables and ask:

> How can a model use more context without creating a separate table entry for
> every possible history?

Do not fully answer it. That is the reason to continue.

Be precise about the immediate sequence of videos:

1. Next video: implement this count-based model on a larger names dataset and
   verify the same concepts and invariants.
2. After that: replace counting with learned weights to address the structural
   limitations exposed here.

The coding episode should not reproduce the toy values; it should reproduce the
logic.

## 9. On-camera, screen, and visual balance

### On camera

Use Hussain's face for:

- Cold-open reaction or framing
- Personal motivation
- Major conceptual transitions
- Honest reactions to generated failures
- Recap and next-episode bridge

Target roughly 20–30% of the episode as visible A-roll. The exact amount can
vary; the goal is personal presence without covering the technical visuals.

### Screen recording

Use screen recording for:

- Dataset inspection
- Code implementation
- Matrix construction
- Running generation
- Evaluation results
- Comparing smoothing values

Do not show prolonged typing. Show a small code change, explain its purpose,
then run it.

### Designed visuals

Create reusable visual components for:

- Character cards
- START and END boundary cards
- Sliding bigram window
- Count matrix and probability heatmap
- Probability tickets or weighted wheel
- 100-attempt likelihood funnel
- Probability-to-NLL surprise chart
- Smoothing redistribution
- Context collapse

These components can return in later episodes and evolve with the model.

## 10. Code reveal strategy

The code should follow the viewer's mental model.

### Reveal order

1. Dataset as a list of strings
2. Vocabulary mapping
3. Boundary insertion
4. Transition extraction
5. Count matrix update
6. Row normalization
7. Greedy generator
8. Sampling generator
9. Evaluation NLL
10. Smoothing parameter

### Representative pseudocode

Transition counting:

~~~python
for example in training_examples:
    tokens = [START, *example, END]

    for current, target in adjacent_pairs(tokens):
        counts[current, target] += 1
~~~

Normalization:

~~~python
smoothed_counts = counts + smoothing
probabilities = normalize_each_row(smoothed_counts)
~~~

Evaluation:

~~~python
for current, target in evaluation_pairs:
    probability = probabilities[current, target]
    total_nll += -log(probability)

average_nll = total_nll / number_of_transitions
~~~

The final implementation may use explicit operations rather than helper
functions when that improves transparency.

## 11. What not to teach in Episode 1

Do not expand into:

- Backpropagation
- Gradient descent
- Embeddings
- Neural-network layers
- Attention
- Transformers
- Perplexity
- Beam search
- Detailed information theory
- Advanced smoothing algorithms
- Production inference systems

It is acceptable to name a later concept while postponing its explanation.

The episode has succeeded if the viewer understands a complete simple model,
not if every future topic has been previewed.

## 12. Research and accuracy safeguards

Before scripting:

- Check every technical claim against the theory chapter and primary sources.
- Label constructed examples as illustrations.
- Use real program output for final demonstrations.
- Do not imply that a bigram model is a modern LLM.
- Say that the bigram and modern autoregressive LMs share a next-token
  framework, not equal capabilities or architecture.
- Distinguish training data from held-out validation data on screen.
- Keep unseen transitions separate from unseen vocabulary tokens.
- Verify that probabilities sum to one.
- Verify NLL calculations independently in tests.

Show a brief source card or description link containing the primary references.

## 13. Assets required before scripting

### Technical assets

- Final dataset and its source/license
- Deterministic train/validation/test split
- Working bigram implementation
- Test coverage for counts, normalization, generation, and NLL
- Fixed example rows used in explanations
- Real greedy output
- Real sampled outputs from selected seeds
- Training and validation NLL
- Unsmoothed and smoothed comparison
- At least one representative model failure

### Visual assets

- Count matrix graphic
- Probability row graphic
- Character transition animation
- Sampling illustration
- Likelihood funnel
- Log/NLL illustration
- Smoothing before-and-after graphic
- Context limitation graphic

### Recording assets

- A-roll setup and framing test
- Screen-recording layout
- Terminal or notebook theme
- Code font and zoom level
- Microphone test
- Consistent series intro/outro treatment

## 14. Production order

Do not write the final script before the model is implemented. The most credible
story will use actual outputs and actual failures.

Recommended order:

1. Approve this video plan.
2. Choose and document the dataset.
3. Implement the transparent reference model.
4. Write automated correctness tests.
5. Run experiments and preserve representative outputs.
6. Update the theory if implementation reveals a meaningful gap.
7. Lock the technical demonstrations.
8. Write the narration and A-roll script around those demonstrations.
9. Create the storyboard and visual assets.
10. Record A-roll and screen demonstrations.
11. Edit a rough cut.
12. Perform technical, narrative, audio, and visual QA.
13. Extract Shorts only after the long-form story works.

## 15. Episode success criteria

The episode is ready to publish when:

- A beginner can explain what the model predicts.
- The transition-counting animation matches the code exactly.
- The probability row visibly sums to one.
- Greedy and sampled generation visibly differ.
- The evaluation target clearly comes from held-out text.
- The multiplication, log, negative sign, and average each have a stated
  purpose.
- Smoothing uses an unseen transition, not an unknown token.
- The limitation is demonstrated rather than merely asserted.
- The final generated examples are genuine program outputs.
- The next episode follows naturally from the limitation discovered here.

## 16. Decisions to make after implementation

These should remain open until we see the real model:

- Final title
- Exact thumbnail expression and generated text
- Which generated samples appear in the cold open
- Whether the code is shown primarily in a notebook or editor
- Exact runtime
- Which smoothing value makes the clearest comparison
- Whether the next episode immediately introduces a neural bigram model or
  pauses first for foundational neural-network mechanics

The plan provides the structure. The implementation will supply the evidence
and personality that turn it into a specific episode.
