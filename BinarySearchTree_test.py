# pyright: reportOptionalMemberAccess=none
from BinarySearchTree import BinarySearchTreeNode
from unittest import TestCase


class BinarySearchTreeNodeTest(TestCase):
    def build(self, func, iterable):
        node = BinarySearchTreeNode(iterable[0])
        for v in iterable[1:]:
            if (n := func(node, v)) is not None:
                node = n
        return node

    def test_creation(self):
        node = self.build(BinarySearchTreeNode.add, [42])
        self.assertEqual(node.value, 42)
        self.assertIsNone(node.pnode)
        self.assertIsNone(node.lnode)
        self.assertIsNone(node.rnode)

    def test_add_left(self):
        node = self.build(BinarySearchTreeNode.add, [0, -1])
        self.assertEqual(node.lnode.value, -1)
        self.assertIs(node.lnode.pnode, node)

    def test_add_right(self):
        node = self.build(BinarySearchTreeNode.add, [0, 1])
        self.assertEqual(node.rnode.value, 1)
        self.assertIs(node.rnode.pnode, node)

    def test_add_same_value(self):
        node = self.build(BinarySearchTreeNode.add, [0, 0])
        self.assertEqual(node.value, 0)
        self.assertIsNone(node.pnode)
        self.assertIsNone(node.lnode)
        self.assertIsNone(node.rnode)

    def test_add_leftleft_leftright(self):
        node = self.build(BinarySearchTreeNode.add, [0, -2, -3, -1])
        self.assertEqual(node.lnode.lnode.value, -3)
        self.assertIs(node.lnode.lnode.pnode, node.lnode)
        self.assertEqual(node.lnode.rnode.value, -1)
        self.assertIs(node.lnode.rnode.pnode, node.lnode)

    def test_add_rightleft_rightright(self):
        node = self.build(BinarySearchTreeNode.add, [0, 2, 3, 1])
        self.assertEqual(node.rnode.rnode.value, 3)
        self.assertIs(node.rnode.rnode.pnode, node.rnode)
        self.assertEqual(node.rnode.lnode.value, 1)
        self.assertIs(node.rnode.lnode.pnode, node.rnode)

    def test_finding_notfound(self):
        node = self.build(BinarySearchTreeNode.add, [0, -1, 1])
        self.assertFalse(node.find(42))

    def test_finding_found(self):
        node = self.build(BinarySearchTreeNode.add, [0, -1, 1])
        self.assertTrue(node.find(0))
        self.assertTrue(node.find(-1))
        self.assertTrue(node.find(1))

    def test_maximum(self):
        node = self.build(BinarySearchTreeNode.add, [0, -1, -2, 1, 2])
        self.assertEqual(node.maximum().value, 2)

    def test_minimum(self):
        node = self.build(BinarySearchTreeNode.add, [0, 2, 1, -2, -1])
        self.assertEqual(node.minimum().value, -2)

    def test_successor(self):
        node = self.build(BinarySearchTreeNode.add, [0, 2, 1, 3])
        self.assertEqual(node.successor().value, 1)
        node = self.build(BinarySearchTreeNode.add, [0])
        self.assertIsNone(node.successor())
        node = self.build(BinarySearchTreeNode.add, [-1, 0])
        node = node.rnode
        self.assertIsNone(node.successor())
        node = self.build(BinarySearchTreeNode.add, [1, -1, 0])
        node = node.lnode.rnode
        self.assertEqual(node.successor().value, 1)
        node = self.build(BinarySearchTreeNode.add, [1, 0])
        node = node.lnode
        self.assertEqual(node.successor().value, 1)

    def test_predecessor(self):
        node = self.build(BinarySearchTreeNode.add, [0, -2, -3, -1])
        self.assertEqual(node.predecessor().value, -1)
        node = self.build(BinarySearchTreeNode.add, [0])
        self.assertIsNone(node.predecessor())
        node = self.build(BinarySearchTreeNode.add, [1, 0])
        node = node.lnode
        self.assertIsNone(node.predecessor())
        node = self.build(BinarySearchTreeNode.add, [-1, 1, 0])
        node = node.rnode.lnode
        self.assertEqual(node.predecessor().value, -1)
        node = self.build(BinarySearchTreeNode.add, [-1, 0])
        node = node.rnode
        self.assertEqual(node.predecessor().value, -1)

    def test_deletion_nonexists(self):
        node = self.build(BinarySearchTreeNode.add, [0, -1, 1])
        new_node, result = node.delete(42)
        self.assertEqual(new_node, node)
        self.assertFalse(result)
        new_node, result = node.delete(-42)
        self.assertEqual(new_node, node)
        self.assertFalse(result)

    def test_deletion_exists(self):
        node = self.build(BinarySearchTreeNode.add, [0])
        new_node, result = node.delete(0)
        self.assertIsNone(new_node)
        self.assertTrue(result)
        node = self.build(BinarySearchTreeNode.add, [0, -1])
        new_node, result = node.delete(0)
        self.assertIsNotNone(new_node)
        self.assertEqual(new_node.value, -1)
        self.assertIsNone(new_node.pnode)
        self.assertTrue(result)
        node = self.build(BinarySearchTreeNode.add, [0, 1])
        new_node, result = node.delete(0)
        self.assertIsNotNone(new_node)
        self.assertEqual(new_node.value, 1)
        self.assertIsNone(new_node.pnode)
        self.assertTrue(result)
        node = self.build(BinarySearchTreeNode.add, [0, -1, 1])
        new_node, result = node.delete(0)
        self.assertIsNotNone(new_node)
        self.assertIn(new_node.value, (-1, 1))
        self.assertIsNone(new_node.pnode)
        self.assertTrue(result)
        node = self.build(BinarySearchTreeNode.add, [1, -2, 0, -1])
        node = node.lnode.rnode
        new_node, result = node.delete(0)
        self.assertEqual(new_node.value, -1)
        self.assertTrue(result)
        self.assertEqual(new_node.pnode.value, -2)
        node = self.build(BinarySearchTreeNode.add, [0, -1, 1])
        new_node, result = node.delete(-1)
        self.assertIs(new_node, node)
        self.assertTrue(result)
        self.assertEqual(node.inorder(), (0, 1))
        new_node, result = node.delete(1)
        self.assertIs(new_node, node)
        self.assertTrue(result)
        self.assertEqual(node.inorder(), (0,))
        new_node, result = node.delete(0)
        self.assertIsNone(new_node)
        self.assertTrue(result)

    def test_inorder(self):
        node = self.build(BinarySearchTreeNode.add, [0, -2, -3, -1, 2, 1, 3])
        self.assertEqual(node.inorder(), (-3, -2, -1, 0, 1, 2, 3))

    def test_preorder(self):
        node = self.build(BinarySearchTreeNode.add, [0, -2, -3, -1, 2, 1, 3])
        self.assertEqual(node.preorder(), (0, -2, -3, -1, 2, 1, 3))

    def test_postorder(self):
        node = self.build(BinarySearchTreeNode.add, [0, -2, -3, -1, 2, 1, 3])
        self.assertEqual(node.postorder(), (-3, -1, -2, 1, 3, 2, 0))
