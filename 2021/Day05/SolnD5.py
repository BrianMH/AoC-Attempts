#############################################################
#   Soln for P1 & P2 of Day 5 for AoC
#
# Problem:
#   Find the number of overlapping positions on a grid
#   made up of a bunch of vertical/horizontal (only) lines.
#
#   P2 seems to clarify that the diagonal lines are always 45
#   degrees so they can actually be plotted properly on an
#   integer aligned grid. The answer is pretty much the same
#   as the above but now including the diagonal lines.
#############################################################
from collections import defaultdict

class Line:
    '''
        Auto orients non-diagonal lines to have the lesser value
        on the non-set axis.
    '''
    def __init__(self, x1y1: tuple[int, int], x2y2: tuple[int, int]):
        self.x1 = x1y1[0]
        self.x2 = x2y2[0]
        self.y1 = x1y1[1]
        self.y2 = x2y2[1]

        if not self.isDiag():
            self.reorient()

        # signum helper for delta func
        self.sig = lambda x: int(-1*(x<0) or 1*(x>0))

    def isDiag(self) -> bool:
        return not ((self.x1 == self.x2) or (self.y1 == self.y2))

    def reorient(self) -> None:
        if (self.x1 == self.x2):
            if self.y1 > self.y2:
                self.y1, self.y2 = self.y2, self.y1
        else:
            if self.x1 > self.x2:
                self.x1, self.x2 = self.x2, self.x1

    def getDelta(self) -> tuple[int, int]:
        '''
            Delta value from point (x1, y1) to (x2, y2) can be defined as
                 Delta := (signum(x2-x1), signum(y1-y1))
        '''
        return (self.sig(self.x2-self.x1), self.sig(self.y2-self.y1))

class Grid:
    '''
        A grid is a class that contains lines. Because it's possible
        lines need to be identifiable, it keeps in the matrix references
        of lines that intersect instead of a duplicity count.
        Diagonal lines might come into play later, so they are kept
        separately in an iterable container.

        (From P2)
        With knowledge that the diagonal lines are exactly 45 degrees, we
        know that the delta must be constrained to one of four deltas:
        (1, 1), (-1, -1), (-1, 1), or (1, -1). This makes processing easier.
    '''
    def __init__(self):
        self.matrix = defaultdict(list)
        self.diagLines = list()

        # helper for processing diagonal lines
        self.tupAdder = lambda tupL, tupR: (tupL[0] + tupR[0], tupL[1] + tupR[1])
    
    def addLine(self, x1y1: tuple[int, int], x2y2: tuple[int, int]) -> None:
        '''
            Keeps track of any diagonal lines and applies any horizontal
            / vertical lines directly onto the matrix by reference.
        '''
        curLine = Line(x1y1, x2y2)
        if curLine.isDiag():
            self.diagLines.append(curLine)
            return

        if curLine.x1 == curLine.x2: # horz line
            for yInd in range(curLine.y1, curLine.y2 + 1):
                self.matrix[(curLine.x1, yInd)].append(curLine)
        else: # vert line
            for xInd in range(curLine.x1, curLine.x2 + 1):
                self.matrix[(xInd, curLine.y1)].append(curLine)

    def processDiagLines(self) -> None:
        ''' 
            Processes the list of diagonal lines assuming that they represent
            perfect 45 degree lines
        '''
        for line in self.diagLines:
            delta = line.getDelta()
            sPt = (line.x1, line.y1)
            ePt = (line.x2, line.y2)
            self.matrix[ePt].append(line)
            while sPt != ePt:
                self.matrix[sPt].append(line)
                sPt = self.tupAdder(sPt, delta)

    def calculateOverlappingCells(self) -> int:
        '''
            The solution to P1. Essentially counts the number of cells that
            are home to more than one line reference.
        '''
        dupCnt = 0
        for lineList in self.matrix.values():
            dupCnt += (len(lineList) > 1)
        return dupCnt

if __name__ == "__main__":
    # prepare env for p1
    inFile = "./2021/Day05/input"

    # execute algo for p1
    curGrid = Grid()
    with open(inFile, 'r') as lineFile:
        for lineString in lineFile.readlines():
            x1y1, x2y2 = [[int(val) for val in tupStr.split(',')] for tupStr in lineString.split(" -> ")]
            curGrid.addLine(x1y1, x2y2)

    sol1 = curGrid.calculateOverlappingCells()
    print("The answer to part 1 is {}".format(sol1))

    # and now for p2
    curGrid.processDiagLines()
    sol2 = curGrid.calculateOverlappingCells()
    print("The answer to part 2 is {}".format(sol2))