###############################################################
#   Soln for P1 of Day 22 for AoC
#
# Problem:
#     Basically just following a map along with a sequence of 
#     actions. The final coordinate is used to generate the final
#     answer.
###############################################################
class MazeElements:
    WALL = '#'
    EMPTY = '.'

# for solution encoding
class Facing:
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)
    UP = (-1, 0)

    @staticmethod
    def calculateAnswer(finRow: int, finCol: int, finHeading: tuple[int, int]) -> int:
        headVal = -1
        match finHeading:
            case Facing.RIGHT:
                headVal = 0
            case Facing.DOWN:
                headVal = 1
            case Facing.LEFT:
                headVal = 2
            case Facing.UP:
                headVal = 3
        return (1000 * (finRow + 1)) + (4 * (finCol + 1)) + headVal

    @staticmethod
    def turnRight(curHeading: tuple[int, int]) -> tuple[int, int]:
        match curHeading:
            case Facing.RIGHT:
                return Facing.DOWN
            case Facing.DOWN:
                return Facing.LEFT
            case Facing.LEFT:
                return Facing.UP
            case Facing.UP:
                return Facing.RIGHT

    @staticmethod
    def turnLeft(curHeading: tuple[int, int]) -> tuple[int, int]:
        match curHeading:
            case Facing.RIGHT:
                return Facing.UP
            case Facing.UP:
                return Facing.LEFT
            case Facing.LEFT:
                return Facing.DOWN
            case Facing.DOWN:
                return Facing.RIGHT
    

# Given an input, returns:
#      - A dict containing all rocks
#      - A dict recording all row-wise limits
#      - A dict recording all column-wizse limits
#      - A list containing all movement commands
def parseInput(inFile: str) -> tuple[dict[tuple[int, int], str], dict[int, tuple[int, int]], dict[int, tuple[int, int]], list[str]]:
    wallMap = dict()
    rowLimDict = dict()
    colLimDict = dict()
    commandList = list()

    with open(inFile, 'r') as inVals:
        curLine = inVals.readline().rstrip()
        curRow = 0

        while curLine: # this parses the arena row by row
            arStartInd, arEndInd = len(curLine) - len(curLine.lstrip()), len(curLine)
            for rowInd in range(arStartInd, arEndInd):
                if curLine[rowInd] == MazeElements.WALL:
                    wallMap[(curRow, rowInd)] = True
            
            rowLimDict[curRow] = (arStartInd, arEndInd)
            curLine = inVals.readline().rstrip()
            curRow += 1
        
        # and then we can parse the commands
        commandList = inVals.readline().rstrip().replace('L', '|L|').replace('R','|R|').split('|')

    # Then compute the column limits separately)
    maxColInd = max([end for _, end in rowLimDict.values()])
    for colInd in range(maxColInd):
        colStartInd = 0
        while colInd < rowLimDict[colStartInd][0] or colInd >= rowLimDict[colStartInd][1]:
            colStartInd += 1
        colEndInd = colStartInd + 1
        while colEndInd < len(rowLimDict) and rowLimDict[colEndInd][0] <= colInd < rowLimDict[colEndInd][1]:
            colEndInd += 1
        colLimDict[colInd] = (colStartInd, colEndInd)

    return wallMap, rowLimDict, colLimDict, commandList

def moveInDirection(sPos: tuple[int, int], facing: tuple[int, int], numMoves: int, walls: dict, rLims: dict, cLims: dict) -> tuple[int, int]:
    tupRowAdder = lambda tup1, tup2, rowSize, offset: (tup1[0] + tup2[0], (tup1[1] + tup2[1] - offset)%rowSize + offset)
    tupColAdder = lambda tup1, tup2, colSize, offset: ((tup1[0] + tup2[0] - offset)%colSize + offset, tup1[1] + tup2[1])
    curPos = sPos

    if facing == Facing.DOWN or facing == Facing.UP:
        curUpLim, curDownLim = cLims[sPos[1]]
        for _ in range(numMoves):
            newPos = tupColAdder(curPos, facing, curDownLim - curUpLim, curUpLim)
            if newPos not in walls:
                curPos = newPos
            else:
                break
    else:
        curLeftLim, curRightLim = rLims[sPos[0]]
        for _ in range(numMoves):
            newPos = tupRowAdder(curPos, facing, curRightLim - curLeftLim, curLeftLim)
            if newPos not in walls:
                curPos = newPos
            else:
                break

    return curPos

def traverseMazeUsingInput(inputs: list[str], mazeWalls: dict, mazeRLims: dict, mazeCLims: dict) -> tuple[int, int, tuple[int, int]]:
    curPos = (0, mazeRLims[0][0])
    curFacing = Facing.RIGHT

    for cmdIn in inputs:
        match cmdIn:
            case 'R':
                curFacing = Facing.turnRight(curFacing)
            case 'L':
                curFacing = Facing.turnLeft(curFacing)
            case _:
                curPos = moveInDirection(curPos, curFacing, int(cmdIn), mazeWalls, mazeRLims, mazeCLims)

    return curPos[0], curPos[1], curFacing

###############################################################
#   Soln for P2 of Day 22 for AoC
#
# Problem:
#     Force the input to correspond to a specific mesh given
#     rotations and then figure out the face correspondences.
#     It does seem like adjacent faces formed by a L shape are
#     guaranteed to be connected and then the leftover connections
#     were implicit (either from a 4-group present or 2-group outer
#     connection).
#     This way was much hackier than should have been needed for this.
###############################################################
from functools import lru_cache
import numpy as np

class TDSurfaceWalker:
    def __init__(self, inFile: str):
        inNet, self.cellWidth = self.parseInitialNetMetadata(inFile)
        adjPlan = self.generateNetAdjustPlan(inNet)
        self.dataMat, self.indMat, self.oStr = self.parseArrays(inFile)

        # We can transform the matrices now according to the discovered plan
        # and fix an orientation for convenience
        for tup in list(self.indMat[0,:]):
            if tup == 0:
                continue
            self.sPoint = tup
            break
        self.sDir = Facing.RIGHT
        self.adjNet = self.transformArrays(self.dataMat, self.indMat, adjPlan, inNet)
        self.rotated = self.adjustMatricesAndStart()

    def traverseMazeUsingInput(self, inputs: list[str]) -> tuple[int, int, tuple[int, int]]:
        curPos = self.sPoint
        curFacing = self.sDir

        for cmdIn in inputs:
            match cmdIn:
                case 'R':
                    curFacing = Facing.turnRight(curFacing)
                case 'L':
                    curFacing = Facing.turnLeft(curFacing)
                case _:
                    curPos, curFacing = self.moveInDirection(curPos, curFacing, int(cmdIn))

        # Before returning, convert back to absolute directions
        for _ in range(self.adjNet[curPos[0]//self.cellWidth][curPos[1]//self.cellWidth]):
            curFacing = Facing.turnLeft(curFacing)
        if self.rotated:
            curFacing = Facing.turnRight(curFacing)
        curPos = self.indMat[curPos]

        return curPos[0], curPos[1], curFacing

    def moveInDirection(self, sPos: tuple[int, int], sHeading: tuple[int, int], numMoves: int) -> tuple[tuple[int, int], tuple[int, int]]:
        tupAdder = lambda tupL, tupR: (tupL[0] + tupR[0], tupL[1] + tupR[1])
        validPos = lambda x, y: 0 <= x < self.dataMat.shape[0] and 0 <= y < self.dataMat.shape[1]

        curPos = sPos
        curHeading = sHeading
        for _ in range(numMoves):
            newPos = tupAdder(curPos, curHeading)

            if validPos(*newPos) and self.dataMat[newPos] == MazeElements.EMPTY:
                curPos = newPos
            elif validPos(*newPos) and self.dataMat[newPos] == MazeElements.WALL:
                return curPos, curHeading
            else: # wrap-around logic must occur here
                curInvalidBlock = (newPos[0]//self.cellWidth, newPos[1]//self.cellWidth)
                match curInvalidBlock:
                    case (-1, 1) | (4, 1):  # wrap around with no directional change
                        newHeading = curHeading
                        newPos = (newPos[0]%self.dataMat.shape[0], newPos[1])
                    case (1, -1) | (3, 0) | (1, 3) | (3, 2): # 180 deg turn case
                        newHeading = Facing.turnRight(Facing.turnRight(curHeading))
                        newPos = self.findNewPosHeading180(curPos, curInvalidBlock)
                    case _: # 90 deg turns
                        newPos, newHeading = self.findNewPosHeading90(curPos, curHeading, curInvalidBlock)

                # after we still have to check what we might have come accross
                if self.dataMat[newPos] == MazeElements.EMPTY:
                    curPos, curHeading = newPos, newHeading
                else:
                    return curPos, curHeading
        return curPos, curHeading

    def findNewPosHeading180(self, bPos: tuple[int, int], invBlock: tuple[int, int]) -> tuple[int ,int]:
        curValidBlock = (bPos[0]//self.cellWidth, bPos[1]//self.cellWidth)
        keyVal = (curValidBlock, invBlock)

        match keyVal:
            case ((1,0), (1, -1)) | ((1, 2), (1, 3)):
                moveVal = bPos[0] % self.cellWidth
                newPos = (bPos[0] + 3*self.cellWidth - 2*moveVal - 1, bPos[1] + (curValidBlock[1]-invBlock[1])*self.cellWidth)
            case ((3, 1), (3, 0)) | ((3, 1), (3, 2)):
                moveVal = bPos[0] % self.cellWidth
                newPos = (bPos[0] - self.cellWidth - 2*moveVal - 1, bPos[1] + (curValidBlock[1]-invBlock[1])*-1*self.cellWidth)
            case _:
                raise RuntimeError("Invalid scenario was passed into function")

        return newPos

    def findNewPosHeading90(self, bPos: tuple[int, int], bHeading: tuple[int, int], invBlock: tuple[int, int]) -> tuple[tuple[int, int], tuple[int, int]]:
        curValidBlock = (bPos[0]//self.cellWidth, bPos[1]//self.cellWidth)
        keyVal = (curValidBlock, invBlock)

        match keyVal:
            case ((1, 2), (0, 2)): # up and left
                moveVal = bPos[1] % self.cellWidth + 1
                newPos = (bPos[0] - moveVal, bPos[1] - moveVal)
                newHeading = Facing.turnLeft(bHeading)
            case ((0, 1), (0, 2)): # down and right
                moveVal = self.cellWidth - bPos[0]
                newPos = (bPos[0] + moveVal, bPos[1] + moveVal)
                newHeading = Facing.turnRight(bHeading)
            case ((1, 0), (0, 0)): # up and right
                moveVal = self.cellWidth - bPos[1]
                newPos = (bPos[0] - moveVal, bPos[1] + moveVal)
                newHeading = Facing.turnRight(bHeading)
            case ((0, 1), (0, 0)): # down and left
                moveVal = self.cellWidth - bPos[0]
                newPos = (bPos[0] + moveVal, bPos[1] - moveVal)
                newHeading = Facing.turnLeft(bHeading)
            case ((1, 0), (2, 0)): # down and right
                moveVal = self.cellWidth - bPos[1]
                newPos = (bPos[0] + moveVal, bPos[1] + moveVal)
                newHeading = Facing.turnLeft(bHeading)
            case ((2, 1), (2, 0)): # up and left
                moveVal = bPos[0] % self.cellWidth + 1
                newPos = (bPos[0] - moveVal, bPos[1] - moveVal)
                newHeading = Facing.turnRight(bHeading)
            case ((2, 1), (2, 2)): # up and right
                moveVal = bPos[0] % self.cellWidth + 1
                newPos = (bPos[0] - moveVal, bPos[1] + moveVal)
                newHeading = Facing.turnLeft(bHeading)
            case ((1, 2), (2, 2)): # down and left
                moveVal = bPos[1] % self.cellWidth + 1
                newPos = (bPos[0] + moveVal, bPos[1] - moveVal)
                newHeading = Facing.turnRight(bHeading)
            case _:
                raise RuntimeError("Invalid scenario was passed into function")
                
        return newPos, newHeading

    # Completely overwrites all relevant matrices to have proper vertical positioning
    def adjustMatricesAndStart(self) -> bool:
        if self.dataMat.shape[1] > self.dataMat.shape[0]:
            self.sDir = Facing.turnLeft(self.sDir)
            self.dataMat = np.rot90(self.dataMat)
            self.indMat = np.rot90(self.indMat)

            # since net is list of lists, manually rotate
            finNet = list()
            for colInd in range(len(self.adjNet[0])):
                tempCol = list()
                for rowInd in range(len(self.adjNet)):
                    tempCol.append(self.adjNet[rowInd][colInd])
                finNet.append(tempCol)
            finNet.reverse()
            self.adjNet = finNet

            # Find new starting point
            for xVal in range(self.indMat.shape[0]):
                for yVal in range(self.indMat.shape[1]):
                    if self.indMat[xVal, yVal] == self.sPoint:
                        self.sPoint = (xVal, yVal)
                        return True

        return False

    def transformArrays(self, datMat: np.ndarray, indMat: np.ndarray, adjPlan: list[tuple[tuple, tuple]], inNet: tuple[tuple[int]]) -> list[list[int]]:
        # readjusts net for calculating final heading rotation
        finNet = list([list(row) for row in inNet])
        for rowVal in range(len(inNet)):
            for colVal in range(len(inNet[0])):
                finNet[rowVal][colVal] -= 1

        # Determines a CW or CCW movement w.r.t a center point of (1,1) on the grid
        isCW = lambda initPos, finalPos: ((initPos[1]-1)*(finalPos[0]-1) - (initPos[0]-1)*(finalPos[1]-1)) > 0

        for swappedBlockPos in adjPlan:
            onePos, zPos = swappedBlockPos
            if isCW(onePos, zPos):
                rotatedDatMat = np.rot90(datMat[onePos[0]*self.cellWidth:(onePos[0]+1)*self.cellWidth, onePos[1]*self.cellWidth:(onePos[1]+1)*self.cellWidth], -1)
                rotatedIndMat = np.rot90(indMat[onePos[0]*self.cellWidth:(onePos[0]+1)*self.cellWidth, onePos[1]*self.cellWidth:(onePos[1]+1)*self.cellWidth], -1)
                adjDel = 1
            else:
                rotatedDatMat = np.rot90(datMat[onePos[0]*self.cellWidth:(onePos[0]+1)*self.cellWidth, onePos[1]*self.cellWidth:(onePos[1]+1)*self.cellWidth])
                rotatedIndMat = np.rot90(indMat[onePos[0]*self.cellWidth:(onePos[0]+1)*self.cellWidth, onePos[1]*self.cellWidth:(onePos[1]+1)*self.cellWidth])
                adjDel = 3
            datMat[zPos[0]*self.cellWidth:(zPos[0]+1)*self.cellWidth, zPos[1]*self.cellWidth:(zPos[1]+1)*self.cellWidth] = rotatedDatMat
            datMat[onePos[0]*self.cellWidth:(onePos[0]+1)*self.cellWidth, onePos[1]*self.cellWidth:(onePos[1]+1)*self.cellWidth] = ' '
            indMat[zPos[0]*self.cellWidth:(zPos[0]+1)*self.cellWidth, zPos[1]*self.cellWidth:(zPos[1]+1)*self.cellWidth] = rotatedIndMat
            indMat[onePos[0]*self.cellWidth:(onePos[0]+1)*self.cellWidth, onePos[1]*self.cellWidth:(onePos[1]+1)*self.cellWidth] = 0
            finNet[onePos[0]][onePos[1]], finNet[zPos[0]][zPos[1]] = finNet[zPos[0]][zPos[1]], finNet[onePos[0]][onePos[1]] + adjDel

        return finNet

    def parseArrays(self, inFile: str) -> tuple[np.ndarray, np.ndarray, list[str]]:
        # Data arr
        mat = list()
        with open(inFile, 'r') as inArr:
            origStr = inArr.read().split("\n\n")[0].split("\n")
            mat = [line.rstrip() for line in origStr]
        maxW = max([len(line) for line in mat])
        mat = np.array([list(line + " "*(maxW-len(line))) for line in mat], dtype=str)

        # Index arr (for solution)
        indArr = np.array([[(rowInd, colInd) for colInd in range(mat.shape[1])] for rowInd in range(mat.shape[0])], dtype="i,i").astype(np.object_)
        indArr = np.where(mat == " ", 0, indArr)

        return mat, indArr, origStr


    # generates a plan that corresponds to the change needed to modify
    # a net into becoming the default net
    # TODO: Adjust this to apply to any type of net orientation. Maybe rotate? Would need
    #       to take into account specific net structures
    def generateNetAdjustPlan(self, inNet: tuple[tuple[int]]) -> list[tuple[tuple, tuple]]:
        # this is hardcoded for this special type of net
        DEFAULT_NET = ((0, 0, 1, 0), (1, 1, 1, 1), (0, 0, 1, 0)) if len(inNet[0]) > len(inNet) else \
                      ((0, 1, 0), (1, 1, 1), (0, 1, 0), (0, 1, 0))

        sol = [((-1, -1), (-1, -1))] * 1000
        cache = dict()
        startNet = [list(row) for row in inNet]
        self.recursivelySearchSwaps(startNet, cache, [], sol, tuple((tuple(row) for row in DEFAULT_NET)))
        return sol
    
    ############################# HELPER FUNCS ########################################
    @lru_cache
    def enumerateNearbyCoords(self, curPos: tuple[int, int], netRows: int, netCols: int) -> list[tuple[int, int]]:
        posDels = [(0, -1), (0, 1), (1, 0), (-1, 0)]
        isValidCoord = lambda rInd, cInd: 0 <= rInd < netRows and 0 <= cInd < netCols
        tupAdder = lambda tupL, tupR: (tupL[0]+tupR[0], tupL[1]+tupR[1])
        
        tReturn = list()
        for delta in posDels:
            newPos = tupAdder(curPos, delta)
            if isValidCoord(*newPos):
                tReturn.append(newPos)
        
        return tReturn

    def recursivelySearchSwaps(self, curNet: list[list[int]], netCache: dict[tuple[tuple[int]], int], curAdjs: list[tuple[tuple, tuple]], solAdjs: list[tuple[tuple, tuple]], tNet: tuple[tuple[int]], maxDepth: int = 7) -> None:
        tupCurNet = tuple((tuple(row) for row in curNet))
        if tupCurNet == tNet:                                              # potential solution found
            if len(curAdjs) <= len(solAdjs):
                solAdjs.clear()
                solAdjs.extend(curAdjs)
            return
        elif len(curAdjs) > maxDepth:
            return
        elif tupCurNet in netCache and netCache[tupCurNet] <= len(curAdjs): # prune node visited earlier
            return

        # record visit
        netCache[tupCurNet] = len(curAdjs)

        # continue swapping where possible
        for rowInd in range(len(curNet)):
            for colInd in range(len(curNet[0])):
                if curNet[rowInd][colInd] == 0:
                    continue

                for sPos in self.enumerateNearbyCoords((rowInd, colInd), len(curNet), len(curNet[0])):
                    if curNet[sPos[0]][sPos[1]] == 0:
                        curNet[rowInd][colInd], curNet[sPos[0]][sPos[1]] = curNet[sPos[0]][sPos[1]], curNet[rowInd][colInd]
                        self.recursivelySearchSwaps(curNet, netCache, curAdjs + [((rowInd, colInd), (sPos[0], sPos[1]))], solAdjs, tNet)
                        curNet[rowInd][colInd], curNet[sPos[0]][sPos[1]] = curNet[sPos[0]][sPos[1]], curNet[rowInd][colInd]

    @staticmethod
    def parseInitialNetMetadata(inFile: str) -> tuple[tuple[tuple[int]], int]:
        # first extract block sizes
        # 3-3 net can mess this up, accounting for it can be done
        # by finding the GCD between col size and min row len
        with open(inFile, 'r') as initBlock:
            curLine = initBlock.readline().rstrip()
            numLines = 0
            minLen = 100000
            while curLine.strip():
                minLen = min(len(curLine.lstrip()), minLen)
                numLines += 1
                curLine = initBlock.readline().rstrip()
        
        # now parse the NxN blocks
        netStructure = list()
        with open(inFile, 'r') as initBlock:
            curLine = initBlock.readline().rstrip()
            while curLine:
                rowLen = len(curLine.lstrip())
                rowOffset = (len(curLine) - rowLen) // minLen
                curRow = [0] * rowOffset + [1] * (rowLen // minLen)
                netStructure.append(curRow)

                for _ in range(minLen):
                    curLine = initBlock.readline().rstrip()

        # pad final output for consistent sizing
        maxLen = max([len(row) for row in netStructure])
        [row.extend([0]*(maxLen-len(row))) for row in netStructure]

        return tuple((tuple(row) for row in netStructure)), minLen

    @staticmethod
    def extractFileCommands(inFile: str) -> list[str]:
        with open(inFile, 'r') as potList:
            cmds = potList.read().split("\n\n")[-1]
        
        return cmds.rstrip().replace('L', '|L|').replace('R','|R|').split('|')

if __name__ == "__main__":
    # prepare env for p1
    inFile = './2022/Day22/input'
    wMap, rDict, cDict, cList = parseInput(inFile)
    solCoords = traverseMazeUsingInput(cList, wMap, rDict, cDict)
    print("Solution to part 1 is {}".format(Facing.calculateAnswer(*solCoords)))

    # now eval on p2
    w2 = TDSurfaceWalker(inFile)
    cmds = w2.extractFileCommands(inFile)
    solCoords = w2.traverseMazeUsingInput(cmds)
    print("Solution to part 2 is {}".format(Facing.calculateAnswer(*solCoords)))