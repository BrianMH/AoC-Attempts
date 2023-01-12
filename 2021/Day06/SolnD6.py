#############################################################
#   Soln for P1 & P2 of Day 6 for AoC
#
# Problem:
#     Simulating the population count of lanternfish given
#     a couple stipulations:
#          1) New lanternfish have an internal timer of 8
#          2) When their internal timer hits 0:
#               2.1) A new fish is produced with a timer of 8
#               2.2) The current fish's timer starts at 6
#          3) Every other value decreases by 1 normally per turn.
#
#   Part 2 was just the same but for longer, which was expected and this
#   algorithm already runs in O(MAX_LIFETIME), which is a hell of a lot
#   better than O(num_fish).
#############################################################
class LanterfishSim:
    def __init__(self, initFile: str):
        self.curFishPop = dict()
        self.initPopulation(initFile)

        # constants
        self.MAX_LIFETIME = 8
        self.RESET_TIMEVAL = 6
    
    def initPopulation(self, inFile: str) -> None:
        '''
            Parses the input file and creates the initial population.
        '''
        with open(inFile, 'r') as popFile:
            popList = [int(val) for val in popFile.readline().rstrip().split(',')]
        
        for lifetime in popList:
            self.curFishPop[lifetime] = self.curFishPop.get(lifetime, 0) + 1

    def simulateDay(self) -> int:
        ''' 
            Simulates a day in the lanternfish population and returns the number of
            total lanternfish by the end of that day.
        '''
        newPop = dict()
        # normal countdown
        for posLifetime in reversed(range(1, self.MAX_LIFETIME+1)):
            newPop[posLifetime-1] = self.curFishPop.get(posLifetime, 0)

        # special case for 0-day fish
        newPop[self.MAX_LIFETIME] = self.curFishPop.get(0, 0)
        newPop[self.RESET_TIMEVAL] += self.curFishPop.get(0, 0)
        self.curFishPop = newPop

        return sum(self.curFishPop.values())

    def simulateDays(self, numDays: int) -> int:
        '''
            Same as the above but for multiple days
        '''
        finVal = sum(self.curFishPop.values())
        for _ in range(numDays):
            finVal = self.simulateDay()
        return finVal

if __name__ == "__main__":
    # prepare env for p1
    inFile = "./2021/Day06/input"
    NUM_DAYS = 80

    # execute algo for p1
    lSim = LanterfishSim(inFile)
    sol1 = lSim.simulateDays(NUM_DAYS)
    print("The answer to part 1 is {}".format(sol1))

    # and now for p2
    leftoverDays = 256 - NUM_DAYS
    sol2 = lSim.simulateDays(leftoverDays)
    print("The answer to aprt 2 is {}".format(sol2))