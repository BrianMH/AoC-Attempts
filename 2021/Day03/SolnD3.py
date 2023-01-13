#############################################################
#   Soln for P1 of Day 3 for AoC
#
# Problem:
#     Perform a bit concensus check along every bit of the set
#     of binary values given.
#     The solution is the product of the binary string given
#     and its inverse.
#############################################################
def parseBinaryList(inFile: str) -> list[str]:
    with open(inFile, 'r') as numList:
        return [list([int(digit) for digit in val]) for val in numList.read().rstrip().split()]

def performConcensusCheck(binList: list[list[int]]) -> str:
    '''
        Performs a concensus check for each bit present in the list.
        For example,
                        0b010101
                        0b000111
                        0b111111
        The binary value generated by the concensus for each bit would
        be              0b010111

        Arguments:
            binList - The list of binary values to parse

        Returns:
            str - The number extracted by the concensus (but in base 2)
    '''
    sumBin = [0] * len(binList[0])
    for val in binList:
        sumBin = [sbVal+vVal for sbVal, vVal in zip(sumBin, val)]
    
    # put answer back into binary
    return "".join(['1' if sbVal > (len(binList)//2) else '0' for sbVal in sumBin])

def calculateP1FromGamma(binVal: str) -> int:
    return int(binVal, 2) * int("".join(['0' if val=='1' else '1' for val in binVal]), 2)

#############################################################
#   Soln for P2 of Day 3 for AoC
#
# Problem:
#     Perform step-wise binary string filtering based on some
#     sort of concensus (least-present/most-present)
#############################################################
def stepwiseConcensusFiltering(binList: list[list[int]], mostPresent = True) -> str:
    '''
        Performs a concensus filtering step-wise from the most-significant bit
        to the least-significant bit. Can be designed to filter either the values
        with the concensus value or the non-concensus value.

        Arguments:
            binList - The values to filter down to a single value
            mostPresent - Whether to filter values not matching the concensus or the opposite. 

        Returns:
            str - The binary string left once there is only one string available.
    '''
    binCopy = binList.copy()
    curDigitInd = 0
    while len(binCopy) > 1:
        # Perform concensus
        cVal = 0
        for val in binCopy:
            cVal += val[curDigitInd]
        cVal = (1 if cVal >= len(binCopy)/2 else 0)
        if not mostPresent: # flip logic if needed
            cVal = 0 if cVal else 1

        # filter values
        binCopy = [val for val in binCopy if val[curDigitInd] == cVal]
        curDigitInd += 1

    return "".join(['1' if digit else '0' for digit in binCopy[0]])

if __name__ == "__main__":
    # prepare env for p1
    inFile = "./2021/Day03/input"
    binVals = parseBinaryList(inFile)

    # execute algo for p1
    sol1 = calculateP1FromGamma(performConcensusCheck(binVals))
    print("The answer to part 1 is {}".format(sol1))

    # and now for p2
    O2Rating = stepwiseConcensusFiltering(binVals)
    CO2Rating = stepwiseConcensusFiltering(binVals, mostPresent = False)
    sol2 = int(O2Rating, 2) * int(CO2Rating, 2)
    print("The answer to part 2 is {}".format(sol2))