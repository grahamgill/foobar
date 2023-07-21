# Google foobar solutions

## Level 1
One week to solve the problem. That's not saying you need a week to solve it. It's in case you have other things going on in your life.
### `bunnyid.py`

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
One week to solve each problem.
### `pieslices.py`

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

### `elevatorversions.py`

```
elevatorversions(l)
```
Given a list `l` of major.minor.patch version number strings, sort them into increasing order and return the sorted list.

Each of major, minor, patch represents an `int >= 0`. Minor and patch are optional, but if patch is given minor must also
be given. (I.e. no string of the form "major..patch".) Missing minor and patch numbers are equivalent to 0.

Major is required.

If two version numbers are equal but have a different number of components (e.g. 2, 2.0, 2.0.0),
then subsort these by increasing number of components.

No instruction is given on comparing e.g. "1.01" vs. "1.1". We'll try first off dropping the leading zeros and see
if the verifier is happy with that, so that ["1.01", "1.1"] will return ["1.1", "1.1"]. 

## Level 3
One week to solve each problem.
### `xorqueue.py`

### `eventualmarkov.py`

### `bombsbaby.py`

## Level 4
Fifteen days to solve each problem.
### `minionkeys.py`

### `distracttrainers.py`