#
# This example shows how to write a basic JSON parser
#
# The code is short and clear, and outperforms every other parser (that's written in Python).
# For an explanation, check out the JSON parser tutorial at /docs/json_tutorial.md
#

import sys,os

from lark import Lark, Transformer, v_args
import pprint


from boneless.arch import opcode

from jinja2 import Template
# get the dict of instructiosn

d = opcode.J.mnemonics
opcodes = list(d.keys())

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
path = "/opt/FPGA/Boneless-CPU/doc/manual/insns"

def parse_file(file_name,path=path):
    print(file_name)
    f = open(path+os.sep+file_name)
    t = parse(f.read())
    print(t.pretty())

if __name__ == '__main__':
    parse_file("J.tex",path=path)
    #for i in  opcodes:
    #    print(i)
