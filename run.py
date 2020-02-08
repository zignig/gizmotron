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
from utils.serial_write import writer
import firmware

import sim_data 

if __name__ == "__main__":
    print("Gizmotronic Boneless")
    p = argparse.ArgumentParser()
    action = p.add_subparsers(dest="action")

    action.add_parser("info")

    action.add_parser("list")

    action.add_parser("build")

    action.add_parser("program")

    action.add_parser("simulate")

    action.add_parser("gatesim")

    p.add_argument("-f",action="store",help="asm file to include",default=None)

    p.add_argument("-p",action="store",help="firmware to run , use list to show",default="uLoader")

    args = p.parse_args()

    platform = BB()
    if args.action == "list":
        fw_list = firmware.show()
        for i,j in enumerate(fw_list):
            print(i," : ",j)

    if args.action == "info":
        print("Show info")
        cpu = construct.CPU(platform,fw=args.p,asm_file=args.f)

    if args.action == "build":
        print("Build")
        cpu = construct.CPU(platform,fw=args.p,asm_file=args.f)
        platform.build(cpu, do_program=True)

    if args.action == "program":
        print("Program")
        cpu = construct.CPU(platform,asm_file=args.f)
        code = cpu.b.code
        hex_out = ""
        lines = []
        for i in code:
            hex_out += '{:04X}\n'.format(i)
            lines.append('{:04X}\n'.format(i))
        hex_out += '{:04X}\n'.format(0xFFFF)
        lines.append('{:04X}\n'.format(0xFFFF))
        print(lines)
        writer(lines,'/dev/ttyUSB0')
        f = open('utils/yay.hex','w')
        f.write(hex_out)
        f.close()
        

    if args.action == "simulate":
        print("Simulate")
        s = Simulator(asm_file=args.f)
        s.run()
        
    if args.action == "gatesim":
        print("Gateware Simulation")
        design = construct.simCPU(platform,fw=args.p,asm_file=args.f)
        fragment = Fragment.get(design, platform)
        f = open("test.vcd", "w")
        dut = design.b.serial_port
        print(dir(dut.RX))
        st = "the quick brown fox jumps over the lazy dog"
        data = sim_data.str_data(st)
        with pysim.Simulator(fragment, vcd_file=f, traces=()) as sim:
            sim.add_clock(100e-6)
            sim.add_sync_process(sim_data.test_rx(data,dut))
            sim.run_until(100e-6 * 300000, run_passive=True)
