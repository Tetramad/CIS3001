from unittest import TestCase
from mergesort import mergesort
from itertools import permutations


class MergeSortTest(TestCase):
    def test_empty(self):
        self.assertSequenceEqual(mergesort([]), [])

    def test_one(self):
        self.assertSequenceEqual(mergesort([0]), [0])

    def test_three(self):
        for xs in permutations(range(3)):
            self.assertSequenceEqual(mergesort(xs), [0, 1, 2])

    def test_reversed(self):
        self.assertSequenceEqual(mergesort(range(14, -1, -1)), range(15))
