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
    start_tag: bs "begin(" NAME "}"  
    bs: "\\"
    end_tag: "\\end(" NAME ")"
    br: "{" str "}" 
    tag: "\\" NAME (br)?
    !ampersand: "&"
    !str: /./s
    content: br | ampersand | tag | str 

    %import common.CNAME -> NAME
    %import common.WS_INLINE
"""


json_parser = Lark(json_grammar, parser='lalr')

parse = json_parser.parse
file_name = ""

if __name__ == '__main__':
    # test()
    with open(sys.argv[1]) as f:
        print(parse(f.read()))
