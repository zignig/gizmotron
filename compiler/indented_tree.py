#
# This example demonstrates usage of the Indenter class.
#
# Since indentation is context-sensitive, a postlex stage is introduced to
# manufacture INDENT/DEDENT tokens.
#
# It is crucial for the indenter that the NL_type matches
# the spaces (and tabs) after the newline.
#

from lark import Lark
from lark.indenter import Indenter

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

parser = Lark(tree_grammar, parser='lalr', postlex=TreeIndenter())

test_tree = """
task bob:
    one
    two
    three

task error:
    abc
    def
    asdf
    asdf
    asdf

func run:
    a
        b
        b
        b
    asdf

menu main:
    config
        boot
        run
        test
    doc
        howto
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
    t  = test()
    print(t.pretty())
    print(t)
    
