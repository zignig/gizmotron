#
# This example shows how to write a basic JSON parser
#
# The code is short and clear, and outperforms every other parser (that's written in Python).
# For an explanation, check out the JSON parser tutorial at /docs/json_tutorial.md
#

import sys

from lark import Lark, Transformer, v_args
import pprint

json_grammar = r"""
    ?start: _NL* begin_tag content+ end_tag
    
    _brac: "{" content* "}" 
    ?tag: "\\" NAME _brac? -> tag
    ?dbs: "\\\\" 
    begin_tag: "\\" "begin" _brac
    end_tag: "\\" "end" _brac
    COMMA: ","
    MINUS: "-"
    DOT: "." | "+" | ":"
    AMP: "&"
    AST:"*"
    WWA: WORD  AST 
    ARR: "←"
    SQB: "[" | "]"
    ?text: ARR | WWA | WORD | NUMBER | COMMA | MINUS | DOT |  AMP  | SQB -> text
    ?content:  begin_tag | tag | _brac | dbs | text+ | end_tag

    _NL: /[\r\n]+/

    %import common.WS 
    %import common.WORD
    %import common.NUMBER
    %ignore WS
    %ignore _NL
    %import common.CNAME -> NAME
"""

class TreeIndenter(Indenter):
    NL_type = '_NL'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 8

class Base:
    pass

class Tag(Base):
    def __init__(self,items):
        self.name = items[0]
        if len(items) > 1:
            self.value = items[1]
        else:
            self.value = ""

    def __repr__(self): 
        return "Tag: " + self.name + "->" + str(self.value)

class tr(Transformer):
    def content(self,items):
        d = ""
        for i in items:
            d += str(i)+' '
        return d
    
    def tag(self,items):
        print(items)
        return Tag(items)

json_parser = Lark(json_grammar, parser='lalr',transformer=tr())

parse = json_parser.parse
file_name = "/opt/FPGA/Boneless-CPU/doc/manual/insns/ADJW.tex"
#file_name = "ADD.tex"

if __name__ == '__main__':
    print(file_name)
    f = open(file_name)
    t = parse(f.read())
    print(t.pretty())

