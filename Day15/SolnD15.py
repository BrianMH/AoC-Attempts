###############################################################
#   Soln for P1 of Day 15 for AoC
#
# Problem:
#     Given a set of readings that indicate the closest beacon
#     given any sensor, indicate the number of positions for
#     a given row that are guaranteed to not contain another
#     beacon.
#     THe main intuition in this problem is that if there is a 
#     signal-beacon reading in one spot, then for any other point
#     with an L1 distance equal to or lower than the one between
#     the sensor and beacon, there must not exist any other beacon.
###############################################################
'''
    Parses input file and returns a tuple containing each sensor's location
    and guaranteed-to-be-clear L1 distance and a set containing known beacon
    locations.
'''
import re
from multiprocessing import Process

l1Dist = lambda loc1, loc2: abs(loc2[0]-loc1[0]) + abs(loc2[1]-loc1[1])

def parseSensorStrengths(inFile: str) -> tuple[dict[tuple[int, int], int], set[tuple[int, int]]]:
    template = r'Sensor at x=(?P<xS>-?[0-9]+), y=(?P<yS>-?[0-9]+): ' \
               r'closest beacon is at x=(?P<xB>-?[0-9]+), y=(?P<yB>-?[0-9]+)'
    beaconLocs = set()
    sensorDists = dict()


    with open(inFile, 'r') as coordInputs:
        curLine = coordInputs.readline()
        while curLine:
            matched = re.match(template, curLine).groupdict()
            beaconLoc = (int(matched['xB']), int(matched['yB']))
            sensorLoc = (int(matched['xS']), int(matched['yS']))

            beaconLocs.add(beaconLoc)
            sensorDists[sensorLoc] = l1Dist(beaconLoc, sensorLoc)
            curLine = coordInputs.readline()

    return sensorDists, beaconLocs

'''
    Takes in the row to be checked as an input along with a dict containing the
    sensor locations and the L1 distance of the beacon they connected to. 
    This function then returns the number of positions on that row that are known to
    be a non-viable location of another beacon.
'''
def checkLineOverlap(relRow: int, signalLocDists: dict[tuple[int, int], int], 
                     beaconLocs: set[tuple[int, int]]) -> int:
    numBlockedLocs = set()
    overlapBlocks = 0
    unusedBLocs = set()
    unusedBLocs.update(beaconLocs)
    used = list()

    # Go through every sensor location and calculate ranges per point and intersect them
    # to find the total number of blocked locations
    xMin = float('inf')
    for sensorLoc, maxDist in signalLocDists.items():
        yDelta = abs(relRow - sensorLoc[1])
        if yDelta >= 0:
            leftDist = maxDist - yDelta
            xMin = sensorLoc[0] - leftDist
            xMax = sensorLoc[0] + leftDist
            numBlockedLocs.update(list(range(xMin, xMax+1)))

            for bLoc in unusedBLocs:
                if bLoc[1] == relRow and xMin <= bLoc[0] <= xMax:
                    overlapBlocks += 1
                    used.append(bLoc)
            if used:
                for bLoc in used:
                    unusedBLocs.remove(bLoc)
                used = list()

    return len(numBlockedLocs) - overlapBlocks

###############################################################
#   Soln for P2 of Day 15 for AoC
#
# Problem:
#     With the same map generated from the points parsed above,
#     now find the single point within the indicated square grid
#     that is the only potential solution for the possible beacon
#     recorded.
#
# Note:
#     Upon consideration, if we imagine every diamond region being
#     extended out by one sector, then we will be guaranteed that
#     one of those intersections will be where the empty point
#     is situated. The only problem is that there can be up to two
#     points of intersection for each diamond and checking would
#     require computing the intersection of 4*(num_sensors) lines
#     between each other, effectively making for a O(N^2) operation.
#
#     I haven't implemented a line class that computes intersections
#     before so it does seem like an interesting way to approach it.
#     Might try it out sooner rather than later.
###############################################################
'''
    This function will by far be the one that takes the longest to execute. Naively checking
    between all the coordinates one-by-one will take far too long. Instead, we use a tactic
    similar to above and find the largest increment by which we can move the cursor along
    the x-direction and then push it that far.
    Because we know there is only one solution, we can also attempt to parallelize the search
    along different y-directions. Might look into it later as the solution does take a bit 
    of time to execute, but it does seem to return the proper answer...
'''
def checkForEmptyLoc(minCoord: int, maxCoord: int, signalLocDists: dict[tuple[int, int], int]) -> tuple[int, int]:
    yCur = minCoord

    while yCur <= maxCoord:
        xCur = minCoord    
        while xCur <= maxCoord:
            maxJump = -1
            for sensorLoc, maxDist in signalLocDists.items():
                curDelta = maxDist - l1Dist((xCur, yCur), sensorLoc)
                maxJump = max(maxJump, curDelta)

            if maxJump == -1:
                return (xCur, yCur)
            else:
                xCur += maxJump + 1
        yCur += 1

    return (-1, -1)

if __name__ == "__main__":
    # prepare env for p1
    inFile = './Day15/input'

    # execute algo for p1
    sDists, bLocs = parseSensorStrengths(inFile)
    sol1 = checkLineOverlap(2000000, sDists, bLocs)
    print("Solution to part 1 is {}".format(sol1))

    # execute algo for p2
    solLoc = checkForEmptyLoc(0, 4000000, sDists)
    sol2 = solLoc[0] * 4000000 + solLoc[1]
    print("Solution to part 2 is {}".format(sol2))