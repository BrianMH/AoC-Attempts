###############################################################
#   Soln for P1 and P2 of Day 18 for AoC
#
# Problem:
#     There is a 3D object of sorts that is being explored.
#     Essentially, we need to count the number of faces that is has
#     for part 1.
#     For part 2, we have to ignore any faces that are internal
#     which means restricting the points visited by our traversal.
###############################################################
from functools import lru_cache
from collections import deque

def parseCubes(inFile: str) -> set[tuple[int, int, int]]:
    cubes = set()
    with open(inFile, 'r') as cubeIns:
        nLine = cubeIns.readline()
        while nLine:
            cubes.add(tuple((int(pos) for pos in nLine.rstrip().split(','))))
            nLine = cubeIns.readline()
    return cubes

adder = lambda tup1, tup2:(tup1[0] + tup2[0], tup1[1] + tup2[1], tup1[2] + tup2[2])
@lru_cache
def adjPos(inCoord: tuple[int, int, int]) -> tuple[tuple[int, int, int]]:
    deltas = [(0, 0, 1), (0, 1, 0), (1, 0 ,0)]
    return tuple((adder(inCoord, delta) for delta in deltas))

@lru_cache
def adjNeg(inCoord: tuple[int, int, int]) -> tuple[tuple[int, int, int]]:
    deltas = [(0, 0, -1), (0, -1, 0), (-1, 0, 0)]
    return tuple((adder(inCoord, delta) for delta in deltas))

# A face is countable pretty much if there's no neighboring cube. So, we can
# test for any adjacent structures to determine the face count.
def countFaces(cubes: set[tuple[int, int, int]]) -> int:
    numFaces = 0
    for cubeCoord in cubes:
        numFaces += 6
        posCubes = adjPos(cubeCoord)
        for check in posCubes:
            if check in cubes:
                numFaces -= 2

    return numFaces

# In this case, it's a bother to start with identifying any inner sections, so
# we use a floodfill to count any faces that we can see from outside
def countExteriorFaces(cubes: set[tuple[int, int, int]], minCoord: tuple[int, int, int], maxCoord: tuple[int, int, int]) -> int:
    numFaces = 0
    coordQueue = deque()
    visited = set()
    coordQueue.appendleft(minCoord)
    validCoord = lambda coord: (minCoord[0] <= coord[0] <= maxCoord[0]) and (minCoord[1] <= coord[1] <= maxCoord[1]) and (minCoord[2] <= coord[2] <= maxCoord[2])

    while coordQueue:
        curCoord = coordQueue.pop()
        if curCoord in visited:
            continue
        else:
            visited.add(curCoord)
        posCoords = adjPos(curCoord) + adjNeg(curCoord)

        for pos in posCoords:
            if validCoord(pos) and pos not in visited:
                if pos in cubes:
                    numFaces += 1
                else:
                    coordQueue.appendleft(pos)

    return numFaces

if __name__ == "__main__":
    # prepare env for p1
    inFile = './2022/Day18/input'

    # Execute algo for p1
    cubeCoords = parseCubes(inFile)
    sol1 = countFaces(cubeCoords)
    print("The solution to part 1 is {}".format(sol1))

    # Execute algo for p2
    sol2 = countExteriorFaces(cubeCoords, (-1, -1, -1), (50, 50, 50))
    print("The solution to part 2 is {}".format(sol2))