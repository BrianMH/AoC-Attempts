###############################################################
#   Soln for P1 of Day 9 for AoC
#
# Problem:
#     Given a sequence of movements taken on some 2-dimensional
#     bridge (which moves our H marker), count how many unique cells
#     the tail visits assuming that the tail moves given the following
#     constraint:
#         1) If H not in the 3x3 subcell T can observe
#              1.1) Move T horizontally/vertically if H on same row/col
#              1.2) Move T diagonally to catch up, otherwise
#     The trick seems to be that there is no given size for the 
#     overall bridge! It can be pre-calculated by parsing all movements
#     in each direction, but a coordinate list and visited hash map
#     can probably suffice for the problem.
###############################################################
class ChaseSimulation:
    def __init__(self, sLoc: tuple[int, int]):
        # All values start in the same place for p1
        self.sLoc = sLoc
        self.hLoc = sLoc
        self.tLoc = sLoc

        # and this keeps track of tail positions
        self.tMemory = set()

        # used for lambdas
        def sign(x: int) -> int:
            if x == 0:
                return 0
            return -1 if x < 0 else 1

        # and some simpler lambdas to simplify view
        self.posUpdater = lambda tup1, tup2:(tup1[0]+tup2[0], tup1[1]+tup2[1])
        self.deltaGen = lambda oldLoc, newLoc:(sign(newLoc[0]-oldLoc[0]), sign(newLoc[1]-oldLoc[1]))
        self.l1Loss = lambda loc1, loc2:abs(loc1[0]-loc2[0]) + abs(loc1[1]-loc2[1])

    # move the piece a certain way. returns the tail delta for chaining
    def moveHeadPiece(self, deltax: int, deltay: int) -> tuple[int, int]:
        # perform movement
        self.hLoc = self.posUpdater(self.hLoc, (deltax, deltay))
        # print("H moved to {}".format(self.hLoc))

        # update tail if necessary
        tDelta = self.selfAdjustTail()
        self.tMemory.add(self.tLoc)
        return tDelta

    # given current hLoc, move tLoc according to problem specifications
    def selfAdjustTail(self) -> tuple[int, int]:
        l1Dist = self.l1Loss(self.hLoc, self.tLoc)
        genDelta = (0, 0)

        if ((self.hLoc[0] == self.tLoc[0] or self.hLoc[1] == self.tLoc[1]) and l1Dist >= 2) \
                or l1Dist >= 3:
            # update in same row/col
            genDelta = self.deltaGen(self.tLoc, self.hLoc)
            self.tLoc = self.posUpdater(self.tLoc, genDelta)

        return genDelta

    def getUniqueTailPosCount(self) -> int:
        return len(self.tMemory)

# Our class naturally supports the double know so we go ahead
# and simulate it directly
def p1Soln(inFile: str) -> int:
    # prepare simulation framework
    curSim = ChaseSimulation(sLoc = (0,0))

    # go through the given commands and process them
    cmdDict = {"R":(0, 1), "U":(-1, 0), "D":(1, 0), "L":(0, -1)}
    with open(inFile, 'r') as cmdList:
        curLine = cmdList.readline()
        while curLine:
            # deal with commands
            dirToMove, numMoves = curLine.rstrip().split()
            [curSim.moveHeadPiece(*cmdDict[dirToMove]) for _ in range(int(numMoves))]

            # and then move on to the next
            curLine = cmdList.readline()

    return curSim.getUniqueTailPosCount()

###############################################################
#   Soln for P2 of Day 9 for AoC
#
# Problem:
#     Unlike before, we now imagine a much longer sequence of 10
#     knots (including the head) is now part of the problem. In
#     this case, we therefore apply the above rules to each 
#     consecutive 2-sequence from the start to end. All this effectively
#     does is chain the knots.
#     Notice that because the class above actually returns the delta value
#     for the updated tail, we can propagate this delta to the end as much
#     as necessary (thank you, foresight!)
###############################################################
# our harness effectively chains these simulation pieces together to form
# the longer tail.
class ChaseHarness:
    def __init__(self, sLoc: tuple[int, int], tailLength = 2):
        self.sLoc = sLoc
        self.tailSegs = [ChaseSimulation(sLoc) for _ in range(tailLength)]

    # update functions by propagating deltas down the chain from the start
    # to end
    def moveHeadPiece(self, deltax: int, deltay: int) -> tuple[int, int]:
        curDeltax, curDeltay = deltax, deltay
        for tailInd in range(len(self.tailSegs)):
            curDeltax, curDeltay = self.tailSegs[tailInd].moveHeadPiece(curDeltax, curDeltay)

        return (curDeltax, curDeltay)

    # returns the tail segment unique positions for the given segment
    # note that this is zero-indexed but begins from the second segment's
    # history
    def getUniqueTailPosCount(self, segInd: int):
        return self.tailSegs[segInd].getUniqueTailPosCount()

def p2Soln(inFile: str, tailLen: int) -> int:
    # prepare simulation framework
    curSim = ChaseHarness(sLoc = (0,0), tailLength = tailLen)

    # go through the given commands and process them
    cmdDict = {"R":(0, 1), "U":(-1, 0), "D":(1, 0), "L":(0, -1)}
    with open(inFile, 'r') as cmdList:
        curLine = cmdList.readline()
        while curLine:
            # deal with commands
            dirToMove, numMoves = curLine.rstrip().split()
            [curSim.moveHeadPiece(*cmdDict[dirToMove]) for _ in range(int(numMoves))]

            # and then move on to the next
            curLine = cmdList.readline()

    return curSim.getUniqueTailPosCount(tailLen-1)

if __name__ == "__main__":
    # prepare env for p1
    inFile = "./Day9/input"

    # evaluate on p1
    sol1 = p1Soln(inFile)
    print("The solution for part 1 is {}".format(sol1))

    # evalute on p2 now
    tailSize = 9
    sol2 = p2Soln(inFile, 9)
    print("The solution for part 2 is {}".format(sol2))