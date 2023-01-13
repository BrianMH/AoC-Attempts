#############################################################
#   Soln for P1 of Day 8 for AoC
#
# Problem:
#     This part seems pretty hardcoded. Since the segments for
#     the values (1, 4, 7, 8) are of size (2, 4, 3, 7), respectively,
#     we want to know the number of times these values are seen
#     AFTER THE PIPE, "|" 
#############################################################
def countP1Segments(inFile: str, sizesToFind: list[int], delimiter: str = "|") -> int:
    '''
        Given an input file, returns the elements beyond the delimiter that contain
        space-separated strings of sizes found in sizesToFind.
    '''
    hits = 0
    with open(inFile, 'r') as toRead:
        curLine = toRead.readline()
        while curLine.rstrip():
            relTokens = [len(tok) for tok in curLine.split("|")[1].strip().split()]
            for tokSize in relTokens:
                if tokSize in sizesToFind:
                    hits += 1
            curLine = toRead.readline()
    return hits

#############################################################
#   Soln for P2 of Day 8 for AoC
#
# Problem:
#   Now we are required to actually solve the code, which
#   should be fairly simply by taking set differences between
#   two sets.
#   Given an input of the form "ENCODED_ENTITIES | VAL_TO_DECODE"
#   the following class can do most of the work.
#   The default 7 segment display is hardcoded to be the following:
#
#      aaaa
#     b    c
#     b    c 
#      dddd 
#     e    f
#     e    f
#      gggg 
#
#   Note: Very hacky. Very brute-force. But I'm not so sure if there
#         was another way without designing your own algorithm to grab
#         values through set manipulations...
#############################################################
class SevenSegmentParser():
    '''
        A class made to parse AoC Day 8's randomized seven segment display
        strings. The algorithm was somewhat worked out on paper and then
        just implemented here. There's probably a more efficient way to
        do this, but this seemed like the most obvious.

        Arguments
            encodedEntities - The list of segment values from 0-9 (in no
                                particular order) to extrapolate the decode
                                map from.
    '''
    def __init__(self, encodedEntities: list[str]):
        self.decodeMap = self.genDecodeMap(encodedEntities)

    def genDecodeMap(self, encodedEntities: list[str]) -> dict[str, str]:
        # start by finding our known maps (1, 4, 7, 8)
        mapDict = dict()
        restToEval = list()
        for entity in encodedEntities:
            if len(entity) == 2:
                 mapDict['1'] = set(list(entity))
            elif len(entity) == 4:
                mapDict['4'] = set(list(entity))
            elif len(entity) == 3:
                mapDict['7'] = set(list(entity))
            elif len(entity) == 7:
                mapDict['8'] = set(list(entity))
            else:
                restToEval.append(set(list(entity)))

        # All elements in restToEval contain only seg 'g'
        aSet = mapDict['7'].difference(mapDict['1'])
        curSet = mapDict['8']
        for elem in restToEval:
            curSet = curSet.intersection(elem)
        gSet = curSet.difference(aSet)

        # And we use that to find the value 9 from 7 U 4
        mapDict['9'] = mapDict['7'].union(mapDict['4']).union(gSet)        

        # 6 can be found through abdeg
        abdegSet = mapDict['8'].difference(mapDict['7']).union(aSet)
        for entity in restToEval:
            if abdegSet.issubset(entity):
                mapDict['6'] = entity

        # And five follows from acquiring 6
        cSet = mapDict['8'].difference(mapDict['6'])
        mapDict['5'] = mapDict['9'].difference(cSet)

        # Then the final three (0, 2, 3) can be found through the
        # segments discovered above
        leftoverEval = list()
        for entity in restToEval:
            if entity not in mapDict.values():
                leftoverEval.append(entity)
        for entity in leftoverEval:
            if len(mapDict['8'].difference(entity)) == 1:
                mapDict['0'] = entity
            elif len(mapDict['8'].difference(entity).intersection(mapDict['1'])) == 0:
                mapDict['3'] = entity
            else:
                mapDict['2'] = entity

        # We can't use sets as entries for the reverse dict, so we convert
        # them into sorted strings
        # You can use mapDict to map forward and then just randomize the values, but that's
        # unnecessary for this day's problem
        revLookupDict = {"".join(sorted(list(val))):key for key, val in mapDict.items()}

        return revLookupDict

    def segToInt(self, segStrList: list[str]) -> int:
        '''
            Performs decoding by a reverse lookup map.

            Arguments
                segStrList - The segment display strings that represent an integer.

            Returns
                int - The value in its base 10 form.
        '''
        return int("".join([self.decodeMap["".join(sorted(strElem))] for strElem in segStrList]))

if __name__ == "__main__":
    # prepare env for p1
    inFile = "./2021/Day08/input"

    # execute algo for p1
    sol1 = countP1Segments(inFile, [2, 4, 3, 7])
    print("The answer to part 1 is {}".format(sol1))

    # and now for p2
    p2Sum = 0
    with open(inFile, 'r') as toParse:
        curLine = toParse.readline()
        while curLine:
            leftToks, rightToks = [tokGroup.strip().split(" ") for tokGroup in curLine.strip().split("|")]
            decoder = SevenSegmentParser(leftToks)
            p2Sum += decoder.segToInt(rightToks)
            curLine = toParse.readline()
    print("The answer to part 2 is {}".format(p2Sum))