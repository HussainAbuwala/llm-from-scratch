# Bridge presenter script

11 frames · 1158 spoken words · clarity takes priority over runtime.
Timings below are rehearsal allocations, not recorded chapter timestamps.

Use [the presentation](../../canvas/bridge_02_to_03.html). Start on camera, then
use the existing canvas style. Read [the learning notes](THEORY.md) first.
Frames 4–10 use word-level illustrations, including an exact three-sentence toy; distinguish them from
our measured character-level experiment. Avoid introducing softmax arithmetic.
Pause at each distinction. The earlier 3–5 minute cap has been removed.
The allocations are rehearsal aids, not deadlines; let the examples make sense.

## 01 · We built a language model. What comes next?

Rehearsal start 0:00 · 20 seconds

We've built language models by counting, and eventually we want a small Transformer. Before moving on, let's connect those steps. What did counting teach us? What limits it? And why does learning weights help us build toward something different?

**Visual cue:** Open on camera, then reveal the route. Point to COUNT as our current position.

**Source:** ../../SERIES_PLAN.md

## 02 · What counting taught us

Rehearsal start 0:20 · 35 seconds

Our bigram model looked at one previous character. The trigram looked at two. Both counted what came next and turned those counts into probabilities. To generate a name, we sampled a character, updated the context, and repeated. We also learned to test predictions on names outside the training data. We started here because every step was visible. Those foundations stay with us, even when the model becomes more complicated.

**Visual cue:** Trace the prediction loop once. Explain that memory length changed, while the next-token task stayed the same.

**Source:** ../01_names/README.md; ../02_trigrams/README.md

## 03 · More context needs more evidence

Rehearsal start 0:55 · 30 seconds

Giving our model more context helped at first. Then validation loss rose as evidence became sparse. More specific questions divided the same examples among more rows. Smoothing made missing cases scoreable, but didn't create observations. That's what our add-k experiment showed. But sparse evidence is the symptom. The deeper issue is how the model organizes what it learns.

**Visual cue:** Follow the validation curve from one to five context characters. Three context characters is a 4-gram; a trigram uses two.

**Source:** ../02_trigrams/README.md

## 04 · Exact matches keep related evidence separate

Rehearsal start 1:25 · 40 seconds

For a moment, imagine words instead of our name characters. Suppose we've often seen 'a cup of tea', but rarely seen what follows 'a mug of'. A plain count table keeps those contexts in separate rows. It doesn't recognize that cup and mug may behave similarly. That relationship might be visible elsewhere in the data, but exact counting has no mechanism to use it here. The problem isn't counting badly. It's needing enough examples for each exact situation separately.

**Visual cue:** Explicitly switch to an imagined word-level example. These are illustrative phrases, not observations or outputs from our names experiment. Compare the separate rows; no fabricated counts.

**Source:** https://www.jmlr.org/papers/v3/bengio03a.html; THEORY.md

## 05 · Training: count each observation at several lengths

Rehearsal start 2:05 · 80 seconds

Let's make the counting explicit with a separate, tiny word dataset: a cup of tea, a mug of coffee, and a bag of rice. Look only at the final word in each sentence. The tea observation contributes to the row for a cup of, the row for cup of, and the row for of, in the respective context-length models. Coffee and rice do the same. So all the longer rows exist, and the shorter of row already contains tea once, coffee once, and rice once. These are different views of the same three observations, not nine independent examples. No row has been moved or deleted. We build these counts first; backoff and interpolation decide how to use them afterward.

**Visual cue:** Read across the tea row, then down the of column. Explicitly introduce this three-sentence corpus as a new exact toy, distinct from the earlier hypothetical common/rare example. Only final-word transitions are shown.

**Source:** THEORY.md; https://web.stanford.edu/~jurafsky/slp3/3.pdf

## 06 · Backoff: choose among rows that already exist

Rehearsal start 3:25 · 105 seconds

Now use those existing rows to predict. For a mug of, our simple missing-row fallback finds a row and stops: coffee has probability one in this tiny sample. It doesn't fall back just because the row has only one example. For the mug of, that exact row is absent, but mug of exists. We drop the, keep mug, and stop there. Neither query reaches of. Now try a glass of. Both a glass of and glass of are absent from our toy training data, so this query reaches the existing of row. It gives tea, coffee, and rice one-third each. Here we can see the tradeoff: we have a prediction based on pooled evidence, but it no longer uses glass. The shorter row doesn't know which container we asked about. Backing off selects among rows that already exist; it doesn't move observations or create counts. This is our introductory whole-row fallback, not the full definition of every backoff method.

**Visual cue:** Trace all three paths in order. Only query 3 reaches of and loses the container information. Glass appears in a supplied query, not as a new training observation. The next learned-sharing illustration returns to the separate hypothetical cup/mug setting; do not claim this corpus taught glass similarity.

**Source:** https://web.stanford.edu/~jurafsky/slp3/3.pdf

## 07 · Interpolation: combine existing probability rows

Rehearsal start 5:10 · 110 seconds

Interpolation uses those same prebuilt rows differently. For a mug of, the three-word row gives all its probability to coffee. The two-word mug of row does too. The one-word of row gives tea, coffee, and rice one-third each. Suppose we give each model one-third of the mixture, just to make the example concrete. The final probabilities are one-ninth for tea, seven-ninths for coffee, and one-ninth for rice. They sum to one. Notice that we used the shorter row even though the longer row existed. We mixed probabilities, not raw counts, and didn't change any training row. This retains the specific coffee evidence while borrowing broader evidence. It still doesn't learn a cup/mug relationship. Equal mixture weights are our teaching choice; they are not claimed to be optimal. The tradeoff is how much to trust each source. More weight on the rare long row relies on little evidence; more weight on the broad row can dilute useful specificity. Learning good mixture weights helps manage this, but doesn't itself learn which words have similar roles.

**Visual cue:** Read component distributions before the result. For coffee: 1/3 times 1 plus 1/3 times 1 plus 1/3 times 1/3 equals 7/9. The toy rows are defined and normalized; unseen targets retain zeros in the unsmoothed components. No performance improvement is claimed.

**Source:** https://web.stanford.edu/~jurafsky/slp3/3.pdf; THEORY.md

## 08 · Which rows does interpolation consult?

Rehearsal start 7:00 · 55 seconds

Let's stay with a mug of. Our interpolation combines predictions from a mug of, mug of, and of. Notice which row isn't directly consulted: a cup of. Cup-related observations can still reach us through the of row. But our rule selects shorter endings of the query; it doesn't look for another word that behaves like mug. Replacing mug with cup is not shortening the history. This is the missing connection: we can borrow broader evidence, but we aren't yet learning which other situations are especially relevant.

**Visual cue:** Trace only the three suffix rows into the mixture. The cup row is separate, not absent. Say directly consulted: cup evidence does contribute indirectly via of.

**Source:** THEORY.md; https://web.stanford.edu/~jurafsky/slp3/3.pdf

## 09 · The broader row loses where evidence came from

Rehearsal start 7:55 · 55 seconds

Look at two observations in our toy data: tea followed cup of, and rice followed bag of. In the of row, these become one count for tea and one for rice, alongside coffee. That row doesn't record which container contributed each count. The longer rows still exist elsewhere. But the of row alone cannot give extra influence to tea because it came from a cup. Changing the mixture weights adjusts trust in whole predictions from different history lengths. It doesn't itself learn that cup-related situations might be more relevant to mugs than bag-related situations.

**Visual cue:** Emphasize that only the pooled row lacks container attribution; nothing was deleted from the training data or longer models.

**Source:** THEORY.md; https://web.stanford.edu/~jurafsky/slp3/3.pdf

## 10 · Can learning about cups help with mugs?

Rehearsal start 8:50 · 60 seconds

Let's focus on one question: what follows a mug of? Imagine a larger training dataset with many examples of people drinking from cups and mugs, or pouring tea into both. Those repeated uses could provide evidence that cups and mugs play similar roles. Can a model learn useful patterns from those examples and use them to help with our mug query, while still letting mug affect the answer? That's the capability we want to explore. Our three toy sentences don't establish that relationship. It must be learned from training data, and we'd need to test whether it helps. This is a goal to build toward, not a result we've already achieved.

**Visual cue:** Start with the single mug query. Read the paired illustrative training examples, then the question below them. These examples are not additions to the exact three-sentence corpus used for the count calculations. Similarity and improved predictions are possibilities to learn and test, not guaranteed results.

**Source:** THEORY.md; https://www.jmlr.org/papers/v3/bengio03a.html

## 11 · The pieces we need to build next

Rehearsal start 9:50 · 100 seconds

We want more flexible ways to use what the model learns. To train that kind of prediction rule, we need numbers we can adjust. Those numbers are weights. Counts record what happened in our data; weights give us adjustable parts whose changes can alter the predictions. Episode 3 introduces them on our familiar character bigram task. Then we need a training method: a way to decide how to change the weights to improve predictions. Episodes 4 to 6 cover gradients, automating their calculation, and using PyTorch. Finally, we need a structure that reuses some of the same weights across inputs. That lets learning from one example affect predictions for other inputs. Episode 7 explores that through embeddings and a small neural network. You don't need to understand those names yet; they mark where we'll learn each piece. Weights alone don't create useful sharing. First we understand adjustable predictions and how to train them, then build the structure that shares learning. We will keep checking whether the predictions improve on held-out data.

**Visual cue:** Start with the motivation sentence, then read the three rows in curriculum order. Treat gradients, autograd, PyTorch, embeddings and MLP as future lesson labels, not concepts to derive here. Shared means the exact same adjustable numbers are reused, not separate numbers with equal values. Counts are learned statistics too; this is a distinction in parameterization, not learning versus no learning. The Episode 04–06 bigram label describes the arc: Episode 04 uses a tiny calculus example, Episode 05 builds scalar autograd, and Episode 06 applies the ideas by rebuilding the bigram in PyTorch.

**Source:** ../../SERIES_PLAN.md; THEORY.md

## Before recording

Check you can explain: backoff pools suffix evidence; interpolation mixes
predictions; learned representations offer a different kind of sharing; a
bigram weight table alone does not yet do that. The experiment compared add-k
models, not all count-based techniques. Keep the claims at that scope.

For the next episode's short independent opening, see [README](README.md).
