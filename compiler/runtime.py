# boneless runtime

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
5: 
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

code goes here
"""

class Runtime:
    pass


