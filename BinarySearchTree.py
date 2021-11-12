class BinarySearchTreeNode:
    def __init__(self, x):
        self.value = x
        self.pnode = None
        self.lnode = None
        self.rnode = None

    def add(self, x):
        prev, curr = None, self
        while curr is not None:
            if curr.value > x:
                prev, curr = curr, curr.lnode
            elif curr.value < x:
                prev, curr = curr, curr.rnode
            else:
                return
        if x < prev.value:
            prev.lnode = BinarySearchTreeNode(x)
            prev.lnode.pnode = prev
        else:
            prev.rnode = BinarySearchTreeNode(x)
            prev.rnode.pnode = prev

    def find(self, x):
        candidate = self
        while candidate is not None:
            if candidate.value > x:
                candidate = candidate.lnode
            elif candidate.value < x:
                candidate = candidate.rnode
            else:
                return True
        return False

    def maximum(self):
        candidate = self
        while candidate.rnode is not None:
            candidate = candidate.rnode
        return candidate

    def minimum(self):
        candidate = self
        while candidate.lnode is not None:
            candidate = candidate.lnode
        return candidate

    def successor(self):
        if self.rnode is not None:
            return self.rnode.minimum()
        elif self.pnode is None:
            return None
        else:
            candidate = self
            while (candidate := candidate.pnode):
                if candidate.lnode and candidate.lnode.pnode is candidate:
                    return candidate
            return None

    def predecessor(self):
        if self.lnode is not None:
            return self.lnode.maximum()
        elif self.pnode is None:
            return None
        else:
            candidate = self
            while (candidate := candidate.pnode):
                if candidate.rnode and candidate.rnode.pnode is candidate:
                    return candidate
            return None

    def delete(self, x):
        if self.value > x:
            if self.lnode is None:
                return self, False
            else:
                new_node, result = self.lnode.delete(x)
                self.lnode = new_node
                return self, result
        elif self.value < x:
            if self.rnode is None:
                return self, False
            else:
                new_node, result = self.rnode.delete(x)
                self.rnode = new_node
                return self, result
        else:
            if self.lnode is None and self.rnode is None:
                return None, True
            elif self.lnode is not None and self.rnode is None:
                self.lnode.pnode = self.pnode
                return self.lnode, True
            elif self.lnode is None and self.rnode is not None:
                self.rnode.pnode = self.pnode
                return self.rnode, True
            else:
                candidate = self.rnode
                assert candidate is not None
                while candidate.lnode is not None:
                    candidate = candidate.lnode
                assert candidate.pnode is not None
                candidate.pnode.lnode = candidate.rnode
                if candidate.rnode:
                    candidate.rnode.pnode = candidate.pnode
                candidate.pnode = self.pnode
                candidate.lnode = self.lnode
                candidate.rnode = self.rnode
                return candidate, True

    def inorder(self):
        return (*(self.lnode.inorder() if self.lnode else ()),
                self.value,
                *(self.rnode.inorder() if self.rnode else ()))

    def preorder(self):
        return (self.value,
                *(self.lnode.preorder() if self.lnode else ()),
                *(self.rnode.preorder() if self.rnode else ()))

    def postorder(self):
        return (*(self.lnode.postorder() if self.lnode else ()),
                *(self.rnode.postorder() if self.rnode else ()),
                self.value)
