###############################################################
#   Soln for P1 and P2 of Day 17 for AoC
#
# Problem:
#     We are just simulating a modified Tetris where the piece
#     begins with 3 units below the lowest point of the piece
#     but above the highest point in the tower. Pieces go in a specific
#     order, and do not stop moving until they collide with another
#     piece or the wall. (Left/Right movements that would collide
#     with another piece or the wall horizontally are performed but
#     have no effect on the game)
#     Part 2 is simply running the algorithm for a lot longer. One
#     thing to notice is that the way to get around the memory limitation
#     is simply to wipe the entire field ones a completely filled row is
#     encountered and then keep track of the number of rows that were below
#     it. (In general, we can only have (min_width-1) open spaces to determine
#     a "full" row)
###############################################################
from functools import lru_cache
from time import sleep
from collections import defaultdict

class TetrisPiece:
    # static constants
    PIECE_VAL = '#'

    def __init__(self, shape: list[str]):
        self.repr = shape
        self.height = len(shape)
        self.width = len(shape[0])

    # returns the bottom face, which is the only face on which a collision
    # would force a block to freeze. (relative to the piece repr list)
    @lru_cache    
    def extractPieceDeltas(self) -> list[tuple[int, int]]:
        eCoords = list()
        for xInd in range(len(self.repr[0])):
            for yInd in range(len(self.repr)):
                if self.repr[yInd][xInd] == TetrisPiece.PIECE_VAL:
                    eCoords.append((yInd, xInd))
        return eCoords

    @lru_cache
    def extractBotFaceDeltas(self) -> list[tuple[int, int]]:
        eCoords = list()
        for xInd in range(len(self.repr[0])):
            for yInd in range(len(self.repr)):
                if self.repr[yInd][xInd] == TetrisPiece.PIECE_VAL:
                    eCoords.append((yInd, xInd))
                    break
        return eCoords

    @staticmethod
    def parseFromFile(inFile: str) -> list['TetrisPiece']:
        with open(inFile, 'r') as pTemplates:
            pieces = pTemplates.read().split("\n\n")
            pieces = [piece.split('\n') for piece in pieces]
            [piece.reverse() for piece in pieces]
        
        return [TetrisPiece(piece) for piece in pieces]

class Tetris:
    LEFT_MOVE = '<'
    RIGHT_MOVE = '>'
    AIR = "-"
    FROZEN = "@"

    def __init__(self, pieceLexicon: list[TetrisPiece], arenaWidth: int, refreshRate: float = 1.0/5):
        # meta
        self.toPlay = pieceLexicon
        self.hPoint = 0
        self.curPieceHeight = 0
        self.curPieceWidth = 0
        self.playWidth = arenaWidth
        self.inPlay = False

        # arena-related
        self.sparseArr = dict()
        self.curPiece = -1
        self.totPieces = 0
        self.pBLCoord = (-1, -1)
        self.clearedFieldSizes = list()

        # constants for printing
        self.DISP_INC = 3
        self.addTups = lambda tupL, tupR: (tupL[0]+tupR[0], tupL[1]+tupR[1])
        self.wait = lambda : sleep(refreshRate)

    '''
        This function determines if the current piece placed has caused an entire row to be filled.
        If so, then this wipes the field up to the completed row and then changes all the coordinates
        in order to properly allow the field to update.
    '''
    def rollOverOnFilledLined(self, wipeThresh: int = 10000):
        # check for filled row
        relYs = {self.addTups(self.pBLCoord, delta)[0] for delta in self.toPlay[self.curPiece].extractPieceDeltas()}
        wipeBelowY = -1
        for yVal in relYs:
            allFlag = True
            for xVal in range(self.playWidth):
                if self.sparseArr.get((yVal, xVal), self.AIR) == self.AIR:
                    allFlag = False
                    break
            
            if allFlag:
                wipeBelowY = max(wipeBelowY, yVal+1)
        
        # wipe if possible
        if wipeBelowY >= wipeThresh:
            newArena = dict()
            for yVal in range(wipeBelowY, self.hPoint):
                for xVal in range(self.playWidth):
                    if self.sparseArr.get((yVal, xVal), None) is not None:
                        newArena[(yVal-wipeBelowY, xVal)] = self.sparseArr.get((yVal, xVal))
                        arenaEmpty = False
            del self.sparseArr
            self.sparseArr = newArena
            self.hPoint -= wipeBelowY
            self.clearedFieldSizes.append(wipeBelowY)

    def executePatternUntilPieceNo(self, pattern: list[str], maxPCnt: int, *, verbose: bool = False) -> None:
        if verbose:
            printField = lambda : print(self)
        else:
            printField = lambda : None

        # parse moves one by one
        patternInd = -1
        while True:
            patternInd = (patternInd + 1)%len(pattern)
            command = pattern[patternInd]

            if self.inPlay: # move piece down
                if self.pBLCoord[0] > 0 and not self.checkCollision((-1, 0), bott_only = True):
                    self.unwritePieceFromField()
                    self.pBLCoord = (self.pBLCoord[0] - 1, self.pBLCoord[1])
                    self.writePieceToField()
                else:       # freeze it
                    self.writePieceToField(self.FROZEN)
                    self.rollOverOnFilledLined()
                    self.inPlay = False
                    self.totPieces += 1
                if verbose: printField(); self.wait()
                if self.totPieces == maxPCnt:
                    return

            if not self.inPlay: # get new piece if necessary
                self.curPiece = (self.curPiece + 1)%len(self.toPlay)
                self.inPlay = True
                self.curPieceHeight = self.toPlay[self.curPiece].height
                self.curPieceWidth = self.toPlay[self.curPiece].width
                self.pBLCoord = (self.hPoint + self.DISP_INC, 2)
                self.writePieceToField()
                if verbose: printField(); self.wait()

            # push piece if possible
            self.unwritePieceFromField()
            if command == self.LEFT_MOVE and self.pBLCoord[1] > 0:
                newCoord = (self.pBLCoord[0], self.pBLCoord[1] - 1)
                if not self.checkCollision((0, -1)):
                    self.pBLCoord = newCoord
            elif command == self.RIGHT_MOVE and self.pBLCoord[1] + self.curPieceWidth < self.playWidth:
                newCoord = (self.pBLCoord[0], self.pBLCoord[1] + 1)
                if not self.checkCollision((0, 1)):
                    self.pBLCoord = newCoord
            self.writePieceToField()
            if verbose: printField(); self.wait()

    # checks if given the delta, the piece will collide with another piece
    def checkCollision(self, delta: tuple[int, int], * , bott_only:bool = False) -> bool:
        if not bott_only:
            relDeltas = self.toPlay[self.curPiece].extractPieceDeltas()
        else:
            relDeltas = self.toPlay[self.curPiece].extractBotFaceDeltas()
        newPBCoord = self.addTups(self.pBLCoord, delta)
        for pDelta in relDeltas:
            if self.sparseArr.get(self.addTups(newPBCoord, pDelta), self.AIR) != self.AIR:
                return True
        
        return False

    # Helper array modificaiton functions
    def unwritePieceFromField(self):
        relDeltas = self.toPlay[self.curPiece].extractPieceDeltas()
        for delta in relDeltas:
            del self.sparseArr[self.addTups(self.pBLCoord, delta)]

    def writePieceToField(self, modVal: str = ""):
        relDeltas = self.toPlay[self.curPiece].extractPieceDeltas()
        for delta in relDeltas:
            newPt = self.addTups(self.pBLCoord, delta)
            if modVal:
                self.hPoint = max(self.hPoint, newPt[0]+1)
            self.sparseArr[newPt] = TetrisPiece.PIECE_VAL if not modVal else modVal

    def __str__(self):
        retStr = ["+" + "-" * self.playWidth + "+"]
        for rowInd in range(self.hPoint+self.DISP_INC+self.curPieceHeight):
            rStr = "|" + "".join([self.sparseArr.get((rowInd,colInd), self.AIR) for colInd in range(self.playWidth)]) + "|"
            retStr.append(rStr)
        retStr.reverse()
        return "\n".join(retStr)

    def getTotalHeight(self):
        return sum(self.clearedFieldSizes) + self.hPoint
 
if __name__ == "__main__":
    # prepare env for part 1
    inFile = './Day17/input'
    pFile = './Day17/pieces'

    # import relative pieces (in order)
    pLex = TetrisPiece.parseFromFile(pFile)
    sim = Tetris(pLex, 7)

    with open(inFile, 'r') as inputFile:
        inputs = list(inputFile.read().strip())
    sim.executePatternUntilPieceNo(inputs, 2022, verbose = False)
    print("Solution to part 1 is {}".format(sim.getTotalHeight()))

    # now execute part 2
    sim = Tetris(pLex, 7)
    sim.executePatternUntilPieceNo(inputs, 1000000000000)
    print("Solution to part 2 is {}".format(sim.getTotalHeight()))