__all__ = ['Assign','Entry','Symbol','Ref','Declare','Var','Section']

class Fail(BaseException):
    pass

class Entry:
    symbol_dict = {}
    section_dict = {}
    def __init__(self,value,children=None):
        self.value = value
        self._more = False
        self.name = None
        if children is not None:
            self._more = True
        self.children = children

    def parse(self):
        print('no parse',type(self),self.value)

    def generate(self):
        print('generate for ',self)

    def eval(self,depth=0):
        self.parse()
        for i in range(depth):
            print('\t',end='')
        print(self.name,type(self),self.value)
        if self._more:
            for i in self.children:
                i.eval(depth=depth+1)

    def sweep(self,fn):
        print(self.__dict__)
        yield fn(self)
        if self._more:
            for i in self.children:
                yield from i.sweep(fn)
        
    def __repr__(self):
       return str(type(self))+"--"+str(self.name)+"\n"


# individual action classes 

class Symbol(Entry):
    def parse(self):
        self.name = self.value.value
        if self.value.value not in self.symbol_dict:
            self.symbol_dict[self.value.value] = self 

class Assign(Entry):
    def parse(self):
        print(self.children)
        if len(self.children) != 2:
            raise Fail(self)
        self.lhs = self.children[0]
        self.rhs = self.children[1] 
    pass
    
class Ref(Entry):
    pass

class Declare(Entry):
    def parse(self):
        print("declaration")
    pass

class Var(Entry):
    pass

class Section(Entry):
    def parse(self):
        print('section')
        self._called = False
        self.name = self.children[0].value.value
        if self not in self.section_dict:
            self.section_dict[self] = self
