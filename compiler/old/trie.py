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
def nl():
    return "\n"


def symbol():
    return _(r"\w+")


def subsection():
    return "-", symbol, nl


def ref():
    return "@", symbol, nl


def section():
    return ":", symbol, nl, OneOrMore([subsection, ref])


def trie():
    return OneOrMore(section), EOF


def comment():
    return [_("//.*"), _("/\*.*\*/")]


class Entry:
    def __init__(self, value, children=None):
        self.value = value
        self._more = False
        if children is not None:
            self._more = True
        self.children = children

    def eval(self):
        print(self.value)
        if self._more:
            for i in self.children:
                i.eval()


class Symbol(Entry):
    pass


class Subsection(Entry):
    pass


class Ref(Entry):
    pass


class Section(Entry):
    pass


class Vis(PTNodeVisitor):
    def visit_symbol(self, node, children):
        # print('symbol->',node,children)
        return Symbol(node)

    def visit_section(self, node, children):
        print("section->", children)
        return Section(node, children=children)

    def visit_subsection(self, node, children):
        print("subsection->", children)
        return Subsection(node, children)

    def visit_ref(self, node, children):
        # print('ref->',node,children)
        return Ref(node)

    def visit_trie(self, node, children):
        return Section(node, children=children)


debug = False
# Load test program from file
current_dir = os.path.dirname(__file__)
test_program = open(os.path.join(current_dir, "menu.tri")).read()

# Parser instantiation. simpleLanguage is the definition of the root rule
# and comment is a grammar rule for comments.
parser = ParserPython(trie, comment, debug=debug, ws="\t\r ")

parse_tree = parser.parse(test_program)
print(parse_tree)
result = visit_parse_tree(parse_tree, Vis(debug=debug))
print(result)
result.eval()
