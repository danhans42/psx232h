# psx232h

## What ?
psx232h is a project which allows a Sony PlayStation(PSX) console to communicate with the outside world via an FTDI FT232h module attached to the PlayStation Expansion Port. Primary focus being on running code over a cable. This was more aimed at being a test exercise rather than a solution to a problem - so it will not really be improved other than fixing the macos client issue.

Why you might ask? We have unirom/hit-serial/sioloader etc? Well its fast, like really f**king fast and also it leaves the PlayStation serial port free for other uses.

We basically have some code that can be run from a PlayStation memory card which is executed in the same way as freepsxboot, the hardware itself and the pc side client. 

The code for both PSX and PC is written in a simple way so hopefully it should be easy to follow.

## How
The repo contains everything you should need to get this up and running. If you wish to build from source this has some extra requirements - I will add instructions for that later.

**PlayStation**

To install the software to a memory card you will need a way to transfer the memory card image to a PSX memory card. You can do this with Unirom, Memcarduino or some other thing. The PSX side code is small and basic so it can be loaded quickly from memory card. The source and binaries are all in the /psx folder.

**Hardware**

Hardware wise you need to connect the hardware as per the schematics in the /hardware folder. To connect to the expansion port you can hack up an old cheat cartridge, wire up directly to the motherboard or use the excellent PIO Breakout. 

Here is my test setup using the pio-breakout :-

<img src="https://github.com/danhans42/psx232h/blob/main/hardware/hardware_test_setup.png?raw=true">

The project currently uses a ATF22V10C PLD device which needs to be programmed. I use a TL866 programmer for this. I have included the CUPL source and a JED file ready for programming. The ATF22v basically delays the control signals slightly so the FTDI reads/writes the data bus correctly. You may be able to replace this with an off the self discrete (hex inverter?) but mileage may vary. We also bring /RESET into the mix for future proofing - more on that to follow. 

CUPL source/JED is in the ATF22V10C folder. To build the CUPL into a JED you will need to use WinCUPL.
Hardware connections/schematic is in the /hardware folder.

**PC Client** 
 
The client is simple - it is supposed to be. It just needs Python 3 (tested on 3.7) and Pyserial installing. The client supports uploading EXEs, uploading data to an address, dump memory, reboot (via BIOS) and a jump/call function. This can be found in the /pc folder.

## Thanks

Built using sicklebrick hello world example (nugget).
Also uses ps1-packer by Nicolas Noble
and freepsxboot builder by Bradlin.

For more playstation development chat join us on our discord.. visit http://psx.dev/

