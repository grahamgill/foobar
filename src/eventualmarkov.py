from fractions import Fraction, gcd
from copy import deepcopy

def eventualmarkov(m):

    # get size of m
    n = len(m)
    for k in range(n):
        assert len(m[k]) == n, "Non-square matrix or non-matrix input m"
        for j in range(n):
            assert type(m[k][j]) == int, "Noninteger in matrix"
            assert m[k][j] >= 0, "Negative integer in matrix"
    
    # convert m to transition probabilities
    P = transition_probabilities(m, n)

    # rows with 1 on diagonal identify absorbing states, others identify transient states
    absorbing = []
    transient = []
    for k in range(n):
        if all(map(lambda x: x == 0, [P[k][j] for j in range(n) if j != k])) and P[k][k] == 1:
            absorbing.append(k)
        else:
            transient.append(k)
    n_absorbing = len(absorbing)
    n_transient = len(transient)

    # construct the linear system Ax = b, where unknown vector x represents the probability of absorption
    # into state k, beginning in state j = 0, ..., n-1. The A matrix is independent of k, but b depends on k.
    # In fact, since we'll row reduce A in exactly the same way for each k, instead of a vector b we can
    # "parallelize" the algorithm to do all vectors b at once, by assembling them into a matrix B.
    #
    # We can limit B to being n x q, where q is the number of absorbing states, since all entries of B in
    # columns corresponding to transient states will be 0.
    #
    # The linear equations representing the "eventual" state transitions are a small modification to P.
    # For absorbing states we don't need to change the row. For transient states we need to subtract 1
    # at the diagonal element of the row.
    # The columns of B, each representing the linear system that needs to be solved for a different absorbing state,
    # put a 1 in the absorbing state's row and 0 elsewhere.
    A = deepcopy(P)
    for k in transient:
        A[k][k] -= Fraction(1)
    B = []
    for k in range(n):
        B.append([Fraction()] * n_absorbing)
    for k in range(n_absorbing):
        B[absorbing[k]][k] = Fraction(1)

    # Next we do forward elimination on the augmented matrix [A|B], leading to a form
    # [U|B*] where U is upper triangular with only 1s and 0s on the diagonal.
    # We operate directly on A and B. No need to preserve them.
    forwardelimination(A, B, n)

    # Finally we do back substitution. This gives us a [E|B**] where E is a diagonal matrix
    # with only 1s and 0s on the diagonal.
    #
    # We're guaranteed at least one absorbing state that will
    # be reached from state 0. We're guaranteed to have no periodic states (absorbing cycles).
    # If the first column of m is entirely 0, then either state 0
    # is absorbing, in which case all of row 0 of m is 0 and we will have P[0][0] == A[0][0] == 1;
    # or state 0 is transient, in which case A[0][0] == -1. If m[0][0] > 0 and P[0][0] == 1, then state 0 can't be
    # transient, it's absorbing, so A[0][0] == 1. If m[0][0] == 0 but m[k][0] > 0 for some 
    # k > 0, then we'll swap rows during forwardelimination to get U[0][0] == 1. Finally if m[0][0] > 0 and
    # 0 < P[0][0] < 1, then state 0 is transient, so A[0][0] == P[0][0] - 1 < 0. Hence we'll always have
    # U[0][0] == E[0][0] == 1.
    #
    # We can make a similar argument about the other diagonal elements to show that E is just the square identity 
    # matrix. It's stated in the problem that every state will go to an absorbing state, which means E must be the identity
    # matrix. (We can assume the unobserved states are absorbing since there's no way to get to them from state 0.)
    #
    # Note that we only care about the first row of E, and we only care that it is of the 
    # form [1, 0, ..., 0]. x[0] is the probability of ending in state k starting in state 0, and (Ex)[0] == x[0]. Setting
    # x[0] sequentially to the elements of B**[0] gives the probabilities of landing in each absorbing state represented
    # by the columns of B.
    # 
    # Once again, we operate directly on A and B instead of introducing new matrices.
    backsubstitution(A, B, n)

    # At last, B[0] gives us what we want, and we just need to convert from fraction back to
    # integer and append the denominator.
    soln = convert_to_common_denominator(B[0])

    return soln


def transition_probabilities(m, n):
    """
        transition_probabilities(m, n)
    Compute transition probability matrix `P` from `n` x `n` problem input matrix `m`.
    `m` is assumed to have nonnegative integer entries and be square.
    
    A fully zero row in `m`, say row `k`, is another indicator of a terminal state. In this case
    we set `m[k][k] = 1` prior to computing `P`, so `m` may be modified by this procedure.
    
    The transition probabilities are just the observation counts of `m` divided by the row sums.
    Transitions probabilities are represented in `P` by Python `Fraction`.
    
    `P` is returned."""
    P = []

    for k in range(n):
        s = sum(m[k])

        # since nonnegative entries, indicates entire row is 0, so set state to be terminal
        if s == 0:
            m[k][k] = 1
            s = 1

        P.append([Fraction(c, s) for c in m[k]])

    return P


def forwardelimination(A, B, n):
    """
    Forward elimination on the augmented matrix `[A|B]`, leading to a form
    `[U|B*]` where `U` is upper triangular with only 1s and 0s on the diagonal.
    We operate directly on `A` and `B`. No need to preserve them.

    `A` is `n` x `n`, `B` is `n` x `q`.

    We expect entries of `A` and `B` to be `Fraction`s or `float`s. If `int`s,
    incorrect divisions will occur. If `Fraction`s, `Fraction`s will be returned.
    """
    for j in range(n):
        # if we don't have a pivot element
        if A[j][j] == 0:
            # find a nonzero in column j below row j
            k = j + 1
            while k < n:
                if A[k][j] != 0:
                    # swap rows k and j
                    swap(A, k, j)
                    swap(B, k, j)
                    break
                else:
                    k += 1

        # if we found a pivot and swapped it into row j
        # (if we didn't, rest of column j is 0 already)
        if A[j][j] != 0:
            # set pivot to 1 and scale row
            recip = 1 / A[j][j]
            A[j] = mul(A[j], recip)
            B[j] = mul(B[j], recip)

            # zero rest of column j below row j
            for k in range(j + 1, n):
                if A[k][j] != 0:
                    scalar = -A[k][j]
                    A[k] = add(A[k], mul(A[j], scalar))
                    B[k] = add(B[k], mul(B[j], scalar))

    return A, B


def backsubstitution(U, B, n):
    """
    `U` is upper triangular `n` x `n`, `B` is `n` x `q`, matrices of `Fraction`s or `float`s.
    Diagonal elements of `U` are 0 or 1.

    We back substitute from the bottom row of `U` back up to the top, then do again with the next to last row, etc.

    Modified `U` and `B` are returned. No need to preserve them.
    """
    for k in range(n - 1, 0, -1):
        for j in range(k - 1, -1, -1):
            if U[k][k] == 1 and U[j][k] != 0:
                scalar = -U[j][k]
                U[j] = add(U[j], mul(U[k], scalar))
                B[j] = add(B[j], mul(B[k], scalar))
            else:
                assert U[k][k] == 0 or U[j][k] == 0, "Unexpected U contents: (k,j) = " + repr((k,j)) + ", U[k][k] = " + repr(U[k][k]) + ", U[j][k] = " + repr(U[j][k])

    return U, B



def convert_to_common_denominator(v):
    """
    `v` is a vector of `Fraction`s. We convert each element of 
    `v` to a common denominator, and return the numerators in 
    a list with the denominator appended.
    """
    d = 1
    for f in v:
        d = lcm(d, f.denominator)
    
    v_ints = [f.numerator * (d // f.denominator) for f in v]
    v_ints.append(d)

    return v_ints


def lcm(p, q):
    """
    `p` and `q` are `int`s (or `Fraction`s) and the return is the least common multiple.

    We only care about positive inputs.
    """
    return p * (q // gcd(p, q))



def add(r1, r2):
    """
    Add rows `r1` and `r2`.
    """
    return [x + y for x, y in zip(r1, r2)]


def mul(r, s):
    """
    Multiply row `r` by scalar `s`.
    """
    return [x * s for x in r]


def swap(m, i, j):
    """
    Swap (exchange) rows `i` and `j` (0-based) of matrix `m`.
    Return the updated matrix.
    """
    m[i], m[j] = m[j], m[i]

    return m


def solution(m):
    """
    Name used by foobar.
    """
    return eventualmarkov(m)


# don't copy to solution
def tests():
    # test input matrices
    ms = []
    # solution vectors
    ss = []

    # doomsday fuel provided test case 1
    ms.append([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]])
    ss.append([7, 6, 8, 21])

    # doomsday fuel provided test case 2
    ms.append([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
    ss.append([0, 3, 2, 9, 14])

    # another case, switching rows in previous
    ms.append([[0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
    ss.append([1, 0, 0, 0, 1])

    testspass = True
    for (m, s) in zip(ms, ss):
        if eventualmarkov(m) != s:
            print("Test failed with " + repr(m) + ". Expecting " + repr(s) + ", got " + repr(eventualmarkov(m)) + ".")
            testspass = False

    return testspass
