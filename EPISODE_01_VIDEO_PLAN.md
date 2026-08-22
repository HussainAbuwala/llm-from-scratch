# Episode 1 Video Plan: The Smallest Language Model

Status: Working production plan

Series: Building an LLM From First Principles

Theory source: [EPISODE_01_THEORY.md](EPISODE_01_THEORY.md)

## 1. Episode purpose

Episode 1 should give the viewer a complete, working language model before
introducing neural networks.

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

The model will be a character-level count-based bigram model trained on a
line-based collection of names. It will generate new name-like sequences one
character at a time.

The episode is not trying to make a useful assistant. It is trying to expose
the complete language-modeling framework in a form small enough to see.

## 2. Viewer promise

By the end of the episode, the viewer will:

- Build a real, minimal language model without a neural network.
- Understand next-token prediction as a probability distribution.
- See how training text becomes transition counts.
- Convert counts into probabilities.
- Generate text using greedy decoding and weighted sampling.
- Evaluate the model on unseen examples using average NLL.
- Understand why smoothing is needed.
- See exactly why a one-character model is limited.
- Know what problem the next episode must solve.

The emotional promise is:

> You do not need to begin with a Transformer. We can make the central idea of
> language modeling visible with a small table and build upward from there.

## 3. Working title and packaging

### Recommended working title

**I Built the Smallest Language Model — No Neural Network**

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

The finished program should:

1. Load a line-based dataset.
2. Split examples into training, validation, and test sets.
3. Build a character vocabulary.
4. Count bigram transitions from the training split.
5. Apply configurable add-k smoothing.
6. Normalize counts into probability rows.
7. Print or visualize selected rows.
8. Generate examples using greedy decoding.
9. Generate examples using weighted sampling.
10. Calculate average NLL for training and validation data.
11. Report the uniform and unigram baselines beside the bigram score.
12. Sweep k and print training and validation NLL side by side.
13. Show at least one failure caused by one-character context.

The final demo should expose controls for:

- Random seed
- Number of generated examples
- Greedy versus sampling
- Smoothing value

The first implementation can be a notebook or terminal program. A web
interface is unnecessary for Episode 1.

## 6. Narrative spine

The episode follows one question:

> What is the smallest machine that can learn patterns from text and generate
> something new?

The story develops through successive discoveries:

1. Show generated names before explaining the machine.
2. Reveal that the model has no neural network.
3. Define language modeling as next-token probabilities.
4. Reduce tokens to characters and context to one character.
5. Discover that learning can begin with counting.
6. Turn counts into probabilities.
7. Use the table to generate text.
8. Watch greedy decoding fail and introduce sampling.
9. Ask how we can objectively judge the model.
10. Use held-out transitions, likelihood, logs, and average NLL.
11. Encounter zero probability and introduce smoothing.
12. Reveal that locally valid transitions can still create nonsense.
13. End with the problem that motivates a more capable model.

This creates a problem-solution chain rather than a list of definitions.

## 7. Proposed runtime and segment plan

Target runtime: approximately 28–32 minutes.

This is a guide rather than a hard timing constraint. Clarity takes priority,
but each section should earn its place by advancing the model.

| Time | Segment | What the viewer sees | Core takeaway |
|---|---|---|---|
| 0:00–0:40 | Cold open | Terminal generates several plausible and strange names; quick cuts between outputs and Hussain | A tiny program learned enough structure to create new text |
| 0:40–1:40 | Personal premise | On-camera introduction to the series and why Hussain wants to understand LLMs from first principles | We are learning and building honestly, not pretending to begin as experts |
| 1:40–3:20 | What are we building? | Simple animation: context enters, probability bars emerge, one token is chosen, loop repeats | A language model predicts a distribution over the next token |
| 3:20–5:00 | Make the problem tiny | Name dataset, character cards, vocabulary and integer mappings | Our tokens are characters and our context is one character |
| 5:00–7:40 | Transitions | Animate START–a–n–n–a–END, then slide a two-token window across it | Training examples become ordered current-token/next-token pairs |
| 7:40–10:30 | Count matrix | Build a few cells by hand, then reveal the complete matrix or heatmap | Training for this model is counting |
| 10:30–12:20 | Normalization | Row [0, 1, 1, 2] becomes [0, .25, .25, .50]; four-ticket analogy | A probability row is a normalized count row |
| 12:20–13:20 | What is the model? | Freeze the vocabulary mapping and probability table; label them as the artifact | The trained model is a lookup table of P(next token given current token) |
| 13:20–15:10 | Greedy generation | Trace the highest-probability arrow repeatedly and show a loop or repetitive output | Highest probability at every step is deterministic but can be locally shortsighted |
| 15:10–17:30 | Sampling | Probability tickets or weighted wheel, followed by multiple generated names | Sampling preserves likely choices while allowing variation |
| 17:30–18:30 | The evaluation question | Put one attractive sample next to several failures; ask whether visual judgment is enough | Samples can be lucky or cherry-picked |
| 18:30–20:20 | Correct targets | Hold out a word, convert it into evaluation pairs, and highlight the probability assigned to each real next token | Evaluation text supplies the answer key |
| 20:20–22:20 | Sequence likelihood | Funnel of 100 attempts: 100 → 80 → 40 → 10 → 4 | Required conditional events along one path multiply |
| 22:20–24:40 | Logs and NLL | Tiny product transforms into summed log penalties; probability-to-surprise chart | Logs make tiny products manageable; NLL measures surprise |
| 24:40–25:50 | Average across data | Two datasets with 100 and 1,000 transitions but equal per-token quality | Average NLL enables fair per-transition comparison |
| 25:50–27:10 | Baselines | Uniform ln(V+1) and unigram beside the bigram score | A loss number means nothing without a reference point |
| 27:10–28:00 | Counting was already optimal | Counts ÷ totals labelled as the exact minimiser, next to "episode 3 will crawl there with gradients" | This model is the analytic answer to the loss a network approximates |
| 28:00–29:40 | Smoothing | Unseen a→x has zero probability; add pseudo-counts and redistribute the row; sweep k and watch train and validation diverge | Unseen in limited data should not automatically mean impossible — and the fix costs training loss |
| 29:40–31:30 | Limitations | Generated nonsense whose every adjacent pair was observed; histories collapse to the same final character | Local plausibility is not global coherence |
| 31:30–33:00 | Recap and bridge | Context growth 30 → 900 → 27,000, then the two things counting structurally cannot do | The next problem is using more context and sharing patterns |

Runtime therefore lands closer to **33 minutes** than the original 28–32 estimate.
The two added segments (baselines, and counting-as-optimum) are worth the minutes:
the first makes every later loss number interpretable, and the second is the
bridge the whole series hangs from.

Scene-by-scene visuals for all of the above are built in
`canvas/episode_01_bigram.excalidraw` (28 frames, numbered to match this order).

## 8. Detailed beat sheet

### Beat 1: Cold open

Show the finished model running before explaining it.

Possible screen output:

~~~text
alyra
marin
annnava
zalen
~~~

Do not claim that every sample is impressive. Include at least one strange
result because failure becomes part of the lesson.

Suggested opening idea:

> These names came from a language model I trained from scratch. It has no
> neural network, no attention, and it remembers exactly one character. That
> sounds almost useless—and that is precisely why it is the right place to
> begin.

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
amelia
noah
liam
~~~

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

### Beat 9: Generate greedily

Trace:

~~~text
START -> highest-probability token -> highest-probability token -> ...
~~~

Use a real output from the implementation. If it loops, that is ideal. If it
does not naturally loop, construct a tiny transparent example that does and
label it as an illustration.

Clarify that greedy decoding chooses the best immediate token, not necessarily
the best complete sequence.

### Beat 10: Generate by sampling

Show weighted randomness rather than an unexplained random-number API.

Possible visual:

- 60 red tickets for a
- 30 blue tickets for b
- 10 yellow tickets for c

Then run multiple seeds and compare outputs. The most probable choices should
appear frequently, but not exclusively.

### Beat 11: Introduce evaluation as a problem

Show one plausible output and ask:

> Is the model good, or did we just get lucky?

Then reveal multiple weaker samples. Explain that a single generated example is
not an objective comparison.

### Beat 12: Use evaluation text as the answer key

Hold out one word that did not create the counts.

Convert it into pairs and display the model's probability for the actual target
in each pair.

Keep generation and evaluation visually distinct:

~~~text
generation: no target is supplied
evaluation: the existing text supplies the target
~~~

### Beat 13: Explain multiplication with a funnel

Use the 100-attempt funnel:

~~~text
100 × 0.80 × 0.50 × 0.25 × 0.40 = 4
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
a -> x was never observed
P(x | a) = 0
~~~

Show how one zero makes the sequence likelihood zero and log(0) unusable.

Add a pseudo-count, normalize again, and show the tradeoff: unseen transitions
gain probability by taking some probability from observed transitions.

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
