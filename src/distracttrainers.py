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
bunny trainer pairs. This is a maximum cardinality matching in a general graph, since in general the graph will have odd cycles
(e.g. the test example [1, 7, 3, 21, 13, 19]) and thus will not be bipartite.

The graph we construct has an edge for all nonterminating bunny trainer matchups. So in the example we have edges (1, 13), (1, 21),
(13, 21), giving a 3-cycle.

We'll try a greedy matching algorithm which takes a remaining edge with least incidence to other edges at each step. Removing the edge
will disconnect its incident vertices from the graph, which will change the edge incidence count for remaining edges. We can get a
maximal cardinality matching in this way but are not guaranteed to get the maximum cardinality matching. However this is much simpler
to code up and will run more quickly, so I'm hoping this will be good enough for foobar to trick the bunny trainers. After all I'm
under the gun here, the station is starting to disintegrate, so I don't have the time for a perfect algorithm.

If it turns out we really need the maximum cardinality matching, we'll have to implement Edmonds' blossom algorithm (or adapt some
code from online). Hopefully not. There are asymptotically better algorithms than the blossom algorithm but they're more complex and
their improvement in worst bounds does not guarantee their runtime is any better on average and relatively small examples. There are
also randomised algorithms giving approximations which, for small examples, may give the maximum with probability only epsilon less than
1. Anyway, we'll see.

If we have a maximal/maximum matching consisting of K edges, then that occupies 2K trainers, leaving N-2K watchful trainers. We return
N-2K.

Woohoo! It worked!
"""

from fractions import gcd
# from collections import deque

def solution(trainerbananas):
    """
    Returns smallest number of trainers who will not be in a match after a finite amount of time.
    
    `trainerbananas` is a list of the number of bananas possessed by each trainer.
    """

    num_trainers = len(trainerbananas)

    # check for valid inputs
    # zero length list is invalid input according to rules, but we can accept it
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

    # store nonterminating pairs of trainers in adjacency matrix graph
    graph = AdjacencyGraph(num_trainers)

    # add edges for nonterminating trainer pairs
    for i in range(num_trainers - 1):
        for j in range(i + 1, num_trainers):
            if not btt_sequence_terminates(tbs[i], tbs[j]):
                graph.addedge(i, j)

    # so now construct a list of edges with their incidence counts and mark an edge with least
    # incidence count
    edgelist = list() 
    minincidencecount = float("Inf") 
    minincidenceindex = None
    for i in range(num_trainers - 1):
        for j in range(i + 1, num_trainers):
            if graph.inE(i, j):
                c = graph.edgeincidencecount(i, j)
                edgelist.append((i, j))
                if c < minincidencecount:
                    minincidencecount = c
                    minincidenceindex = len(edgelist) - 1

    # build maximal (but not necessarily maximum :( ) list of trainer match pairs using
    # greedy algorithm described under Strategy
    trainermatches = list()
    while minincidenceindex is not None:
        # add min incidence count edge to matches list
        u, v = edgelist[minincidenceindex]
        trainermatches.append((u, v))

        # disconnect vertices u and v from graph
        graph.disconnectvertex(u)
        graph.disconnectvertex(v)

        # construct reduced edgelist of remaining edges
        el = list()
        minincidencecount = float("Inf")
        minincidenceindex = None
        for i, j in edgelist:
            if graph.inE(i, j):
                c = graph.edgeincidencecount(i, j)
                el.append((i, j))
                if c < minincidencecount:
                    minincidencecount = c
                    minincidenceindex = len(el) - 1

        edgelist = el

    return num_trainers - 2 * len(trainermatches)


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

    return (y, x) if x > y else (x, y)


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


class AdjacencyGraph:
    """
    Undirected graph based on adjacency matrix representation.
    Constructor returns a graph with `num_vertices` vertices labelled 0..(`num_vertices`-1)
    and no edges.
    * Vertex labels are in `V`.
    * Edges are in adjacency matrix `E`: 1 if edge, 0 if not.
    * Number of vertices is in `cardV`.
    * Number of edges is in `cardE`.
    * Degree of each vertex is in `degrees`.

    Supports:
    * inV: vertex membership test
    * inE: edge membership test
    * addedge: add edge
    * deledge: remove edge
    * disconnectvertex: remove all edges incident to a vertex
    * edgeincidencecount: number of edges incident on a given edge
    """

    def __init__(self, num_vertices):
        self.V = range(num_vertices)
        self.degrees = [0] * num_vertices
        self.E = [[0] * num_vertices for k in range(num_vertices)]
        self.cardV = num_vertices
        self.cardE = 0
    
    def inE(self, v1, v2):
        return bool(self.E[v1][v2])

    def inV(self, v):
        return 0 <= v < self.cardV

    def addedge(self, v1, v2):
        if not self.E[v1][v2]:
            self.E[v1][v2] = 1
            self.cardE += 1
            self.degrees[v1] += 1
            if v2 != v1:
                self.E[v2][v1] = 1
                self.degrees[v2] += 1
    
    def deledge(self, v1, v2):
        if self.E[v1][v2]:
            self.E[v1][v2] = 0
            self.cardE -= 1
            self.degrees[v1] -= 1
            if v2 != v1:
                self.E[v2][v1] = 0
                self.degrees[v2] -= 1
    
    def disconnectvertex(self, v):
        for u in self.V:
            self.degrees[u] -= self.E[u][v]
            self.cardE -= self.E[u][v]
            self.E[u][v] = 0

        self.E[v] = [0] * self.cardV
        self.degrees[v] = 0
    
    def edgeincidencecount(self, v1, v2):
        """
        If `(v1, v2)` is an edge in `E`, return its edge incidence count, including itself, i.e.
        the number of edges incident to `v1` plus the number of edges incident to `v2` other than 
        `(v1, v2)` itself again (so we don't double count it). The incidence count is always at least
        one for an edge of the graph.

        If `(v1, v2)` is not an edge in `E`, return zero.

        In the special case that `v1 == v2` and `(v1, v2)` is in E, just return the degree of `v1`.
        We're not allowing edges with multiplicity in this graph.
        """

        if self.E[v1][v2]:
            if v1 == v2:
                return self.degrees[v1]
            else:
                return self.degrees[v1] + self.degrees[v2] - 1
        else:
            return 0


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

    # graph for trainer bananas list [1, 3, 7, 13, 19, 21]
    graph = AdjacencyGraph(6)
    tbl = [1, 3, 7, 13, 19, 21]
    for i in range(5):
        for j in range(i + 1, 6):
            if not btt_sequence_terminates(tbl[i], tbl[j]):
                graph.addedge(i, j)
    graph.addedge(0, 0)
    graph.deledge(0, 0)
    graph.addedge(0, 3)
    assert not graph.inE(0, 0)
    assert graph.inE(0, 3)
    assert graph.inE(4, 5)
    assert graph.inE(5, 4)
    assert graph.inV(5)
    assert graph.cardV == 6
    assert graph.cardE == 9
    assert graph.degrees == [3, 2, 3, 3, 4, 3]
    assert graph.cardE == 9
    assert graph.edgeincidencecount(4, 5) == 6
    assert graph.edgeincidencecount(0, 3) == 5
    assert graph.edgeincidencecount(0, 1) == 0
    graph.disconnectvertex(4)
    assert not graph.inE(4, 5)
    assert not graph.inE(5, 4)
    assert graph.inE(0, 5)
    assert graph.cardV == 6
    assert graph.cardE == 5
    assert graph.degrees == [2, 1, 2, 3, 0, 2]
    assert graph.edgeincidencecount(4, 5) == 0
    assert graph.edgeincidencecount(0, 3) == 4
    graph.addedge(3, 3)
    assert graph.degrees[3] == 4
    assert graph.edgeincidencecount(3, 3) == 4
    assert graph.edgeincidencecount(0, 3) == 5
    graph.deledge(3, 3)
    assert graph.degrees[3] == 3
    assert graph.edgeincidencecount(3, 3) == 0
    assert graph.edgeincidencecount(0, 3) == 4

    assert solution([]) == 0
    assert solution([2]) == 1
    assert solution([1, 1]) == 2
    assert solution([1, 1, 1]) == 3
    assert solution([1, 2, 3]) == 1
    assert solution([1, 2, 3, 4]) == 0
    assert solution([2, 3, 4, 5]) == 0
    assert solution([1, 2, 3, 4, 5]) == 1
    assert solution([2, 3, 4, 5, 6]) == 1
    assert solution([3, 4, 5, 6, 7]) == 1
    assert solution([1, 2, 3, 4, 5, 6]) == 0
    assert solution([2, 3, 4, 5, 6, 7]) == 0
    assert solution([3, 4, 5, 6, 7, 8]) == 0
    assert solution([1, 3, 5, 7, 9]) == 1
    assert solution([3, 5, 7, 9, 11]) == 1
    assert solution([1, 3, 5, 7, 9, 11]) == 0
    assert solution([1, 3, 5, 7, 9, 23]) == 0
    assert solution([2, 4, 6, 12]) == 0

    assert solution([1, 7, 3, 21, 13, 19]) == 0

    return True