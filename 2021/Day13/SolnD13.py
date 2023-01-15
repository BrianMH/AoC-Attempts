#############################################################
#   Soln for P1 of Day 13 for AoC
#
# Problem:
#   Seems like we are given a set of instructions on how
#   to perform reflections given a set of points on a grid.
#   We can optimize the graph a bit by assuming that the points
#   will not be dense and simply use a set to represent all of
#   the points. A dict can be kept just in case the multiplicity
#   of a point will become relevant later.
#   Part 2 did seem to just be finishing up all the rotations
#   (and then just plotting them to read the string represented
#    by the dots).
#############################################################
# point definition
Point = tuple[int, int]

class PointGraph:
    '''
        A simple representation of sparse points on a grid using a dictionary
        as a container. Can represent point multiplicity as a result.
    '''
    def __init__(self):
        self.points = dict()

        # helper lambda for mirroring
        self.mirrorVal = lambda mPt, val: mPt - abs(val-mPt)
    
    def addPoint(self, pt: Point) -> None:
        self.points[pt] = self.points.get(pt, 0) + 1

    def parseInputPts(self, inFile: str) -> int:
        '''
            Reads in a file along with the points it has formatted as x,y on
            each line. Any values that don't adhere to this are simply ignored.

            Arguments:
                inFile - The file to read the points from
            
            Returns:
                int - The number of points read into the graph
        '''
        numAdded = 0
        with open(inFile, 'r') as ptFile:
            curLine = ptFile.readline()
            while curLine:
                curToks = curLine.rstrip().split(",")
                if len(curToks) == 2:
                    newPt = (int(val) for val in curToks)
                    self.addPoint(newPt)
                    numAdded += 1
                curLine = ptFile.readline()
        
        return numAdded
    
    def countUniquePoints(self) -> int:
        ''' Returns the number of unique spots currently taken up by the points. '''
        return len(self.points.keys())

    def mirrorAboutLine(self, axis: str, mPt: int) -> None:
        '''
            Mirrors the current contained points from the greater
            axis value to the lower value (right to left or down to up).

            Arguments:
                mPt - The value on which to use as the mirroring point.
                axis - The axis to mirror about. Can either be 'x' or 'y'.
        '''
        newPts = dict()
        for ptX, ptY in self.points:
            if axis == 'x':
                relVal = ptX
            elif axis == 'y':
                relVal = ptY
            else:
                raise ValueError("Invalid axis to mirror over.")

            # perform the mirroring 
            if relVal > mPt:
                mirrored = self.mirrorVal(mPt, relVal)
                if axis == 'x':
                    newPt = (mirrored, ptY)
                else:
                    newPt = (ptX, mirrored)
                newPts[newPt] = newPts.get(newPt, 0) + 1
            else:
                newPts[(ptX, ptY)] = newPts.get((ptX, ptY), 0) + 1
        self.points = newPts

    def __str__(self) -> str:
        ''' Returns a string representation of the plot '''
        xMin, xMax, yMin, yMax = 999999, -999999, 999999, -999999
        for ptX, ptY in self.points:
            xMin, xMax = min(xMin, ptX), max(xMax, ptX)
            yMin, yMax = min(yMin, ptY), max(yMax, ptY)

        retStr = ""
        for yVal in range(yMin, yMax + 1):
            for xVal in range(xMin, xMax + 1):
                retStr = retStr+"#" if (xVal, yVal) in self.points else retStr+" "
            retStr += "\n"
        return retStr

if __name__ == "__main__":
    # prepare env for p1
    inFile = "./2021/Day13/input"
    curPlot = PointGraph()
    curPlot.parseInputPts(inFile)

    mExecList = list()
    with open(inFile, 'r') as mirrorLines:
        curLine = mirrorLines.readline()
        while curLine:
            toks = curLine.rstrip().split()
            if len(toks) == 3:
                axisStr, mirrorPt = toks[-1].split("=")
                mExecList.append((axisStr, int(mirrorPt)))
            curLine = mirrorLines.readline()

    # execute algo for p1
    curPlot.mirrorAboutLine(*mExecList[0])
    sol1 = curPlot.countUniquePoints()
    print("The answer to part 1 is {}".format(sol1))

    # and now for p2
    [curPlot.mirrorAboutLine(*tup) for tup in mExecList[1:]]
    print("The formatted string with the answer to part 2 is \n{}".format(curPlot))