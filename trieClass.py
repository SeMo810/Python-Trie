#LastName: Moss
#FirstName: Sean
#Email: sean.moss@colorado.edu
#Comments:

from __future__ import print_function
import sys

# We will use a class called my trie node
class MyTrieNode:
    # Initialize some fields

    def __init__(self, isRootNode):
        #The initialization below is just a suggestion.
        #Change it as you will.
        # But do not change the signature of the constructor.
        self.isRoot = isRootNode
        self.isWordEnd = False # is this node a word ending node
        self.count = 0 # frequency count
        self.next = {} # Dictionary mappng each character from a-z to the child node

    # Helper function for checking if a character is already mapped in this node's children
    def hasCharacter(self, c):
        return c in self.next.keys()

    # Helper function for inserting a new node with the given information
    # 'c' is the character, 'end' is if it is a word end
    def insertNode(self, c, end):
        self.next[c] = MyTrieNode(False)
        self.next[c].isWordEnd = end
        if end:
            self.next[c].count = 1

    # Helper function for returning a list of all possible suffixes from this node, and their frequencies
    # 'appendChar' is the character of the 'self' node
    def getSuffixes(self, appendChar):
        retList = []

        if len(self.next) > 0:
            for ch in self.next:
                node = self.next[ch]
                if node.isWordEnd: # If the next node down is a suffix in and of itself
                    retList.append((str(appendChar) + ch, node.count))
                if len(node.next) > 0:
                    nlist = node.getSuffixes(ch) # Recursively get the suffixes for the lower levels
                    if len(nlist) > 0:
                        for (ch2, count) in nlist: # For each suffix, append the char and add to the retval
                            retList.append((str(appendChar) + ch2, count))

        return retList

    def addWord(self,w):
        assert(len(w) > 0)

        ch = w[0]
        length = len(w)
        if length == 1: # If this last character is going to be in the 'next'
            if self.hasCharacter(ch):
                self.next[ch].count += 1
                self.next[ch].isWordEnd = True
            else:
                self.insertNode(ch, True)
        else: # If we can shave the first letter off and move down the Trie
            if not self.hasCharacter(ch):
                self.insertNode(ch, False)
            self.next[ch].addWord(w[1:])

        return

    def lookupWord(self,w):
        assert(len(w) > 0)

        ch = w[0]
        length = len(w)
        if length == 1:
            if self.hasCharacter(ch):
                return self.next[ch].count
            else:
                return 0
        else:
            if self.hasCharacter(ch):
                return self.next[ch].lookupWord(w[1:])
            else:
                return 0

        return 0


    def autoComplete(self,w):
        assert(len(w) > 0)

        length = len(w)
        nextnode = self
        nextChar = 0
        ch = 0
        while nextChar < length: # Move down the list until we get to the node for the last character in 'w', or fail completely
            ch = w[nextChar]
            if nextnode.hasCharacter(ch):
                nextnode = nextnode.next[ch]
                nextChar += 1
            else:
                return []

        # At this point, nextnode is the node that represents the last character, which is now in 'ch'
        retList = []
        app = w[:length-1]
        if nextnode.isWordEnd:
            retList.append((w, nextnode.count)) # Need to deal with the chance that 'w' itself is also there
        ret = nextnode.getSuffixes(ch) # Get the suffixes from there
        for (ac, cnt) in ret:
            retList.append((app + ac, cnt))
        return retList



if (__name__ == '__main__'):
    t= MyTrieNode(True)
    lst1=['test','testament','testing','ping','pin','pink','pine','pint','testing','pinetree']

    for w in lst1:
        t.addWord(w)

    j = t.lookupWord('testy') # should return 0
    j2 = t.lookupWord('telltale') # should return 0
    j3 = t.lookupWord ('testing') # should return 2
    lst3 = t.autoComplete('pi')
    print('Completions for \"pi\" are : ')
    print(lst3)

    lst4 = t.autoComplete('tes')
    print('Completions for \"tes\" are : ')
    print(lst4)
