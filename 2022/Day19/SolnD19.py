###############################################################
#   Soln for P1 of Day 19 for AoC
#
# Problem:
#     We are given a set of four different machines along with
#     the necessary ingredients to make them. Our end-goal is
#     pretty much to create geode robots by choosing the optimal
#     combination of other robots to be able to mine geodes
#     as optimally as possible. The input represents the ingredients
#     while the robot specs are set in stone.
#
#     Part 2 just seems to be part 1 but longer...
#
# Note:
#     I will be approaching this using a recursive approach first.
###############################################################
import re
from functools import lru_cache

def parseInputs(inFile: str) -> dict[int, list[tuple[int, int, int]]]:
    template = r'Blueprint (?P<ind>\d+): Each ore robot costs (?P<oCost>\d+) ore. ' \
               r'Each clay robot costs (?P<cCost>\d+) ore. Each obsidian robot costs ' \
               r'(?P<obsOreCost>\d+) ore and (?P<obsCCost>\d+) clay. Each geode robot ' \
               r'costs (?P<gOreCost>\d+) ore and (?P<gObsCost>\d+) obsidian.'
    ingDict = dict()

    with open(inFile, 'r') as inTemplates:
        curLine = inTemplates.readline().rstrip()
        while curLine:
            mSeq = re.match(template, curLine).groupdict()
            oCosts = (int(mSeq['oCost']), 0, 0)
            cCosts = (int(mSeq['cCost']), 0, 0)
            obsCosts = (int(mSeq['obsOreCost']), int(mSeq['obsCCost']), 0)
            gCosts = (int(mSeq['gOreCost']), 0, int(mSeq['gObsCost']))
            ingDict[int(mSeq['ind'])] = [oCosts, cCosts, obsCosts, gCosts]
            curLine = inTemplates.readline().rstrip()

    return ingDict

def ceildiv(a, b):
    if a == 0 and b == 0:
        return 0
    return -(a // -b)

@lru_cache
def getNeededTime(robotIngs: tuple, curRate: tuple, curMats: tuple) -> int:
    # first make sure it's possible to craft
    posCraft = min(False if (x>0) and (y==0) else True for x,y in zip(robotIngs, curRate)) != 0

    # otherwise calculate values
    if posCraft:
        ingTimes = list()
        for itemInd in range(len(robotIngs)):
            posTime = ceildiv(robotIngs[itemInd] - curMats[itemInd], curRate[itemInd])
            if posTime >= 0:
                ingTimes.append(posTime + 1)
        return max(ingTimes) if ingTimes else 10000

    return 10000

tupSub = lambda tupL, tupR: (tupL[0] - tupR[0], tupL[1] - tupR[1], tupL[2] - tupR[2], tupL[3] + tupR[3])
# Given a SINGLE recipe, return the largest number of geodes that can
# be extracted following it.
def recursivelyFindRoute(maxTime: int, ingList: list, curRate: list, curMats: tuple, visitCache: dict) -> int:
    if maxTime == 0:        # no more time left
        return curMats[-1]
    
    # look for possible recursion
    posValues = list()
    # print(maxTime, curRate, visitCache)
    for robInd, robIngs in reversed(list(enumerate(ingList))):
        timeNeeded = getNeededTime(tuple(robIngs), tuple(curRate), curMats)
        if timeNeeded <= maxTime and ((robInd == len(ingList)-1) or (curRate[robInd] < max([curList[robInd] for curList in ingList]))):
            # Adjust new materials for what will be used
            newMats = tuple((curMats[ind] + curRate[ind]*timeNeeded for ind in range(len(curMats))))
            newMats = tupSub(newMats, (*robIngs, 0))

            # And then recurse and backtrack
            curRate[robInd] += 1
            posValues.append(recursivelyFindRoute(maxTime - timeNeeded, ingList, curRate, newMats, visitCache))
            curRate[robInd] -= 1

    # if nothing is craftable, just return total geodes until the end
    if not posValues:
        return curMats[-1] + maxTime * curRate[-1] 
    else:
        return max(posValues)

if __name__ == "__main__":
    # prepare env for p1
    inFile = './2022/Day19/input'
    robCosts = parseInputs(inFile)

    # execute algo for p1
    MAX_TIME = 24
    sol1 = sum([ind*recursivelyFindRoute(MAX_TIME, singIngList, [1, 0, 0, 0], (0, 0, 0, 0), dict()) for ind, singIngList in robCosts.items()])
    print("The solution for part 1 is {}".format(sol1))

    # and now for p2
    MAX_TIME = 32
    sol2Vals = [recursivelyFindRoute(MAX_TIME, singIngList, [1, 0, 0, 0], (0, 0, 0, 0), dict()) for singIngList in [robCosts[1], robCosts[2], robCosts[3]]]
    print("The solution for part 1 is {}".format(sol2Vals[0]*sol2Vals[1]*sol2Vals[2]))