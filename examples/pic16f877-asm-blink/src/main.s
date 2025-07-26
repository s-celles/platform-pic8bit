/**
 * PIC16F877 Assembly LED Blink Example
 * 
 * This example demonstrates basic GPIO control in assembly language
 * for PIC16F877 using PlatformIO with XC8 assembler.
 * 
 * Hardware:
 * - PIC16F877 microcontroller  
 * - LED connected to RB0 with current limiting resistor
 * - 20MHz crystal oscillator
 */

#include <xc.inc>

; Processor definition
PROCESSOR 16F877

; Configuration bits
CONFIG FOSC=HS, WDTE=OFF, PWRTE=ON, BOREN=ON, LVP=OFF, CPD=OFF, WRT=OFF, CP=OFF

; Constants
#define _XTAL_FREQ 20000000

; Variables
PSECT udata_bank0
delay_count1: DS 1
delay_count2: DS 1  
delay_count3: DS 1

; Reset vector
PSECT resetVec,class=CODE,delta=2
resetVec:
    goto main

; Main program
PSECT code
main:
    ; Initialize ports
    banksel TRISB
    bcf     TRISB,0     ; Set RB0 as output
    
    banksel PORTB
    
main_loop:
    ; Turn LED on
    bsf     PORTB,0
    call    delay_500ms
    
    ; Turn LED off  
    bcf     PORTB,0
    call    delay_500ms
    
    goto    main_loop

; Delay routine for approximately 500ms at 20MHz
delay_500ms:
    movlw   0x06        ; Load outer loop count
    movwf   delay_count1
    
delay_outer:
    movlw   0xFF        ; Load middle loop count
    movwf   delay_count2
    
delay_middle:
    movlw   0xFF        ; Load inner loop count  
    movwf   delay_count3
    
delay_inner:
    decfsz  delay_count3,f
    goto    delay_inner
    
    decfsz  delay_count2,f
    goto    delay_middle
    
    decfsz  delay_count1,f
    goto    delay_outer
    
    return

END resetVec
