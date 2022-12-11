###############################################################
#   Soln for P1 of Day 11 for AoC
#
# Problem:
#     Given a list of inputs representing a set of monkies that
#     move items between each other one at a time (from 0, 1, ...),
#     simulate several rounds of them moving items to each other
#     and count the number of times they inspect an item. The 
#     solution is the product between the number of inspections
#     held by the monkeys that inspected the most number of items.
#
#     Part 2 pretty much just builds on top by making the simulation
#     run for many more rounds. One small thing that was the true
#     puzzle here was ensuring that the baggage values were under
#     modulo LCM(comparisonVals) in order to prevent the whole
#     thing from blowing up.
###############################################################
from typing import Callable

'''
    MonkeySim

    Sets up the entire simulation (why didn't I just use
    regex for this...) and allows the user to queue rounds. Takes
    in the initialization file and whether or not to reduce worry
    after the round based on p1's specifications.
'''
class MonkeySim:
    def __init__(self, inFile: str, reduceWorryAfterRound: bool = True):
        # init monkeys and what they do / what they hold
        self.monkeyBaggage = list()
        self.monkeyOps = list()
        self.monkeyThrowConds = list()
        self.curRound = 1
        self.numInspections = dict()
        self.redAfterRnd = reduceWorryAfterRound
        self.moduloVal = 1

        # convenient lambda
        self.reduceWorryFunc = lambda worryVal:int(worryVal/3)

        # init logic
        self.initMonkeysFromFile(inFile)

    def simulateRound(self) -> None:
        # Perform simulation
        for monkeyInd in range(len(self.monkeyBaggage)):
            for curItemInd in range(len(self.monkeyBaggage[monkeyInd])):
                curItemVal = self.monkeyBaggage[monkeyInd][curItemInd]

                # inspect item
                curItemVal = self.monkeyOps[monkeyInd](curItemVal)

                # reduce worry after boredom
                if self.redAfterRnd:
                    curItemVal = self.reduceWorryFunc(curItemVal)
                else:
                    # in order to keep things manageable, only keep track of
                    # LCM modulo
                    curItemVal = curItemVal % self.moduloVal

                # perform movement to other monkey
                nextMonkeyInd = self.monkeyThrowConds[monkeyInd](curItemVal)
                self.monkeyBaggage[nextMonkeyInd].append(curItemVal)
            
            # queue exhausted
            self.numInspections[monkeyInd] = self.numInspections.get(monkeyInd, 0) +\
                                                 len(self.monkeyBaggage[monkeyInd])
            self.monkeyBaggage[monkeyInd] = list()
        self.curRound += 1

    def getNumInspections(self) -> list[int]:
        return list(self.numInspections.values())

    # useful for watching updated monkey values progress
    def __str__(self):
        print("== After round {} ==".format(self.curRound))
        for monkeyInd in range(len(self.monkeyBaggage)):
            print("Monkey {} inspected items {} times.".format(monkeyInd, self.numInspections[monkeyInd]))

    ''' Logic here is that we know the input format is 6 lines as follows:
            Monkey X:
                Starting items: x1, x2, ...
                Operation:  new = old (op) val2
                Test: divisible by val3
                        if true: throw to monkey y1
                        if false: throw to monkey y2
        So we parse the file assuming the following structure is followed...'''
    def initMonkeysFromFile(self, inFile: str) -> None:
        # set up some useful constants here
        from operator import mul, add, sub
        from functools import partial # for op binding
        def repArgDecorator(f: Callable): # also for op binding
            def repArgBinder(x1):
                return f(x1, x1)
            return repArgBinder
        opTemplate = lambda trueVal, falseVal, val3, worrylvl: trueVal if (worrylvl % val3) == 0 else falseVal

        NUM_SET_LINES = 7
        opDict = {"*":mul, "+":add}

        with open(inFile, 'r') as monkeyList:
            lineList = monkeyList.readlines()
            monkeysToParse = [lineList[relInds:relInds+6] for relInds in range(0, len(lineList), NUM_SET_LINES)]
            del lineList

        # Then go through each tuple of 6 lines to extract the monkey values
        for monkeyVals in monkeysToParse:
            _, itemLine, opLine, testLine, trueLine, falseLine = monkeyVals

            # now extract values from all the lines
            itemList = [int(itemVal.rstrip(',')) for itemVal in itemLine.rstrip().split()[2:]]

            splitOpVals = opLine.rstrip().split()
            op, val2 = splitOpVals[-2], splitOpVals[-1]
            monkeyOpFunc = partial(opDict[op], int(val2)) if val2 != "old" else repArgDecorator(opDict[op])

            val3 = int(testLine.rstrip().split()[-1])
            y1, y2 = int(trueLine.rstrip().split()[-1]), int(falseLine.rstrip().split()[-1])
            testOpFunc = partial(opTemplate, y1, y2, val3)

            # update simulation settings
            self.monkeyBaggage.append(itemList)
            self.monkeyOps.append(monkeyOpFunc)
            self.monkeyThrowConds.append(testOpFunc)
            self.moduloVal *= val3

def p1Soln(inFile: str, numRounds: int, redAfterRound: bool = True, printCond: Callable = lambda roundIter: False) -> int:
    # initialize simulator and simulate
    p1Sim = MonkeySim(inFile, reduceWorryAfterRound = redAfterRound)
    for roundIter in range(numRounds):
        p1Sim.simulateRound()
        if printCond(roundIter):
            print(p1Sim)
    topInspects = sorted(p1Sim.getNumInspections(), reverse = True)

    return topInspects[0]*topInspects[1]

if __name__ == "__main__":
    # set up env for p1
    inFile = "./Day11/input"

    # execute algo for p1
    sol1 = p1Soln(inFile, 20)
    print("Solution for part 1 is {}".format(sol1))

    # execute algo for p2 (can use the same func as p1)
    sol2 = p1Soln(inFile, 10000, False)
    print("Solution for part 2 is {}".format(sol2))