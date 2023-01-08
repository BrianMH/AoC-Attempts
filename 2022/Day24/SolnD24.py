###################################################################
#   Soln for P1&P2 of Day 24 for AoC
#
# Problem:
#     Seems misleadingly simple. This should be a BFS where the
#     branches of the path chosen are either:
#        1) Move Down*
#        2) Move Right*
#        3) Move Up*
#        4) Move Left*
#        5) Wait
#    One thing to immediately notice is that there is a periodicity
#    in the map, which can allow us to hard-code this map and use a
#    traversal algorithm to pick the optimal path.
####################################################################
from functools import lru_cache
from collections import defaultdict
from typing import Optional
import heapq
import numpy as np

class BlizzardCrossing:
    class CellElements:
        WALL = "#"
        EMPTY = "."
        BLIZ_TO_DEL = {"<":(0, -1), ">":(0, 1), "^":(-1, 0), "v":(1, 0)}

    def __init__(self, inFile: str):
        # Parse initial map state
        walls, blizzards = self.parseInputBlizzards(inFile)
        self.sPos, self.ePos = self.extrapolateStartEndPos(walls)
        self.timeMap = self.generateAllMaps(walls, blizzards)

        # helper lams
        self.isValid = lambda timeInd, rowInd, colInd: (0 <= rowInd < self.timeMap.shape[1]) and (0 <= colInd < self.timeMap.shape[2]) and (0 <= timeInd < self.timeMap.shape[0])
        self.tupAdder = lambda tupL, tupR:((tupL[0] + tupR[0])%self.timeMap.shape[0], tupL[1] + tupR[1], tupL[2] + tupR[2])
        self.heuristic = lambda pt1: abs(pt1[1]-self.ePos[0]) + abs(pt1[2]-self.ePos[1]) # time is not factored here as the exit exists at all times

    '''
        Uses A* in order to find a minimum time path to travel from the start to the finish.
        Supports a custom heuristic, but a simple Manhattan distance should function here.
    '''
    def getMinTimeToGoal(self, * , custStart: Optional[tuple[int, int, int]|None] = None, custEnd: Optional[tuple[int, int]] = None) -> int:
        # Get heuristic ready for use
        hFunc = self.heuristic

        # Prepare algorithm (re-centers start if necessary)
        startPos = (0, *self.sPos) if custStart is None else self.tupAdder(custStart, (0, 0, 0))
        endPos = self.ePos if custEnd is None else custEnd
        visited = {startPos}
        pathMinHeap = [(0, startPos)]
        pastNodes = dict()
        gN = {startPos:0}
        fN = {startPos:hFunc(startPos)}

        while pathMinHeap:
            _, curNode = heapq.heappop(pathMinHeap)
            if curNode[1:] == endPos:
                return len(self._generatePath(pastNodes, curNode)) - 1
            
            posNodes = [node for node in self._generatePosMoves(curNode) if (self.isValid(*node) and self.timeMap[node] != self.CellElements.WALL)]
            for posNode in posNodes:
                nextGN = gN[curNode] + 1
                if nextGN < gN.get(posNode, 10000):
                    pastNodes[posNode] = curNode
                    gN[posNode] = nextGN
                    fN[posNode] = nextGN + hFunc(posNode)
                    if posNode not in visited:
                        visited.add(posNode)
                        heapq.heappush(pathMinHeap, (fN[posNode], posNode))

        return -1
    
    '''
        Since we know the blizzards are periodic w.r.t. the size of the columns and rows
        of the entire maze, a 3d-maze composed in time exists of depth LCM(col_space, row_space)
        that represents the entirety of the maze across time as well.
        This function expands all the possible dimensions and converts them into walls. Since
        the space is relatively dense, a normal 3d matrix is sufficient for this.
    '''
    def generateAllMaps(self, walls: set[tuple[int, int]], blizzards: dict[tuple[int, int], tuple[int, int]]) -> np.ndarray:
        # Now create maps to populate the array with the blizzards
        emptyMap = self._createEmptyMap(walls)
        self.blizWrapper = lambda oLoc, delta: ((oLoc[0] - 1 + delta[0])%(emptyMap.shape[1]-2) + 1, (oLoc[1] - 1 + delta[1])%(emptyMap.shape[2]-2) + 1)
        
        # Now populate the blizzards in each time stemp, converting them to walls
        curState = blizzards
        for timeInd in range(emptyMap.shape[0]):
            newState = defaultdict(list)
            for blizzardPos, deltas in curState.items():
                emptyMap[timeInd, blizzardPos[0], blizzardPos[1]] = self.CellElements.WALL
                for delta in deltas:
                    newState[self.blizWrapper(blizzardPos, delta)].append(delta)
            curState = newState

        return emptyMap

    ############### HELPER FUNCS ####################
    @lru_cache
    def _generatePosMoves(self, curPos: tuple[int, int]):
        deltas = [(1, 0, 1), (1, 1, 0), (1, -1, 0), (1, 0, -1), (1, 0, 0)]
        return [self.tupAdder(curPos, delVal) for delVal in deltas]
    
    '''
        Uses a previously visited dictionary to discover the path used in A*
    '''
    def _generatePath(self, pastDict: dict[tuple[int, int, int], tuple[int, int, int]], curNode: tuple[int, int, int]) -> list[tuple[int, int, int]]:
        path = [curNode]
        while curNode in pastDict:
            curNode = pastDict[curNode]
            path.append(curNode)
        return list(reversed(path))

    '''
        Simple LCM implementation. Add values and factor until the digits are 1 and then find
        the union between the two sets.
    '''
    def _LCM(self, valL: int, valR: int) -> int:
        # Factor values
        lSet = self._factorVal(valL)
        rSet = self._factorVal(valR)

        # Use their factors to generate the LCM
        keySet = set()
        keySet.update(lSet.keys())
        keySet.update(rSet.keys())
        res = 1

        # Find their union and return the product of these values
        for factor in keySet:
            res *= factor ** max(lSet.get(factor, 0), rSet.get(factor, 0))

        return res

    '''
        Given a value, factor it into its prime factors along with their
        multiplicities
    '''
    def _factorVal(self, val) -> dict[int, int]:
        facSet = dict()
        curFactor = 2
        while val > 1:
            if val%curFactor == 0:
                facSet[curFactor] = facSet.get(curFactor, 0) + 1
                val //= curFactor
            else:
                curFactor += 1
    
        return facSet

    def _createEmptyMap(self, walls: set[tuple[int, int]]) -> np.ndarray:
        # Extract maze size
        xVals = [x for x, _ in walls]
        yVals = [y for _, y in walls]
        xRange, yRange = max(xVals) + 1, max(yVals) + 1
        timeRange = self._LCM(xRange-2, yRange-2) # Note that there are no vert blizzards on first/last col to preserve this property

        # Generate empty array with proper sizing
        twoDMap = [[self.CellElements.EMPTY] * yRange for _ in range(xRange)]
        for xC, yC in walls:
            twoDMap[xC][yC] = self.CellElements.WALL

        return np.repeat(np.expand_dims(np.array(twoDMap), axis = 0), timeRange, axis = 0)
    
    ################### PARSING #################
    '''
        Does all the position parsing for the blizzards and walls.
    '''
    def parseInputBlizzards(self, inFile: str) -> tuple[set[tuple[int, int]], dict[tuple[int, int], tuple[int, int]]]:
        wallPos = set()
        blizzards = dict()
        with open(inFile, 'r') as inMap:
            curRowInd = 0
            curLine = inMap.readline().rstrip()
            while curLine:
                for curColInd, elem in enumerate(curLine):
                    if elem == self.CellElements.WALL:
                        wallPos.add((curRowInd, curColInd))
                    elif elem in self.CellElements.BLIZ_TO_DEL:
                        blizzards[(curRowInd, curColInd)] = [self.CellElements.BLIZ_TO_DEL[elem]]

                curRowInd += 1
                curLine = inMap.readline().rstrip()
        
        return wallPos, blizzards
    
    '''
        Using known walls, find the start and ending positions
    '''
    def extrapolateStartEndPos(self, walls: set[tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
        rVals = [rowVal for rowVal, _ in walls]
        minRow, maxRow = min(rVals), max(rVals)
        startCol = 0
        while (minRow, startCol) in walls:
            startCol += 1
        endCol = 0
        while (maxRow, endCol) in walls:
            endCol += 1
        return (minRow, startCol), (maxRow, endCol)
    
if __name__ == "__main__":
    # prepare env for p1
    inFile = "./2022/Day24/input"
    curMaze = BlizzardCrossing(inFile)

    # exec algo for p1 
    sol1 = curMaze.getMinTimeToGoal()
    print("The solution to part 1 is {}".format(sol1))

    # Given the first part, we now calculate the time back and then forward again.
    # This can be done by getting the total time and using that as the starting point
    # for our algorithm.
    sol2P2 = curMaze.getMinTimeToGoal(custStart = (sol1, *curMaze.ePos), custEnd = curMaze.sPos)
    sol2P3 = curMaze.getMinTimeToGoal(custStart = (sol1+sol2P2, *curMaze.sPos))
    print("The solution to part 2 is {} = {}+{}+{}".format(sol1+sol2P2+sol2P3, sol1, sol2P2, sol2P3))