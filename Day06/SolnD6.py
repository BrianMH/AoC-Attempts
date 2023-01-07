###############################################################
#   Soln for P1 of Day 6 for AoC
#
# Problem:
#     Given an input consisting of random chars, identify the
#     index after which four consecutive unique characters have
#     been parsed.
###############################################################
# We use a sliding window to determine whether or not the predicate
# holds for the window. This should take O(N) either way due to the
# fixed string size
def p1Soln(inFile: str, substrLen: int) -> int:
    with open(inFile, 'r') as queriedStrings:
        curInd = substrLen
        query = queriedStrings.read(substrLen)

        while(True):
            # is cur substring's chars unique?
            if len(set(query)) == len(query):
                return curInd

            # otherwise keep looking
            curInd += 1
            query = query[1:] + queriedStrings.read(1)
    
    # This shouldn't be reached ever...
    return -1

if __name__ == "__main__":
    # Setup env for p1
    inFile = "./Day06/input"
    desiredSubstrLen = 4

    # Eval p1
    soln1 = p1Soln(inFile, desiredSubstrLen)
    print("Soluton for p1 is {}".format(soln1))

    # Eval p2 (in this case the solution is the same but with diff args)
    p2DesiredSubstrLen = 14
    soln2 = p1Soln(inFile, p2DesiredSubstrLen)
    print("Solution for p2 is {}".format(soln2))