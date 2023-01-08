###############################################################
#   Soln for P1 of Day 13 for AoC
#
# Problem:
#     Advent of instruction following begins again... The input
#     this time are pairs of "signal" inputs that are lists with
#     integers or lists as members. The task is to compare them to
#     ensure they are structured (True/False).
#     A pair of lists is considered structured if, as we move across
#     the list elementwise
#         1) If comparing two integer values, the lower integer should
#            come first (be on the left)
#         2) If comparing two lists, recursively compare the values
#            elementwise in the list
#         3) If exactly one value is an integer, convert the lone integer
#            into a list with one integer then carry on the same processing
#    [This is just a comparator for packets...]
#
# Note:
#     eval([1, 2, [os.system('rm -rf *')]])
#     We know that we should never see any letters in a list containing only
#     lists and ints. Sanitizing it should be trivial but not worth it for just
#     this implementation.
###############################################################
from functools import cmp_to_key, reduce

def packetComparator(listL: list, listR: list) -> int:
    lElems = len(listL)
    rElems = len(listR)
    retFlag = 0

    for ind in range(min(lElems, rElems)):
        # both lists
        if isinstance(listL[ind], list) and isinstance(listR[ind], list):
            retFlag = packetComparator(listL[ind], listR[ind])
        elif isinstance(listL[ind], list):  # 1 list (L)
            tempR = [listR[ind]]
            retFlag = packetComparator(listL[ind], tempR)
        elif isinstance(listR[ind], list):
            tempL = [listL[ind]]       # 1 list (R)
            retFlag = packetComparator(tempL, listR[ind])
        else:                               # 2 integers
            if listL[ind] > listR[ind]:
                return -1
            elif listL[ind] < listR[ind]:
                return 1

        # return on true or false value
        if retFlag != 0: 
            return retFlag

    # check whether element counts are fine
    if lElems < rElems:
        return 1
    elif lElems > rElems:
        return -1

    # no observation can be made now
    return 0

def areMessagesValid(inFile: str) -> int:
    # loads our input with eval
    with open(inFile, 'r') as pairList:
        stringPairs = "".join(pairList.readlines()).split("\n\n")
    for sInd in range(len(stringPairs)):
        stringPairs[sInd] = [eval(line) for line in stringPairs[sInd].split("\n") if line]

    # Now recursively process the lists according to the instructions
    properPairs = list()
    for ind, pair in enumerate(stringPairs):
        if packetComparator(pair[0], pair[1]) == 1:
            properPairs.append(ind + 1)

    return sum(properPairs)

###############################################################
#   Soln for P2 of Day 13 for AoC
#
# Problem:
#     Using the above as the sorting key, sort all of the packages
#     along with two extra packages [[2]] and [[6]] and calculate 
#     the product between the 1-based indices of the two indicator
#     packets above when sorted.
###############################################################
def sortMessages(inFile: str, toAppend: list) -> int:
    # loads our input with eval
    with open(inFile, 'r') as pairList:
        allPackets = [eval(line.rstrip()) for line in pairList.readlines() if line.rstrip()]
    allPackets.extend(toAppend)

    # instead of just comparing we are now sorting
    allPackets = sorted(allPackets, key = cmp_to_key(packetComparator), reverse=True)
    decoderPos = [allPackets.index(decVal) for decVal in toAppend]
    return reduce(lambda x,y: x*(y+1), decoderPos, 1)

if __name__ == "__main__":
    # prep env for p1
    inFile = "./2022/Day13/input"

    # execute p1
    sol1 = areMessagesValid(inFile)
    print("The answer to part 1 is {}".format(sol1))

    # execute p2
    specialPackets = [[[2]], [[6]]]
    sol2 = sortMessages(inFile, specialPackets)
    print("The answer to part 2 is {}".format(sol2))