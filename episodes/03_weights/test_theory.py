import math
import unittest

import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

from verify_theory import TRAIN, counts, evaluate, log_softmax, pairs


class TheoryChecks(unittest.TestCase):
    def test_boundary_reset_and_count_table(self):
        assert_array_equal(pairs(["ava"]), [[0, 0], [1, 2], [3, 0], [1, 3]])
        self.assertEqual(len(pairs(TRAIN)), 9)
        assert_array_equal(counts(), [[2, 0, 0, 0], [0, 1, 1, 2],
                                     [1, 1, 0, 0], [1, 0, 0, 0]])

    def test_one_hot_really_selects_rows(self):
        weights = np.arange(16).reshape(4, 4)
        ids = np.array([3, 1, 0, 1])
        assert_array_equal(np.eye(4)[ids] @ weights, weights[ids])

    def test_hand_softmax_and_each_batch_row(self):
        logits = [[0, 0, 0, math.log(2)], [0, 0, 0, 0]]
        probabilities = np.exp(log_softmax(logits))
        assert_allclose(probabilities, [[.2, .2, .2, .4], [.25] * 4])
        assert_allclose(probabilities.sum(axis=1), [1, 1])

    def test_shift_invariance_and_scale_difference(self):
        z = np.array([0, 0, 0, math.log(2)])
        assert_allclose(log_softmax(z), log_softmax(z + 1000), atol=1e-12)
        assert_allclose(np.exp(log_softmax(2 * z)), [1/7, 1/7, 1/7, 4/7])

    def test_underflow_does_not_destroy_log_loss(self):
        log_p = log_softmax([1000, -1000, 0, 0])
        self.assertTrue(np.isfinite(log_p).all())
        self.assertAlmostEqual(-log_p[1], 2000)

    def test_cross_entropy_selects_observed_target(self):
        y = np.array([0, 0, 0, 1])
        log_p = log_softmax([0, 0, 0, math.log(2)])
        self.assertAlmostEqual(float(-(y * log_p).sum()), math.log(5/2))

    def test_full_loss_improvement_and_overshoot(self):
        weights = np.zeros((4, 4))
        initial = evaluate(weights, TRAIN)["nll"]
        self.assertAlmostEqual(initial, math.log(4))
        weights[1, 3] = math.log(2)
        good = evaluate(weights, TRAIN)["nll"]
        self.assertAlmostEqual(good, (5*math.log(4)+2*math.log(5)+2*math.log(5/2))/9)
        weights[1, 3] = math.log(100)
        bad = evaluate(weights, TRAIN)["nll"]
        self.assertAlmostEqual(bad, (5*math.log(4)+2*math.log(103)+2*math.log(103/100))/9)
        self.assertLess(good, initial)
        self.assertGreater(bad, initial)

    def test_prediction_weighted_mean(self):
        weights = np.log(counts() + 1)
        a, b = (evaluate(weights, [name])["nll"] for name in TRAIN)
        self.assertAlmostEqual(evaluate(weights, TRAIN)["nll"], (5*a + 4*b)/9)

    def test_add_k_construction_and_held_out_path(self):
        c = counts()
        for k in (.1, 1, 3):
            assert_allclose(np.exp(log_softmax(np.log(c+k))),
                            (c+k)/(c.sum(axis=1, keepdims=True)+4*k))
        scored = evaluate(np.log(c+1), ["ana"])
        self.assertEqual(scored["predictions"], 4)
        self.assertAlmostEqual(scored["nll"], math.log(64)/4)

    def test_an_update_leaves_other_context_rows_unchanged(self):
        weights = np.zeros((4, 4))
        before = log_softmax(weights)
        weights[1, 3] = 3
        assert_array_equal(before[[0, 2, 3]], log_softmax(weights)[[0, 2, 3]])


if __name__ == "__main__":
    unittest.main()
