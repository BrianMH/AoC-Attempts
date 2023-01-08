###############################################################
#   Soln for P1 & P2 of Day 23 for AoC
#
# Problem:
#     Seems like an automata question. The order in which the
#     evolution is considered changes as time moves, which only
#     means that functors along with a modulus should make things
#     function quickly here.
#     Part 2 is just running until the simulation stalls.
###############################################################
from collections import defaultdict

class ElfAutomata():
    def __init__(self, initialStateFile: str):
        self.ruleOffset = -1
        self.curRound = 0
        self.xMin, self.xMax = 100000, 0
        self.yMin, self.yMax = 100000, 0
        self.elfPosVals = self.parseInitialState(initialStateFile)
        self.updateLimits()

        # sets up the rules
        allDeltas = [(-1, -1), (-1, 1), (1, 1), (1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)]
        tupAdder = lambda tupL, tupR: (tupL[0] + tupR[0], tupL[1] + tupR[1])
        self.stayLam = lambda curPos: True if sum([tupAdder(curPos, delta) in self.elfPosVals for delta in allDeltas]) == 0 else False
        NMoveLam = lambda curX, curY: (curX-1, curY) if sum(((curX-1, curY) in self.elfPosVals, \
                                                              (curX-1, curY-1) in self.elfPosVals, \
                                                              (curX-1, curY+1) in self.elfPosVals)) == 0 else None
        SMoveLam = lambda curX, curY: (curX+1, curY) if sum(((curX+1, curY) in self.elfPosVals, \
                                                              (curX+1, curY-1) in self.elfPosVals, \
                                                              (curX+1, curY+1) in self.elfPosVals)) == 0 else None
        WMoveLam = lambda curX, curY: (curX, curY-1) if sum(((curX+1, curY-1) in self.elfPosVals, \
                                                              (curX, curY-1) in self.elfPosVals, \
                                                              (curX-1, curY-1) in self.elfPosVals)) == 0 else None
        EMoveLam = lambda curX, curY: (curX, curY+1) if sum(((curX+1, curY+1) in self.elfPosVals, \
                                                              (curX, curY+1) in self.elfPosVals, \
                                                              (curX-1, curY+1) in self.elfPosVals)) == 0 else None
        self.atomRules = [NMoveLam, SMoveLam, WMoveLam, EMoveLam]

    """
        Simulates the automata for a given number of rounds. If the runUntilStall flag is
        passed as True, then the number of rounds is ignored and the program simply runs until
        no movements are made and returns the round number when nothing moves.
    """
    def simulate(self, * , numRounds: int = 1, runUntilStall: bool = False) -> int:
        simRoundCount = 0

        while simRoundCount < numRounds or runUntilStall:
            self.ruleOffset = (self.ruleOffset + 1)%len(self.atomRules)
            self.curRound += 1
            simRoundCount += 1

            # Calculate potential movements (add any non-movers immediately)
            afterBeforeDict = defaultdict(list)
            afterElfVals = set()
            for elfPos in self.elfPosVals:
                if self.stayLam(elfPos):
                    afterElfVals.add(elfPos)
                    continue

                moved = False
                for curLamInd in range(len(self.atomRules)):
                    lamRes = self.atomRules[(self.ruleOffset+curLamInd)%len(self.atomRules)](*elfPos)
                    if lamRes is not None:
                        moved = True
                        afterBeforeDict[lamRes].append(elfPos)
                        break
                if not moved:
                    afterElfVals.add(elfPos)

            # Perform movements on any elves who won't be overlapping
            if len(afterElfVals) == len(self.elfPosVals): # no movements made
                return self.curRound
            
            for potMovedElf in afterBeforeDict.keys():
                if len(afterBeforeDict[potMovedElf]) > 1:
                    afterElfVals.update(afterBeforeDict[potMovedElf])
                else:
                    afterElfVals.add(potMovedElf)
            self.elfPosVals = afterElfVals
        
        self.updateLimits() # update limits after rounds are done
        return -1

    # Given the limits, simply calculates the number of empty spaces available in the area
    def calculatePart1Ans(self):
        return (self.yMax-self.yMin+1)*(self.xMax-self.xMin+1) - len(self.elfPosVals)

    def parseInitialState(self, inFile: str) -> set[tuple[int, int]]:
        posSet = set()
        with open(inFile, 'r') as inState:
            inMat = [list(row.rstrip()) for row in inState.readlines()]
        
        for xVal in range(len(inMat)):
            for yVal in range(len(inMat[0])):
                if inMat[xVal][yVal] == '#':
                    posSet.add((xVal, yVal))

        return posSet

    def updateLimits(self) -> None:
        for pos in self.elfPosVals:
            self.xMin = min(self.xMin, pos[0])
            self.xMax = max(self.xMax, pos[0])
            self.yMin = min(self.yMin, pos[1])
            self.yMax = max(self.yMax, pos[1])

    def __str__(self):
        finStr = ""
        for xInd in range(self.xMin, self.xMax+1):
            rowStr = ""
            for yInd in range(self.yMin, self.yMax+1):
                if (xInd, yInd) in self.elfPosVals:
                    rowStr += "#"
                else:
                    rowStr += "."
            finStr += rowStr + '\n'
        return finStr

if __name__ == "__main__":
    # Prepare env for p1
    inFile = "./2022/Day23/input"
    eAutomata = ElfAutomata(inFile)
    eAutomata.simulate(numRounds = 10)
    sol1 = eAutomata.calculatePart1Ans()
    print("The answer to part 1 is {}".format(sol1))

    eAutomata = ElfAutomata(inFile)
    sol2 = eAutomata.simulate(runUntilStall = True)
    print("The solution to part 2 is {}".format(sol2))