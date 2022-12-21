###############################################################
#   Soln for P1 of Day 21 for AoC
#
# Problem:
#     Given a sequence of mokies yelling either a number or the
#     operation they will perform, identify the number the monkey
#     named "root" will say based on the dependency tree created
#     by all the other monkeys.
###############################################################
# Parses monkeys and returns a dict representing all operation
# monkeys and all value monkeys.
from typing import Callable

def parseMonkeys(inFile: str) -> tuple[dict[str, tuple[str, str, str]], dict[str, int]]:
    opDict = dict()
    valDict = dict()
    
    with open(inFile, 'r') as inM:
        curLine = inM.readline().rstrip()
        while curLine:
            mName, opVal = curLine.split(":")
            if len(opVal.strip().split()) > 1:
                opDict[mName] = opVal.strip().split()
            else:
                valDict[mName] = int(opVal.strip())
            
            curLine = inM.readline().rstrip()

    return opDict, valDict

def opReader(opToRead: str) -> Callable:
    if opToRead == '*':
        return lambda x, y: x * y
    elif opToRead == '/':
        return lambda x, y: x // y
    elif opToRead == '+':
        return lambda x, y: x + y
    elif opToRead == '-':
        return lambda x, y: x - y
    else:
        return lambda x, y: None

def getRootVal(relMonkey: str, oDict: dict[str, tuple[str, str, str]], vDict: dict[str, int]) -> int:
    if relMonkey in vDict:
        return vDict[relMonkey]
    else: 
        relToks = oDict[relMonkey]
        opToUse = opReader(relToks[1])
        return opToUse(getRootVal(relToks[0], oDict, vDict), getRootVal(relToks[2], oDict, vDict))

###############################################################
#   Soln for P2 of Day 21 for AoC
#
# Problem:
#     The top relied on an implicit dependency graph, but now that
#     we must fill in a leaf node's value on our own, we must now
#     build a proper tree from which we propagate the branch without
#     'humn' to the branch with it in order to find the necessary value
#     to shout.
###############################################################
def doesBranchHaveMonkey(searchMonkey: str, relMonkey: str, oDict: dict[str, tuple[str, str, str]]) -> bool:
    if relMonkey == searchMonkey:
        return True

    if relMonkey in oDict:
        curTerms = oDict[relMonkey]
        return doesBranchHaveMonkey(searchMonkey, curTerms[0], oDict) or doesBranchHaveMonkey(searchMonkey, curTerms[2], oDict)
    
    return False

# If we have some operation a (op) b = c, then this inverts it
def invOpReader(opToInv: str, leftIsUnknown: bool) -> Callable:
    if opToInv == '*':
        return lambda x, y: x // y
    elif opToInv == '/' and not leftIsUnknown:
        return lambda x, y: y // x
    elif opToInv == '/' and leftIsUnknown:
        return lambda x, y: x * y
    elif opToInv == '+':
        return lambda x, y: x - y
    elif opToInv == '-' and leftIsUnknown:
        return lambda x, y: x + y
    elif opToInv == '-' and not leftIsUnknown:
        return lambda x, y: y - x
    else:
        return lambda x, y: None

def calculateMissingVal(missing: str, root: str, oDict: dict[str, tuple[str, str, str]], vDict: dict[str, int]) -> int:
    # Check each branch for the missing monkey
    curTerms = oDict[root]
    lBranch, rBranch = curTerms[0], curTerms[2]
    leftIsMissing = doesBranchHaveMonkey(missing, lBranch, oDict)
    forwardPass = getRootVal(rBranch, oDict, vDict) if leftIsMissing else getRootVal(lBranch, oDict, vDict)

    # Now backpropagate through to form a symbolic expression that can be evaluated
    backPassVal = forwardPass
    curNode = lBranch if leftIsMissing else rBranch
    while curNode != 'humn':
        curNodeExpr = oDict[curNode]
        otherVal = None

        # find branch that must be backpropagated and other value
        leftIsMissing = doesBranchHaveMonkey(missing, curNodeExpr[0], oDict)
        if leftIsMissing:
            curNode = curNodeExpr[0]
            otherNode = curNodeExpr[2]
            otherVal = getRootVal(curNodeExpr[2], oDict, vDict)
        else:
            curNode = curNodeExpr[2]
            otherNode = curNodeExpr[0]
            otherVal = getRootVal(curNodeExpr[0], oDict, vDict)

        invOp = invOpReader(curNodeExpr[1], leftIsMissing)
        backPassVal = invOp(backPassVal, otherVal)

    return backPassVal

if __name__ == "__main__":
    # prepare env for p1
    inFile = './Day21/input'
    oDict, vDict = parseMonkeys(inFile)

    # execute algo for p1
    sol1 = getRootVal('root', oDict, vDict)
    print("Solution for part 1 is {}".format(sol1))

    # execute algo for p2
    del vDict['humn']
    sol2 = calculateMissingVal('humn', 'root', oDict, vDict)
    print("Solution for part 2 is {}".format(sol2))
    