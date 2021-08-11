// Example for blinking a LED on pin 16 to GND
// on Odroid C4

#include <wiringPi.h>

int main(void) {
	puts("led an pin 16");
	wiringPiSetup();
	pinMode(4, OUTPUT);
	
	for(;;)	{
		digitalWrite(4,HIGH);
		delay(1000);
		digitalWrite(4,LOW);
		delay(1000);
	}
	return(0);
}

