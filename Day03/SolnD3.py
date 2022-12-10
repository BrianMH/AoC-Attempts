###############################################################
#   Soln for P1 of Day 3 for AoC
#
# Problem:
#     Given a string of size 2N with only one shared character,
#     return the sum of the priorities of all shared elements
#     in each half strings (That is, the element that is present
#     in both the first N characters and the last N characters).
#     Priority is evaluated as (a-z) => (1-26) + (A-Z) => (27-52).
###############################################################
# helper func for evaluating priorities at the end
from functools import reduce


def evalPriority(charTP: str) -> int:
    if charTP.isupper():
        return ord(charTP) - ord('A') + 27
    else:
        return ord(charTP) - ord('a') + 1

# Returns the list of repeated characters in every half-string given
def p1Soln(inFile: str) -> list[str]:
    dups = list()

    with open(inFile, 'r') as strStream:
        curLine = strStream.readline()[:-1]
        while curLine:
            # process half strings to find the duplicate using hash table
            charIsPres = dict()
            for letter in curLine[:int(len(curLine)/2)]:
                charIsPres[letter] = True
            for letter in curLine[int(len(curLine)/2):]:
                if charIsPres.get(letter, False):
                    dups.append(letter)
                    break
            
            # then process the next
            curLine = strStream.readline()[:-1]

    return dups

###############################################################
#   Soln for P2 of Day 3 for AoC
#
# Problem:
#     Given a string of size 2N with only one shared character,
#     return the sum of the priorities of all shared elements
#     in each set of three strings. Priority remains the same here.
###############################################################
def p2Soln(inFile: str) -> list[str]:
    dups = list()

    with open(inFile, 'r') as strStream:
        line1, line2, line3 = [strStream.readline()[:-1] for _ in range(3)]

        while line1 or line2 or line3:
            # process first two counters and iterate on third to find
            # the right value
            charIsPresL1 = dict()
            charIsPresL2 = dict()
            for letter in line1:
                charIsPresL1[letter] = True
            for letter in line2:
                charIsPresL2[letter] = True
            for letter in line3:
                if charIsPresL1.get(letter, False) and charIsPresL2.get(letter, False):
                    dups.append(letter)
                    break

            line1, line2, line3 = [strStream.readline()[:-1] for _ in range(3)]

    return dups

if __name__ == "__main__":
    # Set up space for P1
    inFile = "./Day3/input"

    # Evaluate P1
    soln1 = p1Soln(inFile)
    print("Sum of priorities of values for part 1 is {}".format(reduce(lambda x, y:x + evalPriority(y), soln1, 0)))

    # Evaluate P2
    soln2 = p2Soln(inFile)
    print("Sum of priorities of values for part 2 is {}".format(reduce(lambda x, y:x + evalPriority(y), soln2, 0)))