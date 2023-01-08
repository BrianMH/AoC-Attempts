###############################################################
#   Soln for P1 & P2 of Day 20 for AoC
#
# Problem:
#     We get an input of numbers corresponding to an encrypted
#     file that should be re-arranged based on the number that
#     is read (move number X spaces to the right).
#     The second part just makes us rerun the first part multiple
#     times so the original function was slightly modified
#     to accommodate that.
###############################################################
# makes input unique if necessary
def parseInput(inFile: str) -> list[tuple[int, int]]:
    inArr = list()
    numCntr = dict()

    with open(inFile, 'r') as inNums:
        parsedVals = [int(val.strip()) for val in inNums.readlines()]

    for val in parsedVals:
        numCntr[val] = numCntr.get(val, 0) + 1
        inArr.append((val, numCntr[val]))

    return inArr

def performMixing(inArr: list, numMixes: int = 1) -> tuple[int, list]:
    outArr = inArr.copy()

    for _ in range(numMixes):
        offset = 0

        for elemToParse in inArr:
            itemInd = outArr.index(elemToParse)

            # set it up to take minimum number of swaps
            direction = 1
            numSwapsToMake = elemToParse[0]%(len(inArr)-1)
            if numSwapsToMake > ((len(inArr)-1) // 2):
                direction = -1
                numSwapsToMake -= (len(inArr)-1)

            for swapInd in range(0, numSwapsToMake, direction):
                lInd, rInd = (itemInd+swapInd)%len(inArr), (itemInd+swapInd+direction)%len(inArr)
                outArr[lInd], outArr[rInd] = outArr[rInd], outArr[lInd]

                if direction == -1 and lInd+rInd == 1:
                    offset += 1
                elif direction == 1 and lInd+rInd == 1:
                    offset -= 1

        # adjust output based on offsets (edge cases)
        outArr = outArr[offset:] + outArr[:offset]

    # now perform decoding
    zInd = outArr.index((0, 1))
    return outArr[(zInd+1000)%len(outArr)][0] + outArr[(zInd+2000)%len(outArr)][0] + outArr[(zInd+3000)%len(outArr)][0], outArr

if __name__ == "__main__":
    # parepare env for p1
    inFile = './2022/Day20/input'
    inArr = parseInput(inFile)

    # execute algo p1
    sol1, _ = performMixing(inArr)
    print("The answer to part 1 is {}".format(sol1))

    # execute algo p2 (it's the same but done again and again)
    NUM_MIXING = 10
    DECRYPT_KEY = 811589153
    newInArr = [(val*DECRYPT_KEY, numCount) for val, numCount in inArr]
    sol2, _ = performMixing(newInArr, NUM_MIXING)
    print("The answer to part 2 is {}".format(sol2))