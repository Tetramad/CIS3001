def heapsort(xs):
    heapify(xs)
    return [heappop(xs) for _ in range(len(xs))]


def heapify(xs):
    if len(xs) == 0:
        return xs
    for i in range(len(xs) - 1, -1, -1):
        siftdown(xs, i)
    return xs


def siftdown(xs, i):
    s = [i]
    while s:
        i = s.pop()
        smallest_i = i
        if len(xs) > 2 * i + 1 and xs[2 * i + 1] < xs[smallest_i]:
            smallest_i = 2 * i + 1
        if len(xs) > 2 * i + 2 and xs[2 * i + 2] < xs[smallest_i]:
            smallest_i = 2 * i + 2
        if smallest_i != i:
            xs[smallest_i], xs[i] = xs[i], xs[smallest_i]
            s.append(smallest_i)


def heappop(xs):
    xs[0], xs[-1] = xs[-1], xs[0]
    x = xs.pop()
    siftdown(xs, 0)
    return x
