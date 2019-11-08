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
def comment():          return [_("//.*"), _("/\*.*\*/")]
def literal():          return _(r'\d*\.\d*|\d+|".*?"')
def symbol():           return _(r"\w+")
def asg():              return _(r":=")
def assign():           return symbol,asg,expression
def operator():         return _(r"\+|\-|\*|\/|\=\=")
def operation():        return symbol, operator, [literal, functioncall]
def expression():       return [literal, operation, functioncall]
def expressionlist():   return expression, ZeroOrMore(",", expression)
def returnstatement():  return Kwd("return"), expression
def ifstatement():      return Kwd("if"), "(", expression, ")", block
def ifelsestatement():  return Kwd("if"), "(", expression, ")", block, Kwd("else"), block
def functioncall():     return symbol,parameterlist
def statement():        return [assign,ifelsestatement,ifstatement,functioncall,returnstatement], ";"
def block():            return "{", OneOrMore(statement), "}"
def parameterlist():    return "(", symbol, ZeroOrMore(",", symbol), ")"
def function():         return Kwd("function"), symbol, parameterlist, block
def simpleLanguage():   return OneOrMore(function),EOF


class instr:
    def __repr__(self):
        return ""

class iffer(instr):
    def __init__(self,condition,statement,elses=None):
        self.condition = condition
        self.statement = statement
        self.elses = elses

class fcall:
    def __init__(self,name,param):
        self.name = name
        self.param = param

class lit:
    def __init__(self,value):
        self.value = value

class op:
    def __init__(self,op):
        self.op = op

class sym:
    # all symbols are global
    s = {}
    def __init__(self,symb):
        self.symbol = symb
        if symb not in self.s:
            self.s[symb] = self

class param:
    def __init__(self,l):
        self.parameters = l
        
class fun:
    def __init__(self,name,params,statements):
        self.name = name 
        self.params = params
        self.statements = statements

    def eval(self):
        for i in self.statements:
            print(i)
            #i.eval()

class assignc:
    def __init__(self,left,right):
        self.left = left
        self.right = right

class Vis(PTNodeVisitor):

    def visit_ifstatement(self,node,children):
        #print('if',node,children)
        return iffer(children[0],children[1])

    def visit_ifelsestatement(self,node,children):
        #print('ifelse',node,children)
        return iffer(children[0],children[1],elses=children[2])

    def visit_assign(self,node,children):
        #print('assignment',node,children)
        return assignc(children[0],children[2])

    def visit_symbol(self,node,children):
        #print(node.value)
        return sym(node.value)

    def visit_parameterlist(self,node,children):
        #print('param',children)
        return param(children)

    def visit_literal(self,node,children):
        #print('lit',node,children)
        return lit(node)

    def visit_statement(self,node,children):
        #print('statement',node,children)
        return children

    def visit_block(self,node,children):
        return children
    
    def visit_operator(self,node,children):
        return op(node)

    def visit_expression(self,node,children):
        #print('expr', node,children)
        return children

    def visit_function(self,node,children):
        print('fun',children)
        return fun(children[0],children[1],children[2])

    def visit_functioncall(self,node,children):
        #print("call",node,children)
        return None

    def visit_simpleLanguage(self,node,children):
        return children

debug=False
# Load test program from file
current_dir = os.path.dirname(__file__)
test_program = open(os.path.join(current_dir, 'program.simple')).read()

# Parser instantiation. simpleLanguage is the definition of the root rule
# and comment is a grammar rule for comments.
parser = ParserPython(simpleLanguage, comment, debug=debug)

parse_tree = parser.parse(test_program)
#print(parse_tree)
result = visit_parse_tree(parse_tree,Vis(debug=debug))
for i in result:
    print(i.eval())
print(sym.s.keys())
