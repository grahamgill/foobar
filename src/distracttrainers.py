"""
Not all of the bunny workers are highly-trained operatives. Some of them are civilians, and they're panicking in all the noise and confusion of the space station's destruction. Several of them have wedged themselves into corners and started thumping, which isn't exactly helping the station's structural integrity...

Distract the Trainers
=====================

The time for the mass escape has come, and you need to distract the bunny trainers so that the workers can make it out! Unfortunately for you, they're watching the bunnies closely. Fortunately, this means they haven't realized yet that the space station is about to explode due to the destruction of the LAMBCHOP doomsday device. Also fortunately, all that time you spent working as first a minion and then a henchman means that you know the trainers are fond of bananas. And gambling. And thumb wrestling.

The bunny trainers, being bored, readily accept your suggestion to play the Banana Games.

You will set up simultaneous thumb wrestling matches. In each match, two trainers will pair off to thumb wrestle. The trainer with fewer bananas will bet all their bananas, and the other trainer will match the bet. The winner will receive all of the bet bananas. You don't pair off trainers with the same number of bananas (you will see why, shortly). You know enough trainer psychology to know that the one who has more bananas always gets over-confident and loses. Once a match begins, the pair of trainers will continue to thumb wrestle and exchange bananas, until both of them have the same number of bananas. Once that happens, both of them will lose interest and go back to supervising the bunny workers, and you don't want THAT to happen!

For example, if the two trainers that were paired started with 3 and 5 bananas, after the first round of thumb wrestling they will have 6 and 2 (the one with 3 bananas wins and gets 3 bananas from the loser). After the second round, they will have 4 and 4 (the one with 6 bananas loses 2 bananas). At that point they stop and get back to training bunnies.

How is all this useful to distract the bunny trainers? Notice that if the trainers had started with 1 and 4 bananas, then they keep thumb wrestling! 1, 4 -> 2, 3 -> 4, 1 -> 3, 2 -> 1, 4 and so on.

Now your plan is clear. You must pair up the trainers in such a way that the maximum number of trainers go into an infinite thumb wrestling loop!

Write a function solution(banana_list) which, given a list of positive integers depicting the amount of bananas the each trainer starts with, returns the fewest possible number of bunny trainers that will be left to watch the workers. Element i of the list will be the number of bananas that trainer i (counting from 0) starts with.

The number of trainers will be at least 1 and not more than 100, and the number of bananas each trainer starts with will be a positive integer no more than 1073741823 (i.e. 2^30 -1). Some of them stockpile a LOT of bananas.

Test cases
==========
Your code should pass the following test cases.

Note that it may also be run against hidden test cases not shown here.

-- Python cases --
Input:
solution.solution([1, 7, 3, 21, 13, 19])
Output:
    0

Input:
solution.solution(1,1)
Output:
    2
"""

"""
Strategy

First we need to determine whether each possible pair of bunny trainers leads to a nonterminating loop of thumb wrestling games, 
or terminates with both trainers ending up with an equal number of bananas.

To do this we'll first sort the trainers by nondecreasing number of bananas held initially. The termination/nontermination decision 
function took a bit of work to discover, but not that hard and a proof that it is the right function will be provided in a PDF 
separately at github.com/grahamgill/foobar/doc/terminating_bunny_trainer_transforms.pdf.

We'll only consider banana pairs (m,n) with m <= n, since (n,m) gives the same termination/nontermination outcome, and a game 
match between trainer i and trainer j is the same game match as between trainer j and trainer i. The list of trainers sorted by 
nondecreasing number of bananas held lets us do this easily. If the sorted N trainers are labelled 0..N-1, then we don't need to 
consider a match between trainer k and trainer k (which would be terminating in any case), but we only need to consider matches
between trainer k (0 <= k < N-1) on the left and trainers k+1..N-1 on the right. The right hand trainers are guaranteed to have at 
least as many bananas as trainer k because of the sort.

After we know which pairings of bunny trainers will not terminate their games, we need to find the largest set of nonterminating 
bunny trainer pairs. This is a job for bipartite graph maximum cardinality matching. If we have a list of N bunny trainers, our 
graph will have N-1 vertices on the left side representing trainers 0..N-2 in left hand positions of matches, and N-1 vertices on 
the right side representing trainers 1..N-1 in right hand positions of matches. A directed edge from left hand side to right hand 
side will be indicated with a 1 if the pair of trainers will have a nonterminating game, and 0 - no edge - otherwise.

We'll use the Edmonds-Karp algorithm to compute a maximum "flow" over our graph by adding a source vertex with edges to all left 
side vertices with capacity 1, and a sink vertex with edges from all right hand vertices with capacity 1. The directed edge indicators
of 1 in the bipartite graph will also represent the flow capacities between left side and right side vertices.

The maximum flow will give us exactly the number of edges in a maximum cardinality matching. We don't care what the actual edges are.
If the max flow is K, then 2K trainers are occupied in nonterminating games, leaving N-2K trainers in terminating games (or unmatched,
in case of an odd number of trainers).

We report N-2K as the solution.

Invaluable pages:
* https://en.wikipedia.org/wiki/Maximum_flow_problem#Maximum_cardinality_bipartite_matching
* https://en.wikipedia.org/wiki/Ford%E2%80%93Fulkerson_algorithm
I adapted the python implementation of Edmonds-Karp from the python example provided on the second page.
"""

from fractions import gcd

def solution(trainerbananas):
    """
    Returns smallest number of trainers who will not be in a match after a finite amount of time.
    
    `trainerbananas` is a list of the number of bananas possessed by each trainer.
    """

    num_trainers = len(trainerbananas)

    # check for valid inputs
    # zero length list is invalid, but we can accept it
    assert num_trainers <= 100, "Trainer bananas list too long, > 100"
    assert all(map(lambda x: isinstance(x, int), trainerbananas)), "Trainer bananas list includes non-int"
    assert all(map(lambda x: 1 <= x <= 2**30-1, trainerbananas)), "Trainer banana count outside range 1 to 2**30-1 inclusive"

    # If no trainers then none to worry about not being in a match.
    # If only one trainer, then no way to keep that trainer occupied in a thumb wrestling match,
    # so will have 1 not in a match.
    if num_trainers in {0, 1}:
        return num_trainers

    # so now at least two trainers, so we can put trainers into game matches
    # sort the trainer bananas count list
    tbs = sorted(trainerbananas)


    return 0


def bunnytrainertransform(m, n):
    """
    This is the transformation (m, n) --> (2m, n - m) (if m <= n) described in the problem, with
    result (p, q) normalised so we always have p <= q.

    Note that we don't actually use this function in the solution. It's just here for reference.
    """
    if m > n:
        m, n = n, m
    
    x = 2 * m
    y = n - m

    if x > y:
        x, y = y, x
    
    return x, y


def btt_sequence_terminates(m, n):
    """
    Repeated application of the bunnytrainertransform to (m, n), both positive integers, will eventually terminate 
    with equal terms in the tuple (or, if you like, with a zero in the tuple, which is the next step after equal
    terms) iff
        (m + n)/d == 2^k for some positive integer k
    where d == gcd(m, n).

    The proof of this proposition is in github.com/grahamgill/foobar/doc/terminating_bunny_trainer_transforms.pdf.

    Returns True if the sequence terminates, and False if it is nonterminating. `m` and `n` must be nonnegative
    integers.
    """
    assert m >= 0 and n >= 0, "Only nonnegative inputs allowed"

    # if either m or n is zero, the sequence has already terminated
    if not (m and n):
        return True
    
    # so both m, n > 0
    d = gcd(m, n)
    # hence x and y are at least 2
    x = y = m/d + n/d

    # count powers of 2 in y
    k = 0
    while not (y & 1):
        y >>= 1
        k += 1
    
    # is x a power of 2?
    # I suppose we could have used `log` to base 2 as well and checked that it's an integer
    return x == 2 ** k


def tests():

    assert bunnytrainertransform(3, 3) == (0, 6)
    assert bunnytrainertransform(4, 2) == (2, 4)
    assert bunnytrainertransform(1, 5) == (2, 4)
    assert bunnytrainertransform(3, 4) == (1, 6)

    assert btt_sequence_terminates(0, 0)
    assert btt_sequence_terminates(1, 0)
    assert btt_sequence_terminates(1, 1)
    assert not btt_sequence_terminates(1, 2)
    assert btt_sequence_terminates(1, 7)
    assert btt_sequence_terminates(1, 3)
    assert not btt_sequence_terminates(1, 21)
    assert not btt_sequence_terminates(1, 13)
    assert not btt_sequence_terminates(1, 19)
    assert not btt_sequence_terminates(7, 3)
    assert btt_sequence_terminates(7, 21)
    assert not btt_sequence_terminates(7, 13)
    assert not btt_sequence_terminates(7, 19)
    assert btt_sequence_terminates(3, 21)
    assert btt_sequence_terminates(3, 13)
    assert not btt_sequence_terminates(3, 19)
    assert not btt_sequence_terminates(21, 13)
    assert not btt_sequence_terminates(21, 19)
    assert btt_sequence_terminates(13, 19)

    assert solution([]) == 0
    assert solution([2]) == 1
    assert solution([1,1]) == 2
    assert solution([1,1,1]) == 3

    assert solution([1, 7, 3, 21, 13, 19]) == 0

    return True