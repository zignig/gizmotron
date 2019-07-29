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
from arpeggio import *
from arpeggio import RegExMatch as _

# Grammar
def esc():          return _(r'\\')

def symbol():           return _(r"\w+")
def amp():              return _(r"\&")
def text():             return _(r'((\\")|[^{}])+')
def block():            return "{", ZeroOrMore([amp,command,text]) , "}"
def command():          return esc,symbol,ZeroOrMore([block,text])

def comment():          return _(r"424323423")

def tex():              return command ,EOF


class Vis(PTNodeVisitor):
    f = {}

    def visit_symbol(self,node,children): print('symbol->',node,children)
    def visit_amp(self,node,children): print('&->',node,children)
    def visit_block(self,node,children): print('block->',node,children)
    def visit_command(self,node,children): print('command->',node,children)
    def visit_tex(self,node,children): print('tex->',node,children)

debug=False
# Load test program from file
current_dir = os.path.dirname(__file__)
test_program = open(os.path.join(current_dir, 'ROLI.tex')).read()

# Parser instantiation. simpleLanguage is the definition of the root rule
# and comment is a grammar rule for comments.
parser = ParserPython(tex, comment, debug=debug,skipws=False)

parse_tree = parser.parse(test_program)
print(parse_tree)
v = Vis(debug=debug)
result = visit_parse_tree(parse_tree,v)

print(v.f)
print(result)
