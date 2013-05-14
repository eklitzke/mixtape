import itertools  # only used for verification
import optparse
import random
import time

_DISTANCES = {}

def gen_distances(num):
    """Pre-populate the list of all song distances."""
    for x in xrange(num):
        for y in xrange(num):
            if x != y:
                _DISTANCES[x, y] = random.random()


def dist(x, y):
    """Convenience method to lookup a distance."""
    return _DISTANCES[(x, y)]


def brute_force_solution(num):
    """Compute the best solution by brute force."""
    longest_dist = 0
    best_path = None
    for perm in itertools.permutations(range(num)):
        perm_dist = 0
        for x in xrange(0, num - 1):
            perm_dist += dist(perm[x], perm[x + 1])
        if perm_dist > longest_dist:
            longest_dist = perm_dist
            best_path = perm
    return list(best_path)


def best_mixtape(num, verify=False):
    """Compute the best mixtape for num songs."""
    assert num >= 2
    lookup = {}

    # seed the lookup table with all pairs
    for i in xrange(num):
        for j in xrange(num):
            if i != j:
                key = (1 << (i + 1)) | (1 << (j + 1))
                lookup[(1 << (i + 1), j)] = [i, j], dist(i, j)
                lookup[(1 << (j + 1), i)] = [j, i], dist(j, i)

    # Now we are going to build new lookup tables for all triples,
    # quadruples, etc.
    for _ in xrange(2, num):
        new_lookup = {}
        for song_id in xrange(num):
            for (int_key, last_node), (path, distance) in lookup.iteritems():
                if song_id in path:
                    continue
                new_path = path + [song_id]
                new_dist = distance + dist(last_node, song_id)
                new_key = int_key | (1 << (song_id + 1))

                existing = new_lookup.get((new_key, song_id))
                if existing is None:
                    new_lookup[(new_key, song_id)] = (new_path, new_dist)
                else:
                    if new_dist > existing[1]:
                        new_lookup[(new_key, song_id)] = (new_path, new_dist)
        lookup = new_lookup

    # We've generated all of the lists for size num, we can find the
    # optimal one now. Note that we could have short-cutted in the
    # previous step and not built a full lookup table for the final
    # vector size for a small speedup (at the cost of making this code
    # a bit more difficult to understand.)
    best_path = None
    longest_dist = 0
    for _, (path, distance) in lookup.iteritems():
        if distance > longest_dist:
            longest_dist = distance
            best_path = path

    if verify:
        brute_force = brute_force_solution(num)
        if best_path != brute_force:
            print 'brute_force: %s' % (brute_force,)
            print 'best path: %s' % (best_path,)


    # Return the longest path
    return longest_dist, best_path

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-n', '--num-songs', type='int', default=20)
    parser.add_option('--verify', action='store_true')
    opts, args = parser.parse_args()

    gen_distances(opts.num_songs)
    t0 = time.time()
    longest_dist, best_path = best_mixtape(opts.num_songs, opts.verify)
    elapsed = time.time() - t0
    print 'best mixtape has score %s, order %s in %s seconds' % (
        longest_dist, best_path, elapsed)
