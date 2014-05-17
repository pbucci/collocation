# Text information for easy classification
class TextMeta(object):
    def __init__(self,textpath):
        # Parse the file path
        splittext = textpath.split("/").pop().split("_")
        
        # Fields
        self.path = textpath
        self.genre = int(splittext[0][1])
        self.school = splittext[1]
        self.genreNum = int(splittext[2])
        self.name = splittext[3]
        self.seg = splittext[4]
        self.punc = splittext[5].split(".")[0]
        self.file = open(self.path)

        self.characterCorrelationProfiles = []
        
    # A profile of two specific character sets
    class CorrelationProfile(object):
        def __init__(self,focalClass,comparisonClasses):
            self.profileId = focalClass.classname + "_to_" + comparisonClass.classname
            self.focalClass = focalClass
            self.comparisonClasses = comparisonClasses
            self.focalMatches = []

        class Match(object):
            def __init__(self,char,cost):
                self.distance = cost
                self.character = match

        def generateFocalMatches(self):
            # Match lists
            focalMatches = []
            comparisonMatches = []
            # Position in file
            pos = 0
            while True:
                # we read the entire file one character at at time
                c = openedFile.read(1)
                # If not c, we've hit the end of the file
                if not c:
                    break
                # only continue (i.e., increment the count, etc)
                # if we aren't ignoring this character
                if (c in characters_to_ignore):
                    continue
                pos = pos + 1
                # If c is a focal character, add it to the match list
                if (c in self.focalClass.chars):
                    fc = focalCharacter(fc,pos)
                    focalMatches.append(fc)
                    continue
                # If c is a comparison class character, add it to the comparison
                # match list
                for characterClass in self.comparisonClasses:
                    for character in CharacterClass:
                if (c in self.comparisonClass):
                
            return focalMatches


            return 1

class CharacterClass(object):
    def __init__(self,classname,charlist):
        # a string identifier such as "gods" or "delimiters"
        self.classname = classname
        # the list of Characters
        self.chars = charlist
    
    class Character(object):
        def __init__(self,c,pos):
            self.char = c
            self.position = pos
            self.matchList = []