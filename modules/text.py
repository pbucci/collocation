import threading
import codecs
import time
import datetime
from node import *
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
        self.file = codecs.open(self.path,encoding='utf-8')
        # Nodes
        self.nodes = []
        # EdgeProfiles
        self.profiles = []
        self.nodify()

    # Makes each non-ignore character-phrase into a node
    # For example, a three-character phrase is one node
    def nodify(self):
        print "Generating nodes for " + self.id
        ts = time.time()
        print datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        # Position in file
        pos = 0
        nodes = NodeHandler(self.parsehandler)
        while True:

            # we read the entire file one character at at time
            s = self.file.read(1)
            current = unicode(s)
            # If not current, we've hit the end of the file
            if not current:
                break
            # only continue (i.e., increment the count, etc)
            # if we aren't ignoring this character
            if (current in self.parsehandler.ignore.chars):
                nodes.clearQueue()
                continue
            pos = pos + 1
            for cc in self.parsehandler.classes:
                for set in cc.chars:
                    if current == set:
                        nodes.add(Node(current,cc,pos,set))
        nodes.clearQueue()
        for node in nodes.nodes:
            self.nodes.append(node)
        for node in self.nodes:
            node.printNode()
        
        self.file.close()
        print("Done generating nodes for " + self.id)

    # focal     : cc
    # compare   : cc
    # stopword  : cc
    # delim     : cc
    # maxcost   : int
    def generateProfile(self,focal,compare,stopword,delim,maxcost=120):
        focals = []
        stopwords = []
        delims = []
        compares = []
        for n in self.nodes[:]:
            if n.cc == focal:
                focals.append(n)
            elif n.cc == stopword:
                stopwords.append(n)
            elif n.cc == delim:
                delims.append(n)
            elif n.cc == compare:
                compares.append(n)
        for f in focals:
            for s in stopwords:
                cost = f.pos - s.pos
                if cost < maxcost:
                    f.add(Edge(f,s,cost))
            for d in delims:
                cost = f.pos - s.pos
                takeaway = 0
                for e in f.edges:
                    if e.abscost < abs(cost) and e.dest.cc == stopword:
                        takeaway = takeaway + 1
                cost = cost - takeaway
                if cost < maxcost:
                    f.add(Edge(f,d,cost))
            for c in compares:
                cost = f.pos - c.pos
                takeaway = 0
                for e in f.edges:
                    if e.abscost < abs(cost) and (e.dest.cc == stopword or e.dest.cc == delim):
                        takeaway = takeaway + 1
                cost = cost - takeaway
                if cost < maxcost:
                    f.add(Edge(f,c,cost))
                    print("Added an edge. " + self.id)

        p = NodeProfile(focals,stopwords,delims,compares,focal,compare,stopword,delim,maxcost)
        self.profiles.append(p)











        














