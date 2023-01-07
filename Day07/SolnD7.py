###############################################################
#   Soln for P1 of Day 7 for AoC
#
# Problem:
#     Given a set of outputs based on cd and ls inputs, find the
#     total sum of the directory sizes for directories which have
#     AT MOST 100 000 bytes within them.
###############################################################
# Make a simple tree that records all of the data sies available.
# A node should contain the path of the current file and the data size
# will be given for all leaf nodes (as these would be the files).
# Directory sizes will be infered by moving through this tree after ingesting
# the directory data.
import typing
class Node:
    def __init__(self, filePath: str, dataSize: int = -1, children: typing.Optional[list] = None, isDir: bool = False):
        self.filePath = filePath
        self.fileSize = dataSize # note that files will have a value passed in
        self.children = children # keeps track of all subnodes
        self.isDir = isDir
    
    def addSubfile(self, childNode):
        if self.children is None:
            self.children = list()
        self.children.append(childNode)

    def setFileSize(self, newSize: int):
        self.fileSize = newSize

# ingests the file
def ingestUserInputs(inFile: str) -> Node:
    # initialize values for parsing
    curPath = "/"
    rootDir = Node("/", isDir = True)
    curDir = rootDir
    nodeMap = {"/":rootDir}

    with open(inFile, 'r') as cmdHist:
        curLine = cmdHist.readline()
        curLine = cmdHist.readline()
        while curLine:
            splitToks = curLine.split()
            if splitToks[0] == "$" and len(splitToks) == 3: # current line is a cd
                if splitToks[-1] == '..':
                    curPath = "/".join(curPath.split("/")[:-1]) # step out one dir
                    if not curPath:
                        curPath = "/" # stepped out to root
                else:
                    curPath += ("/" if curPath!="/" else "") + splitToks[-1] # or append to cur working dir
                curDir = nodeMap[curPath]                       # grab new rel node
            elif splitToks[0] == "$": # ls nodes can be skipped
                pass
            else: # current line is a file/dir listing
                tempFile = Node(curPath + ("/" if curPath!="/" else "") + splitToks[-1])
                if splitToks[0] == "dir":
                    nodeMap[curPath + ("/" if curPath!="/" else "") + splitToks[-1]] = tempFile # save ref
                    tempFile.isDir = True
                else:
                    tempFile.setFileSize(int(splitToks[0]))

                # add to current dir as subfile
                curDir.addSubfile(tempFile)

            # parse next line
            curLine = cmdHist.readline()

    # Now populate the filesizes for all directories properly...
    populateFilesizes(rootDir)

    return rootDir

# recursively calculates the size of the current node by determining the size of the
# children.
def populateFilesizes(curDir: Node)->int:
    if curDir.children:
        curDir.setFileSize(sum([populateFilesizes(subNode) for subNode in curDir.children]))

    return curDir.fileSize

def p1Soln(inFile: str) -> int:
    # set up problem
    rootNode = ingestUserInputs(inFile)

    # with the tree structure we can just iterate on the desired predicate and add these values...
    nodeStack = [rootNode]
    totalSize = 0
    filterPredicate = lambda dirFilesize : dirFilesize <= 100000
    while(nodeStack):
        # check predicate correctness on last node in stack
        curNode = nodeStack.pop()
        if curNode.isDir:
            if filterPredicate(curNode.fileSize):
                totalSize += curNode.fileSize

            # otherwise just add children directories to list
            if curNode.children is not None:
                [nodeStack.append(subNode) for subNode in curNode.children if subNode.isDir]

    return totalSize

###############################################################
#   Soln for P2 of Day 7 for AoC
#
# Problem:
#     Use the same tree created above to find the size of the smallest
#     directory that needs to be deleted that would be sufficient to
#     run an update of size 30 000 000. The total filesystem size is
#     assumed to be 70 000 000.
#
# Notice that this is just an optimization problem. Find the smallest
# value that is larger than (70 000 000 - sizeof("/")).
###############################################################
def p2Soln(inFile: str, totFSSize: int, updateSize: int) -> int:
     # set up problem
    rootNode = ingestUserInputs(inFile)

    # with the tree structure we can just iterate on the desired predicate to optimize
    nodeStack = [rootNode]
    curToDelSize = rootNode.fileSize + 1
    curAvailable = totFSSize - rootNode.fileSize
    reqDeletionSize = updateSize - curAvailable
    filterPredicate = lambda dirFilesize : dirFilesize >= reqDeletionSize
    while(nodeStack):
        # check predicate correctness on last node in stack
        curNode = nodeStack.pop()
        if curNode.isDir:
            if filterPredicate(curNode.fileSize):
                if curNode.fileSize < curToDelSize:
                    curToDelSize = curNode.fileSize

                # otherwise just add relevant children directories to list
                if curNode.children is not None:
                    [nodeStack.append(subNode) for subNode in curNode.children if subNode.isDir]

    return curToDelSize

if __name__ == "__main__":
    # prepare env for p1
    inFile = "./Day07/input"

    # evaluate on p1 algo
    soln1 = p1Soln(inFile)
    print("Solution for part 1 of the problem is {}".format(soln1))

    # evaluate on p2 algo
    soln2 = p2Soln(inFile, 70000000, 30000000)
    print("Solution for part 2 of the problem is {}".format(soln2))