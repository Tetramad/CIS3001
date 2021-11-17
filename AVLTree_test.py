# pyright: reportOptionalMemberAccess=none
from AVLTree import AVLTreeNode
from unittest import TestCase


class AVLTreeNodeTest(TestCase):
    def build(self, func, iterable):
        node = AVLTreeNode(iterable[0])
        for v in iterable[1:]:
            if isinstance((n := func(node, v)), AVLTreeNode):
                node = n
        return node

    def assertNode(self, node, **kwargs):
        for k, v in kwargs.items():
            self.assertEqual(getattr(node, k), v)

    def test_creation(self):
        node = AVLTreeNode(42)
        self.assertNode(
            node,
            value=42,
            pnode=None,
            lnode=None,
            rnode=None,
            height=1
        )

    def test_add_left(self):
        node = self.build(AVLTreeNode.add, [0, -1])
        self.assertNode(node.lnode, value=-1, pnode=node)
        self.assertNode(node, height=2)

    def test_add_right(self):
        node = self.build(AVLTreeNode.add, [0, 1])
        self.assertNode(node.rnode, value=1, pnode=node)
        self.assertNode(node, height=2)

    def test_same_value(self):
        node = self.build(AVLTreeNode.add, [0, 0])
        self.assertNode(
            node,
            value=0,
            pnode=None,
            lnode=None,
            rnode=None,
            height=1
        )

    def test_add_leftleft(self):
        node = self.build(AVLTreeNode.add, [0, -1, -2])
        self.assertNode(node, value=-1, pnode=None, height=2)
        self.assertNode(node.lnode, value=-2, pnode=node, height=1)
        self.assertNode(node.rnode, value=0, pnode=node, height=1)

    def test_add_rightright(self):
        node = self.build(AVLTreeNode.add, [0, 1, 2])
        self.assertNode(node, value=1, pnode=None, height=2)
        self.assertNode(node.lnode, value=0, pnode=node, height=1)
        self.assertNode(node.rnode, value=2, pnode=node, height=1)

    def test_add_leftright(self):
        node = self.build(AVLTreeNode.add, [0, -2, -1])
        self.assertNode(node, value=-1, pnode=None, height=2)
        self.assertNode(node.lnode, value=-2, pnode=node, height=1)
        self.assertNode(node.rnode, value=0, pnode=node, height=1)

    def test_add_rightleft(self):
        node = self.build(AVLTreeNode.add, [0, 2, 1])
        self.assertNode(node, value=1, pnode=None, height=2)
        self.assertNode(node.lnode, value=0, pnode=node, height=1)
        self.assertNode(node.rnode, value=2, pnode=node, height=1)

    def test_add(self):
        node = self.build(AVLTreeNode.add, [0, 1, 2, 3, 4])
        self.assertNode(node, value=1, height=3)
        self.assertNode(node.lnode, value=0, height=1)
        self.assertNode(node.rnode, value=3, height=2)
        self.assertNode(node.rnode.lnode, value=2, height=1)
        self.assertNode(node.rnode.rnode, value=4, height=1)

    def test_finding_failed(self):
        node = self.build(AVLTreeNode.add, [0, -2, 2])
        for i in (-3, -1, 1, 3):
            self.assertFalse(node.find(i))

    def test_finding_success(self):
        node = self.build(AVLTreeNode.add, [0, -1, 1])
        for i in (-1, 0, 1):
            self.assertTrue(node.find(i))

    def assertDeleteResult(self, node, x, enode, eresult):
        anode, aresult = node.delete(x)
        self.assertIs(anode, enode)
        if eresult:
            self.assertTrue(aresult)
        else:
            self.assertFalse(aresult)
        return anode

    def test_deleting_failed(self):
        node = self.build(AVLTreeNode.add, [0])
        self.assertDeleteResult(node, 42, node, False)

    def test_deleting_success(self):
        node = self.build(AVLTreeNode.add, [0])
        self.assertDeleteResult(node, 0, None, True)
        node = self.build(AVLTreeNode.add, [0, -1])
        self.assertDeleteResult(node, 0, node.lnode, True)
        node = self.build(AVLTreeNode.add, [0, 1])
        self.assertDeleteResult(node, 0, node.rnode, True)
        node = self.build(AVLTreeNode.add, [0, -1, 1])
        self.assertDeleteResult(node, 0, node.rnode, True)
        node = self.build(AVLTreeNode.add, [0, -1, 1])
        node = self.assertDeleteResult(node, -1, node, True)
        node = self.assertDeleteResult(node, 1, node, True)
        self.assertEqual(node.height, 1)
        node = self.build(AVLTreeNode.add, [4, 1, 5, 0, 2, 6, 3])
        node = self.assertDeleteResult(node, 6, node.lnode.rnode, True)
        for factor in node.inorder(lambda x: x._balance_factor()):
            self.assertIn(factor, (-1, 0, +1))

    def test_inorder(self):
        node = self.build(AVLTreeNode.add, (-1, 0, -2, 3, 1, -3, 2))
        #     -1
        #    /  \
        #   -2   1
        #  /   /  \
        # -3   0   3
        #         /
        #         2
        self.assertEqual(
            node.inorder(),
            (-3, -2, -1, 0, 1, 2, 3)
        )
        self.assertEqual(
            node.inorder(lambda x: x.height),
            (1, 2, 4, 1, 3, 1, 2)
        )
        self.assertEqual(
            node.inorder(lambda x: x._balance_factor()),
            (0, 1, -1, 0, -1, 0, 1)
        )

    def test_preorder(self):
        node = self.build(AVLTreeNode.add, (-1, 0, -2, 3, 1, -3, 2))
        #     -1
        #    /  \
        #   -2   1
        #  /   /  \
        # -3   0   3
        #         /
        #         2
        self.assertEqual(
            node.preorder(),
            (-1, -2, -3, 1, 0, 3, 2)
        )
        self.assertEqual(
            node.preorder(lambda x: x.height),
            (4, 2, 1, 3, 1, 2, 1)
        )
        self.assertEqual(
            node.preorder(lambda x: x._balance_factor()),
            (-1, 1, 0, -1, 0, 1, 0)
        )

    def test_postorder(self):
        node = self.build(AVLTreeNode.add, (-1, 0, -2, 3, 1, -3, 2))
        #     -1
        #    /  \
        #   -2   1
        #  /   /  \
        # -3   0   3
        #         /
        #         2
        self.assertEqual(
            node.postorder(),
            (-3, -2, 0, 2, 3, 1, -1)
        )
        self.assertEqual(
            node.postorder(lambda x: x.height),
            (1, 2, 1, 1, 2, 3, 4)
        )
        self.assertEqual(
            node.postorder(lambda x: x._balance_factor()),
            (0, 1, 0, 0, 1, -1, -1)
        )
