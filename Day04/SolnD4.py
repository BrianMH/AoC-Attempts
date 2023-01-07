###############################################################
#   Soln for P1 of Day 4 for AoC
#
# Problem:
#     Given an input consisting of pairs of ranges, count the
#     number of completely overlapping ranges. Pairs are not
#     important based on their order so A can be a subset of B
#     as much as B can be a subset of A.
###############################################################
# counts number of subset ranges that are present in the list
# This could be done using a set-like manner, but brute-force is
# concise enough for single intersections like this
def p1Soln(inFile: str) -> int:
    numSubsets = 0

    with open(inFile, 'r') as pairList:
        ranges = pairList.readline().rstrip().split(',')
        while len(ranges) == 2:
            r1, r2 = ranges
            x1, x2 = (int(val) for val in r1.split('-'))
            y1, y2 = (int(val) for val in r2.split('-'))

            # Enforce y1 > x1 or y2 > x2 if x1 == y1
            if not y1 >= x1 or (y1 == x1 and y2 > x2):
                x1, x2, y1, y2 = y1, y2, x1, x2

            # Then check other boundary for subset equality
            if y2 <= x2:
                # print("{}-{} is a subset of {}-{}".format(y1, y2, x1, x2))
                numSubsets += 1

            # Then parse next values
            ranges = pairList.readline().rstrip().split(',')
        
    return numSubsets

###############################################################
#   Soln for P2 of Day 4 for AoC
#
# Problem:
#     Given an input consisting of pairs of ranges, count the
#     number of overlapping ranges. Overlap does not need to be
#     subset containment like the last problem.
###############################################################
# A similar approach to above is used. The only difference is that
# checking for ANY form of subset can be done by instead checking to see
# if any of the border values of the second pair are between the first's
# boundaries
def p2Soln(inFile: str) -> int:
    numOverlaps = 0

    with open(inFile, 'r') as pairList:
        ranges = pairList.readline().rstrip().split(',')
        while len(ranges) == 2:
            r1, r2 = ranges
            x1, x2 = (int(val) for val in r1.split('-'))
            y1, y2 = (int(val) for val in r2.split('-'))

            # Enforce y1 > x1 or y2 > x2 if x1 == y1
            if not y1 >= x1 or (y1 == x1 and y2 > x2):
                x1, x2, y1, y2 = y1, y2, x1, x2

            # Then check other boundary for any overlap
            if x1 <= y1 <= x2 or x1 <= y2 <= x2:
                # print("{}-{} overlaps {}-{}".format(y1, y2, x1, x2))
                numOverlaps += 1

            # Then parse next values
            ranges = pairList.readline().rstrip().split(',')
        
    return numOverlaps

if __name__ == "__main__":
    # Set up env for p1
    inFile = "./Day04/input"

    # Evaluate p1
    sol1 = p1Soln(inFile)
    print("Solution to p1 is {}".format(sol1))

    # Evaluate p2
    sol2 = p2Soln(inFile)
    print("Solution to p2 is {}".format(sol2))