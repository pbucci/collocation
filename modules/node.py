
##############################################
# A focal character and an ordered list of
# edges to comparision characters
class Node(object):
    def __init__(self,fc,id):
        # Focal character
        self.focal = fc
        # Ordered list of edges from
        # nearest to farthest
        self.edgelist = []
        self.id = id
    
    # Adds an edge, maintains edge order
    # in terms of absolute distance
    def add(self,e):
        if len(self.edgelist) == 0:
            self.edgelist.append(e)
        else:
            i = 0
            for edge in self.edgelist:
                if e.abscost < edge.abscost:
                    self.edgelist.insert(i,e)
                    break
                i = i + 1
            self.edgelist.append(e)
    
    # Match count <= cost
    def countWithin(self,cost):
        count = len(getWithin(cost))
        return count
    
    # Get all edges <= cost
    # edges is a filtered list of edges, defaults to full list
    def getWithin(self,cost):
        list = []
        for e in self.edgelist:
            if e.abscost <= cost:
                list.append(e)
        return list
    # else break
    
    # Get all matches between two of a class of character
    def getMatchesBetween(self,charClass,*edges):
        right = None
        left = None
        list = []
        if len(edges) == 0:
            edges = self.edgelist
        else:
            edges = edges[0]
        for e in edges:
            if (right is None or left is None):
                if e.to.type is charClass:
                    if e.cost >= 0:
                        right = e
                    else:
                        left = e
                else:
                    list.append(e)
        return list
    
    # Gets an ordered list of closest n edges
    def getNClosestMatches(self,n):
        return self.edgelist[:n]
    
    # Gets an ordered list of closest 1 edge
    def getClosestMatch(self):
        return self.edgelist[:1]
    
    # Print function for visualization
    def printNode(self):
        print "Character: " + self.focal.name
        print "Type: " + self.focal.typeId
        self.printEdges()
        print "\n"
    
    # Print function for visualization
    def printEdges(self):
        for e in self.edgelist:
            e.printEdge()

##############################################
# A directed edge to a comparison class match
class Edge(object):
    def __init__(self,t,cost):
        self.to = t
        self.cost = cost
        self.abscost = abs(cost)
    
    # Prints all pertainent edge information
    def printEdge(self):
        print "Edge to: " + self.to.name
        print "Cost: " + str(self.cost)

##############################################
# An instance of a matched character
class Match(object):
    def __init__(self,character,pos,type):
        # Unique identifier
        self.name = character + "-" + str(pos)
        # Character
        self.char = character
        # Character class
        self.type = type
        # Character class unique id
        self.typeId = type.id
        # Integer
        self.pos = pos
