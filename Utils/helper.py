# helper imports
from typing import Callable, Optional
from datetime import datetime, timezone, timedelta # time tab-keeping
from os import makedirs, getcwd, path # directory creation
from functools import partial
import selenium.webdriver # used to grab active session cookies
import argparse # used to parse arguments
import requests # performs input check and cookie passing during POST

############################### CONSTANTS #####################################
# Helper file consts
class FileConsts:
    INPUT_PATH = "https://adventofcode.com/{}/day/{}/input"
    DIR_PATH = "{}/Day{}"
    PY_FILENAME = "SolnD{}.py"
    PY_TEMPLATE = "./Utils/template.txt"

# Typing constant that represents possible changes
#    bool  - Whether the change can be performed without user permission
#     str  - The file to be created/changed
# Callable - A function that returns the string object to write to file 
FileWriteTemplate = tuple[bool, str, Optional[Callable[[], str]]]

# Color consts (for verbose output)
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

############################# PARSER RELATED ##################################

def initializeParser(relTimeDelta: int = -5) -> tuple[argparse.ArgumentParser, datetime]:
    '''
        Prepares the parser for this specific usage case. Takes in an argument that allows for
        custom update times, but it will likely not change any time soon.

        Arguments:
            relTimeDelta - Represents the _hour_ shift to apply from UTC for the time tracking.

        Returns:
            ArgumentParser - Used to parse all arguments.
            datetime       - Contains the relevant date information for the application.
    '''
    # Parsing Consts
    PROG_DESCRIPTOR = r"Creates a {YEAR}/{DAY} directory along with the default " +\
                      r"inputs (a simple python file and its input). If the input " +\
                      r"download results in a failure, a flag can be used to create " +\
                      r"a dummy file in the same directory instead."
    POST_MSG = r"Running this script without an argument during December defaults to " +\
               r"grabbing the file for the current day, if possible."
    curDate = datetime.now(tz = timezone(timedelta(hours = -5), name = "EST"))
    curYear, curDay = curDate.year, curDate.day

    # parser
    parser = argparse.ArgumentParser(description = PROG_DESCRIPTOR, epilog = POST_MSG)
    parser.add_argument("-A", "--all", action = 'store_true', help = "Downloads all days (ignores --day flag)")
    parser.add_argument("-v", "--verbose", action = 'store_true', help = "Turns on verbose output.")
    parser.add_argument("-d", "--use-dummy", action = 'store_true', help = "If input retrieval fails, default to an empty input dummy.")
    parser.add_argument("-y", dest = "defaultYes", action = "store_true", help = "Default to yes action for overwriting requests.")
    yHelperStr = "The year to consider when creating the AoC directory."
    parser.add_argument("--year", default = curYear, type = int, help = yHelperStr)
    dHelperStr = "The day for the specified year for which to create a folder for. Supports ranges using '-' and multiple arguments"
    parser.add_argument("--day", nargs = '+', default = curDay, type = str, help = dHelperStr, metavar = ('D1-D2', 'D2-D3'))
    parser.add_argument("-o", nargs = 1, dest = "pPath",  default = ".", help = "Specifies a custom output directory.", metavar = './path/to/outDir')

    return parser, curDate

def combineRanges(rangeList: list[str], filterPred: Callable[[], bool] = lambda x: True) -> list[int]:
    '''
        Takes in the expected list of arguments from the parser and turns them into a valid sequence
        that can be used to acquire the desired files.

        Arguments:
            rangeList - A list of strings representing either ranges or desired days

        Returns:
            list[int] - Containing all the desired days in an ordered fashion.
    '''
    finalSet = set()
    for elem in rangeList:
        if len(elem.split("-")) == 1:
            finalSet.add(int(elem))
        else:
            begRange, endRange = [int(val) for val in elem.split("-")]
            finalSet.update(list(range(begRange, endRange + 1)))

    return sorted([elem for elem in finalSet if filterPred(elem)])

############################# FILE MANIPULATION ###############################

def performWriteOps(toWrite: list[FileWriteTemplate], userSpecs: list[bool], activeSession: dict, * , verbose: bool = False) -> int:
    '''
        Performs all of the relevant writing operations for the program. This takes into account any existing
        files and overwrites them pre-emptively. Writing process can be verbose if necessary.

        Arguments:
            toWrite - A list representing everything that needs to be written to disk.
            cWrites - ([Un]confirmed) writes that require file deletion (if requested) in order to write.
            userSpecs - The user's choice for overwriting elements in cWrites
            verbose - Turns on verbose output for the writing function.

        Returns:
            A 1 if the writing process succesfully finishes (which it should unless an exception is raised)
    '''
    # Go through every change one-by-one with verbosity if requested
    collisionInd = 0
    for writeOp in toWrite:
        dirProc = writeOp[0]
        files = writeOp[1:]

        # First create necessary directories
        if not dirProc[0]:
            makedirs(dirProc[1], exist_ok = False)

        # Then write the files to place
        for fObj in files:
            fExists, fDir, fDataFunc = fObj
            fDat = fDataFunc(userCookie = activeSession)

            if fExists and userSpecs[collisionInd]:
                print("Overwriting file: {}".format(fDir)) if verbose else None
                with open(fDir, 'w') as outFile:
                    outFile.write(fDat)
            elif fExists:
                print("Ignoring file: {}".format(fDir)) if verbose else None
            else:
                print("Writing file: {}".format(fDir)) if verbose else None
                with open(fDir, 'w') as outFile:
                    outFile.write(fDat)
            collisionInd += int(fExists)

    return 1

def planDirectoryStructure(prePath: str, year: int, day: int) -> tuple[FileWriteTemplate, ...]:
    """
        Prepares all the operations for execution on the main thread.

        Arguments:
            prePath - The desired prefix for the path in which the files will be written.
            year    - Used to create the proper time-based directory structure. 
            day     - Like above, also used to create the proper time-based structure.

        Returns:
            tuple[bool, FileWriteTemplate, ...] - Represents whether the directory must be created
                                                  and then a series of proposed file creations along
                                                  with an indicator if the file exists already.
    """
    # First check for existences of subcomponents
    paddedDay = "{:02d}".format(day)
    fName = FileConsts.PY_FILENAME.format(day)
    dirPath = prePath + "/" + FileConsts.DIR_PATH.format(year, paddedDay)
    dirFlag = path.isdir(dirPath)
    
    ifWritePath = dirPath + "/input"
    templWritePath = dirPath + "/" + fName
    tFFlag = path.isfile(templWritePath)
    iFFlag = path.isfile(ifWritePath)

    # Create function that will output the desired string to write
    fArgs = {"day":day, "inFile":dirPath+"/input"}
    wFunc = partial(readFile, FileConsts.PY_TEMPLATE, **fArgs)

    # And now do the same for the input file
    inputPath = FileConsts.INPUT_PATH.format(year, day)
    ifFunc = partial(readFile, inputPath)

    return ((dirFlag, dirPath, None), (iFFlag, ifWritePath, ifFunc), (tFFlag, templWritePath, wFunc))

def readFile(filePath: str, *, userCookie: dict = {}, **formatDict) -> str:
    """
        Reads a designated file from either a URL source or a local source.

        Aruments:
            filePath - The file origin to read from.
            userCookie - Contains the active user session (unused if unneeded)
            formatDict - Used to format a string with kwargs if necessary.

        Returns:
            A string representing the whole file. Since most AoC files are
            fairly small, this should perform sufficiently well. A proper
            implementation would perhaps perform file writing by chunks
            so as to prevent any issues with larger files.
    """
    if filePath.startswith("https://"):
        resp = requests.post(filePath, cookies = userCookie)
        if resp.status_code == 200:
            templToWrite = resp.text
        else:
            raise Exception("Error occured during connection to {}.".format(filePath))
    else:
        with open(filePath, 'r') as templFile:
            templToWrite = templFile.read().format(**formatDict)
    
    return templToWrite

######################## WEBDRIVER COOKIE GRABBER #############################

def grabCookieFromFirefox(profilePath: str = "") -> dict[str, str]:
    '''
        Uses the selenium webdriver to grab the active cookie for firefox.

        Arguments:
            profilePath - The path to the desired profile. If empty, attempts to
                          deduce the active profile via the profile.ini file.

        Returns:
            dict[str, str] - A dictionary of the format {"sessionid":$SESS_ID}
    '''
    # deduce path from profiles.ini
    if not profilePath:
        defProfPath = path.expandvars('$HOME/.mozilla/firefox/profiles.ini')
        with open(defProfPath, 'r') as profFile:
            curLine = profFile.readline()
            while not curLine.startswith("Default="):
                curLine = profFile.readline()
            profilePath = path.expandvars('$HOME/.mozilla/firefox/') + curLine.rstrip().split("=")[1] + "/"
    
    # and now open a selenium session to grab the cookie using the profile
    fProf = selenium.webdriver.FirefoxProfile(profilePath)
    fDOps = selenium.webdriver.firefox.options.Options()
    fDOps.headless = True
    fDriver = selenium.webdriver.Firefox(firefox_profile = fProf, options = fDOps)
    fDriver.get("https://adventofcode.com/")
    sCookie = fDriver.get_cookie('session') 
    fDriver.quit()

    return {'session':sCookie['value']}