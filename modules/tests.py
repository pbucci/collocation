import unittest
from profiler import *

class Tester(unittest.TestCase):
    def setUp(self):
        self.handler = ParseHandler()
        self.handler.setTextDirectoryPath("/Users/bucci/dev/CorrelationProfiler/test_texts")
        self.handler.loadAllTexts()
    
    def test_correlation_build(self):
        focal = self.handler.getClass('null')
        compare_set = (self.handler.getClass('null'),self.handler.getClass('null'))
        for t in self.handler.texts:
            t.generateCorrelationProfile(focal,compare_set)
            p = t.profiles[0]
            p.generateMatches()
            p.generateNodesAndEdges()
            p.printNodes()
    

if __name__ == '__main__':
    unittest.main()