class NodeHandler(object):
    def __init__(self,parsehandler):
        self.parsehandler = parsehandler
        self.queue = []
        self.nodes = []

    def add(self,new):
        for old in self.queue:
            if new.key == old.key and new.cc == old.cc and len(old.key) > 1:
                old.char = old.char + new.char
                break
        else:
            self.queue.append(new)

    def clearQueue(self):
        for n in self.queue:
            if n.key == n.char:
                self.nodes.append(n)
        del self.queue[:]

class Node(object):
    def __init__(self,char,cc,pos,key):
        self.pos = pos
        self.cc = cc
        self.char = char
        self.key = key
        self.edges = []

        def add(self,edge):
            i = 0
            for e in self.edges:
                if edge.abscost < e.abscost:
                    break
                else:
                    i = i + 1
            self.edges.insert(i)

class Edge(object):
    def __init__(self,orig,dest,cost):
        self.orig = orig
        self.dest = dest
        self.cost = cost
        self.abscost = abs(cost)

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

    def getColocations(self,cost):
        colocations = []
        for f in self.focals[:]:
            for e in f.edges:
                if e.dest == compare and e.abscost <= cost:
                    colocations.append(f)
        return colocations

    def countColocations(self,cost):
        return len(self.getColocations(cost))

    


