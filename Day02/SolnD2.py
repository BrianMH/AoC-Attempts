###############################################################
#   Soln for P1 of Day 2 for AoC
#
# Problem:
#     Given an "encrypted" sequence of games that occur exactly
#     as stated, return the overall score of the games given the
#     following:
#     1) (A, B, C) = (X, Y, Z) = (Rock, Paper, Scissors)
#     2) Round_Score = Shape_Score + Round_Outcome .... where
#            Shape_Score => (Rock, Paper, Scissors) = (1, 2, 3)
#            Round_Outcome => (Win, Loss, Tie)      = (6, 0, 3)
###############################################################
# We can create a "fixture" for rock-paper-scissors that avoids all of the hard-coded nonsense within the method.
class RPSFixture():
    def __init__(self, winVal: int, lossVal: int, tieVal: int, shapeScores: dict[str, int], decryptionSchema: dict[str, str]):
        # Saved passed in values
        self.shapeScores = shapeScores
        self.decryptDict = decryptionSchema
        self.winVal = winVal
        self.lossVal = lossVal
        self.tieVal = tieVal

        # Create the winning combinations (tie is simply the same val and loss is handled by exception)
        self.winDict = {"A":"B", "B":"C", "C":"A"}

    def processMatchup(self, inA: str, inB: str) -> int:
        decryptedB = self.decryptDict[inB]
        if decryptedB == self.winDict[inA]:
            return self.shapeScores[decryptedB] + self.winVal
        elif decryptedB == inA:
            return self.shapeScores[decryptedB] + self.tieVal
        else:
            return self.shapeScores[decryptedB] + self.lossVal


def p1Soln(inFile: str, rpsFixture: RPSFixture) -> int:
    totScores = 0
    with open(inFile, 'r') as roundGuide:
        curRound = roundGuide.readline().strip().split()
        while curRound:
            # evaluate round and add to total score
            totScores += rpsFixture.processMatchup(curRound[0], curRound[1])
            curRound = roundGuide.readline().strip().split()

    return totScores

###############################################################
#   Soln for P2 of Day 2 for AoC
#
# Problem:
#     Given an "encrypted" sequence of games that occur exactly
#     as stated, return the overall score of the games given the
#     following:
#     1) (A, B, C) (Rock, Paper, Scissors)
#     2) (X, Y, Z) => Choose the shape needed to either win (Z),
#                     lose (X), or get a draw (Y)
#     3) Round_Score = Shape_Score + Round_Outcome .... where
#            Shape_Score => (Rock, Paper, Scissors) = (1, 2, 3)
#            Round_Outcome => (Win, Loss, Tie)      = (6, 0, 3)
###############################################################
# We modify the top class slightly to be applicable in this scenario
class CondRPSFixture():
    def __init__(self, winVal: int, lossVal: int, tieVal: int, shapeScores: dict[str, int], condDict: dict[str, str]):
        # Saved passed in values
        self.shapeScores = shapeScores
        self.condDict = condDict
        self.winVal = winVal
        self.lossVal = lossVal
        self.tieVal = tieVal

        # Create the winning combinations (tie is simply the same val and loss is handled by exception)
        self.winDict = {"A":"B", "B":"C", "C":"A"}
        self.loseDict = {"A":"C", "B":"A", "C":"B"}

    def processMatchup(self, inA: str, encryptedCond: str) -> int:
        if self.condDict[encryptedCond] == "W":
            return self.shapeScores[self.winDict[inA]] + self.winVal
        elif self.condDict[encryptedCond] == "D":
            return self.shapeScores[inA] + self.tieVal
        else:
            return self.shapeScores[self.loseDict[inA]] + self.lossVal

def p2Soln(inFile: str, rpsFixture: CondRPSFixture) -> int:
    totScores = 0
    with open(inFile, 'r') as roundGuide:
        curRound = roundGuide.readline().strip().split()
        while curRound:
            # evaluate round and add to total score
            totScores += rpsFixture.processMatchup(curRound[0], curRound[1])
            curRound = roundGuide.readline().strip().split()

    return totScores

if __name__ == "__main__":
    # Sets up the hard values for the first problem...
    inFile = "./Day02/input"
    shapeScores = {"A": 1, "B":2, "C":3}
    decryptDict = {"X":"A", "Y":"B", "Z":"C"}
    (winVal, lossVal, tieVal) = (6, 0, 3)
    prefixedRPSFixture = RPSFixture(winVal, lossVal, tieVal, shapeScores, decryptDict)

    # Evaluate P1
    soln1 = p1Soln(inFile, prefixedRPSFixture)
    print("The total score given by the method for part 1 is {}".format(soln1))

    # Sets up the fixture for the second half now
    condDict = {"X":"L", "Y":"D", "Z":"W"}
    condRPSFixture = CondRPSFixture(winVal, lossVal, tieVal, shapeScores, condDict)

    # Evaluate P2
    soln2 = p2Soln(inFile, condRPSFixture)
    print("The total score given by the method for part 2 is {}".format(soln2))