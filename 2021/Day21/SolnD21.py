#############################################################
#   Soln for P1 of Day 21 for AoC
#
# Problem:
#   A game of dice on a circular board played with (at first)
#   a deterministic die.
#
#   P2 was a bit more challenging with what it requested, but a
#   non-pruned DFS seemed to perform decently well. As for
#   improvements, I imagine that it should be possible to cache 
#   particular combinations of scores and positions to more quickly
#   retreive them, but this worked well enough.
#############################################################
from typing import Literal, Union
from functools import reduce
from operator import add

class IntTuple:
    def __init__(self, intA: int, intB: int):
        self.tup = (intA, intB)
    
    def __add__(self, tupR: Union["IntTuple",tuple[int, int]]) -> "IntTuple":
        if isinstance(tupR, IntTuple):
            return IntTuple(self.tup[0]+tupR.tup[0], self.tup[1]+tupR.tup[1])
        else:
            return IntTuple(self.tup[0]+tupR[0], self.tup[1]+tupR[1])

    def __mul__(self, const: int) -> "IntTuple":
        self.tup = tuple((valL*const for valL in self.tup))
        return self

    def __str__(self) -> str:
        return self.tup.__str__()

class Dice:
    '''
        A placeholder if a non-deterministic die is ever used.
        (it wasn't, as expected of the application name)
    '''
    def __init__(self):
        self.numRolls = 0

    def roll(self) -> int:
        return -1

class DeterministicDie(Dice):
    '''
        A die that can only roll the values from (minRoll) to
        (maxRoll) inclusively in sequence.
    '''
    def __init__(self, minRoll: int, maxRoll: int):
        super().__init__()
        self.curVal = minRoll-1
        self.lims = (minRoll, maxRoll)
    
    def roll(self) -> int:
        self.numRolls += 1
        self.curVal += 1
        if self.curVal > self.lims[1]:
            self.curVal -= (self.lims[1]-self.lims[0]+1)
        return self.curVal

class DiracDice:
    '''
        A 2 player game of Dirac Dice played on a board of size N
        that terminates upon a player reaching a score of winScore.
        The starting positions are passed in as (p1Start, p2Start).
    '''
    def __init__(self, boardSize: int, p1Start: int, p2Start: int, winScore: int, * , customDie: Dice|None = None):
        self.P1 = 0
        self.P2 = 1

        # set up game mechanics
        self.die = customDie if customDie is not None else "Dirac"
        self.wVal = winScore
        self.bSize = boardSize
        self.board = list(range(1, boardSize+1))
        self.p1Pos, self.p1Score = p1Start-1, 0
        self.p2Pos, self.p2Score = p2Start-1, 0
        self.curPlayer = self.P1
        self.gameFinished = False

        # set up dirac version if necessary
        # NOTE: NUM_ROLLS IS FIXED TO 3 IN THIS CASE!
        if customDie is None:
            self.diracPosDict = {3:1, 4:3, 5:6, 6:7, 7:6, 8:3, 9:1}
            self.universeCache = dict()

    def simulateTurn(self, * , numRolls: int = 3) -> bool:
        # early terminate if session is already done
        if self.gameFinished:
            return True
        
        totRolls = sum([self.die.roll() for _ in range(numRolls)])
        if self.curPlayer == self.P1:
            self.p1Pos = (self.p1Pos + totRolls)%self.bSize
            self.p1Score += self.board[self.p1Pos]
        else:
            self.p2Pos = (self.p2Pos + totRolls)%self.bSize
            self.p2Score += self.board[self.p2Pos]
        
        # check for win and swap if necessary
        if self.p1Score >= self.wVal or self.p2Score >= self.wVal:
            self.gameFinished = True
        else:
            self.curPlayer = self.P2 if self.curPlayer==self.P1 else self.P1

        return self.gameFinished

    def exploreWinningUniverses(self) -> IntTuple:
        ''' 
            3 consecutive rolls can only produce values 3-9 with a Dirac Dice. The
            frequency of these rolls correspond to the following list constant:
                [1, 3, 6, 7, 6, 3, 1]     [Mag Sum: 3**3=27]
        '''
        return self._recursivelyExploreUniverse(0, 0, self.P1, self.p1Pos, self.p2Pos, self.wVal)

    def _recursivelyExploreUniverse(self, p1Score: int, p2Score: int, curPlayer: int,
                                    p1Pos: int, p2Pos: int, maxScore: int = 21) -> None:
        # check for win
        if p1Score >= maxScore:
            return IntTuple(1, 0)
        elif p2Score >= maxScore:
            return IntTuple(0, 1)

        if curPlayer == self.P1:
            allUniverses = [self._recursivelyExploreUniverse(p1Score+self.board[(p1Pos+dieSum)%self.bSize], p2Score,
                                self.P2, (p1Pos+dieSum)%self.bSize, p2Pos, maxScore)*freq for dieSum, freq in self.diracPosDict.items()]
            return reduce(add, allUniverses[1:], allUniverses[0])
        else:
            allUniverses = [self._recursivelyExploreUniverse(p1Score, p2Score+self.board[(p2Pos+dieSum)%self.bSize],
                                self.P1, p1Pos, (p2Pos+dieSum)%self.bSize, maxScore)*freq for dieSum, freq in self.diracPosDict.items()]
            return reduce(add, allUniverses[1:], allUniverses[0])

    def getWinnerScore(self) -> int:
        return self.p1Score if (self.gameFinished and self.curPlayer==self.P1) \
                            else self.p2Score
    
    def getLoserScore(self) -> int:
        return self.p2Score if (self.gameFinished and self.curPlayer==self.P1) \
                            else self.p1Score     

if __name__ == "__main__":
    # prepare env for p1
    inFile = "./2021/Day21/input"
    with open(inFile, 'r') as posIn:
        p1Start, p2Start = [int(line.strip().split(':')[1]) for line in posIn.readlines()]

    p1Die = DeterministicDie(1, 100)
    dSim = DiracDice(10, p1Start, p2Start, 1000, customDie = p1Die)

    # execute algo for p1
    gameFinished = False
    while not gameFinished:
        gameFinished = dSim.simulateTurn()
    sol1 = dSim.getLoserScore()
    print("The answer to part 1 is {}".format(sol1*p1Die.numRolls))

    # and now for p2
    dSim = DiracDice(10, p1Start, p2Start, 21)
    winCntTup = dSim.exploreWinningUniverses()
    print("The answer to part 2 is {}".format(max(winCntTup.tup)))