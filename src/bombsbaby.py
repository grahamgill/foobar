from collections import deque

def solution(x, y):
  """
  Interface to foobar.
  """
  m = int(x)
  f = int(y)
  g = bombgenerations(m, f)
  return 'impossible' if g < 0 else str(g)

def bombgenerations_slow(m, f):
  """
  bombgenerations_slow(m : int, f : int) : int

  m: needed number of Mach bombs
  f: needed number of Facula bombs
  bombgenerations_slow(m, f): smallest bomb replication generation (>= 0) at which m, f are achieved,
    starting from 1 Mach and 1 Facula bomb, or -1 if it is impossible to achieve m, f.

  We proceed with an approach like breadth first search. Given a number of M and F bombs (x, y),
  we can use one of the two next generation processes to achieve (x+y, y) or (x, x+y) M and F bombs respectively,
  at the next generation. We work one generation at a time across the whole tree, with all nodes of
  the current generation in a queue, considering each: has it achieved m and f, has it exceeded
  either m or f, or is it less than m or less than f while not exceeding both? Based on this classification,
  we populate the next generation's queue with candidates to inspect.

  In this way, we know that if we have achieved m and f, we've done so at the least generation possible, since
  we can then stop. If the current generation does not yield a solution, then the queue we use to process it
  is empty and we can swap the roles of the next generation queue and the current generation queue.

  We prune paths of the binary tree when we know a branch leads only to non-solutions. Then we know that we can
  stop searching with no solution when both the current and next generations' queues are empty, and return
  the error value -1.

  OK this one's no good a solution. It explodes combinatorially in early generations when m and f are large, since
  there's little pruning that can apply. Eventually pruning takes over and reduces the queue count in each generation
  but e.g. m = f = 100000 takes forever to decide that it's impossible, and goes up to some 209 million candidates in
  generations around 40.

  But I know how to solve this now. Work backwards from the solution and use properties of Euclidean algorithm. Note
  that gcd(m,f) == gcd(m+f,f) = gcd(m,m+f) and so any descendant (m,f) of (1,1) must have gcd(m,f) == 1.
  """
  assert m >= 0 and f >= 0, "Require nonnegative Mach and Facula targets, but got m == " + repr(m) + ", f == " + repr(f)
  assert m <= 10**50 and f <= 10**50, "Require Mach and Facula targets both <= 10^50, but got m == " + repr(m) + ", f == " + repr(f)

  # if we don't need any Ms or any Fs, then definitely impossible given we start with 1 M and 1 F.
  if m == 0 or f == 0:
    return -1

  # now we can guarantee m, f both >= 1
  # generation counter and solution flag
  generation = 0
  solution_not_found = True
  solution_exists_at_generation = 10**100 # upper bound on number of generations required

  # queues for holding current node level (generation) in tree and constructing child level (next generation)
  # at the root (generation 0) we start with (1, 1) representing 1 M and 1 F bomb
  # induction hypothesis: all elements (M, F) of current generation N have M <= m and F <= f
  # base case N = 0 satisfied
  current_generation = deque([(1, 1)])
  next_generation = deque()

  while len(current_generation) > 0 and solution_not_found:
    M, F = current_generation.pop()

    if M == m and F == f:
      solution_not_found = False
    
    # by induction hypothesis, if solution not found, then M < m and F <= f or M <= m and F < f
    else:
      if M == m or F == f:
        if F == f:
          # we don't care about order here
          M, F = F, M
          m_, f_ = f, m
        else:
          m_, f_ = m, f

        # so now we know F < f_, M == m_
        # in this case we'll have a single viable list-like branch below the node and it's easy to say what's on it: (m_, m_ + F), (m_, 2m_ + F), ...
        # so we can prune the tree here and just record a possible future generation solution
        # if r == 0 we have an exact solution on this branch, otherwise no solution
        q, r = divmod(f_ - F, m_)
        if r == 0:
          solution_exists_at_generation = min(solution_exists_at_generation, generation + q)
        
      else:
        # M < m and F < f
        newbombcount = M + F
        M_left, F_left = newbombcount, F
        M_right, F_right = M, newbombcount
        # we can show that if newbombcount > m or f, the whole subtree rooted here is unviable
        if newbombcount <= m and newbombcount <= f:
          next_generation.extend([(newbombcount, F), (M, newbombcount)])
          # thus we've guaranteed that the next gen also doesn't exceed m and f, for induction purposes
      
      if len(current_generation) == 0:
        # we've run out of the current gen, so
        # need to increment generation and swap in next gen queue
        current_generation, next_generation = next_generation, current_generation
        generation += 1
        # print(repr(generation) + ", " + repr(len(current_generation)))
        if generation == solution_exists_at_generation:
          solution_not_found = False

  # either we have a solution here, or we've run out of tuples to check
  # if we've run out of tuples it could be that we know a future generation solution exists, but
  # tree pruning means we won't actually get to visit it, so then report that as solution
  if solution_not_found and solution_exists_at_generation < 10**100:
    solution_not_found = False
    generation = solution_exists_at_generation

  return -1 if solution_not_found else generation


def bombgenerations(m, f):
  """
  bombgenerations(m : int, f : int) : int

  m: needed number of Mach bombs
  f: needed number of Facula bombs
  bombgenerations(m, f): smallest bomb replication generation (>= 0) at which m, f are achieved,
    starting from 1 Mach and 1 Facula bomb, or -1 if it is impossible to achieve m, f.

  In this approach we work backwards from a desired pair (m, f) to see if we can get to an initial set
  of (M, F) bombs (1, 1).

  The algorithm is in fact exactly the Euclidean algorithm for computing gcd(m, f), where the successive
  quotients count generations, and the final step is to reach a pair (gcd(m, f), 0). If m and f are
  coprime then gcd(m, f) = 1 and from (1, 0) we can produce (1, 1) in one generation, so the generation
  count we return is 1 less than the sum of successive quotients we've computed.

  On the other hand, if gcd(m, f) > 1, then we have no way of reaching (1, 1) and there is no solution.
  There is no way to reach (m, f) by starting with (1, 1) and successively producing either (M+F, F) or
  (M, M+F) in the next generation from (M, F) in the current generation. Notice that gcd(M, F) =
  gcd(M+F, F) = gcd(M, M+F), and so gcd(m, f) and gcd(1, 1) = 1 must be equal for the process to produce
  (m, f) from (1, 1) eventually.

  We don't really need to import `gcd` from `fractions` since what we want is the Euclidean algorithm step
  results, not just computation of the greatest common divisor.
  """
  assert m >= 0 and f >= 0, "Require nonnegative Mach and Facula targets, but got m == " + repr(m) + ", f == " + repr(f)
  assert m <= 10**50 and f <= 10**50, "Require Mach and Facula targets both <= 10^50, but got m == " + repr(m) + ", f == " + repr(f)

  generations = 0
  while f > 0:
    q, r = divmod(m, f)
    generations += q
    m, f = f, r
  # now m = gcd of original m, f

  return generations - 1 if m == 1 else -1


# test cases
def tests():
  assert solution('1', '2') == '1'
  assert solution('2', '1') == '1'
  assert solution('1', '1') == '0'
  assert solution('2', '4') == 'impossible'

  assert bombgenerations_slow(1000, 1000) == -1
  assert bombgenerations_slow(1000, 999) == 999
  assert bombgenerations_slow(12, 7) == 5
  assert bombgenerations_slow(11, 9) == 6
  assert bombgenerations_slow(9, 11) == 6

  assert bombgenerations_slow(0, 100) == -1
  assert bombgenerations_slow(10**50, 1) == 10**50 - 1
  assert bombgenerations_slow(1, 10**10) == 10**10 - 1

  assert bombgenerations(1000, 1000) == -1
  assert bombgenerations(1000, 999) == 999
  assert bombgenerations(12, 7) == 5
  assert bombgenerations(11, 9) == 6
  assert bombgenerations(9, 11) == 6

  assert bombgenerations(0, 100) == -1
  assert bombgenerations(100, 0) == -1
  assert bombgenerations(0, 0) == -1
  assert bombgenerations(10**50, 1) == 10**50 - 1
  assert bombgenerations(1, 10**10) == 10**10 - 1

  assert bombgenerations(10**50, 10**50) == -1
  assert bombgenerations(10**50 - 1, 10**50) == 10**50 - 1
  assert bombgenerations(10**50, 10**50 - 1) == 10**50 - 1
  return True