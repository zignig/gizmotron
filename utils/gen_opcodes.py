from boneless.arch.opcode import Instr

names = Instr.mnemonics.keys()

text = """
from simi import SimInstr

class Missing(BaseException):
    pass


"""
sim_dict = "sim_dict = {\n" 
for i in names:
    head = "class s_"+i+"(SimInstr):\n"
    head += "   def run(self):\n"
    head += "       raise Missing(self)\n\n"
    text += head
    sim_dict += '\t"'+i+'": s_'+i+',\n'
sim_dict += '}\n'

print(text)
print(sim_dict)
