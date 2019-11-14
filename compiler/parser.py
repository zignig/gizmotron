from __future__ import unicode_literals

import os
import arpeggio
from arpeggio import *
from arpeggio import RegExMatch as _

from ast import *


def comment():
    return [_("//.*"), _("/\*.*\*/")]


def literal():
    return _(r'\d*\.\d*|\d+|".*?"')


def symbol():
    return _(r"\w+")


def asg():
    return ":="


def assign():
    return symbol, asg, expression


def operator():
    return _(r"\+|\-|\*|\/|\=\=")


def operation():
    return symbol, operator, [literal, functioncall]


def expression():
    return [literal, operation, functioncall]


def expressionlist():
    return expression, ZeroOrMore(",", expression)


def returnstatement():
    return Kwd("return"), expression


def whilestatement():
    return Kwd("while"), "(", expression, ")", block


def ifstatement():
    return Kwd("if"), "(", expression, ")", block


def ifelsestatement():
    return Kwd("if"), "(", expression, ")", block, Kwd("else"), block


def functioncall():
    return symbol, parameterlist

def const() : return Kwd("const"),symbol,symbol
def var() : return Kwd("var"),symbol,symbol

def statement():
    return (
        [
            const,
            var,
            assign,
            whilestatement,
            ifelsestatement,
            ifstatement,
            functioncall,
            returnstatement,
        ],
        semi,
    )


def block():
    return "{", ZeroOrMore(statement), "}"


def semi():
    return Kwd(";")


def comma():
    return ","


def parameterlist():
    return "(", ZeroOrMore(symbol, sep=comma), ")"


def function():
    return Kwd("def"), symbol, parameterlist, block

def task():
    return Kwd("task"),symbol,block

def program():
    return OneOrMore([function,task]), EOF


# Grammar

# def symbol():           return _(r"\w+")
# def var():              return _(r"\w+")
# def number():           return _(r"\d+")
# def stringer():         return '"', _(r'((\\")|[^"])*'),'"'
# def ref():              return '@',symbol
# def compare():          return [eq,lt,gt]
# def declare():          return symbol,':=',[number,stringer]
# def eq():               return '=='
# def lt():               return '>'
# def gt():               return '<'
# def assign():           return symbol,'=',[number,ref,symbol,stringer]
# def call():             return symbol,'(',')'
# def section():          return ":",symbol,ZeroOrMore([section,assign,declare,call]),';'
# def comment():          return [_("//.*"), _("/\*.*\*/")]

# def program():          return section,EOF


class Vis(PTNodeVisitor):
    def visit_task(self,node,children):
        return Task(node,children=children)

    def visit_const(self,node,children):
        return Const(node,children=chidren)

    def visit_var(self,node,children):
        return Var(node,children=children)

    def visit_program(self, node, children):
        # print("\tfunction",node,children)
        return Program(node, children=children)

    def visit_function(self, node, children):
        # print("\tfunction",node,children)
        return Function(node, children=children)

    def visit_block(self, node, children):
        # print('\tblock',node,children)
        b = Block(node, children=children)
        b.statments = children
        return b

    def visit_expression(self, node, children):
        # print('\texpression',node,children)
        return Expression(node, children=children)

    def visit_literal(self, node, children):
        # print('\tliteral',node,children)
        return Literal(node, children=children)

    def visit_symbol(self, node, children):
        # print('\tsymbol',node,children)
        return Symbol(node, children=children)

    def visit_whilestatement(self, node, children):
        # print('\twhile',node,children)
        return While(node, children=children)

    def visit_ifstatement(self, node, children):
        # print('\tif',node,children)
        return If(node, children=children)

    def visit_functioncall(self, node, children):
        # print('\tfunction call',node,children)
        c = Call(node, children=children)
        c.name = children[0]
        return c

    def visit_parameterlist(self, node, children):
        # print('\tparameter list ',node,children)
        return Parameters(node, children=children)

    def visit_assign(self, node, children):
        # print('\tassign',node,children)
        return Assign(node, children=children)

    def visit_statement(self, node, children):
        # print('\tstatement ',node,children)
        return Statement(node, children=children)

    def visit_operation(self, node, children):
        # print('\tOperation',node,children)
        return Operation(node, children=children)

    def visit_operator(self, node, children):
        # print('\tOperator',node,children)
        return Operator(node, children=children)

    def visit_comma(self, node, children):
        pass


"""
    def visit_call(self,node,children):
        return Call(node,children=children)

 
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

    def visit_declare(self,node,children):
        return Declare(node,children=children)

    def visit_stringer(self,node,children):
        return Stringer(node,text=children[0])

    def visit_number(self,node,children):
        return Number(node,children=children)
"""


def parse(file_name, debug=False):
    # Load test program from file
    current_dir = os.path.dirname(__file__)
    test_program = open(os.path.join(current_dir, file_name)).read()
    # Parser instantiation. simpleLanguage is the definition of the root rule
    # and comment is a grammar rule for comments.
    parser = ParserPython(program, comment, debug=debug, reduce_tree=True)
    parse_tree = parser.parse(test_program)
    result = visit_parse_tree(parse_tree, Vis(debug=debug))
    return result
