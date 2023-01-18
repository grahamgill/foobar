from itertools import combinations
from math import factorial

"""
Free the Bunny Workers
======================

You need to free the bunny workers before Commander Lambda's space station explodes! Unfortunately, the Commander was very careful with the highest-value workers -- they all work in separate, maximum-security work rooms. The rooms are opened by putting keys into each console, then pressing the open button on each console simultaneously. When the open button is pressed, each key opens its corresponding lock on the work room. So, the union of the keys in all of the consoles must be all of the keys. The scheme may require multiple copies of one key given to different minions.

The consoles are far enough apart that a separate minion is needed for each one. Fortunately, you have already relieved some bunnies to aid you - and even better, you were able to steal the keys while you were working as Commander Lambda's assistant. The problem is, you don't know which keys to use at which consoles. The consoles are programmed to know which keys each minion had, to prevent someone from just stealing all of the keys and using them blindly. There are signs by the consoles saying how many minions had some keys for the set of consoles. You suspect that Commander Lambda has a systematic way to decide which keys to give to each minion such that they could use the consoles.

You need to figure out the scheme that Commander Lambda used to distribute the keys. You know how many minions had keys, and how many consoles are by each work room.  You know that Command Lambda wouldn't issue more keys than necessary (beyond what the key distribution scheme requires), and that you need as many bunnies with keys as there are consoles to open the work room.

Given the number of bunnies available and the number of locks required to open a work room, write a function solution(num_buns, num_required) which returns a specification of how to distribute the keys such that any num_required bunnies can open the locks, but no group of (num_required - 1) bunnies can.

Each lock is numbered starting from 0. The keys are numbered the same as the lock they open (so for a duplicate key, the number will repeat, since it opens the same lock). For a given bunny, the keys they get is represented as a sorted list of the numbers for the keys. To cover all of the bunnies, the final solution is represented by a sorted list of each individual bunny's list of keys.  Find the lexicographically least such key distribution - that is, the first bunny should have keys sequentially starting from 0.

num_buns will always be between 1 and 9, and num_required will always be between 0 and 9 (both inclusive).  For example, if you had 3 bunnies and required only 1 of them to open the cell, you would give each bunny the same key such that any of the 3 of them would be able to open it, like so:
[
  [0],
  [0],
  [0],
]
If you had 2 bunnies and required both of them to open the cell, they would receive different keys (otherwise they wouldn't both actually be required), and your solution would be as follows:
[
  [0],
  [1],
]
Finally, if you had 3 bunnies and required 2 of them to open the cell, then any 2 of the 3 bunnies should have all of the keys necessary to open the cell, but no single bunny would be able to do it.  Thus, the solution would be:
[
  [0, 1],
  [0, 2],
  [1, 2],
]

Languages
=========

To provide a Python solution, edit solution.py
To provide a Java solution, edit Solution.java

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Python cases --
Input:
solution.solution(2, 1)
Output:
    [[0], [0]]

Input:
solution.solution(4, 4)
Output:
    [[0], [1], [2], [3]]

Input:
solution.solution(5, 3)
Output:
    [[0, 1, 2, 3, 4, 5], [0, 1, 2, 6, 7, 8], [0, 3, 4, 6, 7, 9], [1, 3, 5, 6, 8, 9], [2, 4, 5, 7, 8, 9]]

-- Java cases --
Input:
Solution.solution(2, 1)
Output:
    [[0], [0]]

Input:
Solution.solution(5, 3)
Output:
    [[0, 1, 2, 3, 4, 5], [0, 1, 2, 6, 7, 8], [0, 3, 4, 6, 7, 9], [1, 3, 5, 6, 8, 9], [2, 4, 5, 7, 8, 9]]

Input:
Solution.solution(4, 4)
Output:
    [[0], [1], [2], [3]]
"""


def solution(num_buns, num_required):
  """
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
  [
    [0, 1, 2],
    [0, 3, 4],
    [1, 3, 5],
    [2, 4, 5]
  ]

  is the lexicographically least solution to `(m, n) == (4, 3)`, whereas another solution is given by
  [
    [0, 1, 3],
    [0, 2, 4],
    [1, 2, 5],
    [3, 4, 5]
  ].

  ("Lexicographically least": among all solutions which agree on the first k >= 0 elements, the (k+1)th element of the lexicographically least order is less
  equal to the (k+1)th element of the others.)

  The return value is a list of equal length lists in lexicographic order, giving the key assignments to each minion.

  We have the following limits: `m` is an integer in the range 1 to 9, inclusive. `n` is an integer in the range 0 to 9 inclusive.
  """
  # check for valid inputs
  assert 1 <= num_buns <= 9, "Invalid number of bunnies"
  assert 0 <= num_required <= 9, "Invalid number of required bunnies"
  assert num_required <= num_buns, "Number of bunnies required must be less-equal to number of bunnies available"

  # compute number of unique keys, number of keys held by each bunny, and number of holders of each key
  unique_keys, keys_held, key_holders = keycount(num_buns, num_required)

  # Next form the list of holders of each key.
  # The index in the list is the key ID.
  # The entry at index `k` is the keyholder IDs of key `k`.
  # We want the list in lexicographic order by lists of keyholders.
  # Example: input (4, 3), gives `4 choose 2 = 6` unique keys, `3 choose 2 = 3` keys held by each bunny,
  # and 2 holders for each key.
  # Then we want key 0 to go to bunnies (0,1), key 1 to bunnies (0,2), key 2 to bunnies (0,3),
  # key 3 to bunnies (1,2), key 4 to bunnies (1,3), key 5 to bunnies (2,3). This results in bunny 0
  # holding keys (0,1,2), bunny 1 holding (0,3,4), bunny 2 holding (1,3,5), bunny 3 holding (2,4,5).
  holders_by_key = list(combinations(range(num_buns), key_holders)) if key_holders > 0 else []

  # Length of `key_by_holders` is `num_buns choose key_holders == num_buns choose num_required-1 == unique_keys`.
  assert len(holders_by_key) == unique_keys

  # Now we need to "transpose" this list to get the keys held by each holder.
  keys_by_holder = [[] for k in range(num_buns)]
  for k in range(unique_keys):
    for h in holders_by_key[k]:
      keys_by_holder[h].append(k)

  assert len(keys_by_holder[0]) == keys_held

  return keys_by_holder


def keycount(m, n):
  """
    keycount(m : int, n : int) : int
  Given `m` keyholders of which any `n` (`n <= m`) must hold a complete set, but any `n-1` or fewer
  hold an incomplete set, compute the smallest number of unique keys required, and the count of keys
  each keyholder must hold.

  Observe that if `n` must hold a complete set but `n-1` an incomplete set, then every one of the `X = m choose n-1`
  `(n-1)`-tuples of keyholders must be missing a unique key, for if two such `(n-1)`-tuples were missing the same key, we could
  find `n` keyholders which together did not hold a complete set.

  So there are `X` unique keys.

  Fix a particular keyholder, say 0. There are `m-1 choose n-2` tuples among the `X` `(n-1)`-tuples which include 0, and there are
  `m-1 choose n-1` which do not contain 0. (And in fact we have the identity in general that `p-1 choose q-1 + p-1 choose q = p choose q`.)

  When keyholder 0 is in one of the `X` `(n-1)`-tuples it is missing the corresponding key. So this says that keyholder 0 must be missing
  `m-1 choose n-2` keys and must hold `m-1 choose n-1` keys. By symmetry, each keyholder must hold `m-1 choose n-1` of the keys. 

  How many holders hold one key? From the calculation of `X`, the number of unique keys, we see that a given key is not held by
  `n-1` holders, and so `m-(n-1)` holders must hold the key.

  Returns the number of unique keys, the count of keys held by each keyholder and the number of holders who hold each key.
  """
  # assertions already met in `solution`
  # assert m >= 1, "Need at least one keyholder m"
  # assert 0 <= n <= m, "Required keyholders n must be nonnegative and no greater than available keyholders m"

  if n == 0:
    return 0, 0, 0

  p = n - 1
  unique_keys = choose(m, p)
  keys_held = choose(m - 1, p)
  key_holders = m - p # will never be 0 since `0 <= p < m`

  return unique_keys, keys_held, key_holders


def choose(m, n):
  """
    choose(m : int, n : int) : int
    m >= 0
    0 <= n <= m

  Returns `m choose n`.
  """
  # these conditions already met by assertions in `solution`
  # assert m >= 0, "m must be nonnegative integer"
  # assert 0 <= n <= m, "n must be nonnegative integer no greater than m"
  
  p = m - n
  if p > n:
    n, p = p, n
  prod = 1
  for k in range(n+1, m+1):
    prod *= k

  return prod // factorial(p)


def tests():

  assert solution(1, 0) == [[]]
  assert solution(1, 1) == [[0]]

  assert solution(2, 0) == [[], []]
  assert solution(2, 1) == [[0], [0]]
  assert solution(2, 2) == [[0], [1]]

  assert solution(3, 0) == [[], [], []]
  assert solution(3, 1) == [[0], [0], [0]]
  assert solution(3, 2) == [
    [0, 1], 
    [0, 2], 
    [1, 2]
  ]
  assert solution(3, 3) == [[0], [1], [2]]

  assert solution(4, 0) == [[], [], [], []]
  assert solution(4, 1) == [[0], [0], [0], [0]]
  assert solution(4, 2) == [
    [0, 1, 2],
    [0, 1, 3],
    [0, 2, 3],
    [1, 2, 3]
  ]
  assert solution(4, 3) == [
    [0, 1, 2],
    [0, 3, 4],
    [1, 3, 5],
    [2, 4, 5]
  ]
  assert solution(4, 4) == [[0], [1], [2], [3]]

  assert solution(5, 0) == [[], [], [], [], []]
  assert solution(5, 1) == [[0], [0], [0], [0], [0]]
  assert solution(5, 2) == [
    [0, 1, 2, 3],
    [0, 1, 2, 4],
    [0, 1, 3, 4],
    [0, 2, 3, 4],
    [1, 2, 3, 4]
  ]
  assert solution(5, 3) == [
    [0, 1, 2, 3, 4, 5], 
    [0, 1, 2, 6, 7, 8], 
    [0, 3, 4, 6, 7, 9], 
    [1, 3, 5, 6, 8, 9], 
    [2, 4, 5, 7, 8, 9]
  ]
  assert solution(5, 4) == [
    [0, 1, 2, 3],
    [0, 4, 5, 6],
    [1, 4, 7, 8],
    [2, 5, 7, 9],
    [3, 6, 8, 9]
  ]
  assert solution(5, 5) == [[0], [1], [2], [3], [4]]

  assert choose(9, 4) == choose(9, 5)
  assert choose(9, 0) == choose(9, 9) == 1
  assert choose(9, 1) == choose(9, 8) == 9

  assert keycount(0, 0) == (0, 0, 0)
  assert keycount(9, 0) == (0, 0, 0)
  assert keycount(9, 1) == (1, 1, 9)
  assert keycount(9, 2) == (9, 8, 8)
  assert keycount(9, 3) == (36, 28, 7)
  assert keycount(9, 4) == (84, 56, 6)
  assert keycount(9, 5) == (126, 70, 5)
  assert keycount(9, 6) == (126, 56, 4)
  assert keycount(9, 7) == (84, 28, 3)
  assert keycount(9, 8) == (36, 8, 2)
  assert keycount(9, 9) == (9, 1, 1)

  return True