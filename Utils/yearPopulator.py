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
#############################################################
from os import makedirs, getcwd, path
from datetime import datetime, timezone, timedelta
import argparse
import sys

# File consts
INPUT_PATH = "https://adventofcode.com/{}/day/{}/input"
DIR_PATH = "./{}/Day{}/"
PY_FILENAME = "SolnD{}.py"
PY_TEMPLATE = "./Utils/template.txt"

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

'''
    createDayDirectory

    Creates the relevant directory along with the typical files it includes. This function
    returns a boolean value representing whether a new directory and set of files were
    created.
'''
def createDirectoryStructure(year: int, day: int, * , verbose: bool = False) -> bool:
    # First check for existence
    paddedDay = "{:02d}".format(day)
    fName = DIR_PATH.format(year, paddedDay) + PY_FILENAME.format(day)

    # And then proceed to acquire the input and create the template in place
    inputWebPath = INPUT_PATH.format(year, day)

    with open(PY_TEMPLATE, 'r') as templFile:
        templToUse = templFile.read().format(day = day, inFile = fName)

    return True

if __name__ == "__main__":
    # Parsing Consts
    PROG_DESCRIPTOR = r"Creates a {YEAR}/{DAY} directory along with the default " +\
                      r"inputs (a simple python file and its input). If the input " +\
                      r"download results in a failure, a flag can be used to create " +\
                      r"a dummy file in the same directory instead."
    POST_MSG = r"Running this script without an argument during December defaults to " +\
               r"grabbing the file for the current day, if possible."
    curDate = datetime.now(tz = timezone(timedelta(hours = -5), name = "EST"))
    curYear, curMonth, curDay = curDate.year, curDate.month, curDate.day

    # parser
    parser = argparse.ArgumentParser(description = PROG_DESCRIPTOR, epilog = POST_MSG)
    parser.add_argument("-A", "--all", action = 'store_true', help = "Downloads all days (ignores --day flag)")
    parser.add_argument("-v", "--verbose", action = 'store_true', help = "Turns on verbose output.")
    parser.add_argument("-d", "--use-dummy", action = 'store_true', help = "If input retrieval fails, default to an empty input dummy.")
    yHelperStr = "The year to consider when creating the AoC directory."
    parser.add_argument("--year", default = curYear, type = int, help = yHelperStr)
    dHelperStr = "The day for the specified year for which to create a folder for. Supports ranges using '-' and multiple arguments"
    parser.add_argument("--day", nargs = '+', default = curDay, type = int, help = dHelperStr, metavar = ('D1-D2', 'D2-D3'))
    parser.add_argument("-o", nargs = 1, default = "./", help = "Specifies a custom output directory.", metavar = './path/to/outDir')

    # Show information if not December
    if len(sys.argv) == 1 and curMonth != 12:
        print(bcolors.WARNING + "\t Note: AoC is not currently not active. Automatic file creation failed. Manually provide arguments to acquire files!" + bcolors.ENDC)
        pArgs = parser.parse_args(['-h'])
        sys.exit(1)
    
    # Proceed to evaluate on args otherwise
    pArgs = parser.parse_args()
    try:    
        if len(sys.argv) == 1:
            print(bcolors.WARNING + "\t Attempting to acquire AoC problem for year {} and day {}".format(curYear, curDay))
        evalResponse = 1
    except:
        evalResponse = -1
    finally:
        # attempt to rollback incomplete changes
        pass

    sys.exit(evalResponse)