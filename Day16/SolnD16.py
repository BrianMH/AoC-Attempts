###############################################################
#   Soln for P1 of Day 16 for AoC
#
# Problem:
#     Given a sequence of valves each with a certain pressure at
#     which they can release and a set of tunnels which allow 
#     you to move to *specific* valves, find the best path
#     that generates the highest pressure and return the
#     maximum that can be generated (no guarantees on uniqueness)
#
# Idea:
#     Approach as recursive tree problem. Instead of recursing on actions
#     we recurse on the decision to move to a specific node and activate
#     it (as walking randomly doesn't solve the problem). This seems
#     to prune enough nodes to make the problem tractable.
###############################################################
import re
from collections import deque, defaultdict # for bfs

def parseInputs(inFile: str) -> tuple[dict[str, int], dict[str, list[str]]]:
    template = r'^Valve (?P<vName>[A-Z]+) has flow rate=(?P<fR>[0-9]+); tunnels? leads? to valves? (?P<tList>[\w,?\W?]*)'
    valveAmtDict = dict()
    valveChildDict = dict()
    startValve = ""

    with open(inFile, 'r') as valveLayout:
        curLine = valveLayout.readline().rstrip()
        while curLine:
            mSeq = re.match(template, curLine).groupdict()
            valveAmtDict[mSeq['vName']] = int(mSeq['fR'])
            valveChildDict[mSeq['vName']] = mSeq['tList'].split(', ')

            curLine = valveLayout.readline().rstrip()

    return valveAmtDict, valveChildDict

'''
    For greedy algorithm to work, we need the shortest distance from our path to any path.
    This essentially performs a BFS while treating every possible node as a source to compute
    the O(V^2) dictionary.
'''
def computeMinPathLengths(childDict: dict[str, list[str]]) -> dict[str, dict[str, int]]:
    sourceNodes = list(childDict.keys())
    minDists = defaultdict(dict)

    for sNode in sourceNodes:
        masterNode = sNode
        visited = {sNode: True}
        curQueue = deque()
        curQueue.appendleft((0, sNode))

        # perform bfs while we have nodes unexplored
        while curQueue:
            curDist, curNode = curQueue.pop()

            # record dist
            minDists[masterNode][curNode] = curDist
            for child in childDict[curNode]:
                if child not in visited:
                    visited[child] = True
                    curQueue.appendleft((curDist + 1, child))

    return minDists

def recursivelyComputePaths(maxRounds: int, curNode: str, visited: set, curScore: int, valDict: dict[str, int], pathDict: dict[str, dict[str, int]]) -> int:
    # early termination
    if len(visited) == len(valDict):
        return curScore
    elif maxRounds == 0:
        return curScore
    
    # attempt going to another node and activating it
    maxScore = curScore
    for posNode in valDict.keys():
        if posNode not in visited:
            timeUsed = pathDict[curNode][posNode] + 1
            timeLeft = maxRounds - timeUsed
            posScore = valDict[posNode] * timeLeft

            if timeLeft >= 0:
                visited.add(posNode)
                maxScore = max(maxScore, recursivelyComputePaths(timeLeft, posNode, visited, curScore + posScore, valDict, pathDict))
                visited.remove(posNode)

    return maxScore

###############################################################
#   Soln for P2 of Day 16 for AoC
#
# Problem:
#     The original problem was treated as a single source BFS problem.
#     In this case, we now represent two people who each aim to optimize
#     by picking the largest available points.
#
# Idea:
#     Essentially perform the above BFS-traversal like above except two
#     points are picked every single iteration. Some optimization can
#     be done by pruning nodes as soon as the shortest path available is
#     larger than the number of rounds left for each player.
#     Extremely brute-force-like and extremely hacky. I don't like this solution
#     at all, but I am at a loss without just straight up pulling up an image
#     of the graph and analyzing if something like a cut algorithm can somehow
#     make this operation faster.
###############################################################
def recursivelyComputeDoublePaths(maxRounds: tuple[int, int], curNode: tuple[str, str], visited: set, curScore: int, valDict: dict[str, int], pathDict: dict[str, dict[str, int]]) -> int:
    # shortest paths available
    tVisit = set(list(valDict.keys())).difference(visited)
    sTMe, sTEl = 30, 30
    for posNode in tVisit:
        timeUsedMe = pathDict[curNode[0]][posNode] + 1
        timeUsedEl = pathDict[curNode[1]][posNode] + 1
        sTMe = min(sTMe, timeUsedMe)
        sTEl = min(sTEl, timeUsedEl)

    # early termination
    if len(visited) == len(valDict):
        return curScore
    elif maxRounds[0] <= sTMe and maxRounds[1] <= sTEl:
        return curScore
    elif maxRounds[0] <= sTMe: # I have finished all possible turns
        return recursivelyComputePaths(maxRounds[1], curNode[1], visited, curScore, valDict, pathDict)
    elif maxRounds[1] <= sTEl: # elephant finished all possible turns
        return recursivelyComputePaths(maxRounds[0], curNode[0], visited, curScore, valDict, pathDict)
    elif len(tVisit) == 1:
        tVisit = tVisit.pop()
        timeUsedMe = pathDict[curNode[0]][tVisit] + 1
        timeUsedEl = pathDict[curNode[1]][tVisit] + 1
        timeLeftMe = maxRounds[0] - timeUsedMe
        timeLeftEl = maxRounds[1] - timeUsedEl
        posScoreMe = valDict[tVisit] * timeLeftMe
        posScoreEl = valDict[tVisit] * timeLeftEl
        maxScorePos = max(posScoreMe, posScoreEl)
        return curScore + max(0, maxScorePos)
    
    # attempt going to another node and activating it
    maxScore = curScore
    for posNodeMe in tVisit:
        for posNodeEl in tVisit:
            if posNodeMe not in visited and posNodeEl not in visited and posNodeMe != posNodeEl:
                timeUsedMe = pathDict[curNode[0]][posNodeMe] + 1
                timeUsedEl = pathDict[curNode[1]][posNodeEl] + 1
                timeLeftMe = maxRounds[0] - timeUsedMe
                timeLeftEl = maxRounds[1] - timeUsedEl
                deltaScore = valDict[posNodeMe] * timeLeftMe + valDict[posNodeEl] * timeLeftEl

                if timeLeftMe >= 0 and timeLeftEl >= 0:
                    visited.update({posNodeEl, posNodeMe})
                    maxScore = max(maxScore, recursivelyComputeDoublePaths((timeLeftMe, timeLeftEl), (posNodeMe, posNodeEl), visited, curScore + deltaScore, valDict, pathDict))
                    visited.remove(posNodeMe)
                    visited.remove(posNodeEl)

    return maxScore

if __name__ == "__main__":
    # prepare env for p1
    inFile = './Day16/input'

    # execute algo for p1
    MAX_TIME = 30
    vAD, vCD = parseInputs(inFile)
    minPaths = computeMinPathLengths(vCD)

    sol1 = recursivelyComputePaths(MAX_TIME, 'AA', set(), 0, {vN:vV for vN, vV in vAD.items() if vAD[vN] != 0}, minPaths)
    print("The solution to part 1 is {}".format(sol1))

    # execute algo for p2
    sol2 = recursivelyComputeDoublePaths((MAX_TIME-4, MAX_TIME-4), ('AA', 'AA'), set(), 0, {vN:vV for vN, vV in vAD.items() if vAD[vN] != 0}, minPaths)
    print("The solution to part 2 is {}".format(sol2))