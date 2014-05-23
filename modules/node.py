class NodeHandler(object):
    def __init__(self,parsehandler):
        self.parsehandler = parsehandler
        # One-item queue
        self.queue = None
        self.nodes = []
    
    # Check before appending to nodes
    def add(self,new):
        if self.queue == None:
            self.queue = new
        else:
            if (new.key == self.queue.key and
                new.cc == self.queue.cc and
                len(self.queue.key) > 1):
                self.queue.char = self.queue.char + new.char
            else:
                self.nodes.append(self.queue)
                self.queue = new

    def clearQueue(self):
        self.nodes.append(self.queue)
        self.queue = None

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
    
    # returns an edge count
    def countEdges(self):
        count = len(self.edges)
        return count
    
    # Prints all of the good info about a node
    def printNode(self):
        print("\t#### Node ####")
        print("\tClass: " + self.cc.id)
        print("\tKey: " + self.key)
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
        self.cc = dest.cc
    
    # Prints all of the good info about an edge
    def printEdge(self):
        print("\t\t#### Edge ####")
        print("\t\tClass: " + self.cc.id)
        print("\t\tId: " + self.id)
        print("\t\tOrigin: " + self.orig.id)
        print("\t\tDestination: " + self.dest.id)
        print("\t\tCost: " + str(self.cost))
        print("\t\tAbsolute cost: " + str(self.abscost) + "\n")

class NodeProfile(object):
    def __init__(self,focals,stopwords,delims,compares,focal,
                 compare,stopword,delim,maxcost):
        self.focals = focals
        self.stopwords = stopwords
        self.delims = delims
        self.compares = compares
        self.focal = focal
        self.compare = compare
        self.stopword = stopword
        self.delim = delim
        self.maxcost = maxcost
        self.id = (focal.id + "_" + compare.id + "_" +
                   stopword.id + "_" + delim.id + "_" + str(maxcost))
        self.generateEdges()
    
    def generateEdges(self):
        print("Generating edges for " + self.id)
        for f in self.focals:
            f_pos = f.pos
            # For each newly-minted focal node, determine the distance to
            # each stopword if the node is within maxcost absolute distance.
            # This is because we don't want to count these words towards the
            # distance of future nodes.
            for s in self.stopwords:
                s_cost = f_pos - s.pos
                if abs(s_cost) <= self.maxcost:
                    f.add(Edge(f,s,s_cost))
            # Do the same for the delimiters.
            for d in self.delims:
                d_cost = f_pos - d.pos
                d_takeaway = 0
                for e in f.edges:
                    if (((e.dest.pos > d.pos and e.dest.pos < f.pos) or
                            (e.dest.pos < d.pos and e.dest.pos > f.pos)) and
                                (e.dest.cc == self.stopword)):
                        d_takeaway += 1
                if d_cost < 0:
                    d_cost += d_takeaway
                elif d_cost > 0:
                    d_cost -= d_takeaway
                if abs(d_cost) <= self.maxcost:
                    f.add(Edge(f,d,d_cost))
                    
            # Now we can calculate the compares by the distance ignoring
            # stopwords and delimiters, giving a better true distance
            for c in self.compares:
                c_cost = f_pos - c.pos
                takeaway = 0
                for e in f.edges:
                    if (((e.dest.pos > c.pos and e.dest.pos < f.pos) or
                         (e.dest.pos < c.pos and e.dest.pos > f.pos)) and
                            (e.dest.cc == self.stopword or
                             e.dest.cc == self.delim)):
                        takeaway += 1
                if c_cost < 0:
                    c_cost += takeaway
                elif c_cost > 0:
                    c_cost -= takeaway
                if abs(c_cost) <= self.maxcost:
                    f.add(Edge(f,c,c_cost))
                        
        print("Done generating edges for " + self.id)

    def printProfile(self):
        print("\n#### Profile ####")
        print("Focals: " + self.focal.id)
        print("Compares: " + self.compare.id)
        for f in self.focals:
            print("\n")
            f.printNode()

    def getColocations(self,abscost):
        colocations = []
        for f in self.focals[:]:
            for e in f.edges:
                if e.dest.cc == self.compare and e.abscost <= abscost:
                    colocations.append(f)
        return colocations

    def countColocations(self,abscost):
        return len(self.getColocations(abscost))
    
    def countFocalEdges(self):
        count = 0
        for f in self.focals:
            count = count + f.countEdges()

    def countCompareNodes(self):
        return len(compares)
    
    def getClosestTwoDelimiterPositions(self,focal):
        first = -1
        second = -1
        for e in focal.edges:
            if first == -1 and e.cc == self.delim:
                first = e.dest.pos
            elif second == -1 and e.cc == self.delim:
                second = e.dest.pos
            elif (first != -1 and second != -1) or (e.abscost > self.maxcost):
                break
        return first,second
    
    def countInSentence(self):
        count = 0
        for f in self.focals:
            closest = self.getClosestTwoDelimiterPositions(f)
            left = min(closest[0],closest[1])
            right = max(closest[0],closest[1])
            for e in f.edges:
                pos = e.dest.pos
                if (e.cc == self.compare and
                  ((pos >= left and pos < f.pos) or
                   (pos <= right and pos > f.pos))):
                    count = count + 1
        return count

# A set of characters with a unique identifier
class CharacterClass(object):
    def __init__(self,id,chars):
        # a string identifier such as "gods" or "delimiters"
        self.id = id
        # A list of character-phrases
        # Each with one or more character
        self.chars = chars