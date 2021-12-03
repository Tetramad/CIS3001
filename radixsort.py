from collections import deque


def radixsort(xs):
    if not xs:
        return list(xs)
    if min(xs) < 0:
        raise ValueError()
    bs = [deque([]) for _ in range(10)]
    nbs = [deque([]) for _ in range(10)]
    n = len(str(max(xs)))
    for x in xs:
        bs[x % 10].append(x)
    for i in range(1, n):
        for b in bs:
            while b:
                x = b.popleft()
                nbs[x % (10 ** (i + 1)) // (10 ** i)].append(x)
        bs, nbs = nbs, bs
    res = []
    for b in bs:
        while b:
            res.append(b.popleft())
    return res
