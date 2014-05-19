## console.py
## Author:   James Thiele
## Date:     27 April 2004
## Version:  1.0
## Location: http://www.eskimo.com/~jet/python/examples/cmd/
## Copyright (c) 2004, James Thiele
## Modified: Paul Bucci 2014
## Website: PaulBucci.ca

import os
import cmd
import readline
from profiler import *

class ParseHandler(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "=>> "
        self.intro  = "Welcome to console!"  ## defaults to None
        self.texts = []
        self.classes = []
        self.loadAllClasses()
        self.ignore = self.getClass('ignore')
        self.maxcost = sys.maxint
        self.dirpath = ""
    
    # Prints available classes
    def do_classes(self,line):
        for c in self.classes:
            print c.id

    def do_load(self,line):
        self.setTextDirectoryPath(line)
        self.loadAllTexts()
    
    def do_print_dirpath(self,line):
        print self.dirpath
    
    def do_set_max(self,line):
        self.maxcost = line
        print "Max cost set to " + line

    # Creates a TextMeta object
    def loadText(self,textpath):
        t = TextMeta(textpath,self)
        self.texts.append(t)
    
    # Loads all texts in a directory
    def loadAllTexts(self,*maxcost):
        for file in os.listdir(self.dirpath):
            if file[0] != ".":
                self.loadText(self.dirpath + "/" + file,maxcost[0])
    
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
            t.generateCorrelationProfile(focal,comparison)
        for t in self.texts:
            text_count = text_count + 1
            print "Generating counts for " + t.id
            report = open('/Users/bucci/reports/' + t.id + '-count-report.txt', 'w')
            for cp in t.profiles:
                for cc in comparison:
                    for char in cc.chars:
                        count = cp.countCharInText(char);
                        report.write(char + "," + str(count) + '\n')
                        charcounts[char] = charcounts[char] + count
                        sumtotals[cc.id][char] = sumtotals[cc.id][char] + count
            report.close()
        summary = open('/Users/bucci/reports/summary-count-report.txt', 'w')
        for c,v in charcounts.iteritems():
            summary.write(c + "," + str(v) + "\n")
        for cc,chars in sumtotals.iteritems():
            count = 0
            for chars,value in sumtotals[cc].iteritems():
                count = count + value
            summary.write(cc + "," + str(count) + "\n")
        summary.close()
        print "Done!"
    
    def fullSentenceReport(self):
        self.runFullComparison('reduced_deity',('reduced_punishment','stopwords'))
        self.runFullComparison('reduced_deity',('reduced_reward','stopwords'))
        self.runFullComparison('reduced_god',('reduced_punishment','stopwords'))
        self.runFullComparison('reduced_god',('reduced_reward','stopwords'))
        self.runFullComparison('reduced_deity',('ubc_morality','stopwords'))
        self.runFullComparison('reduced_deity',('ubc_emotion','stopwords'))
        self.runFullComparison('reduced_deity',('ubc_cognition','stopwords'))
        self.runFullComparison('reduced_deity',('ubc_religion','stopwords'))
        self.runFullComparison('reduced_god',('ubc_morality','stopwords'))
        self.runFullComparison('reduced_god',('ubc_emotion','stopwords'))
        self.runFullComparison('reduced_god',('ubc_cognition','stopwords'))
        self.runFullComparison('reduced_god',('ubc_religion','stopwords'))
        print "Done!"
    
    def runFullComparison(self,f,comps):
        print "Comparision initialized."
        focal = self.getClass(f)
        comparisons = self.loadClassTuple(comps)
        file = open('/Users/bucci/reports/total_summary' + '.csv', 'w')
        total = 0
        for text in self.texts:
            text.generateCorrelationProfile(focal,comparisons)
            for cp in text.profiles:
                total = total + cp.countMatchesInSentenceWithinCost(120,comparisons[1])
            file.write(text.id + '_' + focal.id + '_x_' + comparisons[0].id + ', ' + str(total) + '\n')
        file.close()
    
    # Report for in-sentence counts
    def sentenceReport(self):
        self.runComparison('reduced_deity',('reduced_punishment','stopwords'))
        self.runComparison('reduced_deity',('reduced_reward','stopwords'))
        self.runComparison('reduced_god',('reduced_punishment','stopwords'))
        self.runComparison('reduced_god',('reduced_reward','stopwords'))
        self.runComparison('reduced_deity',('ubc_morality','stopwords'))
        self.runComparison('reduced_deity',('ubc_emotion','stopwords'))
        self.runComparison('reduced_deity',('ubc_cognition','stopwords'))
        self.runComparison('reduced_deity',('ubc_religion','stopwords'))
        self.runComparison('reduced_god',('ubc_morality','stopwords'))
        self.runComparison('reduced_god',('ubc_emotion','stopwords'))
        self.runComparison('reduced_god',('ubc_cognition','stopwords'))
        self.runComparison('reduced_god',('ubc_religion','stopwords'))
        print "Done!"
    
    # Runs a comparision between f and comps classes
    # f : string
    # comps : string tuple
    def runComparison(self,f,comps):
        print "Comparision initialized."
        focal = self.getClass(f)
        comparisons = self.loadClassTuple(comps)
        
        total_ten = 0
        total_five = 0
        total_two = 0
        total_one = 0
        for text in self.texts:
            file = open('/Users/bucci/reports/' + text.id + '_' + focal.id + '_x_' + comparisons[0].id + '_sentence.csv', 'w')
            text.generateCorrelationProfile(focal,comparisons)
            ten = 0
            five = 0
            two = 0
            one = 0
            for cp in text.profiles:
                ten = ten + cp.countMatchesInSentenceWithinCost(10,comparisons[1])
                five = five + cp.countMatchesInSentenceWithinCost(5,comparisons[1])
                two = two + cp.countMatchesInSentenceWithinCost(2,comparisons[1])
                one = one + cp.countMatchesInSentenceWithinCost(1,comparisons[1])
            file.write("10" + ", " + str(ten) + "\n")
            file.write("5" + ", " + str(five) + "\n")
            file.write("2" + ", " + str(two) + "\n")
            file.write("1" + ", " + str(one) + "\n")
            file.close()
            
            total_ten = total_ten + ten
            total_five = total_five + five
            total_two = total_two + two
            total_one = total_one + one
        
        summary = open('/Users/bucci/reports/' + text.id + '_' + focal.id + '_x_' + comparisons[0].id + '_sentence_summary.csv', 'w')
        summary.write("10" + ", " + str(total_ten) + "\n")
        summary.write("5" + ", " + str(total_five) + "\n")
        summary.write("2" + ", " + str(total_two) + "\n")
        summary.write("1" + ", " + str(total_one) + "\n")
    
    ## Command definitions ##
    def do_hist(self, args):
        """Print a list of commands that have been entered"""
        print self._hist
    
    def do_exit(self, args):
        """Exits from the console"""
        return -1
    
    ## Command definitions to support Cmd object functionality ##
    def do_EOF(self, args):
        """Exit on system end of file character"""
        return self.do_exit(args)
    
    def do_shell(self, args):
        """Pass command to a system shell when line begins with '!'"""
        os.system(args)
    
    def do_help(self, args):
        """Get help on commands
            'help' or '?' with no arguments prints a list of commands for which help is available
            'help <command>' or '? <command>' gives help on <command>
            """
        ## The only reason to define this method is for the help text in the doc string
        cmd.Cmd.do_help(self, args)
    
    ## Override methods in Cmd object ##
    def preloop(self):
        """Initialization before prompting user for commands.
            Despite the claims in the Cmd documentaion, Cmd.preloop() is not a stub.
            """
        cmd.Cmd.preloop(self)   ## sets up command completion
        self._hist    = []      ## No history yet
        self._locals  = {}      ## Initialize execution namespace for user
        self._globals = {}
    
    def postloop(self):
        """Take care of any unfinished business.
            Despite the claims in the Cmd documentaion, Cmd.postloop() is not a stub.
            """
        cmd.Cmd.postloop(self)   ## Clean up command completion
        print "Exiting..."
    
    def precmd(self, line):
        """ This method is called after the line has been input but before
            it has been interpreted. If you want to modifdy the input line
            before execution (for example, variable substitution) do it here.
            """
        self._hist += [ line.strip() ]
        return line
    
    def postcmd(self, stop, line):
        """If you want to stop the console, return something that evaluates to true.
            If you want to do some post command processing, do it here.
            """
        return stop
    
    def emptyline(self):
        """Do nothing on empty input line"""
        pass
    
    def default(self, line):
        """Called on an input line when the command prefix is not recognized.
            In that case we execute the line as Python code.
            """
        try:
            exec(line) in self._locals, self._globals
        except Exception, e:
            print e.__class__, ":", e

if __name__ == '__main__':
    console = ParseHandler()
