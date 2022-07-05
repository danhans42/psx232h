#!/bin/bash
make -f build_debug.mk clean
make -f build_debug.mk 
ps1-packer psx232h_debug.exe -booty -o psx232h_debug.payload
#ps1-packer psx232h_debug.exe -o psx232h_debug.exe
#./builder -model 7502 -in psx232h.exe -out psx232h.mcr -fastload


