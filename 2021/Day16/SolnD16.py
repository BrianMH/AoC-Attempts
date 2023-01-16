#############################################################
#   Soln for P1 of Day 16 for AoC
#
# Problem:
#   Apparently we need to re-implement the BITS transmission
#   protocol decoding scheme.
#
#   Part 2 just seems to ask to evaluate it given a certain
#   definition for the packet types. In essence, the literals
#   (or packets of type 4), are pretty much the "leaves" of the
#   tree structure here.
#
#   Note: This really does bring out the most frightening part of
#         microcontrollers. Debugging struct outputs with a
#         series of unions present is almost impossible to do
#         easily on the fly...
#############################################################
from typing import Callable
from functools import reduce

class Packet:
    PAK_VER = 3
    PAK_TYPE = 3
    PAK_DAT_HEADER = 1
    HEADER_LEN = PAK_VER + PAK_TYPE + PAK_DAT_HEADER

    # used only for operator packets
    DEC_LEN = {'0': 15, '1':11}

    # only used for literal packets
    LIT_DAT_LEN = 4

    def __init__(self, pakHeader: str = None):
        self.val = None
        self.version = -1
        self.type = -1
        self.firstSwitch = -1
        self.subPackets = list()

        if pakHeader is not None:
            self._parseHeader(pakHeader)

    def _parseHeader(self, pStr: str):
        self.version = int(pStr[:self.PAK_VER], 2)
        self.type = int(pStr[self.PAK_VER:self.PAK_VER+self.PAK_TYPE], 2)
        self.firstSwitch = pStr[self.PAK_VER+self.PAK_TYPE]

class BITSDecoder:
    '''
        Much like in the microcontroller case, we can create this class
        as a stream decoder to make things slightly simpler to deal with.
        It is, effectively, just tree structure
    '''
    def __init__(self):
        self.rootPacket = None

    def calculateVersionSum(self) -> int:
        '''
            Effectively a tree traversal that calculates the sum of all the 
            packet versions. This is used to solve part 1.

            Returns:
                int - The total sum of all node versions.
        '''
        return self._recursiveVersionSum(self.rootPacket)

    def evaluateRootVal(self, opDict: dict[int, Callable]) -> int:
        '''
            Given the tree structure and a dictionary representing what operations
            to perform on the subpackets of any non-literal nodes, return the root's
            value given the set of operations in opDict.

            Arguments:
                opDict - A dictionary that matches the type value to operations to perform.

            Returns:
                int - The value of the root once all values are propagated upward.
        '''
        return self._recursiveEval(self.rootPacket, opDict)

    def parseStreamPacket(self, stream: str) -> None:
        '''
            Parses a BITS packet recursively as the packet itself is defined as such.

            Arguments:
                stream - The string representing the stream received by the ship to parse.
        '''
        self.rootPacket = Packet(stream[:Packet.HEADER_LEN])
        curStreamInd = Packet.HEADER_LEN

        if self.rootPacket.type != 4: # op packet
            numBitsToRead = Packet.DEC_LEN[self.rootPacket.firstSwitch]
            subpacketLen = int(stream[curStreamInd:curStreamInd+numBitsToRead], 2)
            iSPInd = curStreamInd + numBitsToRead # start of subpacket
            if self.rootPacket.firstSwitch == "0": # parse by length
                fSPInd = iSPInd + subpacketLen # end of subpacket
                self.rootPacket.subPackets.extend(self._parseSubPackets(stream[iSPInd:fSPInd])[0])
            else: # parse by packet count (end cannot be inferred)
                self.rootPacket.subPackets.extend(self._parseSubPackets(stream[iSPInd:], numPackets = subpacketLen)[0])
        else:
            _, self.rootPacket.val = self._parseLiteralSubStr(stream[curStreamInd-1:])

    ###################### HELPER FUNCS ###########################

    def _recursiveVersionSum(self, curNode: Packet) -> int:
        return curNode.version + sum([self._recursiveVersionSum(child) for child in curNode.subPackets])

    def _recursiveEval(self, curNode: Packet, opDict: dict[int, Callable]) -> int:
        if curNode.type == 4: # literal node
            return curNode.val
        else:
            return opDict[curNode.type]([self._recursiveEval(node, opDict) for node in curNode.subPackets])

    def _parseSubPackets(self, stream: str, * , numPackets: int = 0) -> tuple[list[Packet], int]:
        '''
            Uses similar logic to the starter function to evaluate the subpackets of the root.
        '''
        packList = list()
        curInd = 0
        # update numPackets if default
        if numPackets <= 0:
            numPackets = 999999

        # continue parsing until end of stream or packet len reached
        while curInd < len(stream) and len(packList) < numPackets:
            # Parse header and move index
            curPacket = Packet(stream[curInd:curInd+Packet.HEADER_LEN])
            curInd += Packet.HEADER_LEN

            # create packet
            if curPacket.type != 4:
                numBitsToRead = Packet.DEC_LEN[curPacket.firstSwitch]
                subPacketLen = int(stream[curInd:curInd+numBitsToRead], 2)
                iSPInd = curInd + numBitsToRead

                # split on packet type
                if curPacket.firstSwitch == "0": # determine by length
                    subPackets, offsetInd = self._parseSubPackets(stream[iSPInd:iSPInd + subPacketLen])
                else: # otherwise by packet size
                    subPackets, offsetInd = self._parseSubPackets(stream[iSPInd:], numPackets = subPacketLen)

                # augment current packet with subpackets
                curPacket.subPackets.extend(subPackets)
                curInd += offsetInd + numBitsToRead
            else:
                offset, curPacket.val = self._parseLiteralSubStr(stream[curInd-1:])
                curInd += offset

            # and then add it to our list before working on the next
            packList.append(curPacket)

        return packList, curInd

    def _parseLiteralSubStr(self, stream: str) -> tuple[int, int]:
        '''
            A helper designed to parse the literal value passed in. Assumes that the header has
            already been stripped off from the left-most literal value and returns the number of
            bits read in total along with the integer value of the binary substring.
        '''
        bitIntVal = ""
        curIntInd = 0
        
        # read preliminary data bytes
        while stream[curIntInd] == '1':
            offsetInd = curIntInd + Packet.PAK_DAT_HEADER
            bitIntVal += stream[offsetInd:offsetInd+Packet.LIT_DAT_LEN]
            curIntInd = offsetInd + Packet.LIT_DAT_LEN
        # and parse final one
        offsetInd = curIntInd + Packet.PAK_DAT_HEADER
        bitIntVal += stream[offsetInd:offsetInd+Packet.LIT_DAT_LEN]

        # and then convert to base 10
        return offsetInd+Packet.LIT_DAT_LEN-1, int(bitIntVal, 2)

if __name__ == "__main__":
    # prepare env for p1
    inFile = "./2021/Day16/input"
    with open(inFile, 'r') as inStr:
        hexInput = inStr.readline().rstrip()

    # set up decoder tree with proper hex to binary string conversion
    curTree = BITSDecoder()
    binInput = format(int(hexInput, 16), '0'+str(len(hexInput)*4)+'b')
    curTree.parseStreamPacket(binInput)

    # execute algo for p1
    sol1 = curTree.calculateVersionSum()
    print("The answer to part 1 is {}".format(sol1))

    # and now for p2
    opDict = {0: sum,
              1: lambda xList: reduce(lambda x,y:x*y, xList, 1),
              2: min,
              3: max,
              5: lambda xList: int(xList[0]>xList[1]),
              6: lambda xList: int(xList[0]<xList[1]),
              7: lambda xList: int(xList[0]==xList[1])}
    sol2 = curTree.evaluateRootVal(opDict)
    print("The answer to part 2 is {}".format(sol2))