#############################################################
#   Soln for P1 of Day 25 for AoC
#
# Problem:
#   A simulation problem. Since this is day 25, we can also
#   take a few shortcuts when dealing with the problem since
#   we know there won't be a second part to it.
#############################################################
from functools import lru_cache

Point = tuple[int, int]
class SeaCucumberSim:
    def __init__(self, initFile: str):
        # constants for arena
        self.EMPTY = '.'
        self.SCUC = 'v'
        self.ECUC = '>'

        self.sCumber, self.eCumber, self.lims = self.parseInitialState(initFile)
        self.curRound = 0

    def parseInitialState(self, inFile: str) -> tuple[set[Point], set[Point], tuple[int, int]]:
        sMat, eMat = set(), set()
        rowInd = -1
        
        with open(inFile, 'r') as inState:
            curLine = inState.readline()
            arenaWidth = len(curLine.strip())
            while curLine:
                rowInd += 1
                for colInd in range(len(curLine.strip())):
                    if curLine[colInd] == self.SCUC:
                        sMat.add((rowInd, colInd))
                    elif curLine[colInd] == self.ECUC:
                        eMat.add((rowInd, colInd))
                curLine = inState.readline()
            arenaHeight = rowInd + 1

        lims = (arenaHeight, arenaWidth)
        return sMat, eMat, lims

    def simulateRound(self) -> bool:
        '''
            Simulates a round and returns a boolean value which indicates if any
            of the cucumbers moved locations. Note that a round is defined as a
            the time it takes for both the east and south-facing cucumbers to
            move to their new spots.
        '''
        self.curRound += 1
        changedElem = False

        # process the eastward cucumbers first
        newECumber = set()
        for ePos in self.eCumber:
            newPos = self._tupAdder(ePos, (0, 1))
            if newPos not in self.eCumber and newPos not in self.sCumber:
                newECumber.add(newPos)
                changedElem = True
            else:
                newECumber.add(ePos)
        self.eCumber = newECumber

        # And now process the southward cucumbers
        newSCumber = set()
        for sPos in self.sCumber:
            newPos = self._tupAdder(sPos, (1, 0))
            if newPos not in self.eCumber and newPos not in self.sCumber:
                newSCumber.add(newPos)
                changedElem = True
            else:
                newSCumber.add(sPos)
        self.sCumber = newSCumber

        return changedElem

    def __str__(self) -> str:
        retStr = ""
        for rowInd in range(self.lims[0]):
            for colInd in range(self.lims[1]):
                if (rowInd, colInd) in self.eCumber:
                    retStr += self.ECUC
                elif (rowInd, colInd) in self.sCumber:
                    retStr += self.SCUC
                else:
                    retStr += self.EMPTY
            retStr += "\n"
        return retStr
    
    @lru_cache
    def _tupAdder(self, tupL: Point, tupR: Point) -> Point:
        return tuple(((lVal+rVal)%lim for lVal, rVal, lim in zip(tupL, tupR, self.lims)))

if __name__ == "__main__":
    # prepare env for p1
    inFile = "./2021/Day25/input"
    curSim = SeaCucumberSim(inFile)

    # execute algo for p1
    while(curSim.simulateRound()):
        continue

    sol1 = curSim.curRound
    print("The answer to part 1 is {}".format(sol1))
