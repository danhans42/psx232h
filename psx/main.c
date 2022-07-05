
#ifndef  MAINC
#define MAINC

#include <stdarg.h>
#include <stdint.h>
#include <stddef.h>

#include "main.h"

#include "littlelibc.h"
#include "utility.h"
#include "drawing.h"
#include "config.h"
#include "gpu.h"

// Ridin Solo with just a FT232h module (Wire A0 to PSX A20) & you
// need a delay tactic for the control signals (/rd, /wr, /cs0)
// Base address for FTDI232h   0x1F000000
// Status address for FTDI232h 0x1F100000 (A0 - PSX A20)
volatile uint8_t *ftdi_data =  (uchar*) 0xBF000000;
volatile uint8_t *ftdi_stat =  (uchar*) 0xBF100000;


// Using PIO Breakout + Shield + ATF22V10C
// Base address for FTDI232h   0x1F060004
// Status address for FTDI232h 0x1F100005 (A0 - A0)
//volatile uint8_t *ftdi_data =  (uchar*) 0xBF060004;
//volatile uint8_t *ftdi_stat =  (uchar*) 0xBF060005;


uint8_t FT_RxStatus() {
	return (*ftdi_stat & 0x1);
}


void FT_SendString(const char *inChar) {
    int offset = 0;
    while (inChar[offset] != 0) {
        FT_SendByte(inChar[offset]);
        offset++;
    }
}

void FT_SendByte(uint8_t value) {
	//write byte to FTDI
	while  (((*ftdi_stat >> 1) & 0x1) == 0 ) ; //wait until buffer clears?
	*ftdi_data = value;
}

uint8_t FT_ReadByte() {
	//read byte from FTDI
	while  ((*ftdi_stat & 0x1) == 0 ) ; //wait until we have data
	return *ftdi_data;

}

void FT_Send32( uint32_t value) {
	//Send 32bit to FTDI
    FT_SendByte ((value & 0x000000FF) >> 0);
    FT_SendByte ((value & 0x0000FF00) >> 8);
    FT_SendByte ((value & 0x00FF0000) >> 16);
    FT_SendByte ((value & 0xFF000000) >> 24);

}

uint32_t FT_Read32() {
    //Read 32bit from FTDI
	uint32_t value = 0;
    value |= FT_ReadByte() ;
    value |= FT_ReadByte() << 8;
    value |= FT_ReadByte() << 16;
    value |= FT_ReadByte() << 24;
    return value;
}

void CheckCommand(){

	uint8_t response=0;
	DrawTile( 0,0, 512 ,240, 0x00FFFF );
	Draw();
	response = FT_ReadByte();

	if (response==0x62) {
		//load BIN
		uint32_t xaddr, addr, len,x=0;
		addr=FT_Read32();
		len=FT_Read32();
		while (x < len){
			*(uint8_t*)(addr+x) = FT_ReadByte();
			x++;
		}
		DrawTile( 0,0, 512 ,240, 0x000000 );
		Draw();	
	}

	else if (response==0x63) {
		//load EXE
		uint32_t xaddr, addr, len,x=0;
		xaddr=FT_Read32();
		addr=FT_Read32();
		len=FT_Read32();
		while (x < len){
			*(uint8_t*)(addr+x) = FT_ReadByte();
			x++;
		}
		DrawTile( 0,0, 512 ,240, 0x000000 );
		Draw();
		ExitCritical();
		( (int ( * )( int, char ** ))xaddr )( 0, NULL );
	}

	else if (response==0x64) {
		//dump BIN
		uint32_t xaddr, addr, len,x=0;
		addr=FT_Read32();
		len=FT_Read32();
		while (x < len){
			FT_SendByte( *(uint8_t*)(addr+x) );
			x++;
		}
		DrawTile( 0,0, 512 ,240, 0x000000 );
		Draw();	
	}

	else if (response==0x65) {
		//call addr
		uint32_t xaddr ;
		xaddr=FT_Read32();
		DrawTile( 0,0, 512 ,240, 0x000000 );
		Draw();
		goto *(ulong*) xaddr;
	}


	else if (response=='r') {
		DrawTile( 0,0, 512 ,240, 0x000000 );
		Draw();
		goto *(ulong*)0xBFC00000;
	}

}


int main(){

    //setup EXP1 for 8mb address space (Needed if just riding solo with ft232h)
    *((volatile uint32_t *) 0x1f801008) = (23 << 16) | 0x2422;
	ExitCritical();
	InitGPU();
	while ( 1 ){
		DrawBG();
		if (*ftdi_stat == 0xff){
		    DrawTile( 0,0, 512 ,240, 0x0000FF );   
		}
		else DrawTile( 0,0, 512 ,240, 0x00AA00 );
		
		Draw();
	    if (*ftdi_stat !=0xff) if (FT_RxStatus() == 0x1 ) CheckCommand();
	}

}




#endif // ! MAINC

