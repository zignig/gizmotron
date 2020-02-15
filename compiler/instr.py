#
# This example shows how to write a basic JSON parser
#
# The code is short and clear, and outperforms every other parser (that's written in Python).
# For an explanation, check out the JSON parser tutorial at /docs/json_tutorial.md
#

import sys

from lark import Lark, Transformer, v_args

json_grammar = r"""
    ?start: _NL* content+
    
    bs: "\\"
    ?brac: "{" content* "}" 
    ?tag: bs NAME brac? -> tag
    ?dbs: "\\\\" 
    COMMA: ","
    MINUS: "-"
    DOT: "." | "+"
    AMP: "&"
    AST:"*"
    WWA: WORD  AST 
    ARR: "←"
    ?text: ARR | WWA | WORD | NUMBER | COMMA | MINUS | DOT |  AMP 
    ?content:  tag | brac | dbs | text+ 

    _NL: /[\r\n]+/

    %import common.WS 
    %import common.WORD
    %import common.NUMBER
    %ignore WS
    %ignore _NL
    %import common.CNAME -> NAME
"""

class tr(Transformer):
    def content(self,items):
        d = ""
        for i in items:
            d += str(i)+' '
        return d
    
#    def text(self,items):
        print(items)

json_parser = Lark(json_grammar, parser='lalr',transformer=tr())

parse = json_parser.parse
file_name = "/opt/FPGA/Boneless-CPU/doc/manual/insns/CMPI.tex"
#file_name = "ADD.tex"

if __name__ == '__main__':
    print(file_name)
    f = open(file_name)
    t = parse(f.read())
    print(t)

