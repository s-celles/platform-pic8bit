// Universal PIC transpilation stubs for all Microchip PICs
// This file provides Clang-compatible stubs for all PIC16Fxxx
#ifndef PIC_UNIVERSAL_STUBS_H
#define PIC_UNIVERSAL_STUBS_H

#ifdef __clang__
    // Universal transpilation stubs for ALL PICs in Microchip DFP
    #pragma clang diagnostic push
    #pragma clang diagnostic ignored "-Wunknown-pragmas"
    #pragma clang diagnostic ignored "-Wunused-variable"
    #pragma clang diagnostic ignored "-Wimplicit-function-declaration"
    #pragma clang diagnostic ignored "-Wignored-attributes"
    
    // Basic types
    typedef unsigned char uint8_t;
    typedef unsigned int uint16_t;
    typedef unsigned long uint32_t;
    
    // Core CPU registers (common to all PICs)
    typedef struct { unsigned W : 8; } wreg_bits_t;
    extern volatile wreg_bits_t WREGbits;
    extern volatile uint8_t WREG;
    
    typedef struct {
        unsigned C : 1; unsigned DC : 1; unsigned Z : 1; unsigned nPD : 1;
        unsigned nTO : 1; unsigned RP0 : 1; unsigned RP1 : 1; unsigned IRP : 1;
    } status_bits_t;
    extern volatile status_bits_t STATUSbits;
    extern volatile uint8_t STATUS;
    
    typedef struct {
        unsigned RBIF : 1; unsigned INTF : 1; unsigned T0IF : 1; unsigned RBIE : 1;
        unsigned INTE : 1; unsigned T0IE : 1; unsigned PEIE : 1; unsigned GIE : 1;
    } intcon_bits_t;
    extern volatile intcon_bits_t INTCONbits;
    extern volatile uint8_t INTCON;
    
    // PORT registers (A-E common on many PICs)
    typedef struct {
        unsigned RA0 : 1; unsigned RA1 : 1; unsigned RA2 : 1; unsigned RA3 : 1;
        unsigned RA4 : 1; unsigned RA5 : 1; unsigned RA6 : 1; unsigned RA7 : 1;
    } porta_bits_t;
    extern volatile porta_bits_t PORTAbits;
    extern volatile uint8_t PORTA;
    
    typedef struct {
        unsigned RB0 : 1; unsigned RB1 : 1; unsigned RB2 : 1; unsigned RB3 : 1;
        unsigned RB4 : 1; unsigned RB5 : 1; unsigned RB6 : 1; unsigned RB7 : 1;
    } portb_bits_t;
    extern volatile portb_bits_t PORTBbits;
    extern volatile uint8_t PORTB;
    
    typedef struct {
        unsigned RC0 : 1; unsigned RC1 : 1; unsigned RC2 : 1; unsigned RC3 : 1;
        unsigned RC4 : 1; unsigned RC5 : 1; unsigned RC6 : 1; unsigned RC7 : 1;
    } portc_bits_t;
    extern volatile portc_bits_t PORTCbits;
    extern volatile uint8_t PORTC;
    
    typedef struct {
        unsigned RD0 : 1; unsigned RD1 : 1; unsigned RD2 : 1; unsigned RD3 : 1;
        unsigned RD4 : 1; unsigned RD5 : 1; unsigned RD6 : 1; unsigned RD7 : 1;
    } portd_bits_t;
    extern volatile portd_bits_t PORTDbits;
    extern volatile uint8_t PORTD;
    
    typedef struct {
        unsigned RE0 : 1; unsigned RE1 : 1; unsigned RE2 : 1; unsigned RE3 : 1;
        unsigned RE4 : 1; unsigned RE5 : 1; unsigned RE6 : 1; unsigned RE7 : 1;
    } porte_bits_t;
    extern volatile porte_bits_t PORTEbits;
    extern volatile uint8_t PORTE;
    
    // TRIS registers (direction control)
    typedef struct {
        unsigned TRISA0 : 1; unsigned TRISA1 : 1; unsigned TRISA2 : 1; unsigned TRISA3 : 1;
        unsigned TRISA4 : 1; unsigned TRISA5 : 1; unsigned TRISA6 : 1; unsigned TRISA7 : 1;
    } trisa_bits_t;
    extern volatile trisa_bits_t TRISAbits;
    extern volatile uint8_t TRISA;
    
    typedef struct {
        unsigned TRISB0 : 1; unsigned TRISB1 : 1; unsigned TRISB2 : 1; unsigned TRISB3 : 1;
        unsigned TRISB4 : 1; unsigned TRISB5 : 1; unsigned TRISB6 : 1; unsigned TRISB7 : 1;
    } trisb_bits_t;
    extern volatile trisb_bits_t TRISBbits;
    extern volatile uint8_t TRISB;
    
    typedef struct {
        unsigned TRISC0 : 1; unsigned TRISC1 : 1; unsigned TRISC2 : 1; unsigned TRISC3 : 1;
        unsigned TRISC4 : 1; unsigned TRISC5 : 1; unsigned TRISC6 : 1; unsigned TRISC7 : 1;
    } trisc_bits_t;
    extern volatile trisc_bits_t TRISCbits;
    extern volatile uint8_t TRISC;
    
    typedef struct {
        unsigned TRISD0 : 1; unsigned TRISD1 : 1; unsigned TRISD2 : 1; unsigned TRISD3 : 1;
        unsigned TRISD4 : 1; unsigned TRISD5 : 1; unsigned TRISD6 : 1; unsigned TRISD7 : 1;
    } trisd_bits_t;
    extern volatile trisd_bits_t TRISDbits;
    extern volatile uint8_t TRISD;
    
    typedef struct {
        unsigned TRISE0 : 1; unsigned TRISE1 : 1; unsigned TRISE2 : 1; unsigned TRISE3 : 1;
        unsigned TRISE4 : 1; unsigned TRISE5 : 1; unsigned TRISE6 : 1; unsigned TRISE7 : 1;
    } trise_bits_t;
    extern volatile trise_bits_t TRISEbits;
    extern volatile uint8_t TRISE;
    
    // LAT registers (output latch)
    typedef struct {
        unsigned LATA0 : 1; unsigned LATA1 : 1; unsigned LATA2 : 1; unsigned LATA3 : 1;
        unsigned LATA4 : 1; unsigned LATA5 : 1; unsigned LATA6 : 1; unsigned LATA7 : 1;
    } lata_bits_t;
    extern volatile lata_bits_t LATAbits;
    extern volatile uint8_t LATA;
    
    typedef struct {
        unsigned LATB0 : 1; unsigned LATB1 : 1; unsigned LATB2 : 1; unsigned LATB3 : 1;
        unsigned LATB4 : 1; unsigned LATB5 : 1; unsigned LATB6 : 1; unsigned LATB7 : 1;
    } latb_bits_t;
    extern volatile latb_bits_t LATBbits;
    extern volatile uint8_t LATB;
    
    typedef struct {
        unsigned LATC0 : 1; unsigned LATC1 : 1; unsigned LATC2 : 1; unsigned LATC3 : 1;
        unsigned LATC4 : 1; unsigned LATC5 : 1; unsigned LATC6 : 1; unsigned LATC7 : 1;
    } latc_bits_t;
    extern volatile latc_bits_t LATCbits;
    extern volatile uint8_t LATC;
    
    // Timer registers
    extern volatile uint8_t TMR0;
    extern volatile uint8_t TMR1;
    extern volatile uint8_t TMR1L;
    extern volatile uint8_t TMR1H;
    extern volatile uint8_t TMR2;
    extern volatile uint8_t TMR3;
    extern volatile uint8_t TMR4;
    extern volatile uint8_t TMR5;
    extern volatile uint8_t TMR6;
    
    // Option register
    typedef struct {
        unsigned PS0 : 1; unsigned PS1 : 1; unsigned PS2 : 1; unsigned PSA : 1;
        unsigned T0SE : 1; unsigned T0CS : 1; unsigned INTEDG : 1; unsigned nRBPU : 1;
    } option_reg_bits_t;
    extern volatile option_reg_bits_t OPTION_REGbits;
    extern volatile uint8_t OPTION_REG;
    
    // PIR registers (peripheral interrupt flags)
    typedef struct {
        unsigned PIR0_0 : 1; unsigned PIR0_1 : 1; unsigned PIR0_2 : 1; unsigned PIR0_3 : 1;
        unsigned PIR0_4 : 1; unsigned PIR0_5 : 1; unsigned PIR0_6 : 1; unsigned PIR0_7 : 1;
    } pir0_bits_t;
    extern volatile pir0_bits_t PIR0bits;
    extern volatile uint8_t PIR0;
    
    typedef struct {
        unsigned PIR1_0 : 1; unsigned PIR1_1 : 1; unsigned PIR1_2 : 1; unsigned PIR1_3 : 1;
        unsigned PIR1_4 : 1; unsigned PIR1_5 : 1; unsigned PIR1_6 : 1; unsigned PIR1_7 : 1;
    } pir1_bits_t;
    extern volatile pir1_bits_t PIR1bits;
    extern volatile uint8_t PIR1;
    
    // PIE registers (peripheral interrupt enable)
    typedef struct {
        unsigned PIE0_0 : 1; unsigned PIE0_1 : 1; unsigned PIE0_2 : 1; unsigned PIE0_3 : 1;
        unsigned PIE0_4 : 1; unsigned PIE0_5 : 1; unsigned PIE0_6 : 1; unsigned PIE0_7 : 1;
    } pie0_bits_t;
    extern volatile pie0_bits_t PIE0bits;
    extern volatile uint8_t PIE0;
    
    typedef struct {
        unsigned PIE1_0 : 1; unsigned PIE1_1 : 1; unsigned PIE1_2 : 1; unsigned PIE1_3 : 1;
        unsigned PIE1_4 : 1; unsigned PIE1_5 : 1; unsigned PIE1_6 : 1; unsigned PIE1_7 : 1;
    } pie1_bits_t;
    extern volatile pie1_bits_t PIE1bits;
    extern volatile uint8_t PIE1;
    
    // ANSEL registers (analog select)
    typedef struct {
        unsigned ANS0 : 1; unsigned ANS1 : 1; unsigned ANS2 : 1; unsigned ANS3 : 1;
        unsigned ANS4 : 1; unsigned ANS5 : 1; unsigned ANS6 : 1; unsigned ANS7 : 1;
    } ansela_bits_t;
    extern volatile ansela_bits_t ANSELAbits;
    extern volatile uint8_t ANSELA;
    
    typedef struct {
        unsigned ANSB0 : 1; unsigned ANSB1 : 1; unsigned ANSB2 : 1; unsigned ANSB3 : 1;
        unsigned ANSB4 : 1; unsigned ANSB5 : 1; unsigned ANSB6 : 1; unsigned ANSB7 : 1;
    } anselb_bits_t;
    extern volatile anselb_bits_t ANSELBbits;
    extern volatile uint8_t ANSELB;
    
    // WPU registers (weak pull-up)
    typedef struct {
        unsigned WPUA0 : 1; unsigned WPUA1 : 1; unsigned WPUA2 : 1; unsigned WPUA3 : 1;
        unsigned WPUA4 : 1; unsigned WPUA5 : 1; unsigned WPUA6 : 1; unsigned WPUA7 : 1;
    } wpua_bits_t;
    extern volatile wpua_bits_t WPUAbits;
    extern volatile uint8_t WPUA;
    
    // ADC registers
    typedef struct {
        unsigned ADCON0_0 : 1; unsigned ADCON0_1 : 1; unsigned ADCON0_2 : 1; unsigned ADCON0_3 : 1;
        unsigned ADCON0_4 : 1; unsigned ADCON0_5 : 1; unsigned ADCON0_6 : 1; unsigned ADCON0_7 : 1;
    } adcon0_bits_t;
    extern volatile adcon0_bits_t ADCON0bits;
    extern volatile uint8_t ADCON0;
    
    extern volatile uint8_t ADRESH;
    extern volatile uint8_t ADRESL;
    
    // Delay functions for transpilation
    #define __delay_ms(x) do { /* XC8 provides real implementation */ } while(0)
    #define __delay_us(x) do { /* XC8 provides real implementation */ } while(0)
    
    #pragma clang diagnostic pop
#endif // __clang__

#endif // PIC_UNIVERSAL_STUBS_H
