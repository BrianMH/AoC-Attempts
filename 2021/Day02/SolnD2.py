#############################################################
#   Soln for P1 & P2 of Day 2 for AoC
#
# Problem:
#     Keep track of a submarine's horizontal and vertical movement
#     on an imaginary grid.
#############################################################
class Submarine:
    def __init__(self, initialPos: tuple[int, int] = (0, 0), * , useAim: bool = False):
        self.usingAim = useAim
        if useAim:
            self.sPos = (*initialPos, 0)
            self.tupAdder = lambda tupL, tupR: (tupL[0] + tupR[0], tupL[1] + tupR[1], tupL[2] + tupR[2])
        else:
            self.sPos = initialPos
            self.tupAdder = lambda tupL, tupR: (tupL[0] + tupR[0], tupL[1] + tupR[1])
    
    def moveForward(self, numUnits: int) -> None:
        if not self.usingAim:
            self.sPos = self.tupAdder(self.sPos, (0, numUnits))
        else:
            self.sPos = self.tupAdder(self.sPos, (self.sPos[2]*numUnits, numUnits, 0))

    def moveUp(self, numUnits: int) -> None:
        if not self.usingAim:
            self.sPos = self.tupAdder(self.sPos, (-1*numUnits, 0))
        else:
            self.sPos = self.tupAdder(self.sPos, (0, 0, -1*numUnits))

    def moveDown(self, numUnits: int) -> None:
        if not self.usingAim:
            self.sPos = self.tupAdder(self.sPos, (numUnits, 0))
        else:
            self.sPos = self.tupAdder(self.sPos, (0, 0, numUnits))

    def processMovementFile(self, inFile: str) -> None:
        with open(inFile, 'r') as subArgs:
            curLine = subArgs.readline()
            while curLine:
                command, numSteps = curLine.rstrip().split(" ")
                match command:
                    case 'forward':
                        self.moveForward(int(numSteps))
                    case 'down':
                        self.moveDown(int(numSteps))
                    case 'up':
                        self.moveUp(int(numSteps))
                curLine = subArgs.readline()
    
    def generateSolution(self) -> int:
        return self.sPos[0] * self.sPos[1]

if __name__ == "__main__":
    # prepare env for p1
    inFile = "./2021/Day02/input"
    subSim = Submarine()
    subSim.processMovementFile(inFile)

    # execute algo for p1
    sol1 = subSim.generateSolution()
    print("The answer to part 1 is {}".format(sol1))

    # and now for p2
    subSim = Submarine(useAim = True)
    subSim.processMovementFile(inFile)
    sol2 = subSim.generateSolution()
    print("The answer to aprt 2 is {}".format(sol2))