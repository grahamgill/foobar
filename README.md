# Google foobar solutions
I first started doing foobar after being invited in April 2022. There have been some fun and 
challenging problems. I've done them on occasions when I felt that real life wouldn't interfere
too much. Now I have only the one Level 5 problem left to attempt.

I didn't start saving the entire problem text until recently, so I can't reconstruct the original
problem wording in terms of bunnies, trainers, minions and Commander Lambda. What follows are notes
for each problem.

foobar requires solutions be written in python 2.7 (or Java), with only a subset of the standard
library available for use.

## Level 1
One week to solve the problem. That's not saying you need a week to solve it. It's in case you have other things going on in your life.
### `bunnyid.py`

```
bunnyid(x: int, y: int)
```
Enumerate the $\mathbb N^2$ lattice points along diagonals `x + y = n`
of increasing 1-norm distance `n` from the origin `(0,0)` in $\mathbb Z^2$.
Counting should increase with distance along the horizontal axis. So, given
`x` and `y` both positive integers, e.g. `(2,3)`, count the number of lattice
points `(p,q)` in $\mathbb N^2$ such that `p + q <= x + y`, and if `p + q = x + y`
then such that `p <= x`.

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
```
xorqueue(start: int, length: int)
```
Equivalent to forming a square matrix of size `length**2`, consisting of the integers
from `start` to `start + length**2 -1` inclusive, in row major order, then `xor`ing the 
entries in the upper anti-triangle of the matrix as the return value.

`start` should be nonnegative.<br>
`length` should be strictly positive, and such that `start + length**2 - 1 < MAX_WORKER_ID`.<br>
`MAX_WORKER_ID` is 2 billion.

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

There may be hundreds of millions of integers we need to `xor` together, so time performance of the 
solution is paramount. 

### `eventualmarkov.py`
```
eventualmarkov(m)
```
`m` is a square matrix of nonnegative `int`s, represented as a list of `n` lists each of length `n`.<br>
`m[i][j]` records the number of times state `i` was observed to transition to state `j` in experiments.

We're asked to find for each absorbing state the probability of ending up eventually in that absorbing state, beginning from state 0. We're guaranteed that
* there is at least one absorbing state,
* there are no absorbing cycles (periodic states).

We're implicitly told to work with the matrix of observations, to treat them as representations of the
transition probabilities. We're told that some states have been unobserved, that is, both that no transition
into that state was observed from any state (corresponding to a zero column in `m`) and no transition out of
that state was observed to any state (corresponding to a zero row in `m`). Absorbing states correspond to a
zero row in `m`, since once in that state we don't leave it. (The unobserved states are also treated as
absorbing, although we have no way to get in to these states.)

We're asked to return the probabilities of ending up in the different absorbing states as a list of 
`int`s, one for each absorbing state, followed by a common denominator. E.g. a return of the list
`[1,2,3,6]` would indicate three absorbing states, with probabilities of eventually ending up in each
given by `1/6`, `1/3 = 2/6` and `1/2 = 3/6` respectively.

The solution involves first converting to transition probabilities, then forming an augmented linear system
with unknowns representing the probabilities of being absorbed into state `k` (column, limited only to
absorbing states), beginning in state `j` (row). Solving the linear system and reading the top row
gives the probabilities of eventually ending in each absorbing state, beginning from state 0.

### `bombsbaby.py`
```
bombgenerations(m: int, f: int)
```
`m`: needed number of Mach bombs<br>
`f`: needed number of Facula bombs<br>
`bombgenerations(m, f)`: smallest bomb replication generation (>= 0) at which `m`, `f` are achieved,
  starting from 1 Mach and 1 Facula bomb, or -1 if it is impossible to achieve `m`, `f`.

Bombs replicate from one generation to the next via one of the two rules
* `(x, y) -> (x + y, y)`
* `(x, y) -> (x, x + y)`

where `x` is the number of Mach bombs and `y` the number of Facula bombs at a generation.

The description of the problem in foobar was a bit unclear I found, especially the rule describing how the
bombs replicate. (The purpose of the exercise is to know how many bomb generations you have to wait in order
to have the right number of Mach and Facula bombs to explode a space station. M and F bombs are self-replicating.)

Performance is critical since `m` and `f` are nonnegative `int`s each no greater than `10**50`. Depending on
the solution algorithm, `bombgenerations(10**50, 10**50-1)` could take a _long_ time to compute.

I provide both an attempt based on breadth first search of a tree with pruning rules (which I suspected could be too slow, and it certainly was, as my own tests also showed), and a much faster approach which passed the foobar tests which went "backwards" up a tree branch to the root.

## Level 4
Fifteen days to solve each problem.
### `minionkeys.py`

### `distracttrainers.py`