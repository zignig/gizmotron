#
# This example shows how to write a basic JSON parser
#
# The code is short and clear, and outperforms every other parser (that's written in Python).
# For an explanation, check out the JSON parser tutorial at /docs/json_tutorial.md
#

import sys

from lark import Lark, Transformer, v_args

json_grammar = r"""
    ?start: _NL* content*
    
    bs: /\\/                  
    brac: "{" content* "}" 
    str: /./+
    tag: bs NAME brac? -> tag
    dbs: "\\\\" 
    comma: ","
    ampersand: "&"
    content: tag | brac | NAME | comma | ampersand | dbs | str

    _NL: /[\r\n]+/

    %import common.WS 
    %ignore WS
    %ignore _NL
    %import common.CNAME -> NAME
"""


_json_grammar = r"""
    ?start: _NL* main 
    
    main: tag 
    bs: /\\/
    tag: bs NAME brac?
    _NL: /[\r\n]+/
    brac: "{" content+ "}" 
    content: str
    str: /./

    %import common.WS 
    %ignore WS
    %ignore _NL
    %import common.CNAME -> NAME
"""
json_parser = Lark(json_grammar, parser='lalr')

parse = json_parser.parse
file_name = "/opt/FPGA/Boneless-CPU/doc/manual/insns/ADD.tex"
#file_name = "ADD.tex"

if __name__ == '__main__':
    f = open(file_name)
    t = parse(f.read())
    print(t.pretty())

