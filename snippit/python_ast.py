import ast

txt = """
def thing(num):
    for i in range(num):
        print(i)
"""

r = ast.parse(txt)
print(r)


class sweep(ast.NodeVisitor):
    data = []

    def generic_visit(self, node):
        print(node, type(node).__qualname__)
        ast.NodeVisitor.generic_visit(self, node)
        self.data.append(node)


#    def visit_FunctionDef(self,node):
#        print(node.body)
#    def visit_Load(self,node):
#        print('->',node,dir(node))

#    def visit_Store(self,node):
s = sweep()
print(dir(s))
s.visit(r)
