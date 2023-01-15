#############################################################
#   Soln for P1 of Day 12 for AoC
#
# Problem:
#     DFS-able graph problem. We can implement a graph that can
#     then be traversed using a simple algorithm
#
# P2 Addendum:
#   The same as above except now we can visit a single small cave
#   more than once. Since a DFS is fairly flexible, we just let it
#   keep track of whether or not it has double-traversed a cave
#   yet and let it traverse it twice if it wants.
#############################################################
from collections import defaultdict

class UndirectedGraph:
    '''
        A graph is a collection of vertices either connected
        (or not) to via edges to other vertices. An undirected
        graph means an edge can be traversed in either direction.
    '''
    def __init__(self):
        self.adjMap = defaultdict(list)

    def parseConnectionList(self, inFile: str) -> None:
        '''
            Parses an input file containing the set of pairs of
            nodes that are connected in the graph.

            Arguments:
                inFile - The file with edges listed on each line.
        '''
        with open(inFile, 'r') as graphEdges:
            curLine = graphEdges.readline()
            while curLine:
                nodeL, nodeR = curLine.strip().split("-")
                self.adjMap[nodeL].append(nodeR)
                self.adjMap[nodeR].append(nodeL)
                curLine = graphEdges.readline()

    def __getitem__(self, *args):
        return self.adjMap.__getitem__(*args)

def enumerateAllPaths(sNode: str, eNode: str, graph: UndirectedGraph, * , includeDT:bool = False) -> int:
    '''
        Performs a graph traversal on top of an undirected graph. The traversal can be extended to
        a directed graph, but that is unnecessary here. Also allows for the possibility of a double
        traversal to a lowercase node (that isn't the start or end) for P2.

        Arguments:
            sNode - The name of the node to start from.
            eNode - The name of the ending node.
            graph - A graph object that composes the adjacency list.
            includeDT - Whether or not to include the double travel stipulation from the second part.

        Returns:
            int - The total number of unique paths given the above arguments.
    '''
    dfsStack = [(sNode, {sNode}, False)]
    totPaths = 0

    # perform basic DFS
    while dfsStack:
        curNode, visSet, dTravBool = dfsStack.pop()
        if curNode == eNode:
            totPaths += 1
            continue
        
        for posNode in graph[curNode]:
            # consider normal routes
            if posNode.isupper() or posNode not in visSet:
                dfsStack.append((posNode, visSet.union({posNode}), dTravBool))

            # and then double travel routes (if possible)
            if includeDT and not dTravBool and posNode.islower() and posNode in visSet:
                if posNode not in [sNode, eNode]:
                    dfsStack.append((posNode, visSet, True))

    return totPaths

if __name__ == "__main__":
    # prepare env for p1
    inFile = "./2021/Day12/input"
    uGraph = UndirectedGraph()
    uGraph.parseConnectionList(inFile)

    # execute algo for p1
    sol1 = enumerateAllPaths('start', 'end', uGraph)
    print("The answer to part 1 is {}".format(sol1))

    # and now for p2
    sol2 = enumerateAllPaths('start', 'end', uGraph, includeDT = True)
    print("The answer to part 2 is {}".format(sol2))