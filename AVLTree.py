# pyright: reportOptionalMemberAccess=none
class AVLTreeNode:
    def __init__(self, x):
        self.value = x
        self.pnode = None
        self.lnode = None
        self.rnode = None

    def height(self):
        lheight = self.lnode and self.lnode.height() or 0
        rheight = self.rnode and self.rnode.height() or 0
        return max(lheight, rheight) + 1

    def add(self, x):
        if self.value > x:
            if self.lnode:
                self.lnode.add(x)
            else:
                self.lnode = AVLTreeNode(x)
                self.lnode.pnode = self
        elif self.value < x:
            if self.rnode:
                self.rnode.add(x)
            else:
                self.rnode = AVLTreeNode(x)
                self.rnode.pnode = self
        else:
            pass

    def balance(self):
        lheight = self.lnode and self.lnode.height() or 0
        rheight = self.rnode and self.rnode.height() or 0
        if lheight - rheight not in (-2, 2):
            return self
        if lheight - rheight == -2:
            lheight = self.rnode.lnode and self.rnode.lnode.height() or 0
            rheight = self.rnode.rnode and self.rnode.rnode.height() or 0
            if lheight - rheight <= 0:  # RR
                a, b = self, self.rnode
                a.rnode, b.lnode = b.lnode, a
                b.pnode, a.pnode = a.pnode, b
                return b
            else:  # RL
                a, b, c = self, self.rnode, self.rnode.lnode
                b.lnode, c.rnode = c.rnode, b
                a.rnode, c.lnode = c.lnode, a
                c.pnode, a.pnode, b.pnode = a.pnode, c, c
                return c
        else:
            lheight = self.lnode.lnode and self.lnode.lnode.height() or 0
            rheight = self.lnode.rnode and self.lnode.rnode.height() or 0
            if lheight - rheight >= 0:  # LL
                a, b = self, self.lnode
                a.lnode, b.rnode = b.rnode, a
                b.pnode, a.pnode = a.pnode, b
                return b
            else:  # LR
                a, b, c = self, self.lnode, self.lnode.rnode
                b.rnode, c.lnode = c.lnode, b
                a.lnode, c.rnode = c.rnode, a
                c.pnode, a.pnode, b.pnode = a.pnode, c, c
                return c

    def balanced_add(self, x):
        if self.value > x:
            if self.lnode:
                self.lnode = self.lnode.balanced_add(x)
            else:
                self.lnode = AVLTreeNode(x)
            self.lnode.pnode = self
        elif self.value < x:
            if self.rnode:
                self.rnode = self.rnode.balanced_add(x)
            else:
                self.rnode = AVLTreeNode(x)
            self.rnode.pnode = self
        else:
            pass
        return self.balance()

    def find(self, x):
        if self.value > x and self.lnode:
            return self.lnode.find(x)
        elif self.value < x and self.rnode:
            return self.rnode.find(x)
        else:
            return True if self.value == x else False

    def delete(self, x):
        if self.value > x:
            if self.lnode is not None:
                self.lnode, result = self.lnode.delete(x)
                return self, result
            else:
                return self, False
        elif self.value < x:
            if self.rnode is not None:
                self.rnode, result = self.rnode.delete(x)
                return self, result
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
                return successor, True

    def inorder(self):
        return (
            *(self.lnode.inorder() if self.lnode else ()),
            self.value,
            *(self.rnode.inorder() if self.rnode else ())
        )
