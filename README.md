# PIC 8-bit platform for PlatformIO

⚠️  UNOFFICIAL PLATFORM - NOT SUPPORTED BY MICROCHIP ⚠️

This is an unofficial, community-maintained PlatformIO platform for Microchip PIC 8-bit microcontrollers.

It is experimental and not endorsed or supported by Microchip. Use at your own risk.

Features may change and stability is not guaranteed.

## Features
- Build and upload firmware for PIC 8-bit MCUs using PlatformIO
- Supports (at least partially) [XC8 toolchain](https://www.microchip.com/en-us/tools-resources/develop/mplab-xc-compilers/xc8) via `xc8-wrapper`
- Uploads HEX files using `ipecmd-wrapper` and [MPLAB IPECMD](https://microchip.my.site.com/s/article/Automate-MPLAB-programming-process-using-command-lineIPECMD)

## Requirements
- Python 3.9+
- PlatformIO
- Required Python packages:
  - `xc8_wrapper`
  - `ipecmd_wrapper`

Install dependencies:
```sh
cd platform-pic8bit
pip install -r requirements.txt
```

## Usage
1. Add this platform to your PlatformIO project:
   ```ini
   [env:my-pic-project]
   platform = file://./platform-pic8bit
   board = pic16f876a
   framework = pic-xc8
   ```
2. Build your project:
   ```sh
   pio run
   ```
3. Upload firmware to your device:
   ```sh
   pio run -t upload
   ```

## Notes
- This platform is **unofficial** and not supported by Microchip.
- Make sure XC8 compiler is installed for compiling. 
- Make sure MPLAB X and IPECMD are installed for uploading.
- See `requirements.txt` for Python dependencies.
