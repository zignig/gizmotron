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
def assign():           return symbol,'->',[symbol,literal]
def section():          return ":",symbol,OneOrMore([assign,subsection,ref]),';'
def program():             return ZeroOrMore(section),EOF

def comment():          return [_("//.*"), _("/\*.*\*/")]

class Fail(BaseException):
    pass

class Entry:
    symbol_dict = {}
    section_dict = {}
    def __init__(self,value,children=None):
        self.value = value
        self._more = False
        if children is not None:
            self._more = True
        self.children = children

    def parse(self):
        print('no parse',type(self),self.value)

    def eval(self):
        #self.parse()
        if self._more:
            for i in self.children:
                i.eval()

class Symbol(Entry):
    def parse(self):
        print(type(self.value),self.value)
        if self.value not in self.symbol_dict:
            self.symbol_dict[self.value] = 'gotcha'
    
class Subsection(Entry):
    pass 

class Ref(Entry):
    pass

class Section(Entry):
    def parse(self):
        print(self.value)
 
class Assign(Entry):
    pass


class Vis(PTNodeVisitor):

    def visit_symbol(self,node,children):
        print(self,node,children)
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

