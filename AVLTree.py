# pyright: reportOptionalMemberAccess=none
class AVLTreeNode:
    def __init__(self, x):
        self.value = x
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
        elif self.value < x:
            if self.rnode:
                self.rnode.add(x)
            else:
                self.rnode = AVLTreeNode(x)
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
                return b
            else:  # RL
                a, b, c = self, self.rnode, self.rnode.lnode
                b.lnode, c.rnode = c.rnode, b
                a.rnode, c.lnode = c.lnode, a
                return c
        else:
            lheight = self.lnode.lnode and self.lnode.lnode.height() or 0
            rheight = self.lnode.rnode and self.lnode.rnode.height() or 0
            if lheight - rheight >= 0:  # LL
                a, b = self, self.lnode
                a.lnode, b.rnode = b.rnode, a
                return b
            else:  # LR
                a, b, c = self, self.lnode, self.lnode.rnode
                b.rnode, c.lnode = c.lnode, b
                a.lnode, c.rnode = c.rnode, a
                return c

    def balanced_add(self, x):
        if self.value > x:
            if self.lnode:
                self.lnode = self.lnode.balanced_add(x)
            else:
                self.lnode = AVLTreeNode(x)
        elif self.value < x:
            if self.rnode:
                self.rnode = self.rnode.balanced_add(x)
            else:
                self.rnode = AVLTreeNode(x)
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
                _, _ = self.lnode.delete(x)
            else:
                return self, False
        elif self.value < x:
            if self.rnode is not None:
                _, _ = self.rnode.delete(x)
            else:
                return self, False
        else:
            if self.lnode is None and self.rnode is None:
                return None, True
            elif self.lnode is not None and self.rnode is None:
                return self.lnode, True
            elif self.lnode is None and self.rnode is not None:
                return self.rnode, True
            else:
                pass
        return self, False
