###############################################################
#   Soln for P1 of Day 10 for AoC
#
# Problem:
#     Given a sequence of pseudo-assembly code and the assumption
#     that an addx op takes 2 cycles and noop takes 1 cycle with
#     a CPU with only a single register, find the sum of the values
#     on the register at the start of the "interesting" cycle 
#     values of (20 + 40*n).
#
# Observation:
#     We are simulating a single thread computer with specific operation times.
#     We can "queue" an operation and then wait the appropriate cycle
#     time for it to finish.
###############################################################
import heapq

def p1Soln(inFile: str) -> int:
    # set some initial values for our CPU
    jobQueue = list()
    cycleVal = 1
    registerVal = 1
    cycleDict = {"noop":1, "addx":2}
    notedSignal = 0

    with open(inFile, 'r') as progCmds:
        curLine = progCmds.readline()
        while curLine or jobQueue:
            # beginning of cycle (queue op if queue empty)
            if len(jobQueue) == 0:
                curOp = curLine.rstrip().split()
                finCycle = cycleVal + cycleDict[curOp[0]]
                jobReq = (finCycle, 0) if len(curOp) == 1 else (finCycle, int(curOp[1]))
                heapq.heappush(jobQueue, jobReq)
                curLine = progCmds.readline()

            # record interesting elements
            if (cycleVal-20)%40 == 0:
                notedSignal += cycleVal * registerVal

            # end of cycle (process queue)
            cycleVal += 1
            while len(jobQueue) > 0 and jobQueue[0][0] == cycleVal:
                registerVal += heapq.heappop(jobQueue)[1]

    return notedSignal

###############################################################
#   Soln for P1 of Day 10 for AoC
#
# Problem:
#     We now know our register represents the mid position of a 3-char
#     wide element being moved across the screen. Suppose we are using
#     a CRT that is 40 x 6 and update the value of the screen to be
#     turned on only if any pixel of the three-char-wide element is
#     located on the updated pixel in question.
#     It's pretty much the same as above but the mid-cycle action
#     has now been swapped out for something different. Refactoring
#     based on some mid-cycle functor can prob work, but it's more
#     effort than necessary for this.
###############################################################
# reshapes the screen to properly render solution
def reshapeScreen(screenString: str, screenWidth: int) -> str:
    fixedString = ""
    for ind in range(0, len(screenString), screenWidth):
        fixedString += screenString[ind:ind+screenWidth] + "\n"

    return fixedString

def p2Soln(inFile: str, screenWidth: int, screenHeight: int) -> str:
    # readies our CPU yet again
    jobQueue = list()
    cycleVal = 1
    registerVal = 1
    cycleDict = {"noop":1, "addx":2}
    screenOutput = ["-"] * (screenHeight * screenWidth)

    with open(inFile, 'r') as progCmds:
        curLine = progCmds.readline()
        while curLine or jobQueue:
            # beginning of cycle (queue op if queue empty)
            if len(jobQueue) == 0:
                curOp = curLine.rstrip().split()
                finCycle = cycleVal + cycleDict[curOp[0]]
                jobReq = (finCycle, 0) if len(curOp) == 1 else (finCycle, int(curOp[1]))
                heapq.heappush(jobQueue, jobReq)
                curLine = progCmds.readline()

            # update our screen's image (mid cycle)
            screenOutput[cycleVal-1] = "█" if registerVal-1 <= (cycleVal-1)%screenWidth <= registerVal+1 else " "

            # end of cycle (process queue)
            cycleVal += 1
            while len(jobQueue) > 0 and jobQueue[0][0] == cycleVal:
                registerVal += heapq.heappop(jobQueue)[1]

    return reshapeScreen("".join(screenOutput), screenWidth)

if __name__ == "__main__":
    # prepare env for p1
    inFile = "./Day10/input"
    
    # execute algo for p1
    sol1 = p1Soln(inFile)
    print("Solution for p1 is {}".format(sol1))

    # execute algo for p2
    sol2 = p2Soln(inFile, 40, 6)
    print("Solution for p2 is \n{}".format(sol2))