#######################################################################
# Name: calc.py
# Purpose: Simple expression evaluator example
# Author: Igor R. Dejanovic <igor DOT dejanovic AT gmail DOT com>
# Copyright: (c) 2009-2015 Igor R. Dejanovic <igor DOT dejanovic AT gmail DOT com>
# License: MIT License
#
# This example demonstrates grammar definition using python constructs as
# well as using semantic actions to evaluate simple expression in infix
# notation.
#######################################################################

from __future__ import unicode_literals, print_function
try:
    text=unicode
except:
    text=str

from arpeggio import Optional, ZeroOrMore, OneOrMore, EOF, \
    ParserPython, PTNodeVisitor, visit_parse_tree
from arpeggio import RegExMatch as _

def number():     return _(r'\d*\.\d*|\d+')
def symbol():           return _(r"\w+")
def factor():     return Optional(["+","-"]), [number,symbol,("(", expression, ")")]
def term():       return factor, ZeroOrMore(["*","/"], factor)
def expression(): return term, ZeroOrMore(["+", "-"], term)
def calc():       return OneOrMore(expression), EOF


class CalcVisitor(PTNodeVisitor):

    def visit_number(self, node, children):
        """
        Converts node value to float.
        """
        if self.debug:
            print("Converting {}.".format(node.value))
        return float(node.value)

    def visit_symbol(self,node,children):
        return 

    def visit_factor(self, node, children):
        """
        Applies a sign to the expression or number.
        """
        if self.debug:
            print("Factor {}".format(children))
        if len(children) == 1:
            return children[0]
        sign = -1 if children[0] == '-' else 1
        return sign * children[-1]

    def visit_term(self, node, children):
        """
        Divides or multiplies factors.
        Factor nodes will be already evaluated.
        """
        if self.debug:
            print("Term {}".format(children))
        term = children[0]
        for i in range(2, len(children), 2):
            if children[i-1] == "*":
                term *= children[i]
            else:
                term /= children[i]
        if self.debug:
            print("Term = {}".format(term))
        return term

    def visit_expression(self, node, children):
        """
        Adds or substracts terms.
        Term nodes will be already evaluated.
        """
        if self.debug:
            print("Expression {}".format(children))
        expr = children[0]
        for i in range(2, len(children), 2):
            if i and children[i - 1] == "-":
                expr -= children[i]
            else:
                expr += children[i]
        if self.debug:
            print("Expression = {}".format(expr))
        return expr


def main(debug=False):
    # First we will make a parser - an instance of the calc parser model.
    # Parser model is given in the form of python constructs therefore we
    # are using ParserPython class.
    parser = ParserPython(calc)#, debug=debug)

    # An expression we want to evaluate
    input_expr = "bob-(4-1)*5+(2+4.67)+5.89/(.2+7)"

    # We create a parse tree out of textual input_expr
    while(True):
        t = input(">")
        parse_tree = parser.parse(t)
        result = visit_parse_tree(parse_tree, CalcVisitor(debug=debug))
        print(result)

if __name__ == "__main__":
    # In debug mode dot (graphviz) files for parser model
    # and parse tree will be created for visualization.
    # Checkout current folder for .dot files.
    main(debug=False)
