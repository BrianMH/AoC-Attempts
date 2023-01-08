###############################################################
#   Soln for P1 & P2 of Day 12 for AoC
#
# Problem:
#     Given a 2d mapping of heights codified by the letters 'a'-'z',
#     return the length of the shortest path from the start point S
#     to the end point E assuming the following:
#         1) if your travel height is some letter 'c', then you can only
#            traverse to any section of land from 'a' to 'd' (AT MOST 'c'+1)
#
#     For part 2, we consider the problem to be inverted. We instead look
#     for the shortest path from 'Z' to any 'a' under the assumption that
#     we only can step down a maximum height of 1 in order to preserve the
#     property from above when the path is flipped.
#
# Note:
#     I did submit the solution quite early, but it was a naive implementation
#     that called the original BFS on every unique 'a' or 'S'. This runs a lot
#     better and is probably what was being looked for anyway.
###############################################################
from collections import deque

def enumRelNeighbors(curPt: tuple, arrMap: list[str], invertOrder: bool) -> list[tuple[int, int]]:
    relDeltas = [(0,-1), (0, 1), (1, 0), (-1, 0)]
    validBounds = lambda x,y: (0 <= x < len(arrMap)) and (0 <= y < len(arrMap[0]))
    charMutator = lambda char: 'a'*(char=='S') or 'z'*(char=='E') or char
    if not invertOrder:
        validChar = lambda oldChar, newChar: ord(newChar) <= ord(oldChar) + 1
    else:
        validChar = lambda oldChar, newChar: ord(newChar) >= ord(oldChar) - 1
    relList = list()
    curChar = charMutator(arrMap[curPt[0]][curPt[1]])

    for curDelta in relDeltas:
        newPt = (curPt[0] + curDelta[0], curPt[1] + curDelta[1])
        if validBounds(*newPt):
            newChar = charMutator(arrMap[newPt[0]][newPt[1]])
            if validChar(curChar, newChar):
                relList.append(newPt)

    return relList

# parses the map for the problem and returns our start and
# ands out of convenience
def initializeArrMapPts(inFile: str, startChars: str, endChar: str) -> tuple[list[str], tuple[int, int], list[tuple[int, int]]]:
    # parse in our heigh array
    with open(inFile, 'r') as arrMapInput:
        arrMap = [line.rstrip() for line in arrMapInput.readlines()]

    # locate our starting point and end points
    sPoint = (-1, -1)
    ePoint = list()
    for xInd in range(len(arrMap)):
        for yInd in range(len(arrMap[0])):
            if arrMap[xInd][yInd] in startChars:
                sPoint = (xInd, yInd)
            elif arrMap[xInd][yInd] == endChar:
                ePoint.append((xInd, yInd))

    return arrMap, sPoint, ePoint

def bfsLen(inFile: str, startChar: str, endChar: str, invertOrder: bool = False) -> int:
    arrMap, sPoint, ePoint = initializeArrMapPts(inFile, startChar, endChar)

    # Now begin our typical map traversal while focusing on the 
    # closest possible paths
    visited = {sPoint: False}
    visQueue = deque([(int(0), sPoint)])
    
    while visQueue:
        curDist, curPt = visQueue.pop()
        if curPt in ePoint:
            return curDist

        # otherwise continue searching
        posNeighbors = enumRelNeighbors(curPt, arrMap, invertOrder)
        for curNeighbor in posNeighbors:
            if not visited.get(curNeighbor, False):
                visited[curNeighbor] = True
                visQueue.appendleft((curDist + 1, curNeighbor))

    return -1

if __name__ == "__main__":
    # set up env for p1
    inFile = './2022/Day12/input'

    # execute algo
    sol1 = bfsLen(inFile, "S", "E")
    print("Solution for part 1 is {}".format(sol1))

    # now for part 2
    sol2 = bfsLen(inFile, "E", "a", invertOrder = True)
    print("Solution for part 2 is {}".format(sol2))