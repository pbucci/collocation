import threading
import codecs
from printer import log
from node import *
import gc

## TextHandler handles all text metadata ##
class TextHandler(object):
    def __init__(self,path,parsehandler):
        self.parsehandler = parsehandler
        self.path = path
        self.id = path.split("/").pop().split(".")[0]
        splittext = path.split("/").pop().split("_")
        # Fields that parse for organization
        self.genre = int(splittext[0][1])
        self.school = splittext[1]
        self.genreNum = int(splittext[2])
        self.name = splittext[3]
        self.seg = splittext[4]
        self.punc = splittext[5].split(".")[0]
        self.file = None
        self.charnum = 0
        # Nodes
        self.nodes = []
        # EdgeProfiles
        self.profiles = []
    
    # Makes each non-ignore character-phrase into a node
    # For example, a three-character phrase is one node
    def nodify(self):
        ignores = self.parsehandler.ignore.chars
        classes = self.parsehandler.classes
        file = codecs.open(self.path,encoding='utf-8')
        log("Generating nodes for " + self.id)
        # Position in file
        pos = 0
        node_handler = NodeHandler(self.parsehandler)
        # Disable garbage collector while looping
        gc.disable()
        while True:
            # we read the entire file one character at at time
            s = file.read(1)
            current = s
            # If not current, we've hit the end of the file
            if not current:
                break
            # only continue (i.e., increment the count, etc)
            # if we aren't ignoring this character
            if (current in ignores):
                continue
            pos = pos + 1
            for cc in classes:
                for set in cc.chars:
                    for char in set:
                        if current == char:
                            node_handler.add(Node(current,cc,pos,set))
        node_handler.clearQueue()
        self.nodes = node_handler.nodes[:]
        file.close()
        self.charnum = pos
        gc.enable()
        log("\tThere were " + str(self.charnum) +
              " characters, and " + str(len(self.nodes)) + " nodes.")

    def generateProfile(self,focal,compare,stopword,delim,maxcost=120):
        focals = []
        stopwords = []
        delims = []
        compares = []
        # Sort the nodes into their correct categories
        for n in self.nodes[:]:
            if n.cc == focal:
                focals.append(n)
            elif n.cc == stopword:
                stopwords.append(n)
            elif n.cc == delim:
                delims.append(n)
            elif n.cc == compare:
                compares.append(n)
        p = NodeProfile(focals,stopwords,delims,compares,
                        focal,compare,stopword,delim,maxcost)
        self.profiles.append(p)     
