#############################################################
#   Soln for P1 of Day 7 for AoC
#
# Problem:
#   Finding the best place to align to given an input list of
#   values. Something in my mind says that the median is the right
#   place to align, but the implementation will use an expanding
#   search from the median instead.
#############################################################
from math import sqrt
from typing import Callable

def calculateMedian(intVals: list[int]) -> int:
    sList = sorted(intVals)
    if len(intVals)%2 == 0:
        return 0.5*(sList[len(intVals)//2] + sList[(len(intVals)//2)+1])
    else:
        return sList[len(intVals)//2]

def calculateMean(intVals: list[int]) -> int:
    return sum(intVals) / len(intVals)

def calculateStDev(intVals: list[int]) -> int:
    lMean = calculateMean(intVals)
    var = 0
    for val in intVals:
        var += (val - lMean)**2
    return sqrt(var / len(intVals))

def searchForOptimalPosition(intVals: list[int], costFunc: Callable = lambda x,y:abs(y-x), * , uniformCost: bool = False) -> tuple[int, int]:
    '''
        I can't quite explain this, but the optimal position
        should be the median as it represents the "midpoint" of
        a distribution sampled uniformly. This is, of course,
        assuming that the fuel used is 1 per unit moved.
        Here, we take the moderate approach and simply search around
        the mean and 1 st dev away. Given our cost values are symmetric,
        this should be decent enough.
    '''
    if uniformCost:
        midPt = int(calculateMedian(intVals))
        return calculateFuelUsed(intVals, midPt, costFunc), midPt

    valMean = int(calculateMean(intVals))
    valStDev = int(calculateStDev(intVals))
    optFUse, optLoc = None, None
    for posLoc in range(valMean-valStDev, valMean+valStDev+1):
        fCost = calculateFuelUsed(intVals, posLoc, costFunc)
        if optFUse is None or fCost < optFUse:
            optFUse = fCost
            optLoc = posLoc

    return optFUse, optLoc

def calculateFuelUsed(intVals: list[int], loc: int, costFunc: Callable) -> int:
    '''
        Calculates the energy used in order to move all points to a
        specific location.
    '''
    fuelUsed = 0
    for val in intVals:
        fuelUsed += costFunc(val, loc)
    return fuelUsed

if __name__ == "__main__":
    # prepare env for p1
    inFile = "./2021/Day07/input"

    # execute algo for p1
    with open(inFile, 'r') as valsStr:
        inVals = [int(val) for val in valsStr.readline().rstrip().split(',')]
    sol1 = searchForOptimalPosition(inVals, uniformCost = True)
    print("The answer to part 1 is {}".format(sol1))

    # and now for p2
    newCost = lambda x, y: sum(range(abs(y-x)+1))
    sol2 = searchForOptimalPosition(inVals, costFunc = newCost)
    print("The answer to part 2 is {}".format(sol2))