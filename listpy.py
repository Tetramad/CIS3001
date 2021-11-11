from collections.abc import MutableSequence


class listpy(MutableSequence):
    def __init__(self, iterable=(), /):
        self.inner = None
        self.extend(iterable)

    def __len__(self):
        size = 0
        node = self.inner
        while node is not None:
            node = node[1]
            size += 1
        return size

    def __getitem__(self, key):
        head = [None, self.inner]
        node = head
        for _ in range(key):
            if node[1] == None:
                raise IndexError('listpy index out of range')
            node = node[1]
        if node[1] == None:
            raise IndexError('listpy index out of range')
        else:
            return node[1][0]

    def __setitem__(self, key, value):
        if isinstance(key, int):
            head = [None, self.inner]
            node = head
            for _ in range(key):
                if node[1] is None:
                    raise IndexError('listpy assignment index out of range')
                node = node[1]
            if node[1] is None:
                node[1] = [value, node[1]]  # append to end
            else:
                node[1][0] = value  # overwrite to exist item
            self.inner = head[1]
        elif isinstance(key, slice):
            start = key.start if key.start is not None else 0
            stop = key.stop if key.stop is not None else len(self)
            head = [None, self.inner]
            prev = head
            node = head[1]
            for _ in range(start):
                if node is None:
                    break
                prev = node
                node = node[1]
            for _ in range(start, stop):
                if node is None:
                    break
                node = node[1]
            for v in value:
                prev[1] = [v, None]
                prev = prev[1]
            prev[1] = node
            self.inner = head[1]
        else:
            pass

    def __delitem__(self, key):
        head = [None, self.inner]
        prev = head
        node = head[1]
        for _ in range(key):
            if node is None:
                raise IndexError('')
            prev = node
            node = node[1]
        if node is None:
            raise IndexError('')
        else:
            prev[1] = node[1]
        self.inner = head[1]

    def insert(self, key, value):
        self[key:key] = [value]
