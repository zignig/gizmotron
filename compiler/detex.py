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

def comment():          return _(r"\\\\")

def tex():              return command 

#def operation():        return symbol, operator, [literal, functioncall]
#def assignment():       return symbol, _(r":\="),expression
#def expression():       return [literal, operation, functioncall]
#def expressionlist():   return expression, ZeroOrMore(",", expression)
#def returnstatement():  return Kwd("return"), expression
#def ifstatement():      return Kwd("if"), "(", expression, ")", block
#def ifelsestatement():      return Kwd("if"), "(", expression, ")", block, Kwd("else"), block
#def statement():        return [ifelsestatement, ifstatement,returnstatement,assignment], ";"
#def parameterlist():    return "(", symbol, ZeroOrMore(",", symbol), ")"
#def functioncall():     return symbol, "(", expressionlist, ")"
#def function():         return Kwd("function"), symbol, parameterlist, block
#def program():          return Kwd("program"), symbol , ZeroOrMore(function), Kwd("end")
#def simpleLanguage():   return program 


class Vis(PTNodeVisitor):
    f = {}

    #def visit_literal(self,node,children): print(node,children)
    #def visit_operator(self,node,children): print(node,children)
    #def visit_functioncall(self,node,children): print(node,children)
    #def visit_expression(self,node,children): print(node,children)
    #def visit_ifstatement(self,node,children): print(node,children)
    #def visit_ifelsestatement(self,node,children): print(node,children)
#    def visit_simpleLanguage(self,node,children):
#        print("lang->",children)
#        return children
#
#    def visit_block(self,node,children):
#        return children
#
#    def visit_program(self,node,children): 
#        print("prog->",children)
#
#    def visit_function(self,node,children):
#        name = children[0]
#        if name not in self.f:
#            self.f[name] = "FNORD"
#        print(node,"->",children)
#        return (children[0])

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
