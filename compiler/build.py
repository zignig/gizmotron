
import comp
import registers


class Program:
    def __init__(self,file_name='test.prg'):
        self.file_name = file_name
        self.result = comp.parse(self.file_name)

    def build(self):
        print("GO")




p = Program()
p.build()
