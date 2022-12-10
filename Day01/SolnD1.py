#############################################################
#   Soln for P1 of Day 1 for AoC
#
# Problem:
#     Given an input "input" consisting of lines of pos. integers
#     double broken by space to indicate new people, how many
#     calories is the person with the most calories carrying?
#############################################################
def p1Soln(inFile: str) -> int:
    # We don't need to parse it all at once. We process it slowly
    # as the file is completely structured
    maxCals = 0
    curCalTotal = 0
    with open(inFile, 'r') as inCalList:
        curLine = inCalList.readline()
        while curLine:
            # reset value if newline is read
            if curLine == "\n":
                if curCalTotal > maxCals:
                    maxCals = curCalTotal
                curCalTotal = 0
            # otherwise just update value
            else:
                curCalTotal += int(curLine[:-1])

            curLine = inCalList.readline()

    return maxCals

#############################################################
#   Soln for P2 of Day 1 for AoC
#
# Problem:
#     Given an input "input" consisting of lines of pos. integers
#     double broken by space to indicate new people, how many
#     calories are the *THREE* top people who are carrying the
#     most calories carrying.
#
# Observation:
#     The simplest way to implement the difference would be to instead
#     create a min_heap designed to keep only the three top values
#     within it. In other words, if we see a value higher than the
#     lowest value of the min_heap with the desired top N elements,
#     we pop the value and add our larger one.
#############################################################
def p2Soln(inFile: str, N: int) -> list[int]:
    import heapq

    maxCals = list()
    curCalTotal = 0
    with open(inFile, 'r') as inCalList:
        curLine = inCalList.readline()
        while curLine:
            if curLine == "\n":
                # update heap if smaller than N automatically
                if len(maxCals) < N:
                    heapq.heappush(maxCals, curCalTotal)
                # or perform comparison once we reach desired size
                elif curCalTotal > maxCals[0]:
                    heapq.heapreplace(maxCals, curCalTotal)
                    
                curCalTotal = 0
            # otherwise just update value
            else:
                curCalTotal += int(curLine[:-1])

            curLine = inCalList.readline()

    return maxCals

if __name__ == "__main__":
    # Name of the file for part 1
    p1File = "./Day1/input"

    # Executes the first part of the problem
    sol1 = p1Soln(p1File)
    print("Solution for part 1 is: {}".format(sol1))

    # Executes the second part now. Sum of these values
    # is the answer
    numToKeep = 3
    sol2 = p2Soln(p1File, 3)
    print("Solution for part 2 is {}".format(sum(sol2)))