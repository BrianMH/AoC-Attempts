#############################################################
#   Soln for P1 & P2 of Day 11 for AoC
#
# Problem:
#   Seems like an automata question. Basically simulate it for
#   a certain number of turns. Hopefully, it won't be another
#   "simulate this for 20k turns" type of question...
#
#   P2 just asks to simulate until the entire map was wiped.
#   Considering the input array is fairly small, this wasn't
#   that difficult.
#############################################################
from collections import deque
from functools import lru_cache

class OctopusSim:
    '''
        A class that contains a map representing the energy
        levels of the octopus elephants and allows simulating
        of their flashing on a turn-by-turn basis.

        Arguments:
            initFile - An initial state to start from.
            maxVal - The highest value the energy can be at before flashing
    '''
    def __init__(self, initFile: str, maxVal: int):
        self.oMap = self.parseInitState(initFile)
        self.maxVal = maxVal
        self.initFile = initFile

        # helper lambdas
        self.isValid = lambda rInd, cInd: 0 <= rInd < len(self.oMap) and 0 <= cInd < len(self.oMap[0])
        self.tupAdder = lambda tupL, tupR: tuple((valL+valR for valL, valR in zip(tupL, tupR)))

    def parseInitState(self, inFile: str) -> list[list[int]]:
        with open(inFile, 'r') as initFile:
            return [[int(val) for val in list(strLine.rstrip())] for strLine in initFile.readlines()]

    def resetSim(self) -> None:
        self.oMap = self.parseInitState(self.initFile)

    def simulateTurns(self, numTurns: int) -> int:
        return sum([self._simulateTurn()[0] for _ in range(numTurns)])

    def findCompleteWipeTurn(self) -> int:
        '''
            Runs the simulation until the entire map is completely wiped following
            a flash event.

            Returns:
                int - The turn on which the effect occurred.
        '''
        curTurn = 0
        curFlashed = list()
        while len(curFlashed) != (len(self.oMap) * len(self.oMap[0])):
            curTurn += 1
            _, curFlashed = self._simulateTurn()
        return curTurn

    def _simulateTurn(self) -> int:
        '''
            Simulates a single turn in the life of an octopus elephant...

            Returns:
                int - The total number of flashes collected in this turn
                flashedNodes - A list containing all nodes that flashed on this turn
        '''
        flushPts = list()
        for rowInd in range(len(self.oMap)):
            for colInd in range(len(self.oMap[0])):
                self.oMap[rowInd][colInd] += 1
                if self.oMap[rowInd][colInd] > self.maxVal:
                    flushPts.append((rowInd, colInd))

        flashedNodes = self._multiSrcBFS(flushPts)
        for rowInd, colInd in flashedNodes:
            self.oMap[rowInd][colInd] = 0

        return len(flashedNodes), flashedNodes

    def _multiSrcBFS(self, sPts: list[tuple[int, int]]) -> list[tuple[int, int]]:
        '''
            Implements a fairly basic multi-souce BFS (it's effectively the same
            as a single source) that updates the map slowly as it traverses it.

            Arguments:
                sPts - A list containing all source points

            Returns:
                list - A list containing all points that "flashed" this turn.
        '''
        queue = deque(sPts)
        visited = set(sPts)

        while queue:
            curPt = queue.popleft()
            for nPt in self._getNeighbors(curPt):
                self.oMap[nPt[0]][nPt[1]] += 1
                if self.oMap[nPt[0]][nPt[1]] > self.maxVal and nPt not in visited:
                    queue.append(nPt)
                    visited.add(nPt)

        return list(visited)

    @lru_cache
    def _getNeighbors(self, pt: tuple[int, int]) -> list[tuple[int, int]]:
        deltas = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        toRet = list() 
        for delVal in deltas:
            newPt = self.tupAdder(delVal, pt)
            if self.isValid(*newPt):
                toRet.append(newPt)
        return toRet

if __name__ == "__main__":
    # prepare env for p1
    inFile = "./2021/Day11/input"
    octoSim = OctopusSim(inFile, 9)

    # execute algo for p1
    sol1 = octoSim.simulateTurns(100)
    print("The answer to part 1 is {}".format(sol1))

    # and now for p2
    octoSim.resetSim()
    sol2 = octoSim.findCompleteWipeTurn()
    print("The answer to part 2 is {}".format(sol2))