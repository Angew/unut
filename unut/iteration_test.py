import doctest
import unittest

import iteration
from iteration import *


class TestSlidingWindowIter(unittest.TestCase):
    def test_good(self):
        self.assertSequenceEqual(
            list(sliding_window_iter([1, 2, 3, 4], 2)),
            [(1, 2), (2, 3), (3, 4)]
        )

    def test_exact_length(self):
        self.assertSequenceEqual(
            list(sliding_window_iter(["c", "b", "a"], 3)),
            [("c", "b", "a")]
        )

    def test_short(self):
        self.assertSequenceEqual(
            list(sliding_window_iter([1, 2], 3)),
            []
        )

    def test_size_one(self):
        self.assertSequenceEqual(
            list(sliding_window_iter([1, 2, 3, 4], 1)),
            [(1,), (2,), (3,), (4,)]
        )

    def test_bad_size(self):
        with self.assertRaises(ValueError):
            list(sliding_window_iter([1, 2], 0))


def run():
    if not doctest.testmod(iteration)[0]:
        print("doctest: OK")
    unittest.main()


if __name__ == "__main__":
    run()
