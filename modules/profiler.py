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

# A profile of a text docment that contains the list
# of all character correlation profiles
class TextProfile(object):
    def __init__(self,tm):
        self.textmeta = tm
        self.characterCorrelationProfiles = []

class CharacterClass(object):
    def __init__(self,classname,charlist):
        self.charlist = charlist
        self.classname = classname