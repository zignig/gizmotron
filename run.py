#!/usr/bin/python

import argparse
import construct
from plat import BB
from nmigen.hdl.ir import Fragment
from nmigen.back import pysim, rtlil, verilog

if __name__ == "__main__":
    print("Gizmotronic Boneless")
    p = argparse.ArgumentParser()
    action = p.add_subparsers(dest="action")

    action.add_parser("info")

    action.add_parser("build")

    action.add_parser("program")

    action.add_parser("simulate")

    args = p.parse_args()

    platform = BB()
    if args.action == "info":
        print("Show info")
        cpu = construct.CPU(platform)

    if args.action == "build":
        print("Build")
        cpu = construct.CPU(platform)
        platform.build(cpu, do_program=True)

    if args.action == "program":
        print("Program")

    if args.action == "simulate":
        print("Simulation")
        design = construct.simCPU(platform)
        fragment = Fragment.get(design, platform)
        f = open("test.vcd", "w")
        with pysim.Simulator(fragment, vcd_file=f, traces=()) as sim:
            sim.add_clock(100e-6)
            sim.run_until(100e-6 * 50000, run_passive=True)
