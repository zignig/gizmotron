# Gizmotron 

This is an experimental platform to have console (96008n1) access to FGPA development platform. Current development is on a tinyFPGAbx.

You will need the following software installed on you machine.

1. Python 3.6+
2. [nextpnr](https://github.com/YosysHQ/nextpnr)
3. [yosys](https://github.com/YosysHQ/yosys)

Edit the platform in plat.py to alter your hardware setup.

Edit construct.py to add new gizmos , these will auto bind to the boneless memory map.

# TODO
- expose and emulate gizmos in the simulator 
- get flash read write working 
- get monitor working 
- rework simulator for new style boneless
- cleanse Boneless-CPU branch and get it merged upstream
- write and document some more cores
