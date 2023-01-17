#############################################################
#   Soln for P1 & P2 of Day 17 for AoC
#
# Problem:
#     A fairly simple physics problem that can be pretty easily
#     brute-forced with a decent enough heuristic. The only issue
#     is that I'm quite positive that there is a set of y-vels
#     that would be applicable to part 2 that would make it trivial,
#     but that is something to calculate for another day. For now,
#     the naive solution worked well enough.
#############################################################
class TargetSim:
    '''
        Implements a graph-based target shooting simulation. The dynamics are
        defined by the user along with the initial position, and the area
        taken by the target is saved as a hash map to speedup point lookup.

        Arguments:
            shootPos - The position of the element performing the shooting.
            xArea - The limits in the x-axis for the target area.
            yArea - The limits in the y-axis for the target area.
            dynamics - The acceleration (or change in velocity) observed by the
                       environment per turn.
    '''
    def __init__(self, shootPos: tuple[int, int], xArea: tuple[int, int], yArea: tuple[int, int], dynamics = dict[str, int]):
        self.xLims = xArea
        self.yLims = yArea
        self.dynamics = dynamics
        self.sPos = shootPos
        self.targetMap = self.generateMapFromLimits(self.xLims, self.yLims)

        # adder lambda
        self.tupAdder = lambda tupL, tupR: tuple((lVal+rVal for lVal, rVal in zip(tupL, tupR)))
        self.sig = lambda x: (1*(x>0)) or (-1*(x<0)) or 0

    def shootWithVelocity(self, xVel: int, yVel: int) -> tuple[bool, int, list[tuple[int, int]]]:
        ''' 
            Fires a projectile with the initial velocity and returns whether or not
            the projectile hits the target and the maximum height reached.

            Arguments:
                xVel - The starting x velocity
                yVel - The starting y velocity
            
            Returns:
                bool - Whether or not the target was hit
                int - A value representing the peak reached by the projectile
                list - A list representing the path the projectile took (until the simulation ended)
        '''
        projPos = self.sPos
        projPath = list()
        curVel = (xVel, yVel)
        targetHit, peakHeight = False, projPos[1]

        while projPos[1] >= self.yLims[0]: # our y pos limits our calculations
            projPos = self.tupAdder(projPos, curVel)
            projPath.append(projPos)
            curVel = (self.sig(curVel[0])*abs(curVel[0]+self.dynamics['x']), curVel[1]+self.dynamics['y'])

            # record hit and height
            if projPos in self.targetMap:
                targetHit = True
            peakHeight = max(peakHeight, projPos[1])

        return targetHit, peakHeight, projPath

    def findMaxShotHeight(self) -> int:
        '''
            Notice that our x-velocity doesn't matter at all. All we care about
            is moving to the proper y-velocity that gives us a y value between
            our y-limits. We want maximum height so we limit our search to positive
            y-vel, but our ceiling is by definition of the arch path we are taking:
                y_vel_highest = origin_pos_y - y_lim[0] - 1
            Anything higher is guaranteed to overshoot which means this particular
            solution MUST be the highest that hits the target box.
        '''
        yOptVel = self.sPos[1] - self.yLims[0] - 1
        return self.shootWithVelocity(0, yOptVel)[1]

    def countTotalShotsToTarget(self) -> int:
        '''
            We use similar logic as above in order to properly whittle down the problem
            into something tractible. We know that in terms of the y-velocity, it must be
            between the following
                                yLim[0] <= y_vel <= (sPos[1]-yLim[0]-1)
            And similarly for our x velocity...
                         min_to_hit_left  < x_vel <= xLim[1]
            where min_to_hit_left is found heuristically through a loop.
        '''
        velocitySet = set()
        
        # first find the min x velocity to hit the left edge
        minXVel = 0
        finXCoord = self.shootWithVelocity(minXVel, 0)[2][-1][0]
        while not (self.xLims[0] <= finXCoord <= self.xLims[1]):
            minXVel += 1
            finXCoord = self.shootWithVelocity(minXVel, 0)[2][-1][0]

        # naively iterate now
        for xVel in range(minXVel, self.xLims[1]+1):
            for yVel in range(self.yLims[0], (self.sPos[1] - self.yLims[0])):
                if self.shootWithVelocity(xVel, yVel)[0]:
                    velocitySet.add((xVel, yVel))
        
        return len(velocitySet)

    ############## HELPER FUNCTIONS ################

    def generateMapFromLimits(self, xLims: tuple[int, int], yLims: tuple[int, int]) -> dict[tuple[int, int], bool]:
        matrix = dict()
        for yVal in range(yLims[0], yLims[1]+1):
            for xVal in range(xLims[0], xLims[1]+1):
                matrix[(xVal, yVal)] = True

        return matrix

if __name__ == "__main__":
    # prepare env for p1
    inFile = "./2021/Day17/input"
    p1Dyn = {'x':-1,
             'y':-1}
    sOrigin = (0, 0)

    with open(inFile, 'r') as tFile:
        tStrToks = tFile.readline().replace("target area: ","").replace('=',',').strip().split(',')[1:4:2]
        xLTup = [int(val) for val in tStrToks[0].split("..")]
        yLTup = [int(val) for val in tStrToks[1].split("..")]

    # execute algo for p1
    tSim = TargetSim(sOrigin, xLTup, yLTup, p1Dyn)
    sol1 = tSim.findMaxShotHeight()
    print("The answer to part 1 is {}".format(sol1))

    # and now for p2
    sol2 = tSim.countTotalShotsToTarget()
    print("The answer to part 2 is {}".format(sol2))