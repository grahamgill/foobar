def pieslices(s): # foobar doesn't like the type annotation `s: str`
    """
        `pieslices(s: str)`
    Given a string `s` of length at most `MAX_PIE_MandMs` representing M&Ms arranged in a circle around the circular pie,
    return the maximum number of pieces into which the pie can be cut radially so that each piece has the same sequence of
    M&Ms along its edge.

    Clearly the smallest return value is 1, when there is no repeating subsequence which concatenates into the whole string
    `s`, and the largest return value is `len(s)`, when `s` consists of one single character repeated.

    Moreover, the return value will always be a divisor of `len(s)`, so we can limit our searches to divisors
    only. Without further use cases/requirements, we'll assume that computing the divisors for `s` using the Euclidean
    algorithm is good enough, which it certainly is for small maximum string lengths. We won't try to memoise lists of divisors,
    precompute them for every possible length up to small `MAX_PIE_MandMs`, or compute a new divisor only when needed, (since the list will be short,)
    without having more data in favour of needing to do so.

    A zero length `s` results in zero pie slices.
    """
    MAX_PIE_MandMs = 200

    numMandMs = len(s)
    assert numMandMs <= MAX_PIE_MandMs, "We were promised s of length <= " + \
        repr(MAX_PIE_MandMs)
    if numMandMs == 0:
        return 0

    factorpairs = [(x, int(numMandMs / x))
                   for x in range(1, numMandMs + 1) if numMandMs % x == 0]

    # now 1 <= len(s) <= MAX_PIE_MandMs
    # order of factorpairs (x,y) is by increasing length of sequence x, and thus
    # decreasing number of repetitions possible (y) in s
    # So we stop at the first match, which is the shortest substring to match and
    # thus gives the largest number of pieces.
    for (x, y) in factorpairs:
        if s[:x] * y == s:
            break

    return y
