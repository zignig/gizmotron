#
# This example shows how to write a basic JSON parser
#
# The code is short and clear, and outperforms every other parser (that's written in Python).
# For an explanation, check out the JSON parser tutorial at /docs/json_tutorial.md
#

import sys

from lark import Lark, Transformer, v_args

json_grammar = r"""
    ?start: _NL* main 
    
    main: tag content+ tag
    bs: "\\"
    brac: "{" content+ "}" 
    str: /./+
    tag: bs NAME
    dbs: "\\\\" 
    comma: ","
    ampersand: "&"
    content: str| tag | brac | NAME | comma  | ampersand | dbs

    _NL: /[\r\n]+/

    %import common.WS 
    %ignore WS
    %ignore _NL
    %import common.CNAME -> NAME
"""


json_parser = Lark(json_grammar, parser='lalr')

parse = json_parser.parse
file_name = "/opt/FPGA/Boneless-CPU/doc/manual/insns/ADD.tex"

if __name__ == '__main__':
    f = open(file_name)
    print(parse(f.read()))
