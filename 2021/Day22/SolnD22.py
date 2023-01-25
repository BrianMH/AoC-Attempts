#############################################################
#   Soln for P1 & P2 of Day 22 for AoC
#
# Problem:
#   At first I approached this with a brute force since it seemed
#   easy enough, but part 2 definitely just slammed that implementation
#   hard. A proper implementation follows that pretty much functions
#   similar to a selection tool in a paint tool but in 3D.
#   Areas are pretty much "cracked" into smaller areas which are then
#   added to the total area. Turning areas off is simply more of this
#   cracking, but performed on the areas to remove pieces from.
#############################################################
from typing import Optional

class Region:
    '''
        Keeps track of discrete "regions" of interest. Initialized by defining the tuples that
        define the borders of the discrete area (inclusive on both ends).
    '''
    def __init__(self, xLims: tuple[int, int], yLims: tuple[int, int], zLims: tuple[int, int]):
        self.xLims = xLims
        self.yLims = yLims
        self.zLims = zLims
        self.offAreas = list() # keeps track of flipped polarity regions inside itself

    def calculateArea(self) -> int:
        '''
            Recursively calculates a region's area
        '''
        return (self.xLims[1]-self.xLims[0]+1)*(self.yLims[1]-self.yLims[0]+1)*(self.zLims[1]-self.zLims[0]+1)

    def subtractOverlap(self, rRegion: 'Region') -> tuple[Optional['Region'], list['Region']]:
        '''
            This function works by doing the following:
                1) The 3D area of overlap is identified in the space.
                2) The area corresponding to (THIS) piece is then "cracked" into
                   6 new 3d cubes that are NOT the area of overlap.
                   NOTE: This does not apply to the othe region and that must be 
                         calculated seperately. (off's don't need that part)
                3) The results are packaged together as (overlap, [rest, of, non, overlaps, ...])
            If no overlap is identified, then the Region returned is ill-defined.

            There is a very particular way of partitoning for this function, so I'll probably just
            upload a "generalized" diagram of how it's supposed to work since it's hard to 
            convey that through a ASCII representation of intersecting cubes.
        '''
        # edge case (no overlap)
        if not self.isOverlapping(rRegion):
            return None, [self]

        # first we identify the cube of overlap (if possible)
        xROO = max(rRegion.xLims[0], self.xLims[0]), min(rRegion.xLims[1], self.xLims[1])
        yROO = max(rRegion.yLims[0], self.yLims[0]), min(rRegion.yLims[1], self.yLims[1])
        zROO = max(rRegion.zLims[0], self.zLims[0]), min(rRegion.zLims[1], self.zLims[1])
        overlap = Region(xROO, yROO, zROO)

        # And then identify the areas of non-overlap as specified on paper
        nonOverlapping = list()
        if zROO[1] < self.zLims[1]:
            nonOverlapping.append(Region(self.xLims, self.yLims, (zROO[1] + 1, self.zLims[1])))
        if zROO[0] > self.zLims[0]:
            nonOverlapping.append(Region(self.xLims, self.yLims, (self.zLims[0], zROO[0] - 1)))
        if yROO[1] < self.yLims[1]:
            nonOverlapping.append(Region(self.xLims, (yROO[1] + 1, self.yLims[1]), zROO))
        if yROO[0] > self.yLims[0]:
            nonOverlapping.append(Region(self.xLims, (self.yLims[0], yROO[0] - 1), zROO))
        if xROO[1] < self.xLims[1]:
            nonOverlapping.append(Region((xROO[1] + 1, self.xLims[1]), yROO, zROO))
        if xROO[0] > self.xLims[0]:
            nonOverlapping.append(Region((self.xLims[0], xROO[0] - 1), yROO, zROO))

        return overlap, nonOverlapping

    def isOverlapping(self, rRegion: 'Region') -> bool:
        '''
            Reports if there is overlap between another region and the current one.
            Note that a region is overlapping only if it is NOT the case that all the
            points are to the left/right/north/south of the left-most/right-most/up-most/
            south-most border.
        '''
        if rRegion.xLims[0] < self.xLims[0] and rRegion.xLims[1] < self.xLims[0]:
            return False
        elif rRegion.xLims[0] > self.xLims[1] and rRegion.xLims[1] > self.xLims[1]:
            return False
        elif rRegion.yLims[0] < self.yLims[0] and rRegion.yLims[1] < self.yLims[0]:
            return False
        elif rRegion.yLims[0] > self.yLims[1] and rRegion.yLims[1] > self.yLims[1]:
            return False
        elif rRegion.zLims[0] < self.zLims[0] and rRegion.zLims[1] < self.zLims[0]:
            return False
        elif rRegion.zLims[0] > self.zLims[1] and rRegion.zLims[1] > self.zLims[1]:
            return False

        return True

class OuterBlock:
    '''
        A class meant to keep track of regions outside of the small fine-grained area.
        It does so by keeping regions as objects  and instead of managing each cell
        individually, it handles blocks which can be "cracked" at will. Packing could
        keep this from exploding in size, but it seems unnecessary here.
    '''
    def __init__(self):
        self.cRegions : list[Region] = list()

    def calculateArea(self) -> int:
        return sum(elem.calculateArea() for elem in self.cRegions)

    def addBlock(self, bX: tuple[int, int], bY: tuple[int, int], bZ: tuple[int, int]) -> None:
        '''
            Adds a new block given the input ranges. Overlaps are accounted for by cracking
            the new proposed region w.r.t the known contained blocks and then adding these
            non-overlapping regions to the contained regions.
        '''
        propRegs = [Region(bX, bY, bZ)]

        for curReg in self.cRegions:
            newPropRegs = list()
            for propSplitReg in propRegs:
                newPropRegs.extend(propSplitReg.subtractOverlap(curReg)[1])
            propRegs = newPropRegs

        # our final result contains all of our "new" area to account for
        self.cRegions.extend(propRegs)

    def delBlock(self, bX: tuple[int, int], bY: tuple[int, int], bZ: tuple[int, int]) -> None:
        '''
            Unlike before, our "proposed" region is completely irrelevant. We want to "crack"
            our contained regions based on their overlap with the region of deletion and keep
            the areas outside of that area.
        '''
        delReg = Region(bX, bY, bZ)
        newCReg = list()

        for curReg in self.cRegions:
            newCReg.extend(curReg.subtractOverlap(delReg)[1])
        self.cRegions = newCReg

if __name__ == "__main__":
    # prepare env for p1
    inFile = "./2021/Day22/input"
    oFFB = OuterBlock()
    initProc = lambda x, y, z: -50 <= x <= 50 and -50 <= y <= 50 and -50 <= z <= 50

    with open(inFile, 'r') as cmdIn:
        cmds = [line.strip().replace(',',' ').replace('=', ' ').split()[::2] for line in cmdIn.readlines()]

    # p1 can be calculated on the path to calculating p2
    for cmd, xRg, yRg, zRg in cmds:
        xRgF, yRgF, zRgF = [[int(val) for val in elem.split('..')] for elem in (xRg, yRg, zRg)]
        inInit = initProc(*(tup[0] for tup in (xRgF, yRgF, zRgF))) and initProc(*(tup[1] for tup in (xRgF, yRgF, zRgF)))
        if not inInit: # found the halfway point
            initProc = lambda x, y, z: True    # replace with dummy
            print("The answer to part 1 is {}".format(oFFB.calculateArea()))

        # add block
        if cmd == 'on':
            oFFB.addBlock(xRgF, yRgF, zRgF)
        else:
            oFFB.delBlock(xRgF, yRgF, zRgF)

    # and now for p2
    sol2 = oFFB.calculateArea()
    print("The answer to part 2 is {}".format(sol2))