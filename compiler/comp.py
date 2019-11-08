#######################################################################
# Name: simple.py
# Purpose: Simple language based on example from pyPEG
# Author: Igor R. Dejanovic <igor DOT dejanovic AT gmail DOT com>
# Copyright: (c) 2009-2015 Igor R. Dejanovic <igor DOT dejanovic AT gmail DOT com>
# License: MIT License
#
# This example demonstrates grammar definition using python constructs.
# It is taken and adapted from pyPEG project (see http://www.fdik.org/pyPEG/).
#######################################################################

from __future__ import unicode_literals

import os
import arpeggio
from arpeggio import *
from arpeggio import RegExMatch as _

# Grammar
def symbol():           return _(r"\w+")
def literal():          return _(r'\d*\.\d*|\d+|".*?"')
def subsection():       return "-",symbol
def ref():              return '@',symbol
def assign():           return symbol,'->',[ref,symbol,literal]
def section():          return ":",symbol,ZeroOrMore([section,assign,subsection,ref,symbol]),';'
def comment():          return [_("//.*"), _("/\*.*\*/")]

def program():          return section,EOF

class Fail(BaseException):
    pass

class Entry:
    symbol_dict = {}
    section_dict = {}
    def __init__(self,value,children=None):
        self.value = value
        self._more = False
        self.name = None
        if children is not None:
            self._more = True
        self.children = children

    def parse(self):
        print('no parse',type(self),self.value)

    def eval(self,depth=0):
        self.parse()
        for i in range(depth):
            print('\t',end='')
        print(self.name,self.value)
        if self._more:
            for i in self.children:
                i.eval(depth=depth+1)

#    def __repr__(self):
#       return str(self.name)+"--"+str(type(self))+"\n"

class Symbol(Entry):
    def parse(self):
        self.name = self.value.value
        if self.value.value not in self.symbol_dict:
            self.symbol_dict[self.value.value] = self 
    
class Subsection(Entry):
    pass 

class Ref(Entry):
    pass

class Section(Entry):
    def parse(self):
        self.name = self.children[0].value.value
        if self.name not in self.section_dict:
            print(len(self.children))
            if len(self.children) > 2:
                self.section_dict[self] = self.children[2:]
            else:
                self.section_dict[self] = []

class Assign(Entry):
    pass


class Vis(PTNodeVisitor):

    def visit_symbol(self,node,children):
        return Symbol(node) 
 
    def visit_section(self,node,children):
        return Section(node,children=children)

    def visit_subsection(self,node,children):
        return Subsection(node,children)

    def visit_ref(self,node,children):
        return Ref(node)

    def visit_trie(self,node,children):
        return Section(node,children=children)

    def visit_assign(self,node,children):
        return Assign(node,children=children)

    def visit_literal(self,node,children):
        return Literal(node,children=children)

debug=False
# Load test program from file
current_dir = os.path.dirname(__file__)
test_program = open(os.path.join(current_dir, 'test.prg')).read()

# Parser instantiation. simpleLanguage is the definition of the root rule
# and comment is a grammar rule for comments.
parser = ParserPython(program, comment, debug=debug)

parse_tree = parser.parse(test_program)
result = visit_parse_tree(parse_tree,Vis(debug=debug))
result.eval()
print(result.symbol_dict)
print(result.section_dict)
