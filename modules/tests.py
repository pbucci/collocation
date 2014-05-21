import unittest
from text import *
from console import *

class Tester(unittest.TestCase):
    def setUp(self):
        self.p = ParseHandler()
        self.p.setTextDirectory("/Users/bucci/dev/CorrelationProfiler/texts/")
        self.p.loadAllTexts()

    def test_classes(self):
        self.assertEquals(len(self.p.classes), 14)

    def test_nodes(self):
        nodes = self.p.texts[0].nodes
        for n in nodes:
            print n.char

        #self.assertEquals(nodes[0].cc.id, "t_consonants" )
        #self.assertEquals(nodes[1].char, "stop")

if __name__ == '__main__':
    unittest.main()