# psx232h

## Introduction
psx232h is a project which allows a Sony PlayStation(PSX) console to communicate with the outside world via an FTDI FT232h module attached to the PlayStation Expansion Port. Primary focus being on running code over a USB cable faster than the existing serial/parallel solutions. I say faster, its *very* fast in comparison to other solutions. 

For an idea of speed see a video of it in action [here](https://youtube.com/shorts/HCbUtbzJ9Fg). The example EXE being sent over is Mahjongg by Skywalker  ~1600kb.

Feature wise it offers both data/exe upload, download, jump/call and reboot functions via its client.

## psx232h
The project is made up of both hardware and software. From a hardware perspective the PSX needs to be wired to a FT232h module (I used the Adafruit version) with some extra logic for a speed issue. Connecting this to a PSX can be a bit of a blocker due to availability of both the connector and a suitable PCB. Its not impossible though!

Software side there is both the PSX side application, and the python client for communicating with it. The PSX side can be built with standard gcc and doesnt rely on an SDK. To actually run the code I decided to use freepsxboots builder application to make use of the memory card exploit in the PSX shell. For compression I used the ps1-packer from pcsx-redux package.

In order to build from source you will require a working mips gcc compiler working, and both freepsxboot and ps1-packer from pcsx-redux. I will link to their respective repositories at the end of this file.

The project is the output of a simple test exercise to work with the FT232h chip and see how it worked. The code is written in a simple amateur way - reasons being firstly, I am a true amateur. Secondly, I want it to be easily understood and readable, The client I chose Python for both portability and ease of use. Im not its biggest fan - and this is the 3rd thing I have written in it so it could probably be vastly improved.

## Getting Started
The repo contains everything you should need to get this up and running. If you wish to build from source this has some extra requirements - I will add instructions for that later.

## PlayStation Software
In the psx/memorycard_images folder you will find pre-built freepsxboot images for your convenience (slot 1). You will need to write the appropriate version to a spare memory card as you would with freepsxboot. You can do this with unirom/memcardrex etc.

To build from source you will need a working mips gcc compiler. I work on Linux Mint so for that its just a matter of grabbing some packages. You will need make and I used gcc-10-mips-linux-gnu however it should work with other versions. Depending on your system you may need to edit common.mk in /psx/nugget to suit your needs.

That is all you actually need to compile the source to a standard PSX EXE. You should now be able to build the psx232h PSX side application by using make -f build_debug.mk for example. 

The two makefiles just compile the EXE to load to different addresses in memory. Debug is 0x80100000, release is 0x801E0000. It can probably be shoved up higher as its quite small.

To actually run the EXE we need a way to do that. I chose freepsxboot so it could be run from the PSX shell memory card manager. To build a memory card image from the source you will need to clone and build freepsxboot and drop the 'builder' application into the /psx folder. You will also need ps1-packer from the pcsx-redux repo, this allows us some compression which means that the code can be loaded from memory card faster, you will need to drop ps1-packer into the /psx folder too.

Once you have done the above you can then use the scripts in the folder to make the exe, compress it and build a freepsxboot image from it.

When the PS232h program is running, it should show a green screen to say its detected an FT232h and its ready, red means its not detected/usb cable not connected. Yellow means busy.

## Hardware

Hardware wise you need to connect the hardware as per the schematic. Apologies I just used Fritzin for ease.
You will need a FT232h module, a ATF22V10C(and a programmer for it) and a way to wire this up to your PSX. To connect to the expansion port you can hack up an old cheat cartridge, wire up directly to the motherboard or use the excellent PIO Breakout. If you want to do this internally or a PSone, you would need to wire directly to the motherboard.

Here is my test setup using the pio-breakout :-

<img src="https://github.com/danhans42/psx232h/blob/main/hardware/hardware_test_setup.png?raw=true">

The project currently uses a ATF22V10C PLD device which needs to be programmed. I use a TL866 programmer for this. I have included the CUPL source and a JED file ready for programming. The ATF has some simple equations where we are using the pin-pin delay to postpone the control signals slightly. This is so the FTDI reads/writes the data bus correctly (FT232h in CPU mode writes on the falling edge). You may be able to replace this with an off the self discrete (hex inverter?) but mileage may vary and I have yet to test this. 

We also bring /RESET into the mix for future proofing - more on that to follow. Currently it ensures whilst the PSX is in reset read/writes do not happen.

CUPL source and the JED for programming is in the ATF22V10C folder. To build the CUPL into a JED you will need to use WinCUPL.

Also, you will need a way to program the EEPROM of your FT232h - I use FT_Prog for ease, it is Windows only unfortunately. You will need to set your Channel A to CPU FIFO and ensure its setup as VCP (not D2XX).

Schematic
![enter image description here](https://github.com/danhans42/psx232h/blob/main/hardware/psx232h_schem.png?raw=true)

**Python Client** 
 
The client is simple - it is supposed to be. It just needs Python 3 (tested on 3.7) and Pyserial installing. The client supports uploading EXEs, uploading data to an address, dump memory, reboot (via BIOS) and a jump/call function. This can be found in the /pc folder. If you get stuck look at the source or run ./psx232h.py -h

## Thanks/Credits etc.

 - Built using sicklebricks helloworld_flappycredits example https://github.com/JonathanDotCel/helloworld_and_flappycredits
 - freepsxboot builder by Brad-lin https://github.com/brad-lin/FreePSXBoot 
 - ps1-packer by Nicolas Noble/pcsx-redux https://github.com/grumpycoders/pcsx-redux/tree/main/tools/ps1-packer
 - pio-breakout by Nicolas Noble/pcsx-redux https://oshpark.com/shared_projects/f7QNj0ld
 






For more playstation development chat join us on our discord.. visit http://psx.dev/
