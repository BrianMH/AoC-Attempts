###############################################################
#   Soln for P1 & P2 of Day 14 for AoC
#
# Problem:
#     We get a list of lines representing solid rock formations
#     on some grid of unknown dimensions. We are then given a 
#     point from which we will be modeling the dynamics of sand
#     falling down and settling (assuming it settles). The solution
#     for this part is simply the total number of sand particles that
#     settle on top of any of the rock formations (this can be
#     implicitly determined by recording the lowest rock formation)
#
#     Part 2 simply builds on top by instead running the simulation
#     until the source node is covered (as the sand will never fall
#     below the floor to end the simulation)
#
# Note:
#     Execution takes a bit long. 3.6s for both parts but obviously
#     most of the time is spent calculating p2. After looking at the
#     final result, p2 can probably be brute forced by calculating 
#     the negative areas and deducting that (along with the rock count)
#     from the overall pyramid guaranteed to be generated from the source.
#     Time can be saved by starting from last point, teleporting down as far
#     as possible at the start, etc. Lots of optimizations available.
###############################################################
from time import sleep
SLEEP_DUR = 1

class SandSimulation:
    def __init__(self, inFile: str, sandEntry: tuple[int, int], useFloor: bool = False):
        # constants for printing visuals
        self.AIR = ' '
        self.ROCK = '#'
        self.SAND = 'o'
        self.SOURCE = '+'
        self.minX, self.maxX, self.minY, self.maxY = (sandEntry[0], sandEntry[0], 
                                                      sandEntry[1], sandEntry[1])

        # parses all of the rock formations
        self.sparseArr = {sandEntry:self.SOURCE}
        self.entryPt = sandEntry
        self.heldSand = 0
        self.useFloor = useFloor
        self.parseRocks(inFile, useFloor)
        self.lastPath = [self.entryPt]
        self.DELTA_END = (-1, -1)
        self.DELTAS = ((0, 1), (-1, 1), (1, 1), self.DELTA_END)

    # drops a sand particle using prompt's physics
    # post-opt: keep track of last placement for use later
    def dropSandParticle(self, * , printDisplay: bool = False) -> bool:
        # record entry
        curPos = self.lastPath[-1]
        oldNote = self.sparseArr[curPos]
        self.sparseArr[curPos] = self.SAND
        if printDisplay:
            print(self)
            sleep(SLEEP_DUR)

        while curPos[1] <= self.maxY:
            for curDelta in self.DELTAS:
                curCand = (curPos[0]+curDelta[0], curPos[1]+curDelta[1])
                if curDelta == self.DELTA_END:
                    self.heldSand += 1
                    if curPos == self.entryPt:
                        if printDisplay:
                            print(self)
                            sleep(SLEEP_DUR)
                        return False # end sim
                    else:
                        if printDisplay:
                            self.minX = min(self.minX, curPos[0])
                            self.maxX = max(self.maxX, curPos[0])
                        self.lastPath = self.lastPath[:-1]
                        return True # grain has settled
                elif self.getCust(curCand, self.AIR) == self.AIR:
                    self.sparseArr[curPos] = oldNote
                    curPos = curCand
                    self.lastPath.append(curPos)
                    oldNote = self.getCust(curPos, self.AIR)
                    self.sparseArr[curPos] = self.SAND

                    if printDisplay:
                        print(self)
                        sleep(SLEEP_DUR)
                    break

        return False

    # sets up the grid for simulating
    def parseRocks(self, inFile: str, floor: bool) -> None:
        flipAdjuster = lambda ind1, ind2: (ind2, ind1) if ind2 < ind1 else (ind1, ind2)

        with open(inFile, 'r') as lineInputs:
            curLine = lineInputs.readline()
            while curLine:
                # parse tuples from input
                curTups = [tup.split(',') for tup in curLine.rstrip().split(" -> ")]
                curTups = [(int(lElem), int(rElem)) for lElem, rElem in curTups]
                curLine = lineInputs.readline()

                # update sparse matrix
                for tupInd in range(len(curTups)-1):
                    ptL, ptR = curTups[tupInd], curTups[tupInd + 1]
                    xLimL, xLimR = flipAdjuster(ptL[0], ptR[0])
                    yLimL, yLimR = flipAdjuster(ptL[1], ptR[1])
                    self.minX = min(self.minX, xLimL)
                    self.maxX = max(self.maxX, xLimR)
                    self.minY = min(self.minY, yLimL)
                    self.maxY = max(self.maxY, yLimR)

                    if yLimL == yLimR:
                        for xInd in range(xLimL, xLimR+1):
                            self.sparseArr[(xInd, yLimL)] = self.ROCK
                    if xLimL == xLimR:
                        for yInd in range(yLimL, yLimR+1):
                            self.sparseArr[(xLimL, yInd)] = self.ROCK

        # modify dict to efficiently calculate floor
        if floor:
            def floorModGet(floorYVal: int, originalGetFunc: callable) -> callable:
                def modifyGetFunc(*args, **kwargs) -> callable:
                    if args[0][1] == floorYVal:
                        return self.ROCK
                    else:
                        return originalGetFunc(*args, **kwargs)
                return modifyGetFunc

            self.getCust = floorModGet(self.maxY+2, self.sparseArr.get)
            self.maxY += 3
        else:
            self.getCust = self.sparseArr.get

    # returns the current playing field
    def __str__(self):
        outStr = ""
        for yInd in range(self.minY-1, self.maxY+2):
            for xInd in range(self.minX-1, self.maxX+2):
                outStr += (self.getCust((xInd, yInd), self.AIR))
            outStr += "\n"
        return outStr

def simulateSandUntilFlooded(inFile: str, sandEntry: tuple[int,int], useFloor: bool = False, 
                             verbose: bool = False) -> int:
    sim = SandSimulation(inFile, sandEntry, useFloor = useFloor)

    while(sim.dropSandParticle(printDisplay=verbose)):
        pass

    return sim.heldSand

if __name__ == "__main__":
    # prepare env for p1
    inFile = './Day14/input'

    # execute algo p1
    sol1 = simulateSandUntilFlooded(inFile, (500, 0), verbose = False)
    print("The solution to part 1 is {}".format(sol1))

    # execute algo p2
    sol2 = simulateSandUntilFlooded(inFile, (500, 0), useFloor = True)
    print("The solution to part 2 is {}".format(sol2))