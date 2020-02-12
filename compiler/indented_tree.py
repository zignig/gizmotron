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
    ?start: _NL* task* func* menu*

    menu : "menu" NAME ":"  _NL [_INDENT tree+ _DEDENT]
    func: "func" NAME ":" _NL [_INDENT tree+ _DEDENT]
    task: "task" NAME ":" _NL [_INDENT tree+ _DEDENT] 

    tree: NAME _NL [_INDENT tree+ _DEDENT]

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
        print(self.name)
        if self.children is not None:
            for i in self.children:
                i.show()

class Menu(Base):
    pass

class Tree(Base):
    pass

class AutoBot(Transformer):
    def menu(self,items):
        return Menu(items[0],children=items[1:])


    def tree(self,items):
        return Tree(items[0],children=items[1:])

    def task(self,items):
        print("task",items)
        pass 

parser = Lark(tree_grammar, parser='lalr', postlex=TreeIndenter(),transformer=AutoBot())

test_tree = """
menu main:
    config
        boot
        run
        test
    doc
        howto
            one
                blah
                balh
                asdf
            two
            three
        testing
    demo
        blinky
        screen
        abc
"""

def test():
    t = parser.parse(test_tree)
    return t

if __name__ == '__main__':
    m  = test()
    m.show()
    
    
