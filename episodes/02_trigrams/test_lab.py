import math
import random
import unittest

from lab import CountModel, END, START, evaluate, generate, load_splits, windows


class ConceptTests(unittest.TestCase):
    def test_padding_targets_and_reset(self):
        self.assertEqual(list(windows("ava", 2)), [
            ((START, START), "a"), ((START, "a"), "v"),
            (("a", "v"), "a"), (("v", "a"), END)])
        for size in range(1, 6):
            self.assertEqual(len(list(windows("anna", size))), 5)
            model = CountModel(["anna", "ava"], size)
            self.assertEqual(sum(model.totals.values()), 9)
            self.assertEqual(model.counts[(START,) * size]["a"], 2)
            self.assertNotIn(START, model.outcomes)
            self.assertTrue(all(END not in context for context in model.counts))

    def test_hand_worked_likelihoods(self):
        bigram, trigram = CountModel(["anna", "ava"], 1), CountModel(["anna", "ava"], 2)
        for model, name, expected in [(bigram, "ana", 1 / 16),
                                      (trigram, "anna", 1 / 2),
                                      (trigram, "ava", 1 / 2),
                                      (trigram, "ana", 0)]:
            self.assertEqual(math.prod(model.probability(c, t) for c, t in windows(name, model.context_size)), expected)
        smoothed = evaluate(trigram, ["ana"], 1)
        self.assertAlmostEqual(smoothed["nll"], math.log(75) / 4)

    def test_unseen_event_differs_from_unspecified_row(self):
        model = CountModel(["anna", "ava"], 2)
        self.assertEqual(model.probability(("a", "n"), "a"), 0)
        self.assertIsNone(model.probability(("v", "n"), "a"))
        for k in (0.01, 1, 100):
            self.assertEqual(model.probability(("v", "n"), "a", k), 1 / 4)
        before = dict(model.totals)
        result = evaluate(model, ["avna"], 0)
        self.assertEqual(result["zero_probability_predictions"], 1)
        self.assertEqual(result["unseen_context_predictions"], 1)
        self.assertEqual(dict(model.totals), before)
        self.assertEqual(set(model.counts), set(before))

    def test_normalization_and_unknown_targets(self):
        model = CountModel(["anna", "ava"], 2)
        for context in [*model.counts, ("v", "n")]:
            self.assertAlmostEqual(sum(model.probability(context, t, 0.3) for t in model.outcomes), 1)
        with self.assertRaises(ValueError):
            evaluate(model, ["zoe"], 1)

    def test_token_weighted_denominator(self):
        model = CountModel(["anna", "ava"], 2)
        one, two = evaluate(model, ["anna"], 1), evaluate(model, ["ava"], 1)
        both = evaluate(model, ["anna", "ava"], 1)
        self.assertEqual(both["predictions"], 9)
        self.assertAlmostEqual(both["nll"], (5 * one["nll"] + 4 * two["nll"]) / 9)

    def test_generation_shifts_context_and_stops(self):
        model = CountModel(["anna", "ava"], 2)
        rng = random.Random(2026)
        samples = [generate(model, 0, rng) for _ in range(100)]
        self.assertEqual({sample["name"] for sample in samples}, {"anna", "ava"})
        self.assertTrue(all(sample["ended"] for sample in samples))
        self.assertFalse(generate(model, 0, rng, max_steps=1)["ended"])

    def test_episode_one_validation_continuity(self):
        train, validation, test, _ = load_splits()
        self.assertEqual((len(train), len(validation), len(test)), (23595, 2949, 2950))
        self.assertTrue(set(train).isdisjoint(validation))
        self.assertTrue(set(train).isdisjoint(test))
        self.assertTrue(set(validation).isdisjoint(test))
        result = evaluate(CountModel(train, 1), validation, 0.3)
        self.assertAlmostEqual(result["nll"], 2.4566215540070693)


if __name__ == "__main__":
    unittest.main()
