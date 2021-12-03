from unittest import TestCase
from radixsort import radixsort
import random


class RadixSortTest(TestCase):
    def test_empty(self):
        self.assertSequenceEqual(radixsort([]), [])

    def test_two(self):
        self.assertSequenceEqual(radixsort([1, 0]), [0, 1])

    def test_many(self):
        xs = [random.randint(0, 10000000) for _ in range(100)]
        self.assertSequenceEqual(radixsort(xs), sorted(xs))
