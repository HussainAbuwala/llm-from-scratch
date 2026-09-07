"""Check the actual function definitions taught in the notebook, with no plotting dependencies."""

import ast
import copy
import math
from pathlib import Path
import random
import unittest

# Load only the lesson's function definitions; do not rerun its data experiments in unit tests.
source = Path(__file__).with_name("lesson.py").read_text()
functions = [node for node in ast.parse(source).body if isinstance(node, ast.FunctionDef)]
scope = {"math": math, "START": "<START>", "END": "<END>"}
exec(compile(ast.Module(body=functions, type_ignores=[]), "lesson.py", "exec"), scope)


class BigramTests(unittest.TestCase):
    def setUp(self):
        self.rows, self.columns, self.ri, self.ci = scope["make_vocabulary"](["anna", "ava"])
        self.counts = scope["count_bigrams"](["anna", "ava"], self.ri, self.ci)
        self.p = scope["normalize"](self.counts)

    def test_theory_table_and_boundaries(self):
        self.assertEqual(self.rows, ["<START>", "a", "n", "v"])
        self.assertEqual(self.columns, ["a", "n", "v", "<END>"])
        self.assertEqual(self.counts, [[2, 0, 0, 0], [0, 1, 1, 2], [1, 1, 0, 0], [1, 0, 0, 0]])
        self.assertEqual(sum(map(sum, self.counts)), 9)
        self.assertNotIn("<START>", self.ci)
        self.assertNotIn("<END>", self.ri)

    def test_held_out_ana_exact_probability_and_nll(self):
        result = scope["evaluate"](["ana"], self.p, self.ri, self.ci)
        self.assertEqual(result["predictions"], 4)
        self.assertAlmostEqual(result["nll"], math.log(2))
        self.assertAlmostEqual(math.exp(-result["nll"] * 4), 1 / 16)

    def test_zero_probability_is_infinite_and_smoothing_repairs_it(self):
        result = scope["evaluate"](["avna"], self.p, self.ri, self.ci)
        self.assertEqual(result["nll"], math.inf)
        self.assertEqual(result["zero_predictions"], 1)
        self.assertEqual(result["predictions"], 5)
        smoothed = scope["smooth"](self.counts, 1)
        self.assertEqual(smoothed[self.ri["v"]], [0.4, 0.2, 0.2, 0.2])
        self.assertTrue(math.isfinite(scope["evaluate"](["avna"], smoothed, self.ri, self.ci)["nll"]))

    def test_smoothing_normalizes_allowed_outcomes_without_mutation(self):
        original = copy.deepcopy(self.counts)
        for k in [0, 0.1, 1, 100, 1e9]:
            table = scope["smooth"](self.counts, k)
            for row in table:
                self.assertAlmostEqual(sum(row), 1)
                self.assertTrue(all(value >= 0 for value in row))
        self.assertEqual(self.counts, original)
        self.assertEqual(scope["smooth"](self.counts, 0), self.p)
        self.assertAlmostEqual(scope["smooth"](self.counts, 1e9)[0][0], 0.25, places=8)

    def test_nll_weights_predictions_instead_of_names(self):
        ri = {"<START>": 0, "a": 1}
        ci = {"a": 0, "<END>": 1}
        p = [[0.5, 0.5], [0.25, 0.75]]
        result = scope["evaluate"](["a", "aa"], p, ri, ci)
        expected = (-2 * math.log(0.5) - 2 * math.log(0.75) - math.log(0.25)) / 5
        self.assertEqual(result["predictions"], 5)
        self.assertAlmostEqual(result["nll"], expected)

    def test_unknown_characters_are_rejected_even_with_smoothing(self):
        for p in [self.p, scope["smooth"](self.counts, 1)]:
            with self.assertRaisesRegex(ValueError, "Unknown characters"):
                scope["evaluate"](["ax"], p, self.ri, self.ci)

    def test_evaluation_does_not_change_model(self):
        original = copy.deepcopy(self.p)
        scope["evaluate"](["ana"], self.p, self.ri, self.ci)
        self.assertEqual(self.p, original)

    def test_generation_translates_column_tokens_back_to_rows(self):
        # 'a' has column index 0 but row index 1. Reusing the index would loop.
        name, ended = scope["generate"]([[1, 0], [0, 1]], {"<START>": 0, "a": 1},
                                        ["a", "<END>"], random.Random(0))
        self.assertEqual((name, ended), ("a", True))

    def test_cap_and_empty_generation_are_explicit(self):
        ri, columns = {"<START>": 0, "a": 1}, ["a", "<END>"]
        result = scope["generate"]([[1, 0], [0.9, 0.1]], ri, columns, random.Random(0),
                                    greedy=True, max_length=5)
        self.assertEqual(result, ("aaaaa", False))
        self.assertEqual(scope["generate"]([[0, 1], [0, 1]], ri, columns, random.Random(0)), ("", True))

    def test_sampling_reproducibility_and_weights(self):
        ri, columns = {"<START>": 0, "a": 1}, ["a", "<END>"]
        p = [[0.8, 0.2], [0, 1]]
        def batch(seed):
            rng = random.Random(seed)
            return [scope["generate"](p, ri, columns, rng)[0] for _ in range(3000)]
        samples = batch(91)
        self.assertEqual(samples, batch(91))
        self.assertTrue(0.76 < samples.count("a") / len(samples) < 0.84)

    def test_invalid_inputs_are_clear(self):
        with self.assertRaises(ValueError):
            scope["evaluate"]([], self.p, self.ri, self.ci)
        with self.assertRaises(ValueError):
            scope["normalize"]([[0, 0]])
        for k in [-1, math.inf, math.nan]:
            with self.assertRaises(ValueError):
                scope["smooth"](self.counts, k)

    def test_uniform_and_unigram_toy_baselines(self):
        uniform = [[0.25] * 4 for _ in self.rows]
        unigram = [[4 / 9, 2 / 9, 1 / 9, 2 / 9] for _ in self.rows]
        self.assertAlmostEqual(scope["evaluate"](["ana"], uniform, self.ri, self.ci)["nll"], math.log(4))
        expected = -(2 * math.log(4 / 9) + 2 * math.log(2 / 9)) / 4
        self.assertAlmostEqual(scope["evaluate"](["ana"], unigram, self.ri, self.ci)["nll"], expected)


if __name__ == "__main__":
    unittest.main()
