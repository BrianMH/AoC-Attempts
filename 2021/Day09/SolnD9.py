#############################################################
#   Soln for P1 of Day 9 for AoC
#
# Problem:
#   Given a 2D height map, identify the "low points" [AKA 
#   points that are smaller than all of their adjacent values]
#   and return the sum of their risk levels (level + 1).
#############################################################
from functools import lru_cache
from typing import Callable
from collections import deque

# Simplifies some of the function calls
Point = tuple[int, int]

@lru_cache
def getNeighbors(curPoint: Point, fieldWidth: int, fieldHeight: int) -> list[Point, ...]:
    adder = lambda tupL, tupR: tuple((valL+valR for valL, valR in zip(tupL, tupR)))
    isValid = lambda point: 0 <= point[0] < fieldHeight and 0 <= point[1] < fieldWidth
    deltas = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    toRet = list()
    for delVal in deltas:
        newPt = adder(delVal, curPoint)
        if isValid(newPt):
            toRet.append(newPt)
    return toRet

def findLowPoints(heightMap: list[list[int]]) -> tuple[list[Point], list[int]]:
    '''
        Finds the low points and returns the height values
        at those points.
    '''
    relHeights = list()
    relPts = list()
    for rowInd in range(len(heightMap)):
        for colInd in range(len(heightMap[0])):
            nPts = getNeighbors((rowInd, colInd), len(heightMap[0]), len(heightMap))
            allLow = True

            for tComp in nPts:
                if heightMap[rowInd][colInd] >= heightMap[tComp[0]][tComp[1]]:
                    allLow = False
                    break
            
            if allLow:
                relHeights.append(heightMap[rowInd][colInd])
                relPts.append((rowInd, colInd))
    return relPts, relHeights

def parseMap(inFile: str) -> list[list[int]]:
    with open(inFile, 'r') as mapInput:
        return [[int(val) for val in list(rowStr)] for rowStr in mapInput.read().strip().split('\n')]

#############################################################
#   Soln for P2 of Day 9 for AoC
#
# Problem:
#   Instead of calculating their risk levels, we must "flow"
#   inward to the point to mark what positions form a basin.
#
#   Seems like this question can be solved through a BFS that
#   takes into account the last value. If any value higher than
#   the current low value exists, it gets appended to the visited set
#   and the BFS continues. A low point, by default, has at least
#   2 other points to "initiate" a basin. 9's do not belong to
#   any basin.
#############################################################
def getBasinSize(sPt: Point, hMap: list[list[int]]) -> int:
    queue = deque([(sPt, hMap[sPt[0]][sPt[1]])])
    visited = {sPt}
    mapMD = (len(hMap[0]), len(hMap))

    while queue:
        curPt, curHt = queue.popleft()

        intPts = getNeighbors(curPt, *mapMD)
        for pt in intPts:
            if pt not in visited and curHt < hMap[pt[0]][pt[1]] < 9:
                visited.add(pt)
                queue.append((pt, hMap[pt[0]][pt[1]]))

    return len(visited)

if __name__ == "__main__":
    # prepare env for p1
    inFile = "./2021/Day09/input"

    # execute algo for p1
    hMap = parseMap(inFile)
    lowPts, lpHeights = findLowPoints(hMap)
    print("The answer to part 1 is {}".format(sum([val+1 for val in lpHeights])))

    # and now for p2
    lpBasinSizes = sorted([getBasinSize(pt, hMap) for pt in lowPts], reverse = True)
    print("The answer to aprt 2 is {}".format(lpBasinSizes[0]*lpBasinSizes[1]*lpBasinSizes[2]))