# Google foobar solutions
I first started doing foobar after being invited in April 2022. There have been some fun and 
challenging problems. I've done them on occasions when I felt that real life wouldn't interfere
too much. Now I have only the one Level 5 problem left to attempt.

I didn't start saving the entire problem text until recently, so I can't reconstruct the original
problem wording in terms of bunnies, trainers, minions and Commander Lambda. What follows are notes
for each problem. And anyway the problems someone else sees may be different from the problems I've
seen.

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

I provide both an attempt based on breadth first search of a tree with pruning rules (which I suspected could be too slow, and it certainly was, as my own tests also showed), and a much faster approach which passed the foobar tests, which went "backwards" up a tree branch to the root.

## Level 4
Fifteen days to solve each problem.

In level 4 I started to copy the whole problem statement. Because why not?
### `minionkeys.py`
```
solution(num_buns: int, num_required: int)
```

#### Free the Bunny Workers

You need to free the bunny workers before Commander Lambda's space station explodes! Unfortunately, the Commander was very careful with the highest-value workers -- they all work in separate, maximum-security work rooms. The rooms are opened by putting keys into each console, then pressing the open button on each console simultaneously. When the open button is pressed, each key opens its corresponding lock on the work room. So, the union of the keys in all of the consoles must be all of the keys. The scheme may require multiple copies of one key given to different minions.

The consoles are far enough apart that a separate minion is needed for each one. Fortunately, you have already relieved some bunnies to aid you - and even better, you were able to steal the keys while you were working as Commander Lambda's assistant. The problem is, you don't know which keys to use at which consoles. The consoles are programmed to know which keys each minion had, to prevent someone from just stealing all of the keys and using them blindly. There are signs by the consoles saying how many minions had some keys for the set of consoles. You suspect that Commander Lambda has a systematic way to decide which keys to give to each minion such that they could use the consoles.

You need to figure out the scheme that Commander Lambda used to distribute the keys. You know how many minions had keys, and how many consoles are by each work room.  You know that Command Lambda wouldn't issue more keys than necessary (beyond what the key distribution scheme requires), and that you need as many bunnies with keys as there are consoles to open the work room.

Given the number of bunnies available and the number of locks required to open a work room, write a function solution(num_buns, num_required) which returns a specification of how to distribute the keys such that any num_required bunnies can open the locks, but no group of (num_required - 1) bunnies can.

Each lock is numbered starting from 0. The keys are numbered the same as the lock they open (so for a duplicate key, the number will repeat, since it opens the same lock). For a given bunny, the keys they get is represented as a sorted list of the numbers for the keys. To cover all of the bunnies, the final solution is represented by a sorted list of each individual bunny's list of keys.  Find the lexicographically least such key distribution - that is, the first bunny should have keys sequentially starting from 0.

num_buns will always be between 1 and 9, and num_required will always be between 0 and 9 (both inclusive).  For example, if you had 3 bunnies and required only 1 of them to open the cell, you would give each bunny the same key such that any of the 3 of them would be able to open it, like so:
```
[
  [0],
  [0],
  [0],
]
```
If you had 2 bunnies and required both of them to open the cell, they would receive different keys (otherwise they wouldn't both actually be required), and your solution would be as follows:
```
[
  [0],
  [1],
]
```
Finally, if you had 3 bunnies and required 2 of them to open the cell, then any 2 of the 3 bunnies should have all of the keys necessary to open the cell, but no single bunny would be able to do it.  Thus, the solution would be:
```
[
  [0, 1],
  [0, 2],
  [1, 2],
]
```

#### Solution
In this problem we have to assign keys to minions from a consecutive sequence starting at 0.

The minions control a locked mechanism with their keys. The mechanism can be operated by a set of minions each holding the right keys.

We are given a pool of `m` (`num_buns`) minions available to operate the mechanism, and a number `n` (`num_required`) of them which is the minimum number to unlock the mechanism.

The requirement is that any subset of `n` minions from the pool of `m` must hold, together, the complete set of keys. Any subset of `n-1` minions
(or fewer) from the pool must not hold a complete set of keys, so that the mechanism cannot be operated by fewer than `n` minions from the pool.

Multiple minions may have copies of the same key.

We are not given the number of keys needed to operate the mechanism.

The goal is compute the smallest number of keys that form a complete set to operate the mechanism,
the number of keys to assign to each minion (which is the same for all minions), and the exact set of keys to assign to each minion, so that the
requirement above that at least `n` minions from the pool of `m` are necessary in order to unlock the mechanism. Moreover, since in general there are multiple
solutions possible which differ only in the key sequences assigned, we should compute the "lexicographically least" assignment of keys to minions, i.e. the first
minion should always have a consecutive sequence of keys assigned that start at 0.

For example, 
```
[
  [0, 1, 2],
  [0, 3, 4],
  [1, 3, 5],
  [2, 4, 5]
]
```
is the lexicographically least solution to `(m, n) == (4, 3)`, whereas another solution is given by
```
[
  [0, 1, 3],
  [0, 2, 4],
  [1, 2, 5],
  [3, 4, 5]
]
```

("Lexicographically least": among all solutions which agree on the first `k >= 0` elements, the `(k+1)`th element of the lexicographically least order is less
equal to the `(k+1)`th element of the others.)

The return value is a list of equal length lists in lexicographic order, giving the key assignments to each minion.

We have the following limits: `m` is an integer in the range 1 to 9, inclusive. `n` is an integer in the range 0 to 9 inclusive.

### `distracttrainers.py`
```
solution(trainerbananas)
```
`trainerbananas` is a list of the number of bananas possessed by each trainer.

#### Distract the Trainers

The time for the mass escape has come, and you need to distract the bunny trainers so that the workers can make it out! Unfortunately for you, they're watching the bunnies closely. Fortunately, this means they haven't realized yet that the space station is about to explode due to the destruction of the LAMBCHOP doomsday device. Also fortunately, all that time you spent working as first a minion and then a henchman means that you know the trainers are fond of bananas. And gambling. And thumb wrestling.

The bunny trainers, being bored, readily accept your suggestion to play the Banana Games.

You will set up simultaneous thumb wrestling matches. In each match, two trainers will pair off to thumb wrestle. The trainer with fewer bananas will bet all their bananas, and the other trainer will match the bet. The winner will receive all of the bet bananas. You don't pair off trainers with the same number of bananas (you will see why, shortly). You know enough trainer psychology to know that the one who has more bananas always gets over-confident and loses. Once a match begins, the pair of trainers will continue to thumb wrestle and exchange bananas, until both of them have the same number of bananas. Once that happens, both of them will lose interest and go back to supervising the bunny workers, and you don't want THAT to happen!

For example, if the two trainers that were paired started with 3 and 5 bananas, after the first round of thumb wrestling they will have 6 and 2 (the one with 3 bananas wins and gets 3 bananas from the loser). After the second round, they will have 4 and 4 (the one with 6 bananas loses 2 bananas). At that point they stop and get back to training bunnies.

How is all this useful to distract the bunny trainers? Notice that if the trainers had started with 1 and 4 bananas, then they keep thumb wrestling! 1, 4 -> 2, 3 -> 4, 1 -> 3, 2 -> 1, 4 and so on.

Now your plan is clear. You must pair up the trainers in such a way that the maximum number of trainers go into an infinite thumb wrestling loop!

Write a function solution(banana_list) which, given a list of positive integers depicting the amount of bananas the each trainer starts with, returns the fewest possible number of bunny trainers that will be left to watch the workers. Element i of the list will be the number of bananas that trainer i (counting from 0) starts with.

The number of trainers will be at least 1 and not more than 100, and the number of bananas each trainer starts with will be a positive integer no more than 1073741823 (i.e. 2^30 -1). Some of them stockpile a LOT of bananas.

#### Strategy

First we need to determine whether each possible pair of bunny trainers leads to a nonterminating loop of thumb wrestling games, 
or terminates with both trainers ending up with an equal number of bananas.

To do this we'll first sort the trainers by nondecreasing number of bananas held initially. The termination/nontermination decision 
function took a bit of work to discover, but not that hard and a proof that it is the right function is provided in a PDF 
separately at [doc/terminating_bunny_trainer_transforms.pdf](https://github.com/grahamgill/foobar/blob/f5c6ad80b4533b1eadb6fbbd8b1975c1dca0fc17/doc/terminating_bunny_trainer_transforms.pdf "Terminating sequences of Bunny Trainer Transforms").

We'll only consider banana pairs `(m,n)` with `m <= n`, since `(n,m)` gives the same termination/nontermination outcome, and a game 
match between trainer `i` and trainer `j` is the same game match as between trainer `j` and trainer `i`. The list of trainers sorted by 
nondecreasing number of bananas held lets us do this easily. If the sorted `N` trainers are labelled `0..N-1`, then we don't need to 
consider a match between trainer `k` and trainer `k` (which would be terminating in any case), but we only need to consider matches
between trainer `k` `(0 <= k < N-1)` on the left and trainers `k+1..N-1` on the right. The right hand trainers are guaranteed to have at 
least as many bananas as trainer `k` because of the sort.

After we know which pairings of bunny trainers will not terminate their games, we need to find the largest set of nonterminating 
bunny trainer pairs. This is a maximum cardinality matching in a general graph, since in general the graph will have odd cycles
(e.g. the test example `[1, 7, 3, 21, 13, 19]`) and thus will not be bipartite.

The graph we construct has an edge for all nonterminating bunny trainer matchups. So in the example we have edges `(1, 13), (1, 21), (13, 21)`, giving a 3-cycle.

We'll try a greedy matching algorithm which takes a remaining edge with least incidence to other edges at each step. Removing the edge
will disconnect its incident vertices from the graph, which will change the edge incidence count for remaining edges. We can get a
maximal cardinality matching in this way but are not guaranteed to get the maximum cardinality matching. However this is much simpler
to code up and will run more quickly, so I'm hoping this will be good enough for foobar to trick the bunny trainers. After all I'm
under the gun here, the station is starting to disintegrate, so I don't have the time for a perfect algorithm.

If it turns out we really need the maximum cardinality matching, we'll have to implement Edmonds' blossom algorithm (or adapt some
code from online). Hopefully not. There are asymptotically better algorithms than the blossom algorithm but they're more complex and
their improvement in worst bounds does not guarantee their runtime is any better on average and relatively small examples. There are
also randomised algorithms giving approximations which, for small examples, may give the maximum with probability only epsilon less than 1. Anyway, we'll see.

If we have a maximal/maximum matching consisting of `K` edges, then that occupies `2K` trainers, leaving `N-2K` watchful trainers. We return
`N-2K`.

##### Epilogue
Woohoo! It worked!
