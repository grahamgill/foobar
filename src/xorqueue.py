import operator


def xorqueue(start, length):
    """
        xorqueue(start: int, length: int)
    Equivalent to forming a square matrix of size `length**2`, consisting of the integers
    from `start` to `start + length**2 -1` inclusive, in row major order, then `xor`ing the 
    entries in the upper anti-triangle of the matrix as the return value.

    `start` should be nonnegative.
    `length` should be strictly positive, and such that `start + length**2 - 1 < 2,000,000,000`

    E.g.
    `xorqueue(17,4)` is equivalent to generating the matrix
    ```
    17 18 19 20
    21 22 23 24
    25 26 27 28
    29 30 31 32
    ```
    then `xor`ing together the integers of the upper anti-triangle
    ```
    17 18 19 20
    21 22 23
    25 26
    29
    ```
    to give the result 14.

    Queue can't wrap after worker 2000000000, because they'd reorganise themselves to be in
    increasing ID order and with no gaps.
    """

    assert start >= 0, "start promised to be between nonnegative, but got " + \
        repr(start)
    assert length >= 1, "length promised to be positive, but got " + \
        repr(length)
    assert start - 1 + length**2 <= 2000000000, """all worker IDs promised to lie between 0 and 2000000000 inclusive,
            and be strictly increasing with no gaps, but then implied final ID at checkpoint is """ + \
        repr(start - 1 + length**2)

    checkpointqueue = [k for j in range(0, length) for k in range(
        start + j * length, start + (j + 1) * length - j)]
    # print(checkpointqueue)

    return reduce(operator.xor, checkpointqueue, 0)
