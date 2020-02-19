#/bin/bash
CompileDaemon -build "echo" -command "python instr.py" -pattern "(.|\\.py)$"
