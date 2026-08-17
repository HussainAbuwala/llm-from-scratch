# Research and Education Standard

This project teaches established language-modeling and deep-learning ideas. We
may create our own examples, diagrams, code organization, and narrative, but we
do not present invented explanations as accepted theory.

## Three labels we will keep separate

### 1. Established theory

Definitions, mathematical results, algorithms, and architectures supported by
textbooks, peer-reviewed papers, original technical reports, or official
documentation.

Examples include n-gram language models, maximum-likelihood estimation,
negative log-likelihood, backpropagation, tokenization, self-attention, and the
Transformer architecture.

### 2. Pedagogical simplification

A deliberately smaller or less general version used to make an idea visible.
It must be described as a simplification and its limitations must be stated.

Examples include character-level tokenization, a one-character bigram context,
tiny datasets, scalar autograd, and single-head attention.

### 3. Project engineering choice

A decision made for this repository rather than a universal rule.

Examples include filenames, model size, dataset choice, Python version,
hyperparameters, visual style, and the order in which we teach topics.

## Source hierarchy

For core technical claims, prefer sources in this order:

1. Original research papers or technical reports.
2. Established university textbooks and course materials.
3. Official framework documentation.
4. High-quality educational implementations for comparison.

Blogs, social posts, and secondary videos can suggest examples or analogies,
but they will not be the sole support for foundational claims.

## Per-episode requirements

Before an episode moves from learning into production, its theory document
should contain:

- The established concepts being taught.
- The prerequisite knowledge required.
- Any pedagogical simplifications and their limitations.
- Any project-specific engineering choices.
- Primary or authoritative references.
- A correctness review of equations, terminology, and code.
- A short understanding check that can be answered without memorization.

If reputable sources disagree or terminology is overloaded, the episode should
say so rather than silently choosing one interpretation.

## Episode 1 provenance

The first episode's count-based character bigram model is a pedagogical instance
of an n-gram language model. The established ideas are:

- A language model assigns probabilities to sequences or next-token outcomes.
- An n-gram approximation conditions on a limited preceding context.
- Count-based n-gram probabilities can be estimated from observed transition
  frequencies and normalized into conditional distributions.
- Sequence likelihood, log-likelihood, negative log-likelihood, and smoothing
  are standard language-modeling concepts.

Using characters instead of words and a tiny name-like dataset are pedagogical
choices. The underlying n-gram method is not invented for this project.

## Foundational references

- Dan Jurafsky and James H. Martin, *Speech and Language Processing*, Chapter
  3, “N-gram Language Models”:
  https://web.stanford.edu/~jurafsky/slp3/ed3book.pdf
- Yoshua Bengio, Réjean Ducharme, Pascal Vincent, and Christian Jauvin, “A
  Neural Probabilistic Language Model,” JMLR 3 (2003):
  https://www.jmlr.org/papers/v3/bengio03a.html
- Ashish Vaswani et al., “Attention Is All You Need,” NeurIPS 2017:
  https://proceedings.neurips.cc/paper/7181-attention-is-all-you-need
- Alec Radford et al., “Language Models are Unsupervised Multitask Learners”
  (GPT-2 technical report, 2019):
  https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf
- Andrej Karpathy, *makemore*, an educational progression from a character
  bigram model to a Transformer:
  https://github.com/karpathy/makemore

This list will grow as the series reaches tokenization, neural networks,
optimization, attention, Transformers, scaling, evaluation, and fine-tuning.
