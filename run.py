#!/usr/bin/python

import argparse
import construct
from plat import BB
from nmigen.hdl.ir import Fragment
from nmigen.back import pysim, rtlil, verilog

from boneless.arch.asm import Assembler 
import array
import intelhex

if __name__ == "__main__":
    print("Gizmotronic Boneless")
    p = argparse.ArgumentParser()
    action = p.add_subparsers(dest="action")

    action.add_parser("info")

    action.add_parser("build")

    action.add_parser("program")

    action.add_parser("simulate")

    p.add_argument("-f",action="store",help="asm file to include",default="asm/blink.asm")

    args = p.parse_args()
    print(args)

    platform = BB()
    if args.action == "info":
        print("Show info")
        cpu = construct.CPU(platform,asm_file=args.f)

    if args.action == "build":
        print("Build")
        cpu = construct.CPU(platform,asm_file=args.f)
        platform.build(cpu, do_program=True)

    if args.action == "program":
        print("Program")
        a = Assembler()
        a.parse(open("asm/base.asm").read())
        a.assemble()
        #as_byte = array.array("H",a.code).tobytes()
        #h = intelhex.IntelHex()
        #h.frombytes(as_byte)
        #h.write_hex_file('bootloader.hex')
        

    if args.action == "simulate":
        print("Simulation")
        design = construct.simCPU(platform)
        fragment = Fragment.get(design, platform)
        f = open("test.vcd", "w")
        with pysim.Simulator(fragment, vcd_file=f, traces=()) as sim:
            sim.add_clock(100e-6)
            sim.run_until(100e-6 * 50000, run_passive=True)
