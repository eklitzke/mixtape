The Question
------------

This is an algorithms question that I commonly ask of interview
candidates.

You're given a list of songs (say, a list of numeric song ids). You're
also given a scoring function that takes two songs, and then returns
how good it sounds to listen to the second songs after listening to
the first song. In general, this score is not commutative, i.e. the
score of listening to song A after listening to song B is different
from the score of listening to song B after listening to song A.

The task is to find the optimal playlist order to listen to the full
list of songs and have the most goodness. The solution should be brute
force, not a heuristic, and your program can have any running time.

Observations
--------------

This question is actually a variation of the Travelling Salesman
Problem. The main differences are:

 * in TSP, the starting city does not matter; in the mixtape
   variation, the first song on the playlist is significant
 * in TSP you need to form a loop, i.e. return to the original city,
   whereas in the mixtape variation you end on the last song

Naive Solution
--------------

The naive solution is to generate a list of all song permutations,
score each permutation, and then return the list with the best
permutation. This is fine, this solution has running time n! and
correctly implementing a permutations function is tricky enough that a
lot of people still don't correctly finish the problem after coming to
this realization.

While this is the solution that 99% of the candidates I ask the
question of identify, many (I would wager, most) do not realize that
the solution they're implementing is equivalent to generating
permutations (or say the word "permutations" in their response). It's
my observation that having the insight that the brute force solution
is equivalent to trying all possible song lists, and therefore is
equivalent to generating all song permutations, significantly helps
people compared to those who dive straight into a recursive
depth-first search solution without making this insight.


Optimal Solution
----------------

The optimal solution has running time 2^n, and works by transforming
the problem from permutations, to powerset. This is actually the
"dynamic programming" solution of the problem. The idea is that we can
work on building up solutions for smaller subsets of songs, first all
pairs, then all triples, then all quadruples, etc. At each stage of
buliding up the solution size N, we can re-use the optimal paths and
distances for problems of the N-1 size. Because we have to generate
all doubles, triples, quadruples, etc. this is equivalent to
generating the powerset of the input song list (minus the empty set
and size one sets).

Another advantage of this solution, in my opinion, is that this
dynamic programming solution is naturally iterative and not
recursive. It's absolutely possible to generate all of the song
permutations without using recursion, but for some reason it seems
much more difficult to most programmers.

The mixtape.py program provided implements this solution.
