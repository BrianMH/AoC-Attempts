#############################################################
#   Soln for P1 & P2 of Day 24 for AoC
#
# Problem:
#   This problem begged to be somewhat parsed manually, so
#   the first part of this problem was spent simply analyzing the
#   logic behind what happens to the z value depending on the input.
#   The most important thing to notice was that there were only
#   seven possible indices where the z value could decrease, and
#   seven or more possible indices where the z value could increase.
#   Since the decrease occurred in increments of factors of 26, it was
#   quite clear that the problem treated a value as a sort of stack
#   which then produced the next value to test.
#   Of course, part of the challenge is keeping this generic, so, 
#   instead of designing a parser from scratch, instead the initial
#   parsing will generate the indices where we want certain actions
#   to occur.
#
#   Part 2 is then finding the smallest value, which just means
#   we can reverse the search list and terminate once we found any
#   solution from the bottom up.
#
#   I am fairly content with this solution as it runs extremely quickly,
#   but the most frustrating part is that it does feel quite hard-coded
#   due to the analysis needed.
#############################################################
import re

# string used for the regex
regStr = r'''inp w
mul x 0
add x z
mod x 26
div z \d+
add x (?P<val1>-?\d+)
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y (?P<val3>-?\d+)
mul y x
add z y'''

def parseMonad(inFile: str) -> list[tuple[int, int]]:
    with open(inFile, 'r') as monadInput:
        inExec = monadInput.read()
    
    return [tuple((int(val) for val in row)) for row in re.findall(regStr, inExec)]

def recursivelyFindMonad(curValStr: str, execRules: list[tuple[int, int]], curZVal: int, * , reverse: bool = True) -> str | None:
    # edge cases
    if len(curValStr) == len(execRules) and curZVal == 0:
        return curValStr
    elif len(curValStr) == len(execRules):
        return None
    
    # or continue searching under the assumption that the value must go up or down
    curInputs = execRules[len(curValStr)]
    if curInputs[0] < 0: # force the division with negative first values
        setVal = (curZVal % 26) + curInputs[0]
        if setVal < 1 or setVal > 9:    # prune this branch if impossible
            return None
        return recursivelyFindMonad(curValStr + str(setVal), execRules, curZVal//26, reverse = reverse)
    else:                # recursively brute force on positive first values
        searchRange = range(1,10) if not reverse else reversed(range(1,10))
        for curPosVal in searchRange:
            newZVal = 26*curZVal + (curPosVal + curInputs[1])
            posSol = recursivelyFindMonad(curValStr + str(curPosVal), execRules, newZVal, reverse = reverse)
            if posSol is not None:
                return posSol
    
    # this is never reached with a valid input
    return None

if __name__ == "__main__":
    # prepare env for p1
    inFile = "./2021/Day24/input"
    execRules = parseMonad(inFile)

    # execute algo for p1
    sol1 = recursivelyFindMonad("", execRules, 0)
    print("The answer to part 1 is {}".format(sol1))

    # and now for p2
    sol2 = recursivelyFindMonad("", execRules, 0, reverse = False)
    print("The answer to part 2 is {}".format(sol2))