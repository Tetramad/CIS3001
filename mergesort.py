def mergesort(xs):
    if len(xs) in (0, 1):
        return [*xs]
    p = len(xs) // 2
    lh = mergesort(xs[:p])
    rh = mergesort(xs[p:])
    acc = []
    while len(lh) != 0 and len(rh) != 0:
        if lh[0] < rh[0]:
            acc.append(lh[0])
            lh = lh[1:]
        else:
            acc.append(rh[0])
            rh = rh[1:]
    return [*acc, *lh, *rh]
