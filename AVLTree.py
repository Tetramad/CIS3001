from typing import Any, Optional, Tuple, Callable


class AVLTreeNode:
    def __init__(
        self,
        value: Any,
        pnode: Optional['AVLTreeNode'] = None,
        lnode: Optional['AVLTreeNode'] = None,
        rnode: Optional['AVLTreeNode'] = None,
        height: int = 1
    ):
        self.value = value
        self.pnode = pnode
        self.lnode = lnode
        self.rnode = rnode
        self.height = height

    def add(self, x: Any) -> 'AVLTreeNode':
        node = self
        ps = []
        while x < node.value and node.lnode or x > node.value and node.rnode:
            if x < node.value:
                ps.append(-1)
                assert node.lnode is not None
                node = node.lnode
            else:
                ps.append(+1)
                assert node.rnode is not None
                node = node.rnode
        if node.value == x:
            return self
        else:
            if x < node.value:
                node.lnode = AVLTreeNode(x, pnode=node)
            else:
                node.rnode = AVLTreeNode(x, pnode=node)
            for d in reversed(ps):
                node.height = node._height()
                node = node.pnode
                if d == -1:
                    node.lnode = node.lnode._balance()
                else:
                    node.rnode = node.rnode._balance()
            node.height = node._height()
            return node._balance()

    def _height(self):
        return self._calculate_height()

    def _balance(self) -> 'AVLTreeNode':
        factor = self._balance_factor()
        if factor not in (-2, 2):
            return self
        if factor == 2:
            assert self.lnode is not None
            factor = self.lnode._balance_factor()
            if factor == 1:
                a, b = self, self.lnode
                a.lnode, b.rnode = b.rnode, a
                b.pnode, a.pnode = a.pnode, b
                a.height = a._height()
                b.height = b._height()
                return b
            else:
                assert self.lnode.rnode is not None
                a, b, c = self, self.lnode, self.lnode.rnode
                b.rnode, c.lnode = c.lnode, b
                a.lnode, c.rnode = c.rnode, a
                c.pnode, a.pnode, b.pnode = a.pnode, c, c
                a.height = a._height()
                b.height = b._height()
                c.height = c._height()
                return c
        else:
            assert self.rnode is not None
            factor = self.rnode._balance_factor()
            if factor == -1:
                a, b = self, self.rnode
                a.rnode, b.lnode = b.lnode, a
                b.pnode, a.pnode = a.pnode, b
                a.height = a._height()
                b.height = b._height()
                return b
            else:
                assert self.rnode.lnode is not None
                a, b, c = self, self.rnode, self.rnode.lnode
                b.lnode, c.rnode = c.rnode, b
                a.rnode, c.lnode = c.lnode, a
                c.pnode, a.pnode, b.pnode = a.pnode, c, c
                a.height = a._height()
                b.height = b._height()
                c.height = c._height()
                return c

    def _lheight(self) -> int:
        return self.lnode and self.lnode.height or 0

    def _rheight(self) -> int:
        return self.rnode and self.rnode.height or 0

    def _balance_factor(self) -> int:
        return self._lheight() - self._rheight()

    def _calculate_height(self) -> int:
        return max(
            self.lnode.height if self.lnode else 0,
            self.rnode.height if self.rnode else 0
        ) + 1

    def balance(self) -> 'AVLTreeNode':
        factor = self._balance_factor()
        if factor not in (-2, 2):
            return self
        if factor == -2:
            assert self.rnode is not None
            lheight = self.rnode._lheight()
            rheight = self.rnode._rheight()
            if lheight - rheight <= 0:  # RR
                a, b = self, self.rnode
                a.rnode, b.lnode = b.lnode, a
                b.pnode, a.pnode = a.pnode, b
                a.height = a._calculate_height()
                b.height = b._calculate_height()
                return b
            else:  # RL
                assert self.rnode.lnode is not None
                a, b, c = self, self.rnode, self.rnode.lnode
                b.lnode, c.rnode = c.rnode, b
                a.rnode, c.lnode = c.lnode, a
                c.pnode, a.pnode, b.pnode = a.pnode, c, c
                a.height = a._calculate_height()
                b.height = b._calculate_height()
                c.height = c._calculate_height()
                return c
        else:
            assert self.lnode is not None
            lheight = self.lnode._lheight()
            rheight = self.lnode._rheight()
            if lheight - rheight >= 0:  # LL
                a, b = self, self.lnode
                a.lnode, b.rnode = b.rnode, a
                b.pnode, a.pnode = a.pnode, b
                a.height = a._calculate_height()
                b.height = b._calculate_height()
                return b
            else:  # LR
                assert self.lnode.rnode is not None
                a, b, c = self, self.lnode, self.lnode.rnode
                b.rnode, c.lnode = c.lnode, b
                a.lnode, c.rnode = c.rnode, a
                c.pnode, a.pnode, b.pnode = a.pnode, c, c
                a.height = a._calculate_height()
                b.height = b._calculate_height()
                c.height = c._calculate_height()
                return c

    def balanced_add(self, x: Any) -> 'AVLTreeNode':
        if self.value > x:
            if self.lnode:
                self.lnode = self.lnode.balanced_add(x)
            else:
                self.lnode = AVLTreeNode(x, pnode=self)
        elif self.value < x:
            if self.rnode:
                self.rnode = self.rnode.balanced_add(x)
            else:
                self.rnode = AVLTreeNode(x, pnode=self)
        new_self = self.balance()
        new_self.height = new_self._calculate_height()
        return new_self

    def find(self, x: Any) -> bool:
        if x < self.value and self.lnode:
            return self.lnode.find(x)
        elif x > self.value and self.rnode:
            return self.rnode.find(x)
        else:
            return x == self.value

    def delete(self, x: Any) -> Tuple[Optional['AVLTreeNode'], bool]:
        if self.value > x:
            if self.lnode is not None:
                self.lnode, result = self.lnode.delete(x)
                self.height = self._calculate_height()
                return self.balance(), result
            else:
                return self, False
        elif self.value < x:
            if self.rnode is not None:
                self.rnode, result = self.rnode.delete(x)
                self.height = self._calculate_height()
                return self.balance(), result
            else:
                return self, False
        else:
            if self.lnode is None and self.rnode is None:
                return None, True
            elif self.lnode is not None and self.rnode is None:
                self.lnode.pnode = None
                return self.lnode, True
            elif self.lnode is None and self.rnode is not None:
                self.rnode.pnode = None
                return self.rnode, True
            else:
                candidate = self.rnode
                while candidate.lnode:
                    candidate = candidate.lnode
                successor = candidate
                assert successor is not None
                assert type(successor.pnode) is AVLTreeNode
                if successor is self.rnode:
                    successor.lnode = self.lnode
                    assert self.lnode is not None
                    self.lnode.pnode = successor
                    successor.pnode = self.pnode
                    if self.pnode:
                        self.pnode.lnode = successor
                else:
                    successor.pnode.lnode = successor.rnode
                    pnode = successor.pnode
                    while pnode is not self:
                        pnode = pnode.balance().pnode
                    successor.pnode = self.pnode
                    successor.lnode = self.lnode
                    if self.lnode:
                        self.lnode.pnode = successor
                    successor.rnode = self.rnode
                    if self.rnode:
                        self.rnode.pnode = successor
                successor.height = successor._calculate_height()
                return successor.balance(), True

    def inorder(
            self,
            visit: Callable[['AVLTreeNode'], Any] = lambda x: x.value
    ) -> Tuple[Any, ...]:
        return (
            *(self.lnode.inorder(visit) if self.lnode else ()),
            visit(self),
            *(self.rnode.inorder(visit) if self.rnode else ())
        )

    def preorder(
        self,
        visit: Callable[['AVLTreeNode'], Any] = lambda x: x.value
    ) -> Tuple[Any, ...]:
        return (
            visit(self),
            *(self.lnode.preorder(visit) if self.lnode else ()),
            *(self.rnode.preorder(visit) if self.rnode else ())
        )

    def postorder(
        self,
        visit: Callable[['AVLTreeNode'], Any] = lambda x: x.value
    ) -> Tuple[Any, ...]:
        return (
            *(self.lnode.postorder(visit) if self.lnode else ()),
            *(self.rnode.postorder(visit) if self.rnode else ()),
            visit(self)
        )
