#!/bin/bash
make -f build_release.mk clean
make -f build_release.mk
ps1-packer psx232h.exe -booty -o psx232h.payload
ps1-packer psx232h.exe -o psx232h.exe
./builder -all -in psx232h.exe -out ./mc_images/psx232h.mcr -fastload


