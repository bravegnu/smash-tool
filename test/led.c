
#include<stdio.h>
//#include <8051.h>
#include <p89v51rd2.h>

void init_gpio(void)
{
	//P3_3 = 0;
	
	P3 = 0x00;
	P2 = 0x00;
	
	//P0 = 0x00;
	P0 = 0x00;
	
	//P1 = 0x00;
	P1 = 0x00;
}
void putchar(char c)
{
	while(!TI)
	;
	TI =0;
	SBUF = c;
	//while(!TI);
}

void init_ser(){
	TMOD=0x20;      //timer1 as 8 bit auto reloaad timer.
	PCON|=0x80;     //set SMOD bit in PCON.
	TL1=0x0F3;      //load counter1 for 4800 baud rate.
	TH1=0x0F3;      //at 12 Mhz crystal freq. for 80c31 microcontroller.
	SCON=0x52;      //8 bit UART variable baub rate and receive enable.
	//start_timer1(); //start timer1.
}

void main ()
{	
	init_gpio();
		
	while(1)			// infinite loop
	{
		init_gpio();
		// send the string to the serial port
		
	}// end of while(1)
}// end of main
