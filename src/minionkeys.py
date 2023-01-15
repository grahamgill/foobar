import itertools
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


def solution(m, n):
  """
  In this problem we have to assign keys to minions from a consecutive sequence starting at 0.

  The minions control a locked mechanism with their keys. The mechanism can be operated by a set of minions each holding the right keys.

  We are given a pool of `m` minions available to operate the mechanism, and a number `n` of them which is the minimum number to unlock the mechanism.

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
  pass

def comb(m, n):
  """
    comb(m : int, n : int) : int
    m >= 0
    0 <= n <= m

  Returns `m` choose `n`.
  """
  assert m >= 0, "m must be nonnegative integer"
  assert 0 <= n <= m, "n must be nonnegative integer no greater than m"
  p = m - n
  if p > n:
    n, p = p, n
  prod = 1
  for k in range(n+1, m+1):
    prod *= k

  return prod // factorial(p)


def tests():
  pass

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

  assert comb(9, 4) == comb(9, 5)
  assert comb(9, 0) == comb(9, 9) == 1
  assert comb(9, 1) == comb(9, 8) == 9