#!/usr/bin/env python
#############################################################
#   yearPopulator.py
#
#   Used to create the directory for the year, and (if it exists) can
#   also creates all the 25 sub-directories required to complete the
#   problems along with their input files if possible.
#
#   This can also be used in order to only generate the files for
#   a single day by specifying the proper arguments for that. On December,
#   this function also can immediately create the templated directory
#   automatically.
#
# TODO: Save token to cache and rerun only when current session is dead.
#############################################################
from helper import bcolors, FileWriteTemplate, planDirectoryStructure, performWriteOps, \
                   initializeParser, combineRanges, grabCookieFromFirefox
from argparse import Namespace
from os import get_terminal_size
import sys

def retreiveUserPreferences(filesToPrompt: list[FileWriteTemplate], * , oPad: int = 10) -> list[bool]:
    '''
        Used to ask the user about the desired action on files that exist.

        Arguments:
            filesToPrompt - A collection of all files that require user input.

        Returns:
            list[bool] - A list representing a collection of the user's choices.
    '''
    userInputs = list()
    while not userInputs:
        # First prompt for user inputs
        for fileProc in filesToPrompt:
            print("Overwrite " + bcolors.BOLD + \
                  "{path: >{width}}".format(path = fileProc[1], width = oPad) + \
                  bcolors.ENDC + " (y/n)? ", end = " ")
            curInput = ""
            while curInput not in ("y", "n"):
                curInput = input()
            userInputs.append(True if curInput=="y" else False)

        # Then confirm all changes
        print("\n" + bcolors.OKBLUE + bcolors.BOLD + "User-specified changes: " + bcolors.ENDC)
        for fileInd, fileProc in enumerate(filesToPrompt):
            action = bcolors.WARNING + "Overwriting" + bcolors.ENDC if userInputs[fileInd] else "Ignoring"
            print(action + " " + bcolors.BOLD + \
                  "{path: >{width}}".format(path = fileProc[1], width = oPad) + bcolors.ENDC)
        print("Confirm? (y/n)", end = " ")
        curInput = ""
        while curInput not in ("y", "n"):
            curInput = input()
        if curInput == "n":
            userInputs = list()

    return userInputs

def fileOpCoordinator(parsedArgs: Namespace) -> int:
    '''
        Pretty much performs all of the coordination between planning and writing.
        Also handles pretty much all of the verbose output.

        Arguments:
            parsedArgs - The namespace returned by a parser with the relevant arguments.

        Returns:
            int - A value representing either the success (1) or failure (otherwise)
    '''

    # first grab relevant arguments neede to create the plan
    if parsedArgs.all:
        parsedArgs.day = ["1-25"]
    relDays = combineRanges(parsedArgs.day, lambda x: 1 <= x <= 25)

    # If no session passed, automatically grab it from the browser
    print("Grabbing current AoC session token...", end = " ")
    sys.stdout.flush()
    curCookie = grabCookieFromFirefox()
    print("Done.")

    # Now create the procedure list
    procList = list()
    for day in relDays:
        procList.append(planDirectoryStructure(parsedArgs.pPath, parsedArgs.year, day))

    # Create a template and show the user the potential changes to be made
    numCols = get_terminal_size().columns // 2
    rTermWidth = 10
    lTermWidth = max(0, numCols - rTermWidth)
    print(bcolors.WARNING + "Files to be created:" + bcolors.ENDC + "\n" + "="*lTermWidth)
    print(bcolors.BOLD + "{mL: <{lW}}    {mR: <{rW}}".format(
        mL = "File:", mR = "Exists:", lW = lTermWidth, rW = rTermWidth) + bcolors.ENDC)
    boolColorWrapper = lambda boolVal: bcolors.WARNING + str(boolVal) + bcolors.ENDC if boolVal else \
                                       bcolors.OKGREEN + str(boolVal) + bcolors.ENDC

    collisions = list()
    valid = list()
    for change in procList:
        inFileProc, templFileProc = change[1], change[2]

        # keep track of collisions
        collisions.append(inFileProc) if inFileProc[0] else valid.append(inFileProc)
        collisions.append(templFileProc) if templFileProc[0] else valid.append(templFileProc)
        
        # input file output
        print("{inFile: <{lTermWidth}}    {boolVal: <{rTermWidth}}".format(
                inFile = inFileProc[1], boolVal =  boolColorWrapper(inFileProc[0]),
                lTermWidth = lTermWidth, rTermWidth = rTermWidth))

        # template file output
        print("{inFile: <{lTermWidth}}    {boolVal: <{rTermWidth}}".format(
                inFile = templFileProc[1], boolVal = boolColorWrapper(templFileProc[0]),
                lTermWidth = lTermWidth, rTermWidth = rTermWidth))
    
    # Deal with collisions by prompting the user
    userFinArg = [False] * len(collisions)
    if not parsedArgs.defaultYes and collisions:
        print(bcolors.BOLD + "\nExisting files found. " + bcolors.ENDC + \
                "Would you like to review each overwrite individually (i) or collectively accept them all (y/n)?", end=" ")
        userInput = ""
        while userInput not in ['i', 'y', 'n']:
            userInput = input()

        if userInput == "i":
            userFinArg = retreiveUserPreferences(collisions)
        elif userInput == 'y':
            userFinArg = [True] * len(collisions)

    # Finally write any necessary files to disk along with the final prompt.
    return performWriteOps(procList, userFinArg, curCookie, verbose = parsedArgs.verbose)

if __name__ == "__main__":
    parser, curDate = initializeParser()
    curYear, curMonth, curDay = curDate.year, curDate.month, curDate.day

    # Show information if not December
    if len(sys.argv) == 1 and curMonth != 12:
        print(bcolors.WARNING + "\t Note: AoC is not currently not active. Automatic file creation failed. Manually provide arguments to acquire files!" + bcolors.ENDC)
        parser.parse_args(['-h'])
        sys.exit(1)
    
    # Proceed to evaluate on args otherwise
    pArgs = parser.parse_args()
    try:    
        if len(sys.argv) == 1:
            print(bcolors.WARNING + "\t Attempting to acquire AoC problem for year {} and day {}".format(curYear, curDay) + bcolors.ENDC)
        evalResponse = fileOpCoordinator(pArgs)
        print(bcolors.OKGREEN + "\nFiles created succesfully." + bcolors.ENDC)
    except Exception as e:
        print("Exception encountered during writing: {}".format(e.args[0]))
        raise e

    sys.exit(evalResponse)