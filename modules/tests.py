import unittest
from profiler import *

class TestMeta(unittest.TestCase):
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