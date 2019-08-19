#!/usr/bin/python

import argparse
import construct
from plat import BB
from nmigen.hdl.ir import Fragment
from nmigen.back import pysim, rtlil, verilog


from boneless.arch.asm import Assembler 
import array
import intelhex
from sim import Simulator

if __name__ == "__main__":
    print("Gizmotronic Boneless")
    p = argparse.ArgumentParser()
    action = p.add_subparsers(dest="action")

    action.add_parser("info")

    action.add_parser("build")

    action.add_parser("program")

    action.add_parser("simulate")

    action.add_parser("gatesim")

    p.add_argument("-f",action="store",help="asm file to include",default="asm/echo.asm")

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
        cpu = construct.CPU(platform,asm_file=args.f)
        code = cpu.b.code
        hex_out = ""
        for i in code:
            hex_out += '{:04X}\n'.format(i)
        hex_out += '{:04X}\n'.format(0xFFFF)
        print(hex_out)
        f = open('utils/yay.hex','w')
        f.write(hex_out)
        f.close()
        

    if args.action == "simulate":
        print("Simulate")
        s = Simulator(asm_file=args.f)
        s.run()
        
    if args.action == "gatesim":
        print("Gateware Simulation")
        design = construct.simCPU(platform,asm_file=args.f)
        fragment = Fragment.get(design, platform)
        f = open("test.vcd", "w")
        with pysim.Simulator(fragment, vcd_file=f, traces=()) as sim:
            sim.add_clock(100e-6)
            sim.run_until(100e-6 * 50000, run_passive=True)
