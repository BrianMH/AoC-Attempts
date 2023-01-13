#############################################################
#   Soln for P1 of Day 10 for AoC
#
# Problem:
#     The usual parenthesis matching problem (at least for now).
#     Patterns which have mismatched closing values are the only
#     ones considered for P1.
#############################################################
def getFirstMismatch(openCloseMap: dict[str, str], strToCheck: str) -> tuple[str, str]:
    '''
        Returns the first instance of a mismatched parenthesis pair if it exists.

        Arguments:
            openCloseMap - A mapping from the open parenthesis to closing parenthesis
                           types.
            strToCheck - The string to evaluate on.

        Returns:
            tuple - If a string is mismatched, then a tuple representing the first
                    mismatched character and an empty list. If not, then the return
                    is an empty string and a list of the remaining values on the stack.
    '''
    stack = list()
    for char in strToCheck.strip():
        if char in openCloseMap:
            stack.append(char)
        else:
            expCloseChar = openCloseMap[stack.pop()]
            if char != expCloseChar:
                return char, list()
    
    # no mismatches found (can still be wrong)
    return "", stack

#############################################################
#   Soln for P2 of Day 10 for AoC
#
# Problem:
#     Using the leftover stacks from above, we just want to
#     score the values given a point array.
#############################################################
def processLeftoverStacks(lStacks: list[list[str]], openCloseDict: dict[str, str], scoreDict: dict[str, int]) -> list[int]:
    '''
        Applies the algorithm given by AoC on a list of leftover autocorrect stacks
        to extract their autocorrect scores.

        Arguments:
            lStacks - The collection of leftover stacks.
            openCloseDict - The mapping between opening parenthesis values to their close values.
            scoreDict - The mapping between expected closing parenthesis chars and their autocorrect
                        score
        
        Returns:
            list - A list representing the collection of autocorrect scores, sorted from the largest
                   to smallest.
    '''
    curACScores = list()
    for stack in lStacks:
        curScore = 0
        for elem in reversed(stack):
            curScore = (curScore * 5) + scoreDict[openCloseDict[elem]]
        curACScores.append(curScore)
    return sorted(curACScores, reverse = True)

if __name__ == "__main__":
    # prepare env for p1
    inFile = "./2021/Day10/input"
    parenMap = {"(":")", "[":"]", "<":">", "{":"}"}
    pointMap = {")":3, "]":57,"}":1197, ">":25137}
    leftoverStacks = list() # used for p2

    # execute algo for p1
    p1SolList = list()
    with open(inFile, 'r') as strsToParse:
        curLine = strsToParse.readline()
        while curLine:
            resE, stackLeft = getFirstMismatch(parenMap, curLine)
            p1SolList.append(resE) if resE else leftoverStacks.append(stackLeft)
            curLine = strsToParse.readline()
    sol1 = sum([pointMap[wrongChar] for wrongChar in p1SolList])
    print("The answer to part 1 is {}".format(sol1))

    # and now for p2
    sDict = {")":1, "]":2, "}":3, ">":4}
    sol2 = processLeftoverStacks(leftoverStacks, parenMap, sDict)
    print("The answer to part 2 is {}".format(sol2[len(sol2)//2]))