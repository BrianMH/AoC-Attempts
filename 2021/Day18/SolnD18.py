#############################################################
#   Soln for P1 of Day 18 for AoC
#
# Problem:
#   It's time to perform some addition, but with a twist that
#   makes it slightly more annoying to work with without a 
#   stack following it around.
#
#   I believe explosions can technically be done in a single pass,
#   but doing it like this keeps the logic simple. Doing it in
#   a single pass would mean keeping track of the offset generated
#   by the exploded tuples (which seems like a pain)
#############################################################
from functools import reduce

class SnailExpr:
    def __init__(self, expr: str):
        self.expr = self._str2List(expr)
        self.split = lambda val: ['[',val//2,',',(val+1)//2,']']

        # constants
        self.SPLIT_VAL = 10
        self.E_THRESH = 4

    def __add__(self, rExpr: 'SnailAdder') -> 'SnailAdder':
        # create the new packet from the two
        newPacket = SnailExpr('['+str(self)+','+str(rExpr)+']')
        return newPacket.performReduction()

    def getMagnitude(self) -> int:
        return self._recursiveMagnitude(self.expr)

    def _recursiveMagnitude(self, toParse: list) -> int:
        # exit conds
        if len(toParse) == 1:
            return toParse[0]

        # first identify the left/right portions via stack parsing
        parenStack = list()
        for ind, elem in enumerate(toParse):
            if elem == '[':
                parenStack.append('[')
            elif elem == ']':
                parenStack.pop()
            elif elem == ',' and len(parenStack) == 1:
                return 3 * self._recursiveMagnitude(toParse[1:ind]) + \
                       2 * self._recursiveMagnitude(toParse[ind+1:-1])
        
        return -1 # this is never reached

    def performReduction(self) -> 'SnailAdder':
        '''
            Performs the reduction of an addition string. Returns
            the same object as the change is performed in place.
        '''
        changeOccured = True
        while changeOccured:
            # first process all explosions
            explBool = self._reduceExplosion()

            # and then perform a split if necessary
            splitBool = self._reduceSplit()
            changeOccured = explBool or splitBool
        return self

    ############## HELPER FUNCTIONS ######################

    def _reduceExplosion(self) -> int:
        ''' Continuously processes explosions until none are left. '''
        changeRequired = True
        numExpl = 0
        newExpr = list()

        while changeRequired:
            # check if expr changed between turns
            if newExpr:
                self.expr = newExpr
                numExpl += 1
                newExpr = list()

            # Check for explosions/splits
            explSepStack = list()
            explNumInds = list()

            for ind, elem in enumerate(self.expr):
                newExpr.append(elem)
                if isinstance(elem, str):   # separator
                    if elem == '[':
                        explSepStack.append(elem)
                    elif elem == ']':
                        explSepStack.pop()
                else:                       # value
                    if len(explSepStack) > self.E_THRESH:
                        newExpr = newExpr[:-2] + [0]
                        if explNumInds:
                            newExpr[explNumInds[-1]] += elem
                        carryOver = self.expr[ind+2]
                        newExpr.extend(self._computeCOList(carryOver, ind))
                        break   # resets check

                    explNumInds.append(ind) # keep track of number locs
                
                # exit if no changes have been made
                if ind == len(self.expr)-1:
                    changeRequired = False

        return numExpl

    def _reduceSplit(self) -> bool:
        ''' Processes only a single split (as explosions have precedence) '''
        newExpr = list()
        splitProc = False
        for ind, elem in enumerate(self.expr):
            newExpr.append(elem)
            if isinstance(elem, int) and elem >= self.SPLIT_VAL:
                newExpr.extend(self.split(newExpr.pop()))
                newExpr.extend(self.expr[ind+1:])
                splitProc = True
                break   # resets check

        if splitProc:
            self.expr = newExpr
        return splitProc

    def _computeCOList(self, co: int, explInd: int) -> list:
        retList = list()

        for restInd in range(explInd+4, len(self.expr)):
            if isinstance(self.expr[restInd], int) and co:
                retList.append(self.expr[restInd] + co) 
                co = 0
            else:
                retList.append(self.expr[restInd])
        
        return retList

    def __str__(self) -> str:
        strList = [str(val) for val in self.expr]
        return "".join(strList)

    def _str2List(self, expr: str) -> list:
        exprList = list()
        curVal = ''

        for ind in range(len(expr)):
            if expr[ind] in ('[', ']', ','):
                if curVal:
                    exprList.append(int(curVal))
                    curVal = ''
                exprList.append(expr[ind])
            else:
                curVal += expr[ind]

        return exprList

#############################################################
#   Soln for P2 of Day 18 for AoC
#
# Problem:
#     We have to find the two strings which produce the highest
#     snail expressions. Since the operation is not commutative,
#     this means that we have to process N^2 additions.
#############################################################
def findMaxSnailSum(strsToUse: list[str]) -> int:
    maxMag = 0
    snailExprs = [SnailExpr(expr) for expr in strsToUse]
    for lInd in range(len(snailExprs)):
        for rInd in range(len(snailExprs)):
            if lInd == rInd:
                continue

            curMag =(snailExprs[lInd]+snailExprs[rInd]).getMagnitude()
            maxMag = max(maxMag, curMag)

    return maxMag

if __name__ == "__main__":
    # prepare env for p1
    inFile = "./2021/Day18/input"
    with open(inFile, 'r') as exprs:
        exprStrs = [line.strip() for line in exprs.readlines()]

    # execute algo for p1
    sol1Expr = reduce(lambda xStr, yStr:xStr+SnailExpr(yStr), exprStrs[1:], SnailExpr(exprStrs[0]))
    print("The answer to part 1 is {}".format(sol1Expr.getMagnitude()))

    # and now for p2
    sol2 = findMaxSnailSum(exprStrs)
    print("The answer to part 2 is {}".format(sol2))