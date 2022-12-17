###############################################################
#   Soln for P1 of Day 17 for AoC
#
# Problem:
#     We are just simulating a modified Tetris where the piece
#     begins with 3 units below the lowest point of the piece
#     but above the highest point in the tower. Pieces go in a specific
#     order, and do not stop moving until they collide with another
#     piece or the wall. (Left/Right movements that would collide
#     with another piece or the wall horizontally are performed but
#     have no effect on the game)
###############################################################
from functools import lru_cache


class TetrisPiece:
    # static constants
    AIR = ' '
    PIECE = '#'

    def __init__(self, shape: list[list[str]]):
        self.repr = shape
        self.height = len(shape)
        self.width = len(shape[0])

    # returns the bottom face, which is the only face on which a collision
    # would force a block to freeze. (relative to the piece repr list)
    @lru_cache    
    def extractBottomFaceCoords(self) -> list[tuple[int, int]]:
        eCoords = list()
        for xInd in range(len(self.repr[0])):
            for yInd in range(len(self.repr)):
                if self.repr[yInd][xInd] == TetrisPiece.PIECE:
                    eCoords.append((yInd, xInd))
                    break
        return eCoords


class ScuffedTetris:
    def __init__(self, pieceLexicon: list[TetrisPiece], arenaWidth: int):
        # meta
        self.toPlay = pieceLexicon
        self.hPoint = 0
        self.playWidth = arenaWidth

        # arena-related
        self.sparseArr = dict()
        self.curPiece = 0
 
if __name__ == "__main__":
    # prepare env for part 1
    inFile = './Day17/input'

    # import relative pieces (in order)