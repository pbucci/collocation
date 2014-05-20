class NodeHandler(object):
    def __init__(self,parsehandler):
        self.parsehandler = parsehandler
        self.queue = []
        self.nodes = []
    
    # Check before appending to nodes
    def add(self,new):
        for old in self.queue:
            if new.key == old.key and new.cc == old.cc and len(old.key) > 1:
                old.char = old.char + new.char
                break
        else:
            self.queue.append(new)

    # Remove all nodes in queue
    def clearQueue(self):
        for n in self.queue:
            if n.key == n.char:
                self.nodes.append(n)
        del self.queue[:]

# All pertainent characters in a text are represented
# as nodes.
class Node(object):
    def __init__(self,char,cc,pos,key):
        self.pos = pos
        self.cc = cc
        self.char = char
        self.key = key
        self.edges = []
        self.id = self.key + "_" + str(self.pos)
    
    # Maintains list of edges with order least -> highest cost
    def add(self,edge):
        if edge.abscost > 0:
            i = 0
            for e in self.edges:
                if edge.abscost < e.abscost:
                    break
                else:
                    i = i + 1
            self.edges.insert(i,edge)

    # Get right position for multi-character nodes
    def getRight(self):
        rpos = self.pos + len(self.char) - 1
        return rpos

    # Prints all of the good info about a node
    def printNode(self):
        print "\t#### Node ####"
        print "\tClass: " + self.cc.id
        print "\tKey: " + self.key
        for e in self.edges:
            e.printEdge()

# The relationship between two nodes, directed from
# origin node as a focal node to dest as a compare
class Edge(object):
    def __init__(self,orig,dest,cost):
        self.id = orig.id + "_" + dest.id + "_" + str(cost)
        self.orig = orig
        self.dest = dest
        self.cost = cost
        self.abscost = abs(cost)

    # Prints all of the good info about an edge
    def printEdge(self):
        print "\t\t#### Edge ####"
        print "\t\tId: " + self.id
        print "\t\tOrigin: " + self.orig.id
        print "\t\tDestination: " + self.dest.id
        print "\t\tCost: " + str(self.cost)
        print "\t\tAbsolute cost: " + str(self.abscost) + "\n"


class NodeProfile(object):
    def __init__(self,focals,stopwords,delims,compares,focal,compare,stopword,delim,maxcost):
        self.focals = focals
        self.stopwords = stopwords
        self.delims = delims
        self.compares = compares
        self.focal = focal
        self.compare = compare
        self.stopword = stopword
        self.delim = delim
        self.maxcost = maxcost
    
    def printProfile(self):
        print "\n#### Profile ####"
        print "Focals: " + self.focal.id
        print "Compares: " + self.compare.id
        for f in self.focals:
            print
            f.printNode()

    def getColocations(self,abscost):
        colocations = []
        for f in self.focals[:]:
            for e in f.edges:
                if e.dest.cc == self.compare and e.abscost <= abscost:
                    colocations.append(f)
        return colocations

    def countColocations(self,cost):
        return len(self.getColocations(cost))

    def countInSentence(self):
        right = None
        left = None
        list = []
        for f in focals:
            for e in f.edges:
                if right == None or left == None:
                    if e.dest.cc == delim:
                        if e.cost > 0:
                            left = e
                        if e.cost < 0:
                            right = e
                list.append(e)
        return len(list)




