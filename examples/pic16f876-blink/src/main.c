/*
 * PIC16F876 LED Blink Example
 * 
 * This example demonstrates basic GPIO control on PIC16F877
 * using the XC8 compiler through PlatformIO.
 * 
 * Hardware:
 * - PIC16F876 microcontroller
 * - LED connected to RB0 with current limiting resistor
 * - 20MHz crystal oscillator
 * 
 * Board: pic16f876
 * Framework: pic-xc8
 */

#include <xc.h>

// Configuration bits
#pragma config FOSC = HS        // High Speed Crystal/Resonator
#pragma config WDTE = OFF       // Watchdog Timer disabled
#pragma config PWRTE = ON       // Power-up Timer enabled
#pragma config BOREN = ON       // Brown-out Reset enabled
#pragma config LVP = OFF        // Low Voltage Programming disabled
#pragma config CPD = OFF        // Data EEPROM Memory Code Protection disabled
#pragma config WRT = OFF        // Flash Program Memory Write Enable disabled
#pragma config CP = OFF         // Flash Program Memory Code Protection disabled

// Define oscillator frequency for delay calculations
#define _XTAL_FREQ 4000000

int main(void) {
    // Configure RB0 as output
    TRISBbits.TRISB0 = 0;
    
    // Main loop
    while(1) {
        // Turn LED on
        PORTBbits.RB0 = 1;
        __delay_ms(500);
        
        // Turn LED off
        PORTBbits.RB0 = 0;
        __delay_ms(500);
    }
    
    return 0;
}
