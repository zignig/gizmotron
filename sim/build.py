from boneless.arch import opcode

from jinja2 import Template
# get the dict of instructiosn

d = opcode.J.mnemonics
opcodes = list(d.keys())

tmpl = """
from .simi import SimInstr

class Missing(BaseException):
    pass

{% for name in names -%}
class s_{{name}}(SimInstr):
    def run(self):
        raise Missing(self)


{% endfor %}

# dict 
d = {
{% for name in names %} "{{name}}" : s_{{name}},
{% endfor %}
}
"""
t = Template(tmpl)
print(t.render(names=opcodes))
