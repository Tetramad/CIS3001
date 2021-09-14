from listpy import listpy
from unittest import TestCase, skip
from collections.abc import MutableSequence


class TestListpy(TestCase):
    def test_setitem_and_getitem(self):
        obj = listpy()
        obj[0] = 10
        self.assertEqual(obj[0], 10)

    def test_setitem_and_getitem_two_items(self):
        obj = listpy()
        obj[0] = 1
        obj[1] = 10
        self.assertEqual(obj[0], 1)
        self.assertEqual(obj[1], 10)

    def test_setitem_to_exists(self):
        obj = listpy()
        obj[0] = 1
        obj[1] = 10
        obj[0] = 5
        self.assertEqual(obj[0], 5)
        self.assertEqual(obj[1], 10)

    def test_getitem_out_of_range(self):
        obj = listpy()
        with self.assertRaises(IndexError):
            obj[0]

    def test_setitem_out_of_range(self):
        obj = listpy()
        with self.assertRaises(IndexError):
            obj[42] = 0

    def test_len_empty(self):
        obj = listpy()
        self.assertEqual(len(obj), 0)

    def test_len_one(self):
        obj = listpy()
        obj[0] = 42
        self.assertEqual(len(obj), 1)

    def test_len_overwrite(self):
        obj = listpy()
        obj[0] = 42
        self.assertEqual(len(obj), 1)

    def test_list_conversion(self):
        obj = listpy()
        obj[0] = 0
        obj[1] = 1
        obj[2] = 2
        obj[3] = 3
        obj[1] = 42
        self.assertListEqual(list(obj), [0, 42, 2, 3])

    def test_delitem(self):
        obj = listpy()
        obj[0] = 0
        del obj[0]
        self.assertSequenceEqual(obj, [])

        obj = listpy()
        obj[0] = 0
        obj[1] = 1
        obj[2] = 2
        del obj[1]
        self.assertSequenceEqual(obj, [0, 2])

    def test_delitem_out_of_range(self):
        obj = listpy()
        with self.assertRaises(IndexError):
            del obj[0]
        with self.assertRaises(IndexError):
            del obj[10]

        obj[0] = 42
        with self.assertRaises(IndexError):
            del obj[1]
        with self.assertRaises(IndexError):
            del obj[10]

    def test_insert(self):
        obj = listpy()
        obj.insert(0, 10)
        self.assertSequenceEqual(obj, [10])
        obj.insert(0, 5)
        self.assertSequenceEqual(obj, [5, 10])
        obj.insert(2, 9)
        self.assertSequenceEqual(obj, [5, 10, 9])
        obj.insert(1, 7)
        self.assertSequenceEqual(obj, [5, 7, 10, 9])

    def test_setitem_slice(self):
        obj = listpy()
        obj[:] = [10, 10]
        self.assertSequenceEqual(obj, [10, 10])
        obj[0:2] = [10, 10]
        self.assertSequenceEqual(obj, [10, 10])
        obj[1:2] = [10, 10]
        self.assertSequenceEqual(obj, [10, 10, 10])
        obj[3:10] = [10, 10]
        self.assertSequenceEqual(obj, [10, 10, 10, 10, 10])
        obj[5:10] = [0, 0]
        self.assertSequenceEqual(obj, [10, 10, 10, 10, 10, 0, 0])

    def test_getitem_slice(self):
        obj = listpy()
        obj[0:0] = [10, 20, 30, 40, 50]

    def test_listpy_should_be_MutableSequence(self):
        self.assertIsInstance(listpy(), MutableSequence)
        self.assertTrue(issubclass(listpy, MutableSequence))

    def test_listpy_should_have_mixins(self):
        obj = listpy()
        obj.append(0)
        obj.extend((1, 2, 3, 4))
        self.assertEqual(len(obj), 5)
        self.assertEqual(obj[3], 3)
        obj.reverse()
        self.assertEqual(obj[3], 1)
        obj.pop()
        self.assertEqual(len(obj), 4)
        obj.remove(3)
        self.assertEqual(len(obj), 3)
        obj += (10, 20, 30)
        self.assertEqual(len(obj), 6)
        self.assertEqual(obj[5], 30)
        # self.assertEqual(obj[-1], 30)
        obj.clear()
        self.assertEqual(len(obj), 0)

        '''
        # issue 34427
        # extending self should not cause infinite loop
        items = [1, 2, 3, 4]
        obj2 = listpy()
        obj2.extend(items + items)
        obj.clear()
        obj.extend(items)
        obj.extend(obj)
        self.assertEqual(len(obj), len(obj2))
        self.assertEqual(list(obj), list(obj2))
        '''
