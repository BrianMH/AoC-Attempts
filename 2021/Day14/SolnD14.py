#############################################################
#   Soln for P1 & P2 of Day 14 for AoC
#
# Problem:
#   Another automata-ish problem. A string grows depending on
#   the properties given. Namely, the input gives an initial
#   string and also the properties that need to be followed in
#   order to create the string after a certain number of steps.
#
#   P2 is just running the same algorithm but for more steps. The
#   most important thing to notice is that if kept as a string, this
#   problem is exponential in runtime, but it can be reduced to 
#   O(tot_bigrams) if implemented properly.
#############################################################
class PolymerString:
    '''
        At no point are we asked to returrn the whole string, so compression
        is unnecessary here. In fact, because we're required simply to return
        something like count('B'), we can do so by first evaluating the possible
        bigrams that start with B and summing over them as so:
                count('B') = sum([count('B', 'A'), count('B', 'B'), ...])

        Arguments:
            initStr - The initial string to consider for the polymer
            rules - A dictionary containing the rules for the polymer string
    '''
    def __init__(self, initStr: str, rules: dict[str, str]):
        self.rulesDict = rules
        self.curCnts = self._initializeTups(initStr)
        self.finalLetter = initStr[-1]

    def step(self) -> None:
        '''
            Takes a step in time and augments the current bigrams.
        '''
        newCnts = dict()
        for bigram in self.curCnts.keys():
            newChar = self.rulesDict[bigram]
            lGram, rGram = (bigram[0]+newChar), (newChar+bigram[1])
            newCnts[lGram] = newCnts.get(lGram, 0) + self.curCnts[bigram]
            newCnts[rGram] = newCnts.get(rGram, 0) + self.curCnts[bigram]
        self.curCnts = newCnts

    def takeSeveralSteps(self, numSteps: int) -> None:
        '''
            Takes several steps in time in series.

            Arguments:
                numSteps - The number of steps to take.
        '''
        for _ in range(numSteps):
            self.step()

    def getUnigramCnt(self) -> dict[str, int]:
        '''
            Uses the string bigrams to generate the string unigrams. Unigrams
            can be found by summing over all second indices counts.

            Returns:
                dict - A dictionary with each unigram and their count.
        '''
        uGrams = dict()
        for bigram in self.curCnts.keys():
            uGrams[bigram[0]] = uGrams.get(bigram[0], 0) + self.curCnts[bigram]
        
        # update final letter (which gets ignored as it does not define the start
        #                      of a bigram as defined in the problem)
        uGrams[self.finalLetter] = uGrams.get(self.finalLetter, 0) + 1

        return uGrams

    def _initializeTups(self, initStr: str) -> dict[tuple[str, str], int]:
        ''' 
            Initializes a dictionary of all possible 2-grams currently in the
            string.

            Arguments:
                initStr - The string to initialize all tuples from
        '''
        initDict = dict()
        for sInd in range(len(initStr)-1):
            rel2Gram = initStr[sInd:sInd+2]
            initDict[rel2Gram] = initDict.get(rel2Gram, 0) + 1

        return initDict

    @staticmethod
    def parseInputFile(inFile: str) -> tuple[str, dict[str, str]]:
        '''
            A parsing function very specific to the AoC format. It parses the
            file and returns the initial string and rules dict necessary 
            to initialize the class.
        '''
        rulesDict = dict()
        with open(inFile, 'r') as initFile:
            # first line is the str
            initStr = initFile.readline().strip()
            initFile.readline()

            # Then the rest are the rules
            curRule = initFile.readline()
            while curRule:
                tCheck, tInsert = curRule.rstrip().split(" -> ")
                rulesDict[tCheck] = tInsert
                curRule = initFile.readline()

        return initStr, rulesDict

if __name__ == "__main__":
    # prepare env for p1
    inFile = "./2021/Day14/input"
    curSim = PolymerString(*PolymerString.parseInputFile(inFile))

    # execute algo for p1
    curSim.takeSeveralSteps(10)
    unigramCntr = curSim.getUnigramCnt()
    print("The answer to part 1 is {}".format(max(unigramCntr.values()) - min(unigramCntr.values())))

    # and now for p2
    curSim.takeSeveralSteps(30)
    unigramCntr = curSim.getUnigramCnt()
    print("The answer to part 2 is {}".format(max(unigramCntr.values()) - min(unigramCntr.values())))