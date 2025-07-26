# PIC16F877 LED Blink Example

This example demonstrates basic GPIO control on the PIC16F877 microcontroller using the XC8 compiler through PlatformIO.

## Hardware Requirements

- PIC16F877 microcontroller
- LED connected to RB0 with appropriate current limiting resistor (typically 330Ω)
- 20MHz crystal oscillator with 22pF capacitors
- Appropriate power supply (5V)

## Circuit Diagram

```
    VDD
     |
     +-- PIC16F877
     |   |
     |   RB0 ----[330Ω]----[LED]----GND
     |
    OSC1 ----[22pF]----[20MHz XTAL]----[22pF]----OSC2
                            |
                           GND
```

## Features

- Configures RB0 as digital output
- Blinks LED with 1 second period (500ms on, 500ms off)
- Uses XC8 built-in delay functions
- Proper configuration bits for 20MHz operation

## Building and Uploading

```bash
# Build the project
pio run

# Upload to device (requires appropriate programmer)
pio run -t upload

# Clean build files
pio run -t clean
```

## Configuration

The example uses these configuration bits:
- `FOSC = HS`: High Speed Crystal (20MHz)
- `WDTE = OFF`: Watchdog Timer disabled
- `PWRTE = ON`: Power-up Timer enabled
- `BOREN = ON`: Brown-out Reset enabled
- `LVP = OFF`: Low Voltage Programming disabled

## Notes

- Ensure your programmer is properly configured in `platformio.ini`
- The crystal frequency must match the `_XTAL_FREQ` definition for accurate delays
- This example is compatible with any PIC16F877-based development board
