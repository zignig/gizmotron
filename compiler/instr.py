#
# This example shows how to write a basic JSON parser
#
# The code is short and clear, and outperforms every other parser (that's written in Python).
# For an explanation, check out the JSON parser tutorial at /docs/json_tutorial.md
#

import sys

from lark import Lark, Transformer, v_args

json_grammar = r"""
    ?start: main 
    
    main : (start_tag content+ end_tag)+
    start_tag: bs "begin" br
    bs: "\\"
    end_tag: bs "end" br
    br: "{" str "}" 
    tag: bs str (br)?
    !ampersand: "&"
    !str: /./s
    content: br | ampersand | tag | str 

    %import common.WS_INLINE
"""


json_parser = Lark(json_grammar, parser='lalr')

parse = json_parser.parse
file_name = "/opt/FPGA/Boneless-CPU/doc/manual/insns/ADD.tex"

if __name__ == '__main__':
    f = open(file_name)
    print(parse(f.read()))
