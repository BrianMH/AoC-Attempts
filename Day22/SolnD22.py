###############################################################
#   Soln for P1 of Day 22 for AoC
#
# Problem:
#     Basically just following a map along with a sequence of 
#     actions. The final coordinate is used to generate the final
#     answer.
###############################################################
class MazeElements:
    ROCK = '#'
    EMPTY = '.'

# Given an input, returns:
#      - A dict containing all rocks
#      - A dict recording all row-wise limits
#      - A dict recording all column-wizse limits
#      - A list containing all movement commands
def parseInput(inFile: str) -> dict[tuple[int, int], str], dict[int, tuple[int, int]], dict[int, tuple[int, int]], list[str]:
    rockMap = dict()
    rowLimDict = dict()
    colLimDict = dict()
    commandList = list()

    with open(inFile, 'r') as inVals:
        pass

if __name__ == "__main__":
    # prepare env for p1
    inFile = './Day22/input'
    