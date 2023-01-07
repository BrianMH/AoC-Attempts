###############################################################
#   Soln for P1 of Day 5 for AoC
#
# Problem:
#     Given a starting position for a certain block stacking
#     situation, determine the boxes at the top of the stacks
#     once the actions are all carried out.
###############################################################
# Some helper functions for parsing
READ_IN_CHARS = 4        # Need this for the silly parsing at the start
def parseInitialState(inFile: str) -> list[list[str]]:
    # values used later...
    numStacks = None

    # Determine stack count using a certain line
    with open(inFile, 'r') as initFile:
        curLine = initFile.readline()
        while not curLine[0] == " ":
            curLine = initFile.readline()

        # Determine the number of stacks from this line
        numStacks = int(curLine.split()[-1])

    # Now form and populate every stack
    initState = [list() for _ in range(numStacks)]
    with open(inFile, 'r') as initFile:
        curLine = initFile.readline()
        while not curLine[0] == " ":
            # parse current line for tokens to add to stacks
            tokens = [curLine[i:i+READ_IN_CHARS].strip() for i in range(0, len(curLine), READ_IN_CHARS)]
            
            # for any given token found, add these elements to the stacks as if it were a queue
            for stackInd, token in enumerate(tokens):
                if token:
                    initState[stackInd].append(token)

            # Then move onto the next line
            curLine = initFile.readline()

    # This stack is flipped as we started from the top, so we go ahead and reverse it here
    [stack.reverse() for stack in initState]

    # return with 0-index modifier list to keep things legible
    return [[]] + initState

# Performs the set of desired operations and returns the top elements
# of each stack
def p1Soln(inFile: str) -> str:
    # process initial state
    curStacks = parseInitialState(inFile)

    # process updates
    with open(inFile, 'r') as dirFile:
        # get rid of initial state garbage
        while dirFile.readline().strip() != "":
            continue

        # grab and perform updates
        curLine = dirFile.readline().rstrip()
        while curLine:
            # parse line
            numToMove, fromStack, toStack = (int(val) for val in curLine.split()[1::2])

            # move values
            for _ in range(numToMove):
                curStacks[toStack].append(curStacks[fromStack].pop())

            # grab next line
            curLine = dirFile.readline().rstrip()

    # Then simply read off the top of the stacks
    stackTops = [curStack[-1].strip("[]") for curStack in curStacks[1:]]
    return "".join(stackTops)

###############################################################
#   Soln for P2 of Day 5 for AoC
#
# Problem:
#     Given a starting position for a certain block stacking
#     situation, determine the boxes at the top of the stacks
#     once the actions are all carried out.
#     In this scenario, we assume more than one box can be picked
#     up at a given time. (This can be simulated with a dummy stack
#     to move things into and out of without much modification.)
###############################################################
def p2Soln(inFile: str) -> str:
    # process initial state
    curStacks = parseInitialState(inFile)
    tempStack = list()

    # process updates
    with open(inFile, 'r') as dirFile:
        # get rid of initial state garbage
        while dirFile.readline().strip() != "":
            continue

        # grab and perform updates
        curLine = dirFile.readline().rstrip()
        while curLine:
            # parse line
            numToMove, fromStack, toStack = (int(val) for val in curLine.split()[1::2])

            # move values to temp stack then to proper stack (simulate N box removal)
            for _ in range(numToMove):
                tempStack.append(curStacks[fromStack].pop())
            for _ in range(numToMove):
                curStacks[toStack].append(tempStack.pop())

            # grab next line
            curLine = dirFile.readline().rstrip()

    # Then simply read off the top of the stacks
    stackTops = [curStack[-1].strip("[]") for curStack in curStacks[1:]]
    return "".join(stackTops)

if __name__ == "__main__":
    # Set up env for first problem
    inFile = "./Day05/input"

    # Then evaluate the problem
    sol1 = p1Soln(inFile)
    print("Solution for p1 is {}".format(sol1))

    # Evaluate second half now
    sol2 = p2Soln(inFile)
    print("Solution for p2 is {}".format(sol2))