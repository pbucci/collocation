import unittest

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

class TestSuite(unittest.TestCase):

    def setUp(self):
        self.pathstring = "../texts/G1_Rujia_01_lunyu_seg_nopunc.txt"
        self.textmeta = TextMeta(self.pathstring)

    def testTextMetaFields(self):
        self.assertEqual(self.textmeta.path, self.pathstring)

    def testGenre(self):
        self.assertEqual(self.textmeta.genre, 1)

    def testSchool(self):
        self.assertEqual(self.textmeta.school, "Rujia")

    def testGenreNum(self):
        self.assertEqual(self.textmeta.genreNum, 1)

    def testName(self):
        self.assertEqual(self.textmeta.name, "lunyu")

    def testSeg(self):
        self.assertEqual(self.textmeta.seg, "seg")

    def testPunc(self):
        self.assertEqual(self.textmeta.punc, "nopunc")


if __name__ == '__main__':
    unittest.main()