import os
class Node(object):
    def __init__(self,fc):
        # Focal character
        self.focal = fc
        # Ordered list of edges from
        # nearest to farthest
        self.edgelist = []
    
    # Adds an edge, maintains edge order
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

    def getNClosestMatches(self,n):
        return self.edgelist[:n]

    def getClosestMatch(self):
        return self.edgelist[:1]
    
    def printNode(self):
        print "Character: " + self.focal.char
        print "Type: " + self.focal.typeId
        self.printEdges()
        print "\n"

    def printEdges(self):
        for e in self.edgelist:
            e.printEdge()

# A directed edge to a comparison class match
class Edge(object):
    def __init__(self,t,cost):
        self.to = t
        self.cost = cost
        self.abscost = abs(cost)

    def printEdge(self):
        print "Edge to: " + self.to.char
        print "Cost: " + str(self.cost)

# An instance of a matched character
class Match(object):
    def __init__(self,character,pos,type):
        self.char = character + "-" + str(pos)
        self.type = type
        self.typeId = type.id
        self.pos = pos

# A set of characters with a unique identifier
class CharacterClass(object):
    def __init__(self,id,chars):
        # a string identifier such as "gods" or "delimiters"
        self.id = id
        # the list of Characters
        self.chars = chars

characters_to_ignore = CharacterClass("ignore",('\ '))

class ParseHandler(object):
    def __init__(self):
        self.texts = []
        self.classes = []
    
    # Creates a TextMeta object
    def loadText(self,textpath):
        t = TextMeta(textpath)
        self.texts.append(t)
    
    def loadAllTexts(self):
        for file in os.listdir(self.dirpath):
            self.loadText(self.dirpath + "/" + file)
    
    # Creates a character class
    # id    : string
    # chars : list of characters
    def loadClass(self,id,chars):
        c = CharacterClass(id,chars)
        self.classes.append(c)

    def setTextDirectoryPath(self,path):
        self.dirpath = path

    def loadAllClasses(self):
        from classes import classes
        for id,chars in classes.iteritems():
            self.loadClass(id,chars)

# Text information for easy classification
class TextMeta(object):
    def __init__(self,textpath):
        # Parse the file path
        splittext = textpath.split("/").pop().split("_")
        # Fields that parse for organization
        self.path = textpath
        self.genre = int(splittext[0][1])
        self.school = splittext[1]
        self.genreNum = int(splittext[2])
        self.name = splittext[3]
        self.seg = splittext[4]
        self.punc = splittext[5].split(".")[0]
        # The text file itself
        self.file = open(self.path)
        # The analyses
        self.profiles = []
    
    # A function that generates a profile for comparing two or more
    # classes. The profile can be seen as a directed weighted graph
    # focalClass        : CharacterClass
    # comparisonClass   : list of CharacterClass
    def generateCorrelationProfile(self, focalClass, comparisonClasses):
        profile = CorrelationProfile(focalClass, comparisonClasses, self)
        self.profiles.append(profile)
    
# A profile of character sets interactions, lives as an inner
# class because it is metadata about a particular text
class CorrelationProfile(object):
    def __init__(self,focalClass,comparisonClasses,textmeta):
        self.textmeta = textmeta
        self.focalClass = focalClass
        self.comparisonClasses = comparisonClasses
        # Match lists
        self.focalMatches = []
        self.comparisonMatches = []
        # Nodes are directed
        self.nodes = []

    
    # Parses the input file character by character to
    # find matches.
    def generateMatches(self):
        # Position in file
        pos = 0
        while True:
            # we read the entire file one character at at time
            c = self.textmeta.file.read(1)
            # If not c, we've hit the end of the file
            if not c:
                break
            # only continue (i.e., increment the count, etc)
            # if we aren't ignoring this character
            if (c in characters_to_ignore.chars):
                continue
            pos = pos + 1
            # If c is a focal character, add it to the match list
            if (c in self.focalClass.chars):
                m = Match(c,pos,self.focalClass)
                self.focalMatches.append(m)
                continue
            # If c is a comparison class character, add it to the comparison
            # match list
            for characterClass in self.comparisonClasses:
                if c in characterClass.chars:
                    m = Match(c,pos,characterClass)
                    self.comparisonMatches.append(m)

    # Calculates edges between match nodes and generates
    # a directed edge object
    def generateNodesAndEdges(self):
        for f in self.focalMatches:
            n = Node(f)
            for c in self.comparisonMatches:
                cost = c.pos - f.pos
                e = Edge(c,cost)
                n.add(e)
            self.nodes.append(n)

    def printNodes(self):
        for n in self.nodes:
            n.printNode()
