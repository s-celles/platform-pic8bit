# Platform PIC8bit Examples

This directory contains example projects for the PIC8bit platform, demonstrating various features and capabilities of PIC microcontrollers using PlatformIO.

## Available Examples

### PIC16F877 Examples

#### 🔥 Basic Examples
- **[pic16f877-blink](./pic16f877-blink/)** - Basic LED blinking in C
- **[pic16f877-asm-blink](./pic16f877-asm-blink/)** - Basic LED blinking in Assembly

## How to Use Examples

### Method 1: Copy Example to New Project

```bash
# Copy an example to your workspace
cp -r platform-pic8bit/examples/pic16f877-blink my-pic-project
cd my-pic-project

# Build and upload
pio run
pio run -t upload
```

### Method 2: Use PlatformIO Project Generator

```bash
# Initialize new project based on example
pio project init --board pic16f877 --project-option "framework=pic-xc8"

# Copy example source code
cp platform-pic8bit/examples/pic16f877-blink/src/* src/
```

## Example Structure

Each example follows this structure:

```
example-name/
├── platformio.ini          # Project configuration
├── src/                    # Source code
│   └── main.c (or main.s)  # Main application file
├── README.md               # Example documentation
└── docs/                   # Additional documentation (optional)
    ├── schematic.png       # Circuit diagram
    └── notes.md            # Implementation notes
```

## Board-Specific Configuration

### PIC16F877
- **MCU**: PIC16F877
- **Clock**: 20MHz crystal (configurable)
- **Flash**: 8KB
- **RAM**: 368 bytes
- **Frameworks**: pic-xc8

### Build Flags
Common build flags used in examples:

```ini
build_flags = 
    -DDEBUG=1           # Enable debug mode
    -Wall               # Enable all warnings
    -O2                 # Optimization level 2
    -xassembler-with-cpp # Enable C preprocessor for assembly (assembly projects)
    -Wa,-a              # Generate assembly listing (assembly projects)
```

## Hardware Setup

### Basic PIC16F877 Circuit
```
    VDD (5V)
     |
     +-- PIC16F877
     |   |
     |   RB0 ----[330Ω]----[LED]----GND
     |   |
     |   OSC1 ----[22pF]----[20MHz XTAL]----[22pF]----OSC2
     |                            |
     |                           GND
     +-- MCLR ----[10kΩ]----VDD
```

## Programming

All examples support these programmers:
- PICkit 2
- PICkit 3  
- PICkit 4
- MPLAB ICE

Configure your programmer in `platformio.ini`:

```ini
upload_protocol = pickit3
```

## Contributing Examples

To contribute a new example:

1. Create a new directory following the naming convention: `boardname-feature`
2. Include complete `platformio.ini`, source code, and `README.md`
3. Add hardware requirements and circuit diagrams
4. Test thoroughly on real hardware
5. Submit a pull request

## Troubleshooting

### Common Issues

**Build Errors:**
- Ensure XC8 compiler is installed
- Check that xc8-wrapper is properly configured
- Verify board selection in `platformio.ini`

**Upload Errors:**
- Check programmer connection
- Verify upload protocol in configuration
- Ensure target device is powered

**Runtime Issues:**
- Verify crystal frequency matches code configuration
- Check hardware connections
- Review configuration bits

### Getting Help

- Check example README files for specific guidance
- Review platform documentation
- Open an issue on GitHub for bugs or questions

## License

These examples are provided under the same license as the platform-pic8bit project.

## Disclaimer

⚠️ **UNOFFICIAL EXAMPLES** - These examples are community-contributed and not officially supported by Microchip. For official support and examples, use MPLAB X IDE.
