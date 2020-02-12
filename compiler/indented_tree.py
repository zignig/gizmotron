#
# This example demonstrates usage of the Indenter class.
#
# Since indentation is context-sensitive, a postlex stage is introduced to
# manufacture INDENT/DEDENT tokens.
#
# It is crucial for the indenter that the NL_type matches
# the spaces (and tabs) after the newline.
#

from lark import Lark,v_args
from lark.indenter import Indenter
from lark import Transformer

tree_grammar = r"""
    ?start: _NL* menu*

    menu : "menu" NAME ":"  _NL [_INDENT heading+ _DEDENT]
    heading: NAME ":" _NL [_INDENT (heading*|item*) _DEDENT]
    item: NAME ("->" NAME)? _NL

    %import common.CNAME -> NAME
    %import common.WS_INLINE
    %declare _INDENT _DEDENT
    %ignore WS_INLINE

    _NL: /(\r?\n[\t ]*)+/
"""

class TreeIndenter(Indenter):
    NL_type = '_NL'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 8

class Base:
    def __init__(self,name,children=None):
        self.name = name.value
        self.children = children

    def show(self):
        self._show(0)

    def _show(self,depth):
        print(depth*2*' ' ,self.name)
        if self.children is not None:
            depth += 1
            for i in self.children:
                i._show(depth)

class Menu(Base):
    pass

class Heading(Base):
    pass

class Item(Base):
    pass

class AutoBot(Transformer):
    def menu(self,items):
        return Menu(items[0],children=items[1:])

    def heading(self,items):
        return Heading(items[0],children=items[1:])

    def item(self,items):
        return Item(items[0],children=items[1:])

parser = Lark(tree_grammar, parser='lalr', postlex=TreeIndenter())#,transformer=AutoBot())

test_tree = """
menu main:
    config:
        boot -> booter 
        run
        test
    help:
        two
        three
    setting:
        asdf
        asdf
    stuff:
    thanks:
"""

def test():
    t = parser.parse(test_tree)
    return t

if __name__ == '__main__':
    m  = test()
    print(m)
    #m.show()
    
    
