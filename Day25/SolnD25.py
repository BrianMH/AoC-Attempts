###############################################################
#   Soln for P1 of Day 25 for AoC
#
# Problem:
#     Pretty much just N-ary number representations. This is pretty
#     simple and wrapping backwards is easier since it's pretty much
#     a summation caried over to larger digits not in the right
#     digit value range.
################################################################
class BaseFive:
    def __init__(self, encoding: dict[str, int]):
        self.baseVal = 5 # This is set in stone for now
        self.decDict = encoding
        self.encDict = {val:key for (key, val) in encoding.items()}

        # grab max-value for looping
        self.maxEncVal = max(list(self.decDict.values()))

    def decodeString(self, inStr: str) -> int:
        curFactor = 1
        curVal = 0
        for char in inStr[::-1]:
            curVal += curFactor * self.decDict[char]
            curFactor *= self.baseVal
        return curVal
    
    def encodeInt(self, inVal: int) -> str:
        # First encode into normal base 5 with padding 0
        baseNList = [0] + self._origBaseEnc(inVal, self.baseVal)

        # Then using the known maximum, loop the values around to proper
        # values for return
        for elemInd in reversed(range(1, len(baseNList))):
            if baseNList[elemInd] > self.maxEncVal:
                baseNList[elemInd] -= self.baseVal
                baseNList[elemInd-1] += 1

        # remove padding 0 if unneeded
        if baseNList[0] == 0:
            baseNList = baseNList[1:]
            
        return "".join([self.encDict[curVal] for curVal in baseNList])
    
    '''
        Helper function that encodes a number into the non-shifted
        encoding. In this case, it would be the normal base N value
        with possible encoding values [0, 1, 2, ... , N-1]
    '''
    def _origBaseEnc(self, tEncode: int, baseVal: int) -> list[int]:
        encVals = list()
        curFactor = 1
        while (curFactor*baseVal) <= tEncode:
            curFactor *= baseVal

        # Begin encoding from largest digit
        while curFactor >= 1:
            encVals.append(tEncode//curFactor)
            tEncode %= curFactor
            curFactor //= baseVal
        
        if encVals:
            return encVals
        else:
            return [0]


if __name__ == "__main__":
    # Prepare env for p1
    inFile = "./Day25/input"
    encoding = {"=":-2, "-":-1, "0":0, "1":1, "2":2}
    b5Mod = BaseFive(encoding)

    sol1 = 0
    with open(inFile, 'r') as inNums:
        curLine = inNums.readline().rstrip()
        while curLine:
            sol1 += b5Mod.decodeString(curLine)
            curLine = inNums.readline().rstrip()
    print("Solution to part 1 is {}".format(b5Mod.encodeInt(sol1)))