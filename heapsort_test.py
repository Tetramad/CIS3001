from heapsort import heapsort, heapify, heappop
from unittest import TestCase


class HeapAssertion:
    def is_heap(self, xs):
        if len(xs) == 0:
            return True
        s = [0]
        while s:
            c = s.pop()
            if 2 * c + 1 < len(xs):
                if xs[2 * c + 1] < xs[c]:
                    return False
                else:
                    s.append(2 * c + 1)
            if 2 * c + 2 < len(xs):
                if xs[2 * c + 2] < xs[c]:
                    return False
                else:
                    s.append(2 * c + 2)
        return True

    def assertHeap(self, expr):
        assert self.is_heap(expr), f'{expr!r} is not heap'


class HeapSortTest(TestCase):
    def test_empty(self):
        self.assertEqual(heapsort([]), [])

    def test_two(self):
        self.assertEqual(heapsort([-1, 1]), [-1, 1])
        self.assertEqual(heapsort([1, -1]), [-1, 1])

    def test_many(self):
        self.assertEqual(heapsort(list(range(14, -1, -1))), list(range(15)))


class HeapifyTest(TestCase, HeapAssertion):
    def test_empty(self):
        self.assertHeap(heapify([]))

    def test_three(self):
        self.assertHeap(heapify([-1, 0, 1]))
        self.assertHeap(heapify([-1, 1, 0]))
        self.assertHeap(heapify([0, -1, 1]))
        self.assertHeap(heapify([0, 1, -1]))
        self.assertHeap(heapify([1, -1, 0]))
        self.assertHeap(heapify([1, 0, -1]))

    def test_four(self):
        self.assertHeap(heapify([1, 2, 3, 0]))
        self.assertHeap(heapify([1, 0, 3, 2]))
        self.assertHeap(heapify([1, 0, 2, 3]))

    def test_many(self):
        self.assertHeap(heapify(list(range(14, -1, -1))))


class HeappopTest(TestCase, HeapAssertion):
    def test(self):
        xs = heapify(list(range(14, -1, -1)))
        for x in range(15):
            self.assertEqual(heappop(xs), x)
            self.assertHeap(xs)
        self.assertEqual(xs, [])
