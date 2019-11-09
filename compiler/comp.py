from __future__ import unicode_literals

import os
import arpeggio
from arpeggio import *
from arpeggio import RegExMatch as _

from ast import *
# Grammar
def symbol():           return _(r"\w+")
def var():              return _(r"\w+")
def literal():          return _(r'\d*\.\d*|\d+|".*?"')
def ref():              return '@',symbol
def compare():          return [eq,lt,gt]
def declare():          return symbol,'as',var
def eq():               return '=='
def lt():               return '>'
def gt():               return '<'
def assign():           return symbol,'<-',[ref,symbol,literal]
def section():          return ":",symbol,ZeroOrMore([section,assign,declare,ref,symbol]),';'
def comment():          return [_("//.*"), _("/\*.*\*/")]

def program():          return section,EOF



class Vis(PTNodeVisitor):

    def visit_symbol(self,node,children):
        return Symbol(node) 
 
    def visit_var(self,node,children):
        return Var(node) 

    def visit_section(self,node,children):
        return Section(node,children=children)

    def visit_ref(self,node,children):
        return Ref(node)

    def visit_trie(self,node,children):
        return Section(node,children=children)

    def visit_assign(self,node,children):
        return Assign(node,children=children)

    def visit_literal(self,node,children):
        return Literal(node,children=children)

    def visit_declare(self,node,children):
        return Declare(node,children=children)


def parse(file_name):
    debug=False
    # Load test program from file
    current_dir = os.path.dirname(__file__)
    test_program = open(os.path.join(current_dir, file_name)).read()

    # Parser instantiation. simpleLanguage is the definition of the root rule
    # and comment is a grammar rule for comments.
    parser = ParserPython(program, comment, debug=debug)
    parse_tree = parser.parse(test_program)
    result = visit_parse_tree(parse_tree,Vis(debug=debug))
    result.eval()
    return result
