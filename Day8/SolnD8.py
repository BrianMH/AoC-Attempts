###############################################################
#   Soln for P1 of Day 8 for AoC
#
# Problem:
#     Given a map of tree heights, identify how many trees are visible
#     from the outside. More formally, we consider a tree visible
#     if and only if there exists a path from the edge to the tree
#     in question following a cardinal direction (NSWE) where all
#     tree sizes are strictly increasing. 
###############################################################
# This can use a DP method to solve but it would require two passes
# in order to consolidate information. Instead, it's simpler to use
# a BFS starting from all outer nodes and simply propagate the information
# through the map. This will use O(NxM) size to store but should function
# the simplest.
class CARDINAL_DIRS():
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)

# Extracts all matrix edges along with appending them with their appropriate exploration
# direction.
def extractMatEdgesAndDirs(inMat: list[list]) -> tuple[tuple[int, int], CARDINAL_DIRS]:
    edgesAndDirs = list()

    # extract all non-outermost edges
    topRefs = zip([0]*(len(inMat[0])-2), range(1,len(inMat[0])-1))
    botRefs = zip([len(inMat)-1]*(len(inMat[0])-2), range(1, len(inMat[0])-1))
    leftRefs = zip(range(1,len(inMat)-1), [0]*(len(inMat)-2))
    rightRefs = zip(range(1,len(inMat)-1), [len(inMat[0])-1]*(len(inMat)-2))
    totRefs = [topRefs, botRefs, leftRefs, rightRefs]
    totDirs = [CARDINAL_DIRS.SOUTH, CARDINAL_DIRS.NORTH, CARDINAL_DIRS.EAST, CARDINAL_DIRS.WEST]

    for setInd in range(len(totRefs)):
        edgesAndDirs.extend([(point, totDirs[setInd]) for point in totRefs[setInd]])

    return edgesAndDirs

def p1Soln(inFile: str) -> int:
    # prepare the data for processing by reading in the height matrix
    hMat = list()
    with open(inFile, 'r') as heightRecs:
        curLine = heightRecs.readline()
        while curLine:
            hMat.append([int(hVal) for hVal in curLine.strip()])
            curLine = heightRecs.readline()
    visibleList = [[0] * len(hMat[0]) for _ in range(len(hMat))]

    # good lord naive O(4*N*M) traversal-like solution
    toVisit = extractMatEdgesAndDirs(hMat)
    validPoint = lambda x,y : (0 <= x < len(hMat)) and (0 <= y < len(hMat[0]))
    for (point, deltas) in toVisit:
        curX, curY = point[0], point[1]
        deltaX, deltaY = deltas[0], deltas[1]
        visibleList[curX][curY] = 1
        curHeight = hMat[curX][curY]

        while(validPoint(curX+deltaX, curY+deltaY)):
            curX += deltaX
            curY += deltaY
            newHeight = hMat[curX][curY]
            # need to take care of adjusting heights when not strictly increasing
            visibleList[curX][curY] = 1 if newHeight > curHeight else visibleList[curX][curY]
            curHeight = newHeight if newHeight > curHeight else curHeight
    
    return sum([sum(row) for row in visibleList]) + 4

###############################################################
#   Soln for P2 of Day 8 for AoC
#
# Problem:
#     Given a map of tree heights, identify the highest scenic
#     score available for a given position in the matrix. Like above
#     the scenic score is calculated by finding the total product of
#     all the trees visible in each of the four cardinal directions.
#     Unlike before, calculation terminates the moment the view is
#     blocked by a tree of the same height.
###############################################################
def p2Soln(inFile: str) -> int:
    # prepare the data for processing by reading in the height matrix
    hMat = list()
    with open(inFile, 'r') as heightRecs:
        curLine = heightRecs.readline()
        while curLine:
            hMat.append([int(hVal) for hVal in curLine.strip()])
            curLine = heightRecs.readline()

    # we must traverse the entire matrix calculating these scores
    # in all directions...
    validPoint = lambda x,y : (0 <= x < len(hMat)) and (0 <= y < len(hMat[0]))
    dirsToCheck = [CARDINAL_DIRS.NORTH, CARDINAL_DIRS.EAST, 
                  CARDINAL_DIRS.SOUTH, CARDINAL_DIRS.WEST]
    maxScore = 0
    for xInd in range(1,len(hMat)-1):
        for yInd in range(1,len(hMat[0])-1):
            locHeight = hMat[xInd][yInd]
            curScore = 1

            for deltaX, deltaY in dirsToCheck:
                curMultiple = 0
                curX, curY = xInd + deltaX, yInd + deltaY
                while(validPoint(curX, curY)):
                    curMultiple += 1

                    if hMat[curX][curY] >= locHeight:
                        break
                    curX, curY = curX + deltaX, curY + deltaY

                # update score
                curScore *= curMultiple

            # check max 
            if curScore > maxScore:
                maxScore = curScore

    return maxScore


if __name__ == "__main__":
    # Set up env for p1
    inFile = "./Day8/input"

    # Process algo for p1
    soln1 = p1Soln(inFile)
    print("Solution for part 1 is {}".format(soln1))

    # Process algo for p2
    soln2 = p2Soln(inFile)
    print("Solution for part 2 is {}".format(soln2))