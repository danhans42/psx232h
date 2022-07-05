#!/usr/bin/env python3
# psx232h.py - simple exe uploader for ft232h
# Runs on Python 3.7 - requires the pyserial libaries to be installed
# Tested on Windows & Linux 
# by @danhans42 (instag/twitter/psxdev/@gmail.com)

import sys
import serial
import os

args = int(len(sys.argv))

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write("%s Data [%s] %s%s %s\r" % (stat,bar, percents, "%", status))
    sys.stdout.flush()

def usage():
    sys.stdout.write("-h                                  help (this screen)\n")
    sys.stdout.write("-exe    <port> <psx exe>            upload & execute PSX-EXE\n")    
    sys.stdout.write("-bin    <port> <file> <addr>        upload file to address\n")    
    sys.stdout.write("-goto   <port> <addr>               goto to <addr>\n")
    sys.stdout.write("-dump   <port> <file> <addr> <len>  download data from PSX\n")
    sys.stdout.write("-reboot <port>                      reboot attached PSX\n\n")
    sys.exit()

def resetpsx():
	serialport = sys.argv[2]
	sys.stdout.write("Port       : ")
	sys.stdout.write(serialport)
	sys.stdout.write("\n")
	ser = serial.Serial(serialport,115200,writeTimeout = 1)
	ser.write(b'\x72')
	sys.stdout.write("Command    : Reset PSX\n\n")
	sys.stdout.write("Operation Complete\n\n")

def download():
	serialport = sys.argv[2]
	file = sys.argv[3]
	addr = (int(sys.argv[4],16)).to_bytes(4, byteorder='little',signed=False)
	len = (int(sys.argv[5],16)).to_bytes(4, byteorder='little',signed=False)
	sys.stdout.write("Port       : ")
	sys.stdout.write(serialport)
	sys.stdout.write("\nFilename   : {}\n".format(file))
	sys.stdout.write("Address    : ")
	sys.stdout.write(hex(int(sys.argv[4],16)))
	sys.stdout.write("\n")
	sys.stdout.write("Length     : ")
	sys.stdout.write(str(int(sys.argv[5],16)))
	sys.stdout.write(" bytes\n")
	sys.stdout.write("Command    : Download data\n")
	ser = serial.Serial(serialport,115200,writeTimeout = 1)
	dump = open(file,'wb')
	buffer = bytearray()
	ser.write(b'\x64')
	ser.write(addr)
	ser.write(len)
	progress(1, 100, status='')
	buffer=ser.read(int(sys.argv[5],16))
	progress(100, 100, status='')
	sys.stdout.write("\nOperation Complete\n\n")
	dump.write(buffer)
	dump.close()

def gotoaddr():
	serialport = sys.argv[2]
	addr = (int(sys.argv[3],16)).to_bytes(4, byteorder='little',signed=False)
	sys.stdout.write("Port       : ")
	sys.stdout.write(serialport)
	sys.stdout.write("\n")
	ser = serial.Serial(serialport,115200,writeTimeout = 1)
	ser.write(b'\x65')
	sys.stdout.write("Command    : Goto address ")
	sys.stdout.write(hex(int(sys.argv[3],16)))
	ser.write(addr)
	sys.stdout.write("\n\nOperation Complete\n\n")


def uploadexe():
    serialport = sys.argv[2]
    filename = sys.argv[3]
    filesize = os.path.getsize(filename)
    inputfile = open(filename, 'rb')
    inputfile.seek(0, 0)
    header = inputfile.read(2048)
    inputfile.seek(16,0)
    pc = inputfile.read(4)
    inputfile.seek(24,0)
    addr= inputfile.read(4)
    inputfile.seek(28,0)
    fsz = inputfile.read(4)
    sys.stdout.write("Port       : ")
    sys.stdout.write(serialport)
    sys.stdout.write("\nEXE Name   : {}\n".format(filename))
    sys.stdout.write("File Size  : {} bytes\n".format(filesize))
    ser = serial.Serial(serialport,115200,writeTimeout = 1)
    ser.write(b'\x63')
    sys.stdout.write("Command    : Execute PS-X EXE\n\n")
    ser.write(pc)
    sys.stdout.write("Sending Exec Address\n")
    ser.write(addr)
    sys.stdout.write("Sending Load Address\n")
    ser.write(fsz)
    sys.stdout.write("Sending Filesize\n")
    offset = 2048
    while offset < filesize:
        inputfile.seek(offset,0)
        bin = inputfile.read(2048)
        ser.write(bin)
        offset += 2048
        progress(offset, filesize, status='')
    sys.stdout.write("\nExecuting")
    sys.stdout.write("\nOperation Complete\n\n")

def upload():
	serialport = sys.argv[2]
	filename = sys.argv[3]
	addr = (int(sys.argv[4],16)).to_bytes(4, byteorder='little',signed=False)
	filesize = (os.path.getsize(filename)).to_bytes(4, byteorder='little',signed=False)
	inputfile = open(filename, 'rb')
	inputfile.seek(0, 0)
	sys.stdout.write("Port       : ")
	sys.stdout.write(serialport)
	sys.stdout.write("\nFilename   : {}\n".format(filename))
	sys.stdout.write("File Size  : {} bytes\n".format(os.path.getsize(filename)))
	sys.stdout.write("Address    : ")
	sys.stdout.write(hex(int(sys.argv[4],16)))
	sys.stdout.write("\n")
	bin = inputfile.read(os.path.getsize(filename))
	ser = serial.Serial(serialport,115200,writeTimeout = 1)
	ser.write(b'\x62')
	sys.stdout.write("Command    : Upload data\n\n")
	ser.write(addr)
	sys.stdout.write("Sending Load Address\n")
	ser.write(filesize)
	sys.stdout.write("Sending Filesize\n")
	progress(1, 100, status='')
	ser.write(bin)
	progress(100, 100, status='')
	sys.stdout.write("\nOperation Complete\n\n")

#main

sys.stdout.write("psx232h.py - by @danhans42\n\n")

if args < 2:
    sys.stdout.write("insufficient parameters - try psx232h.py -h\n\n")
    sys.exit()

command = sys.argv[1]

if  command == "-h":
    usage()

elif  command == "-exe":
    if args < 4:
        sys.stdout.write("insufficient parameters - try psx232h.py -h\n\n")
        sys.exit()
    serialport = sys.argv[2]
    file = sys.argv[3]
    stat = "Uploading"
    uploadexe()

elif  command == "-bin":
    if args < 5:
        sys.stdout.write("insufficient parameters - try psx232h.py -h\n\n")
        sys.exit()
    serialport = sys.argv[2]
    file = sys.argv[3]
    stat = "Uploading"
    upload()

elif  command == "-reboot":
    if args < 3:
        sys.stdout.write("insufficient parameters - try psx232h.py -h\n\n")
        sys.exit()
    serialport = sys.argv[2]
    resetpsx()

elif  command == "-goto":
    if args < 3:
        sys.stdout.write("insufficient parameters - try psx232h.py -h\n\n")
        sys.exit()
    serialport = sys.argv[2]
    gotoaddr()

elif  command == "-dump":
	if args < 6:
		sys.stdout.write("insufficient parameters - try psx232h.py -h\n\n")
		sys.exit()
	stat = "Downloading"
	download()

else:
    sys.stdout.write("error: invalid command\n\n")
    usage()
	
	
	
