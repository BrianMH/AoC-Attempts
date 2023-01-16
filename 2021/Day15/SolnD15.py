#############################################################
#   Soln for P1 & P2 of Day 15 for AoC
#
# Problem:
#   A path-finding problem that also desires the path to be
#   the path that is the least expensive to traverse (or minimized
#   the risk level). This can be implemented by A* fairly easily,
#   but really any sort of traversal can solve it assuming the
#   unnecessary heads are pruned properly.
#
#   Part 2 extends on this slightly by further assuming that the
#   input only represents a block of size 1/5x1/5 of the original
#   input. The function that performs A* is simply adapted to take
#   a matrix that it can wrap to use for path finding.
#
#   Note: Forgive the horrible ((val - 1)%9)+1 noise. It had to be
#         done because the problem required 9+1 to wrap back to 1...
#############################################################
from functools import lru_cache
import heapq

def parseRiskMaze(inFile: str) -> list[list[int]]:
    with open(inFile, 'r') as initMaze:
        return [[int(val) for val in list(row.strip())] for row in initMaze.readlines()]

Point = tuple[int, int]
def findOptimalPath(sPt: Point, ePt: Point, maze: list[list[int]], * , wrapMat: int = 1) -> list[int]:
    '''
        Finds the risk-minimizing path in a maze. Also allows us to use a wrapped version of
        the matrix as the input if necessary.

        Arguments:
            sPt - The point to start from
            ePt - The end point for the A* algorithm
            maze - The maze structure to iterate over
            wrapMat - The number of times we are allowed to repeat the matrix block
    '''
    # under-evaluating heuristic
    hFunc = lambda curPt: sum([abs(curVal-eVal) for curVal, eVal in zip(curPt, ePt)])
    matMeta = (len(maze)*wrapMat, len(maze[0])*wrapMat)

    # init A*
    visited = {sPt}
    pastNodes = dict()
    pathMinHeap = [(0, sPt)]
    gN = {sPt:0}
    fN = {sPt:hFunc(sPt)}

    # And then somewhat greedily explore points
    while pathMinHeap:
        _, curNode = heapq.heappop(pathMinHeap)
        if curNode == ePt:
            return generatePathFromHist(pastNodes, curNode)

        # otherwise continue searching neighbors
        for posNode in getNeighborNodes(curNode, *matMeta):
            lBlockDist = (posNode[0]//len(maze)) + (posNode[1]//len(maze[0]))
            nextGN = gN[curNode] + (((maze[posNode[0]%len(maze)][posNode[1]%len(maze[0])] + lBlockDist)-1)%9) + 1
            if nextGN < gN.get(posNode, 9999999):
                pastNodes[posNode] = curNode
                gN[posNode] = nextGN
                fN[posNode] = nextGN + hFunc(posNode)
                if posNode not in visited:
                    visited.add(posNode)
                    heapq.heappush(pathMinHeap, (fN[posNode], posNode))

    return -1

@lru_cache
def getNeighborNodes(curPt: Point, maxY: int, maxX: int) -> list[Point]:
    tupAdder = lambda tupL, tupR: tuple((lVal+rVal for lVal, rVal in zip(tupL, tupR)))
    isValid = lambda ptY, ptX: 0 <= ptY < maxY and 0 <= ptX < maxX
    deltas = [(-1, 0), (1, 0), (0, 1), (0, -1)]

    toRet = list()
    for delVal in deltas:
        newPt = tupAdder(delVal, curPt)
        if isValid(*newPt):
            toRet.append(newPt)

    return toRet

def generatePathFromHist(pNodes: dict[Point, Point], curNode: Point) -> list[int]:
    '''
        A helper function for the A* function. Given the history dict and the last
        node traversed, this function builds up the path in reverse and flips it.

        Arguments:
            pNodes - A dictionary representing the past node connections.
            curNode - The node to begin creating the path from.
        
        Returns:
            list - A list representing the chain of nodes traversed to reach the
                   final node. Note that this contains their coordinates, not their
                   values in the matrix.
    '''
    path = [curNode]
    while curNode in pNodes:
        curNode = pNodes[curNode]
        path.append(curNode)
    return list(reversed(path))

if __name__ == "__main__":
    # prepare env for p1
    inFile = "./2021/Day15/input"
    rMaze = parseRiskMaze(inFile)

    # execute algo for p1
    sPt, ePt = (0, 0), (len(rMaze)-1, len(rMaze[0])-1)
    optPath = findOptimalPath(sPt, ePt, rMaze)
    sol1 = sum([rMaze[xVal][yVal] for xVal, yVal in optPath[1:]])
    print("The answer to part 1 is {}".format(sol1))

    # and now for p2
    sPt, ePt = (0, 0), (len(rMaze)*5-1, len(rMaze[0])*5-1)
    optPath = findOptimalPath(sPt, ePt, rMaze, wrapMat = 5)
    sol2 = sum([((rMaze[xVal%len(rMaze)][yVal%len(rMaze[0])]+(xVal//len(rMaze)+yVal//len(rMaze[0]))-1)%9)+1 for xVal, yVal in optPath[1:]])
    print("The answer to part 2 is {}".format(sol2))