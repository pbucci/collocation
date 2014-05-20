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
from text import *
from characterclass import *
import sys

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
    
    # Creates a TextMeta object
    def loadText(self,textpath):
        t = TextHandler(textpath,self)
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
    def setTextDirectory(self,path):
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
    
    ## Command definitions ##

    # Prints available classes
    def do_classes(self,line):
        for c in self.classes:
            print c.id
    
    def do_load(self,line):
        self.setTextDirectoryPath(line)
        self.loadAllTexts()
    
    def do_generate_profiles(self,line):
        for t in self.texts:
            t.generateNodeProfile(line)
    
    def do_print_dirpath(self,line):
        print self.dirpath
    
    def do_set_max(self,line):
        self.maxcost = line
        print "Max cost set to " + line
    
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
    console.cmdloop()