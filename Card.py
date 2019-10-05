"""
Card.py
Defines the class Card, a class to read card files for general input information
Input information to be used in simulation
""" #docstring

import sys
import shlex

class Card(dict):

    def __init__(self, filename):
        self.name = filename
        self.ParseFile(filename)

    def ParseFile(self, filename):
        infile = open(filename,'r')
        for line in infile:
            hashtag = line.find('#')
            line = line[:hashtag]

            if line.strip().endswith('Start'):
                keyPos = line.rfind('Start')
                keyVal = line[:keyPos]
                self[keyVal] = ''
                for line in infile:
                    if line.startswith('%sEnd'%(keyVal)):
                        break
                    self[keyVal] += line

            words = shlex.split(line)
            if len(words) < 2:
                continue
            if len(words) > 2 and not words[2].startswith('#'):
                continue
            self[words[0]] = words[1]

    def Print(self):
        print(repr(self))

    def __repr__(self):
        out = str(self)
        for info in self:
            out += "\n{!s}: {!s}".format(info, self[info])
        return out

    def GetFileName(self):
        return self.name

    def __str__(self):
        return "Card info from file: {}".format(self.name)

    def Has(self,info):
        return (info in self)


    def Get(self,info):
        if not self.Has(info):
            print( info, 'not found in card', self.name)
            sys.exit()
        return self[info]


