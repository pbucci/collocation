# -*- coding: utf-8 -*-
import os
import threading

##############################################
class ParseHandler(object):
    def __init__(self):
        self.texts = []
        self.classes = []
        self.loadAllClasses()
        self.ignore = self.getClass('ignore')
    
    # Creates a TextMeta object
    def loadText(self,textpath):
        t = TextMeta(textpath,self)
        self.texts.append(t)
    
    # Loads all texts in a directory
    def loadAllTexts(self):
        for file in os.listdir(self.dirpath):
            if file[0] != ".":
                self.loadText(self.dirpath + "/" + file)

    # Returns a class from self.classes
    def getClass(self,id):
        for c in self.classes:
            if c.id == id:
                return c
        return None
    
    # Sets the directory in which to look for texts
    def setTextDirectoryPath(self,path):
        self.dirpath = path
    
    # Loads classes from classes.py
    def loadAllClasses(self):
        from classes import classes
        for id,chars in classes.iteritems():
            self.loadClass(id,chars)

    # Creates a character class
    # id    : string
    # chars : list of characters
    def loadClass(self,id,chars):
        c = CharacterClass(id,chars)
        self.classes.append(c)
    
    # Loads all classes in tuple into a tuple
    def loadClassTuple(self,tuple):
        list = []
        for t in tuple:
            list.append(self.getClass(t))
        return list
    
    # Report for character counts
    def countReport(self):
        focal = self.getClass('null')
        comparison = self.loadClassTuple(('reduced_deity','reduced_god','reduced_punishment','reduced_reward','ubc_emotion','ubc_cognition','ubc_religion','ubc_morality'))
        charcounts = {}
        for cc in comparison:
            for char in cc.chars:
                charcounts[char] = 0
        sumtotals = {}
        for cc in comparison:
            dict = {}
            for char in cc.chars:
                dict[char] = 0
            sumtotals[cc.id] = dict
        text_count = 0
        for t in self.texts:
            text_count = text_count + 1
            print "Generating CP for file number " + str(text_count) + " : " + t.id
            thread = threading.Thread(target=t.generateCorrelationProfile,args=(focal,comparison,))
            thread.start()
        for t in self.texts:
            print "Generating counts for " + t.id
            report = open('/Users/bucci/reports/' + t.id + '-count-report.txt', 'w')
            for cp in t.profiles:
                for cc in comparison:
                    for char in cc.chars:
                        count = cp.countCharInText(char);
                        report.write(char + "," + count + '\n')
                        charcounts[char] = charcounts[char].value() + count
                        sumtotals[cc.id[char]] = sumtotals[cc.id[char]].value() + count
            report.close()
        summary = open('/Users/bucci/reports/summary.txt', 'w')
        for c,v in charcounts.iteritems():
            summary.write(c + "," + str(v) + "\n")
        for cc,chars in sumtotals.iteritems():
            count = 0
            for chars,value in sumtotals[cc].iteritems():
                count = count + value
            summary.write(cc + "," + str(count) + "\n")
        summary.close()

##############################################
# A focal character and an ordered list of
# edges to comparision characters
class Node(object):
    def __init__(self,fc):
        # Focal character
        self.focal = fc
        # Ordered list of edges from
        # nearest to farthest
        self.edgelist = []
    
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
    def getWithin(self,cost):
        list = []
        for e in self.edgelist:
            if e.abscost <= cost:
                list.append(e)
            # else break

    # Get all matches between two of a class of character
    def getMatchesBetween(self,charClass):
        right
        left
        list = []
        for e in self.edgelist:
            if (right is undefined or left is undefined):
                if e.to.type is charClass:
                    if e.cost >= 0:
                        right = e
                    else:
                        left = e
                else:
                    list.append(e)

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

##############################################
# A set of characters with a unique identifier
class CharacterClass(object):
    def __init__(self,id,chars):
        # a string identifier such as "gods" or "delimiters"
        self.id = id
        # the list of Characters
        self.chars = chars

##############################################
# Text information for easy classification
class TextMeta(object):
    def __init__(self,textpath,ph):
        print textpath
        # The handler
        self.parsehandler = ph
        # Parse the file path
        self.id = textpath.split("/").pop()
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

##############################################
# A profile of character sets interactions
# metadata about a particular text
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
        self.generateMatches()
        self.generateNodesAndEdges()

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
            if (c in self.textmeta.parsehandler.ignore.chars):
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

    # Prints pertainent information from all nodes
    def printNodes(self):
        for n in self.nodes:
            n.printNode()

    # Counts all matches within a certain distance for all
    # focal characters matches, allows double-counting for
    # places where two focal characters are in proximity <= 2*cost
    def countWithin(self,cost):
        count = 0
        for n in self.nodes:
            count = count + n.countWithin(cost)
        return count
    
    # Count character occurence in a text
    def countCharInText(self,char):
        count = 0
        for f in self.focalMatches:
            if f.char == char:
                count = count + 1
        for c in self.comparisonMatches:
            if c.char == char:
                count = count + 1
        return count

    # Counts totals for specific occurance of a character
    # with absolute distance <= cost
    def countMatchesForCharacterWithin(char,cost):
        return len(getMatchesForCharacterWithin(char,cost))
    
    # Gets all matches in node list with char as focal
    # and absolute distance <= cost
    def getMatchesForCharacterWithin(self,char,cost):
        list = []
        for n in self.nodes:
            nodelist = n.getWithin(cost)
            for nl in nodelist:
                if nl.focal == char:
                    list.append(nl)
        return list

if __name__ == '__main__':
    handler = ParseHandler()
    handler.setTextDirectoryPath("/Users/bucci/dev/CorrelationProfiler/texts")
    handler.loadAllTexts()
    handler.countReport()