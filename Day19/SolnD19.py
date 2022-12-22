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
# Note:
#     I will be approaching this using a recursive approach first.
###############################################################
import re

# robot manufacturing rates
class Robot:
    ORE = (1, 0, 0, 0)
    CLAY = (0, 1, 0, 0)
    OBSIDIAN = (0, 0, 1, 0)
    GEODE = (0, 0, 0, 1)

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
            oCosts = (mSeq['oCost'], 0, 0)
            cCosts = (mSeq['cCost'], 0, 0)
            obsCosts = (mSeq['obsOreCost'], mSeq['obsCCost'], 0)
            gCosts = (mSeq['gOreCost'], 0, mSeq['gObsCost'])
            ingDict[mSeq['ind']] = [oCosts, cCosts, obsCosts, gCosts]
            curLine = inTemplates.readline().rstrip()

    return ingDict

# Given a SINGLE recipe, return the largest number of geodes that can
# be extracted following it.
def recursivelyFindRoute(maxTime: int, ingList: list, startingRate: tuple) -> int:
    

    return -1

if __name__ == "__main__":
    # prepare env for p1
    inFile = './Day19/input'
    robCosts = parseInputs(inFile)
    print(robCosts)

    # execute algo for p2
    MAX_TIME = 24
    sol1 = sum([ind * recursivelyFindRoute(MAX_TIME, singIngList, (1, 0, 0, 0)) for ind, singIngList in robCosts.items()])
    print("The solution for part 1 is {}".format(sol1))