# boneless runtime
from collections import OrderedDict

from registers import Window,VectorTable

from boneless.arch.opcode import *
"""
#Boneless runtime

This is a first cut layout for a boneless runtime.

All references are single words for now

## Info Header

The first 8 words contain program information

0:  high byte, Major Version , bootloader to check
    low  byte, Minor Version , should be compatible within major version

1: program length
2: program start
3: start window 
4: window count 
5: checksum 
6: running task bitfield 
7: task count (0..8) , defined in the next part of the header

## Task Header

code vector to the entry point of the tasks

8: console
9: blinker
10:
11:
12: 
13:
14:
15: 
16:

## Vector Header 

contains relative vector addresses for common code

17: error1
18: error2
19: coredump
20:
21:
22:
23:
24:

## program entry point 

- code goes here
- static content

- heap

#TODO align 8
- window stack
- task windows
- root window (last address % 8)
"""


class BORK(Exception):
    pass

class TaskError(BORK):
    pass

class Task:
    " individual task "
    def __init__(self,name):
        self.name = name
        self.code = []
        
class Scheduler:
    " Upper class for the scheduling "
    pass

class BasicScheduler(Scheduler):
    pass

class Runtime:
    debug = True 

    def __init__(self):
        self.info = VectorTable('info')
        self.task = VectorTable('task')
        self.vector = VectorTable('vector')

        self.tasks = OrderedDict()

        self.sections = OrderedDict(
            {"info": self.info, "task": self.task, "vector": self.vector}
        )
        
        self.code = []

    # 
    def add_task(self,task):
        if not isinstance(task,Task):
            raise(TaskError)
        self.tasks[task.name] = task

    # build sections 
    def build_info(self):
        " build the info header "
        return []

    def build_task(self):
        " build the task table"
        return self.task.dump() 

    def build_vector(self):
        " build the vector table"
        return []

    def build_static(self):
        " build the static data"
        return []

    def build_code(self):
        " build the code section "
        return []

    def build(self):
        " Build all the sections"
        self.code = []
        self.code += [
                L('runtime_info'),
                self.build_info(),
                L('runtime_task'),
                self.build_task(),
                L('runtime_vector'),
                self.build_vector(),
                L('runtime_static'),
                self.build_static(),
                L('runtime_code'),
                self.build_code(),
                L('runtime_codeend'),
        ]
        return self.code

    def fetch(self):
        raise BORK

    def dump(self):
        for i, j in self.sections.items():
            print(i, j.dump())


if __name__ == "__main__":
    r = Runtime()
    r.dump()
