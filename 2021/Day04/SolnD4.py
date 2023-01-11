#############################################################
#   Soln for P1 & P2 of Day 4 for AoC
#
# Problem:
#     Bingo boards and finding the first and last winner. Keeping
#     everything in terms of bits makes things significantly faster
#     but did cause a few trip ups for bit shift values. Seems fast
#     enough for now.
#############################################################
from collections import defaultdict
from typing import Optional
from copy import deepcopy

class BingoBoard:
    '''
        Creates the structure to hold the 5x5 board for the game.
        Initialization takes in the array that represents the 5x5 board.
    '''
    def __init__(self, valArr: list[list[int]]):
        self.board = [0b00000] * 5
        self.boardCopy = None
        self.mapping = self.generateMapFromArray(valArr)
    
    def generateMapFromArray(self, valArr: list[list[int]]) -> dict[int, tuple[int, int]]:
        '''
            Creates a mapping from a value to the position in the array in terms of
             (y, x).

             Argument:
                valArr - The board represented in a list of lists.

            Returns:
                dict - A dictionary representing the (val) -> (pos,tuple) mapping
        '''
        self.boardCopy = deepcopy(valArr)
        mapDict = dict()
        for rowInd in range(len(valArr)):
            for colInd in range(len(valArr[0])):
                mapDict[valArr[rowInd][colInd]] = (rowInd, colInd)
        return mapDict

    def checkWin(self) -> bool:
        # row-wise check
        boardCC = 0b11111
        for row in self.board:
            boardCC &= row
            if row == 0b11111:
                return True
        
        # column wise-check
        if boardCC > 0:
            return True
        return False

    def markOnBoard(self, valToMark: int) -> bool:
        '''
            Marks the value on the board if it exists. Returns true
            if the value existed and was marked and false otherwise.

            Argument:
                valToMark - The integer value to mark on the board.
        '''
        toMark = self.mapping.get(valToMark, None)
        if toMark is None:
            return False

        self.board[toMark[0]] = self.board[toMark[0]] | (0b00001 << toMark[1])
        return True

    def calculateP1Answer(self, lastValPlayed: int) -> int:
        '''
            Calculates the solution to part 1 by finding the sum of all the
            unmarked numbers and multiplying that by the last value played.
        '''
        nonMarkedSum = 0
        for rowInd in range(len(self.boardCopy)):
            for colInd in range(len(self.boardCopy)):
                notMarked = 1 - ((self.board[rowInd] & (0b00001 << colInd)) > 0)
                nonMarkedSum += self.boardCopy[rowInd][colInd] * notMarked

        return lastValPlayed * nonMarkedSum

class BingoGame:
    '''
        A collection of bingo boards that represents an entire session
        of a bingo game.
    '''
    def __init__(self):
        self.boards = list()
        self.playedVals = set()
        self.valLookup = defaultdict(list)

    def initializeBoardsFromFile(self, inFile: str, * , ignoreHeader: bool = True) -> None:
        '''
            Creates an array of boards from a given file.
        '''
        with open(inFile, 'r') as boardFile:
            if ignoreHeader:
                boardFile.readline()

            curBoards = boardFile.read().split("\n\n")
            for boardInd, boardStr in enumerate(curBoards):
                cleanedBoard = [[int(val) for val in line.strip().split()] for line in boardStr.split("\n") if line.strip()]
                self.boards.append(BingoBoard(cleanedBoard))
                self._updateLookup(cleanedBoard, boardInd)

    def _updateLookup(self, curBoardArr: list[list[int]], boardInd: int) -> None:
        '''
            Takes in a board array and updates the class' lookup table to easily
            identify which boards to update.
        '''
        for row in curBoardArr:
            for val in row:
                self.valLookup[val].append(boardInd)

    def playValues(self, valsToPlay: list[int], * , findLast: bool = False) -> Optional[tuple[int, BingoBoard]]:
        '''
            Plays the game of bingo given a sequence of integers that includes no duplicates.
            Returns the winning number and the winning board.
        '''
        wonBitString = 2**(len(self.boards)) - 1
        totWins = 0
        for valInPlay in valsToPlay:
            for relBoardInd in self.valLookup.get(valInPlay, list()):
                self.boards[relBoardInd].markOnBoard(valInPlay)
                if (wonBitString & (0b01 << relBoardInd)) and self.boards[relBoardInd].checkWin():
                    if not findLast:
                        return (valInPlay, self.boards[relBoardInd])
                    
                    totWins += 1
                    wonBitString ^= (0b01 << relBoardInd)
                    if wonBitString == 0:
                        return (valInPlay, self.boards[relBoardInd])

        return None # no games win by the end of the value list

    @staticmethod
    def extractValArrHeader(inFile: str) -> list[int]:
        '''
            Extracts the list of commands present at the top of the input file.
        '''
        with open(inFile, 'r') as toParse:
            return [int(val) for val in toParse.readline().rstrip().split(',')]

if __name__ == "__main__":
    # prepare env for p1
    inFile = "./2021/Day04/input"
    curGame = BingoGame()
    curGame.initializeBoardsFromFile(inFile)
    valCmds = BingoGame.extractValArrHeader(inFile)

    # calculate sol for p1
    lastVal, winningBoard = curGame.playValues(valCmds)
    print("The answer to part 1 is {}".format(winningBoard.calculateP1Answer(lastVal)))

    # reset and and now find p2 sol
    curGame = BingoGame()
    curGame.initializeBoardsFromFile(inFile)
    lastVal, failBoard = curGame.playValues(valCmds, findLast = True)
    print("The answer to aprt 2 is {}".format(failBoard.calculateP1Answer(lastVal)))