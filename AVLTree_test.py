# pyright: reportOptionalMemberAccess=none
from AVLTree import AVLTreeNode
from unittest import TestCase, expectedFailure, skip


class AVLTreeNodeTest(TestCase):
    def build(self, func, iterable):
        node = AVLTreeNode(iterable[0])
        for v in iterable[1:]:
            if (n := func(node, v)) is not None:
                node = n
        return node

    def test_creation(self):
        node = AVLTreeNode(42)
        self.assertEqual(node.value, 42)
        self.assertIsNone(node.pnode)
        self.assertIsNone(node.lnode)
        self.assertIsNone(node.rnode)

    def test_add_left(self):
        node = self.build(AVLTreeNode.add, [0, -1])
        self.assertEqual(node.lnode.value, -1)
        self.assertIs(node.lnode.pnode, node)

    def test_add_right(self):
        node = self.build(AVLTreeNode.add, [0, 1])
        self.assertEqual(node.rnode.value, 1)
        self.assertIs(node.rnode.pnode, node)

    def test_same_value(self):
        node = self.build(AVLTreeNode.add, [0, 0])
        self.assertEqual(node.value, 0)
        self.assertIsNone(node.pnode)
        self.assertIsNone(node.lnode)
        self.assertIsNone(node.rnode)

    def test_add_leftleft(self):
        node = self.build(AVLTreeNode.add, [0, -1, -2])
        node = node.balance()
        self.assertEqual(node.value, -1)
        self.assertEqual(node.lnode.value, -2)
        self.assertEqual(node.rnode.value, 0)
        self.assertIsNone(node.pnode)
        self.assertIs(node.lnode.pnode, node)
        self.assertIs(node.rnode.pnode, node)

    def test_add_rightright(self):
        node = self.build(AVLTreeNode.add, [0, 1, 2])
        node = node.balance()
        self.assertEqual(node.value, 1)
        self.assertEqual(node.lnode.value, 0)
        self.assertEqual(node.rnode.value, 2)
        self.assertIsNone(node.pnode)
        self.assertIs(node.lnode.pnode, node)
        self.assertIs(node.rnode.pnode, node)

    def test_add_leftright(self):
        node = self.build(AVLTreeNode.add, [0, -2, -1])
        node = node.balance()
        self.assertEqual(node.value, -1)
        self.assertEqual(node.lnode.value, -2)
        self.assertEqual(node.rnode.value, 0)
        self.assertIsNone(node.pnode)
        self.assertIs(node.lnode.pnode, node)
        self.assertIs(node.rnode.pnode, node)

    def test_add_rightleft(self):
        node = self.build(AVLTreeNode.add, [0, 2, 1])
        node = node.balance()
        self.assertEqual(node.value, 1)
        self.assertEqual(node.lnode.value, 0)
        self.assertEqual(node.rnode.value, 2)
        self.assertIsNone(node.pnode)
        self.assertIs(node.lnode.pnode, node)
        self.assertIs(node.rnode.pnode, node)

    def test_balanced_add(self):
        node = self.build(AVLTreeNode.balanced_add, [0, -1, -2])
        self.assertEqual(node.value, -1)
        self.assertIsNone(node.pnode)
        self.assertEqual(node.lnode.value, -2)
        self.assertIs(node.lnode.pnode, node)
        self.assertEqual(node.rnode.value, 0)
        self.assertIs(node.rnode.pnode, node)
        node = self.build(AVLTreeNode.balanced_add, [0, 1, 2])
        self.assertEqual(node.value, 1)
        self.assertIsNone(node.pnode)
        self.assertEqual(node.lnode.value, 0)
        self.assertIs(node.lnode.pnode, node)
        self.assertEqual(node.rnode.value, 2)
        self.assertIs(node.rnode.pnode, node)
        node = self.build(AVLTreeNode.balanced_add, [0, -2, -1])
        self.assertEqual(node.value, -1)
        self.assertIsNone(node.pnode)
        self.assertEqual(node.lnode.value, -2)
        self.assertIs(node.lnode.pnode, node)
        self.assertEqual(node.rnode.value, 0)
        self.assertIs(node.rnode.pnode, node)
        node = self.build(AVLTreeNode.balanced_add, [0, 1, 2])
        self.assertEqual(node.value, 1)
        self.assertIsNone(node.pnode)
        self.assertEqual(node.lnode.value, 0)
        self.assertIs(node.lnode.pnode, node)
        self.assertEqual(node.rnode.value, 2)
        self.assertIs(node.rnode.pnode, node)
        node = self.build(AVLTreeNode.balanced_add, [0, 1, 2, 3, 4])
        self.assertEqual(node.value, 1)
        self.assertEqual(node.lnode.value, 0)
        self.assertEqual(node.rnode.value, 3)
        self.assertEqual(node.rnode.lnode.value, 2)
        self.assertEqual(node.rnode.rnode.value, 4)

    def test_finding_notfound(self):
        node = self.build(AVLTreeNode.balanced_add, [0, -1, 1])
        self.assertFalse(node.find(42))

    def test_finding_found(self):
        node = self.build(AVLTreeNode.balanced_add, [0, -1, 1])
        self.assertTrue(node.find(0))
        self.assertTrue(node.find(1))
        self.assertTrue(node.find(-1))

    def test_delete_nonexists(self):
        node = self.build(AVLTreeNode.balanced_add, [0])
        new_node, result = node.delete(42)
        self.assertEqual(new_node, node)
        self.assertFalse(result)

    def test_delete_exists(self):
        node = self.build(AVLTreeNode.balanced_add, [0])
        new_node, result = node.delete(0)
        self.assertIsNone(new_node)
        self.assertNotEqual(new_node, node)
        self.assertTrue(result)
        node = self.build(AVLTreeNode.balanced_add, [0, -1])
        new_node, result = node.delete(0)
        self.assertIsNotNone(new_node)
        self.assertNotEqual(new_node, node)
        self.assertTrue(result)
        node = self.build(AVLTreeNode.balanced_add, [0, 1])
        new_node, result = node.delete(0)
        self.assertIsNotNone(new_node)
        self.assertNotEqual(new_node, node)
        self.assertTrue(result)
        node = self.build(AVLTreeNode.balanced_add, [0, -1, 1])
        new_node, result = node.delete(0)
        self.assertIsNotNone(new_node)
        self.assertTrue(result)
        self.assertIn(new_node.value, (-1, 1))
        self.assertIs((new_node.lnode or new_node.rnode).pnode, new_node)
        node = self.build(AVLTreeNode.balanced_add, range(-3, 4))
        deletes = (1, 3, -2, -1, 2, 0, -3)
        for i, v in enumerate(deletes):
            node, result = node.delete(v)
            self.assertTrue(result)
            for x in deletes[i + 1:]:
                self.assertTrue(node.find(x))

    def test_inorder(self):
        node = self.build(AVLTreeNode.balanced_add, [0, -2, -3, -1, 2, 1, 3])
        self.assertEqual(node.inorder(), (-3, -2, -1, 0, 1, 2, 3))
