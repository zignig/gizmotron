from boneless.arch.opcode import *

__all__ = [
    "Assign",
    "Entry",
    "Symbol",
    "Ref",
    "Declare",
    "Var",
    "Call",
    "Stringer",
    "Number",
    "Function",
    "Parameters",
    "Expression",
    "Literal",
    "Statement",
    "Block",
    "Operator",
    "Operation",
    "If",
    "Program",
]    


class Fail(BaseException):
    pass


class Redeclaration(BaseException):
    pass


class NoBuild(BaseException):
    pass


class MetaEntry(type):
    overview = {}

    def __new__(cls, clsname, bases, attrs):
        newclass = super(MetaEntry, cls).__new__(cls, clsname, bases, attrs)
        cls.register(newclass)  # here is your register function
        return newclass
    
    def register(cls):
        if cls not in MetaEntry.overview:
            MetaEntry.overview[cls] = 0


class Entry(metaclass=MetaEntry):
    symbol_dict = {}
    sections = {}
    declarations = {}
    variables = {}

    def __init__(self, value, children=None,text=None):
        self.value = value
        self._more = False
        self.name = None
        self.text = text
        if children is not None:
            self._more = True
        self.children = children

    def parse(self):
        print("no parse", type(self), self.value)

    def generate(self):
        print("generate for ", self)

    def build(self):
        print("no build for", self)
        print(self.value)
        yield []

    def make(self):
        print("no make for",self)
        yield []

    def eval(self):
        self.parse()
        if self._more:
            for i in self.children:
                i.eval()

    def show(self, depth=0):
        for i in range(depth):
            print("  ", end="")
        print(type(self).__qualname__,self.value)
        if self._more:
            for i in self.children:
                if isinstance(i,Entry):
                    i.show(depth=depth + 1)
                else:
                    print("fail on type ",type(i),i)

    def sweep(self, fn):
        print(self.__dict__)
        yield fn(self)
        if self._more:
            for i in self.children:
                yield from i.sweep(fn)

    def __repr__(self):
        return str(type(self)) + "--" + str(self.name)


# individual action classes

class Program(Entry):
    pass 

class If(Entry):
    pass

class Operator(Entry):
    pass

class Operation(Entry):
    pass

class Block(Entry):
    def parse(self):
        self.statements = self.children

    
    def build(self):
        for i in self.statements:
            print('build -->',i)
            yield from i

class Expression(Entry):
    pass

class Literal(Entry):
    pass


class Statement(Entry):
    pass

class Stringer(Entry):
    def parse(self):
        pass 

    def make(self):
        l = len(self.text)
        t = [] 
        for i in self.text:
            t.append(ord(i)) 
        yield [l,t]

class Number(Entry):
    def parse(self):
        self.value= int(self.value.value)

    def make(self):
        yield self.value

class Symbol(Entry):
    def parse(self):
        self.name = self.value.value
        if self.value.value not in self.symbol_dict:
            self.symbol_dict[self] = self.text


class Assign(Entry):
    def parse(self):
        if len(self.children) != 2:
            raise Fail(self)
        self.lhs = self.children[0]
        self.rhs = self.children[1]

class Parameters(Entry):
    pass

class Ref(Entry):
    pass


class Declare(Entry):
    def parse(self):
        target = self.children[0]
        self.name = target.value.value
        self.target = self.children[1] 
        if self.name not in self.declarations:
            self.declarations[self.name] = self 
        else:
            raise Redeclaration(target)
        if self.name not in self.variables:
            self.variables[self.name] = self.target

    def build(self):
        yield [] 

    def make(self):
        yield L(self.name)
        yield from self.target.make()


class Var(Entry):
    def make(self):
        yield 0


class Call(Entry):
    def parse(self):
        self.name = self.children[0].value

    def build(self):
        yield JAL(R7, str(self.name))


class Function(Entry):
    def parse(self):
        self._called = False
        self.statements = []
        self.name = self.children[0].value.value
        self.statements = self.children[1:]
        if self not in self.sections:
            self.sections[self.name] = self

    def build(self):
        yield L(self.name)
        for i in self.statements:
            # don't build sections , they are written at the top
            if type(i) is not Function:
                yield from i.build()
        yield JR(R7, 0)
