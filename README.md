# Google foobar solutions

## Level 1
* `bunnyid.py`

```
bunnyid(x: int, y: int)
```
Enumerate the $\mathbb N^2$ lattice points along diagonals `x + y = n`
of increasing 1-norm distance `n` from the origin `(0,0)` in $\mathbb Z^2$.
Counting should increase with distance along the horizontal axis.

E.g., count
```
| 7
| 4 8
| 2 5 9
| 1 3 6 10
----------
```
from:
```
(1,1) => 1
(1,2) => 2
(2,1) => 3
(1,3) => 4
(2,2) => 5
(3,1) => 6
(1,4) => 7
(2,3) => 8
(3,2) => 9
(4,1) => 10
```

Stringify the return result. `x` and `y` are guaranteed to be `int`s in the range 1 to 100000.

## Level 2
* `pieslices.py`

```
pieslices(s: str)
```
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

