#############################################################
#   Soln for P1 of Day 20 for AoC
#
# Problem:
#   Image enhancement, but really just a test in array parsing.
#   In reality, because our array is infinite, it's better off
#   represented as a dictionary that we parse through to create
#   the expanding image.
#
#   Yet again, P2 is just the same exact thing as before but
#   running it for longer.
#############################################################
from functools import lru_cache

Point = tuple[int, int]
class ImageEnhancer:
    '''
        Because this enhancer runs several times to completely adjust
        the overall state of an image, it makes sense to deal with it
        by encapsulating the image along with the enhancement string.

        Arguments:
            inputImage - The initial seed for the infinite image.
            eString - The encoding string to use for the enhancement.
    '''
    def __init__(self, inputImage: list[str], eString: str):
        # parsing constants
        self.EMPTY = '.'
        self.FULL = '#'
        self.parseDict = {self.EMPTY: '0', self.FULL: '1'}
        self.W_SIZE = 3
        self.outVal = self.EMPTY

        # parse image and enhancement string
        self.imMat = self._arr2dict(inputImage)
        self.xLims = (0, len(inputImage))
        self.yLims = (0, len(inputImage[0]))
        self.eStr = eString

        # Some lambda helpers (we consider window size 3x3 to be fixed)
        self.extractBin = lambda curPos: "".join([self.parseDict[self.getPaddedChar(nPos)] for nPos in self.get3by3Window(curPos)])

    def performEnhancement(self) -> 'ImageEnhancer':
        '''
            Performs enhancement on the infinite image. One thing to notice is
            that every enhancement increases the apperture by a factor of
            (window_size-2) on every corner.

            Returns:
                ImageEnhancer - A self reference to the image.
        '''
        limDel = self.W_SIZE-2
        newXLims = (self.xLims[0]-limDel, self.xLims[1]+limDel)
        newYLims = (self.yLims[0]-limDel, self.yLims[1]+limDel)

        # and now process the new infinite image
        newIm = dict()
        for xInd in range(newXLims[0], newXLims[1]):
            for yInd in range(newYLims[0], newYLims[1]):
                cVal = self.eStr[int(self.extractBin((xInd, yInd)), 2)]
                if cVal == self.FULL:
                    newIm[(xInd, yInd)] = cVal

        # adjust edge value for next iter
        if self.eStr[0] == self.FULL and self.eStr[-1] == self.EMPTY:
            self.outVal = self.FULL if self.outVal == self.EMPTY else self.EMPTY

        # update class values
        self.xLims = newXLims
        self.yLims = newYLims
        self.imMat = newIm
        return self

    def countFullSpaces(self) -> int:
        ''' Returns the number of bright pixels when not infinite. '''
        if self.outVal == self.FULL:
            raise ValueError("Cannot calculate size of infinitely light image.")
        return len(self.imMat.keys())

    ######################## HELPER FUNCTIONS #############################

    @lru_cache
    def get3by3Window(self, curPos: Point) -> list:
        ''' Grabs the relevant 3x3 window and caches the coordinate output '''
        tupAdder = lambda tupL, tupR: tuple((lVal+rVal for lVal, rVal in zip(tupL, tupR)))
        relDeltas = [(-1, -1), (-1, 0), (-1, 1),
                     (0, -1), (0, 0), (0, 1),
                     (1, -1), (1, 0), (1, 1)]
        return [tupAdder(curPos, delVal) for delVal in relDeltas]

    def getPaddedChar(self, curPos: Point) -> str:
        ''' Realized late that the input is intentionally tricky by flipping edge values
            through the enhancer implementation. This takes that into account if necessary. '''
        if self.xLims[0] <= curPos[0] < self.xLims[1] and self.yLims[0] <= curPos[1] < self.yLims[1]:
            return self.imMat.get(curPos, self.EMPTY)
        else: # use padded values in this case
            return self.outVal

    def __str__(self) -> str:
        pStr = ""
        for xInd in range(self.xLims[0]-self.W_SIZE, self.xLims[1]+self.W_SIZE):
            for yInd in range(self.yLims[0]-self.W_SIZE, self.yLims[1]+self.W_SIZE):
                pStr += self.getPaddedChar((xInd, yInd))
            pStr += "\n"
        return pStr

    def _arr2dict(self, inImage: list[list[str]]) -> dict[Point, str]:
        imDict = dict()
        for i in range(len(inImage)):
            for j in range(len(inImage[0])):
                if inImage[i][j] == self.FULL:
                    imDict[(i,j)] = inImage[i][j]
        
        return imDict

if __name__ == "__main__":
    # prepare env for p1
    inFile = "./2021/Day20/input"
    with open(inFile, 'r') as imInput:
        eString = imInput.readline().strip()
        im = imInput.read().strip().split('\n')
    enSim = ImageEnhancer(im, eString)

    # execute algo for p1
    sol1 = enSim.performEnhancement().performEnhancement()
    print("The answer to part 1 is {}".format(sol1.countFullSpaces()))

    # and now for p2
    NUM_ENHANCES = 50 - 2
    for _ in range(NUM_ENHANCES):
        sol2 = enSim.performEnhancement()
    print("The answer to part 2 is {}".format(sol2.countFullSpaces()))