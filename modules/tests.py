import unittest
from profiler import *

class Tester(unittest.TestCase):
    def setUp(self):
        self.handler = ParseHandler()
        self.handler.setTextDirectoryPath("/Users/bucci/dev/CorrelationProfiler/test_texts")
        self.handler.loadAllClasses()
        self.handler.loadAllTexts()
    
    def test_loadClasses(self):
        self.assertEqual(self.handler.classes[2].id, "focal_set")

    def test_focalSet_is_loaded_correctly(self):
        self.assertEqual(self.handler.classes[2].chars, ('a','b','c'))

    def test_correlation_build(self):
        focal = self.handler.classes[2]
        compare_set = (self.handler.classes[0],self.handler.classes[1])
        for t in self.handler.texts:
            t.generateCorrelationProfile(focal,compare_set)
            p = t.profiles[0]
            p.generateMatches()
            p.generateNodesAndEdges()
            p.printNodes()

if __name__ == '__main__':
    unittest.main()