#############################################################
#   Soln for P1 of Day 1 for AoC
#
# Problem:
#     Find the number of times the number increased since the last.
#     Seems fairly straightforward.
#############################################################
def parseNums(inFile: str) -> list[int]:
    with open(inFile, 'r') as inNums:
        strNums = inNums.readlines()
    return [int(num.rstrip()) for num in strNums if num.rstrip()]

def countGreaterIndicator(nums: list[int]) -> int:
    return sum([nums[i] > nums[i-1] for i in range(1, len(nums))])

#############################################################
#   Soln for P2 of Day 1 for AoC
#
# Problem:
#     The same as above except now using a sliding window of
#     three numbers as the comparison
#############################################################
def countGreaterThreeTuples(nums: list[int]) -> int:
    return sum([sum(nums[i:i+3]) > sum(nums[i-1:i+2]) for i in range(1, len(nums)-2)])

if __name__ == "__main__":
    # prepare env for p1
    inFile = "./2021/Day01/input"

    # execute algo for p1
    numList = parseNums(inFile)
    sol1 = countGreaterIndicator(numList)
    print("The answer to part 1 is {}".format(sol1))

    # and now for p2
    sol2 = countGreaterThreeTuples(numList)
    print("The answer to part 2 is {}".format(sol2))