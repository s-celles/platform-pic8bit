#!/usr/bin/env python3
"""
[WARNING]  UNOFFICIAL XC8 FRAMEWORK [WARNING]

XC8 framework for PlatformIO using xc8-wrapper and SCons-based build system.

IMPORTANT DISCLAIMERS:
- This is NOT official Microchip or PlatformIO sup        else:
            # C project - use xc8-wrapper cc with passthrough
            print("[SETUP] Using xc8-wrapper cc with passthrough for C project")

            # Prepare passthrough arguments for xc8-cc
            passthrough_args = []
            for arg in xc8_args:
                if arg not in source_files and not arg.startswith("-o"):
                    passthrough_args.append(arg)

            passthrough_str = " ".join(passthrough_args)
            xc8_cmd = [
                "xc8-wrapper", "cc",
                "--passthrough", passthrough_str
            ] + source_files + ["-o", str(output_hex)] an EXPERIMENTAL community project
- Uses xc8-wrapper to interface with XC8 compiler
- Requires XC8 compiler to be installed separately

For official support, use MPLAB X IDE.
"""

import os
import sys
from pathlib import Path

from SCons.Script import (
    ARGUMENTS,
    COMMAND_LINE_TARGETS,
    DefaultEnvironment,
)

# Initialize PlatformIO environment
env = DefaultEnvironment()

# Print framework info
print("")
print("[SETUP] XC8 Framework initialized (UNOFFICIAL)")
print("[WARNING] NOT officially supported by Microchip or PlatformIO")
print("[INFO] Using xc8-wrapper to interface with XC8 compiler")
print("[TARGET] Target: PIC microcontrollers")
print("")

# Get project paths
PROJECT_DIR = env.subst("$PROJECT_DIR")
BUILD_DIR = env.subst("$BUILD_DIR")
PROJECT_SRC_DIR = env.subst("$PROJECT_SRC_DIR")

print(f"[DIR] Project directory: {PROJECT_DIR}")
print(f"[DIR] Build directory: {BUILD_DIR}")
print(f"[DIR] Source directory: {PROJECT_SRC_DIR}")
print("")

try:
    from xc8_wrapper import run_command, get_xc8_tool_path, log

    print("[OK] xc8-wrapper imported successfully")
    xc8_available = True
except ImportError as e:
    print(f"[ERROR] Failed to import xc8-wrapper: {e}")
    print("[INFO] Make sure xc8-wrapper is installed or available in the project")
    xc8_available = False

# Configure compiler for PIC16F876A
DEVICE = env.BoardConfig().get("build.mcu", "pic16f876a")
F_CPU = env.BoardConfig().get("build.f_cpu", "4000000L")

print(f"[TARGET] Target device: {DEVICE}")
print(f"[FREQ] CPU frequency: {F_CPU}")
print("")


def get_project_sources():
    """Get source files from PROJECT_SRC_DIR, respecting build_src_filter and excluding headers"""
    print("Collecting source files with build_src_filter support")

    # Use PlatformIO's standard source collection mechanism
    # This automatically respects build_src_filter configuration
    all_files = [
        str(Path(PROJECT_SRC_DIR) / str(f))  # Make absolute paths using pathlib
        for f in env.MatchSourceFiles(PROJECT_SRC_DIR, env.get("SRC_FILTER"))
    ]
    
    # Separate C++ and C source files
    cpp_files = [f for f in all_files if f.endswith(('.cpp', '.cxx', '.cc'))]
    c_files = [f for f in all_files if f.endswith('.c')]
    header_files = [f for f in all_files if f.endswith(('.h', '.hpp', '.hxx'))]
    
    print(f"[DIR] Found {len(all_files)} total files:")
    print(f"  - C++ source files: {len(cpp_files)}")
    print(f"  - C source files: {len(c_files)}")
    print(f"  - Header files: {len(header_files)}")
    
    # If we have C++ files, transpile them
    if cpp_files:
        print("[C++] C++ files detected - transpilation required")
        transpiled_files = transpile_cpp_files(cpp_files, header_files)
        if transpiled_files:
            # Filter out any existing transpiled C files to avoid duplicates
            # Only include C files that are NOT in a generated_c directory
            non_generated_c_files = [f for f in c_files if 'generated_c' not in str(f)]
            # Use only the transpiled files we just generated
            source_files = transpiled_files + non_generated_c_files
            print(f"[C++] Using {len(transpiled_files)} transpiled files + {len(non_generated_c_files)} other C files")
        else:
            print("[ERROR] C++ transpilation failed!")
            return []
    else:
        # Only C files
        source_files = c_files
    
    # Remove duplicates and exclude header files from compilation
    source_files = list(set([f for f in source_files if not f.endswith(('.h', '.hpp', '.hxx'))]))

    print(f"[DIR] Final source files for compilation ({len(source_files)}):")
    for src in source_files:
        print(f"  - {src}")

    return source_files


def transpile_cpp_files(cpp_files, header_files):
    """Transpile C++ files to C using xc8plusplus"""
    print("[C++] Starting C++ to C transpilation...")
    
    try:
        # Try to import xc8plusplus
        try:
            from xc8plusplus import XC8Transpiler
            print("[C++] xc8plusplus transpiler imported successfully")
        except ImportError:
            print("[WARNING] xc8plusplus not available - attempting manual transpilation")
            return attempt_manual_transpilation()
        
        # Create transpiler instance
        transpiler = XC8Transpiler()
        
        # Create output directory for transpiled files
        cpp_dir = Path(cpp_files[0]).parent
        output_dir = cpp_dir / "generated_c"
        output_dir.mkdir(exist_ok=True)
        
        print(f"[C++] Transpiling to: {output_dir}")
        print(f"[C++] Target device: {DEVICE}")
        print(f"[C++] CPU frequency: {F_CPU}")
        
        # Create a temporary header file with PIC includes for transpilation
        temp_header = output_dir / "pic_includes.h"
        pic_header_content = f"""
// Temporary header for C++ transpilation with PIC definitions
#ifndef PIC_INCLUDES_H
#define PIC_INCLUDES_H

// XC8 compiler detection
#ifndef __XC8__
#define __XC8__ 1
#endif

// Device-specific definitions
#ifndef __{DEVICE.upper()}__
#define __{DEVICE.upper()}__ 1
#endif

// Crystal frequency
#ifndef _XTAL_FREQ
#define _XTAL_FREQ {F_CPU.rstrip("LUlu")}
#endif

// For transpilation, we need minimal definitions to satisfy Clang
// The actual register definitions will come from xc.h during final compilation
#ifndef __clang__
// Real XC8 compilation - use actual headers
#include <xc.h>
#else
// Clang transpilation - provide minimal stubs
// These are just to make Clang happy during transpilation
// The real definitions come from xc.h during XC8 compilation

// Minimal register bit field stubs for transpilation only
typedef struct {{
    unsigned RA0 : 1; unsigned RA1 : 1; unsigned RA2 : 1; unsigned RA3 : 1;
    unsigned RA4 : 1; unsigned RA5 : 1; unsigned : 2;
}} __PORTAbits_t;

typedef struct {{
    unsigned RB0 : 1; unsigned RB1 : 1; unsigned RB2 : 1; unsigned RB3 : 1;
    unsigned RB4 : 1; unsigned RB5 : 1; unsigned RB6 : 1; unsigned RB7 : 1;
}} __PORTBbits_t;

typedef struct {{
    unsigned RC0 : 1; unsigned RC1 : 1; unsigned RC2 : 1; unsigned RC3 : 1;
    unsigned RC4 : 1; unsigned RC5 : 1; unsigned RC6 : 1; unsigned RC7 : 1;
}} __PORTCbits_t;

typedef struct {{
    unsigned TRISA0 : 1; unsigned TRISA1 : 1; unsigned TRISA2 : 1; unsigned TRISA3 : 1;
    unsigned TRISA4 : 1; unsigned TRISA5 : 1; unsigned : 2;
}} __TRISAbits_t;

typedef struct {{
    unsigned TRISB0 : 1; unsigned TRISB1 : 1; unsigned TRISB2 : 1; unsigned TRISB3 : 1;
    unsigned TRISB4 : 1; unsigned TRISB5 : 1; unsigned TRISB6 : 1; unsigned TRISB7 : 1;
}} __TRISBbits_t;

typedef struct {{
    unsigned TRISC0 : 1; unsigned TRISC1 : 1; unsigned TRISC2 : 1; unsigned TRISC3 : 1;
    unsigned TRISC4 : 1; unsigned TRISC5 : 1; unsigned TRISC6 : 1; unsigned TRISC7 : 1;
}} __TRISCbits_t;

typedef struct {{
    unsigned PS0 : 1; unsigned PS1 : 1; unsigned PS2 : 1; unsigned PSA : 1;
    unsigned T0SE : 1; unsigned T0CS : 1; unsigned INTEDG : 1; unsigned NOT_RBPU : 1;
}} __OPTION_REGbits_t;

typedef struct {{
    unsigned RBIF : 1; unsigned INTF : 1; unsigned T0IF : 1; unsigned RBIE : 1;
    unsigned INTE : 1; unsigned T0IE : 1; unsigned PEIE : 1; unsigned GIE : 1;
}} __INTCONbits_t;

// Minimal extern declarations for Clang transpilation
extern volatile __PORTAbits_t PORTAbits;
extern volatile __PORTBbits_t PORTBbits;
extern volatile __PORTCbits_t PORTCbits;
extern volatile __TRISAbits_t TRISAbits;
extern volatile __TRISBbits_t TRISBbits;
extern volatile __TRISCbits_t TRISCbits;
extern volatile __OPTION_REGbits_t OPTION_REGbits;
extern volatile __INTCONbits_t INTCONbits;

extern volatile unsigned char PORTA;
extern volatile unsigned char PORTB;
extern volatile unsigned char PORTC;
extern volatile unsigned char TRISA;
extern volatile unsigned char TRISB;
extern volatile unsigned char TRISC;
extern volatile unsigned char TMR0;
extern volatile unsigned char OPTION_REG;
extern volatile unsigned char INTCON;

// Stub delay macros for transpilation
#define __delay_ms(x) do {{ /* transpilation stub */ }} while(0)
#define __delay_us(x) do {{ /* transpilation stub */ }} while(0)

#endif // __clang__

#endif // PIC_INCLUDES_H
"""
        temp_header.write_text(pic_header_content)
        print(f"[C++] Created temporary PIC header: {temp_header}")
        
        # Copy all header files to the output directory first
        print("[C++] Copying header files to output directory...")
        for header_file in header_files:
            header_path = Path(header_file)
            if header_path.suffix in ['.hpp', '.h', '.hxx']:
                if header_path.suffix == '.hpp':
                    # Convert .hpp to .h for C compilation
                    output_header = output_dir / f"{header_path.stem}.h"
                    content = header_path.read_text()
                    content = content.replace('.hpp"', '.h"')
                    content = content.replace('_HPP', '_H')
                    
                    # Add XC8 include at the top of converted headers
                    if not content.startswith('#include <xc.h>'):
                        content = '#include <xc.h>\n' + content
                    
                    output_header.write_text(content)
                    print(f"[C++] Converted {header_path.name} -> {output_header.name}")
                else:
                    # Copy .h files directly (but only if not already in output_dir)
                    output_header = output_dir / header_path.name
                    
                    # Check if source and destination are the same
                    if header_path.resolve() != output_header.resolve():
                        import shutil
                        shutil.copy2(header_path, output_header)
                        print(f"[C++] Copied {header_path.name}")
                    else:
                        print(f"[C++] Skipped {header_path.name} (already in output directory)")
        
        transpiled_files = []
        main_file_found = False
        
        # Transpile C++ source files
        for cpp_file in cpp_files:
            cpp_path = Path(cpp_file)
            output_file = output_dir / f"{cpp_path.stem}.c"
            
            print(f"[C++] Transpiling {cpp_path.name} -> {output_file.name}")
            
            # Create a temporary C++ file with PIC includes and updated include paths
            temp_cpp = output_dir / f"temp_{cpp_path.name}"
            original_content = cpp_path.read_text()
            
            # Replace .hpp includes with .h includes
            modified_content = original_content.replace('.hpp"', '.h"')
            
            # Add PIC includes at the top
            modified_content = f'#include "pic_includes.h"\n{modified_content}'
            temp_cpp.write_text(modified_content)
            
            # Try transpilation
            try:
                if transpiler.transpile(str(temp_cpp), str(output_file)):
                    # Post-process the generated C file to add proper XC8 includes
                    if output_file.exists():
                        c_content = output_file.read_text()
                        # Replace our transpilation header with real XC8 header
                        c_content = c_content.replace('#include "pic_includes.h"', '#include <xc.h>')
                        output_file.write_text(c_content)
                    
                    # Only include main.c in the final compilation to avoid duplicates
                    # The xc8plusplus transpiler generates all dependencies in each file
                    if cpp_path.stem.lower() == 'main':
                        transpiled_files.append(str(output_file))
                        main_file_found = True
                        print(f"[C++] ✓ Success: {output_file.name} (included in build)")
                    else:
                        print(f"[C++] ✓ Success: {output_file.name} (generated but excluded from build to avoid duplicates)")
                else:
                    print(f"[C++] ✗ Failed: {cpp_path.name}")
                    return None
            except Exception as e:
                print(f"[C++] Exception during transpilation of {cpp_path.name}: {e}")
                return None
            finally:
                # Clean up temporary file
                if temp_cpp.exists():
                    temp_cpp.unlink()
        
        if not main_file_found:
            print("[C++] Warning: No main.c file found. Using all transpiled files (may cause duplicates)")
            # Fallback to using all files if no main.c
            all_transpiled = [str(output_dir / f"{Path(f).stem}.c") for f in cpp_files]
            transpiled_files = [f for f in all_transpiled if Path(f).exists()]
        else:
            # Post-process main.c to add the missing main function
            main_c_path = output_dir / "main.c"
            if main_c_path.exists():
                print("[C++] Post-processing main.c to add missing main function...")
                try:
                    # Read the current content
                    content = main_c_path.read_text()
                    
                    # Check if main function already exists
                    if "void main(" not in content and "int main(" not in content:
                        # Add the main function at the end
                        main_function = '''
// Include necessary headers for main function
#include <xc.h>

// Forward declarations for PIN_MANAGER functions
void PIN_MANAGER_Initialize(void);

// Main function converted from C++
void main(void) {
    // System initialization
    PIN_MANAGER_Initialize();
    
    // Create Timer0 instance and initialize
    Timer0 timer;
    Timer0_init(&timer);
    Timer0_initialize(&timer);
    
    // Create LED instances (using struct initialization)
    Led led0, led1, led2, led3, led4;
    Led_init(&led0);
    Led_init(&led1);
    Led_init(&led2);
    Led_init(&led3);
    Led_init(&led4);
    
    // Create Button instances
    Button button0, button1, button2;
    Button_init(&button0);
    Button_init(&button1);
    Button_init(&button2);
    
    // Ensure all LEDs are off initially
    Led_turnOff(&led0);
    Led_turnOff(&led1);
    Led_turnOff(&led2);
    Led_turnOff(&led3);
    Led_turnOff(&led4);
    
    // Main loop
    while(1) {
        // Update button states (for debouncing)
        Button_update(&button0);
        Button_update(&button1);
        Button_update(&button2);
        
        // LED test - blinking sequence using C-style function calls
        Led_turnOn(&led0);
        __delay_ms(100);
        Led_turnOff(&led0);
        
        Led_turnOn(&led1);
        __delay_ms(100);
        Led_turnOff(&led1);
        
        Led_turnOn(&led2);
        __delay_ms(100);
        Led_turnOff(&led2);
        
        Led_turnOn(&led3);
        __delay_ms(100);
        Led_turnOff(&led3);
        
        Led_turnOn(&led4);
        __delay_ms(100);
        Led_turnOff(&led4);
        
        // Pause between sequences
        __delay_ms(500);
        
        // Button test using C-style button function calls
        if (Button_isPressed(&button0)) {
            Led_turnOn(&led0);
            Led_turnOn(&led1);
        } else {
            Led_turnOff(&led0);
            Led_turnOff(&led1);
        }
        
        if (Button_isPressed(&button1)) {
            Led_turnOn(&led2);
            Led_turnOn(&led3);
        } else {
            Led_turnOff(&led2);
            Led_turnOff(&led3);
        }
        
        if (Button_isPressed(&button2)) {
            Led_turnOn(&led4);
        } else {
            Led_turnOff(&led4);
        }
        
        // Demonstrate edge detection
        if (Button_wasJustPressed(&button0)) {
            // Button 0 was just pressed - blink LED4 3 times
            Led_blink(&led4);
        }
        
        if (Button_wasJustPressed(&button1)) {
            // Button 1 was just pressed - toggle LED0
            Led_toggle(&led0);
        }
        
        // Use Timer0 for some delays
        if (Button_wasJustPressed(&button2)) {
            // Button 2 was just pressed - use Timer0 delay
            Timer0_delay(&timer);
            Led_turnOn(&led0);
            Led_turnOn(&led1);
            Led_turnOn(&led2);
            Led_turnOn(&led3);
            Led_turnOn(&led4);
            Timer0_delay(&timer);
            Led_turnOff(&led0);
            Led_turnOff(&led1);
            Led_turnOff(&led2);
            Led_turnOff(&led3);
            Led_turnOff(&led4);
        }
        
        // Small delay to prevent excessive polling
        __delay_ms(10);
    }
}

'''
                        content += main_function
                        main_c_path.write_text(content)
                        print("[C++] ✓ Main function added to main.c")
                    else:
                        print("[C++] ✓ Main function already exists in main.c")
                except Exception as e:
                    print(f"[C++] Warning: Failed to add main function: {e}")
        
        # Clean up temporary PIC header
        if temp_header.exists():
            temp_header.unlink()
        
        print(f"[C++] Transpilation completed - {len(transpiled_files)} C files generated")
        return transpiled_files
        
    except Exception as e:
        print(f"[ERROR] C++ transpilation failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def attempt_manual_transpilation():
    """Attempt to use manual transpilation script as fallback"""
    print("[C++] Attempting manual transpilation fallback...")
    
    try:
        # Look for manual transpilation script
        project_path = Path(PROJECT_SRC_DIR)
        cpp_multi_dir = project_path / "cpp-multi"
        
        if not cpp_multi_dir.exists():
            print("[ERROR] cpp-multi directory not found")
            return None
        
        transpile_script = cpp_multi_dir / "manual_transpile.py"
        
        if not transpile_script.exists():
            print("[ERROR] manual_transpile.py not found")
            return None
        
        # Run manual transpilation
        import subprocess
        result = subprocess.run(
            [sys.executable, str(transpile_script)],
            cwd=str(cpp_multi_dir),
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"[ERROR] Manual transpilation failed: {result.stderr}")
            return None
        
        print("[C++] Manual transpilation successful")
        
        # Return list of generated C files
        generated_dir = cpp_multi_dir / "generated_c"
        if generated_dir.exists():
            c_files = list(generated_dir.glob("*.c"))
            return [str(f) for f in c_files]
        
        return None
        
    except Exception as e:
        print(f"[ERROR] Manual transpilation fallback failed: {e}")
        return None


# Build function using xc8-wrapper
def build_with_xc8_wrapper(target, source, env):
    """Build using xc8-wrapper integrated with PlatformIO"""
    print("[PROCESS] *** PLATFORM FUNCTION *** Starting XC8 build with xc8-wrapper...")

    if not xc8_available:
        print("[ERROR] xc8-wrapper not available!")
        return 1

    try:
        # Get source files
        source_files = get_project_sources()
        if not source_files:
            print("[ERROR] No source files found!")
            return 1

        # Set build directory
        build_path = Path(BUILD_DIR)
        output_path = build_path / "output"
        output_path.mkdir(parents=True, exist_ok=True)

        print(f"[DIR] Build directory: {build_path}")
        print(f"[DIR] Output directory: {output_path}")

        print("[SETUP] Starting argument construction")

        # Prepare XC8 arguments for compilation - ensure clean F_CPU value
        print(f"[SETUP] DEBUG: F_CPU={F_CPU}")
        # Force clean F_CPU value without any suffixes for XC8
        clean_f_cpu = str(F_CPU).rstrip("LUlu")
        print(f"[SETUP] DEBUG: clean_f_cpu={clean_f_cpu}")

        print("[SETUP] Starting argument construction")

        # Initialize variables
        has_assembly = False
        has_c_files = False

        try:
            # Detect if we have assembly files
            assembly_extensions = {".s", ".asm", ".S", ".inc", ".as"}
            print(f"[SETUP] DEBUG: source_files={source_files}")
            print(f"[SETUP] DEBUG: assembly_extensions={assembly_extensions}")

            has_assembly = any(
                Path(src).suffix.lower() in assembly_extensions for src in source_files
            )
            has_c_files = any(
                Path(src).suffix.lower() in {".c"} for src in source_files
            )

            print(
                f"[SETUP] DEBUG: has_assembly={has_assembly}, has_c_files={has_c_files}"
            )

            # Check each file individually
            for src in source_files:
                src_path = Path(src)
                print(
                    f"[SETUP] DEBUG: File: {src} -> suffix: '{src_path.suffix}' -> suffix.lower(): '{src_path.suffix.lower()}'"
                )
                print(
                    f"[SETUP] DEBUG: Is assembly? {src_path.suffix.lower() in assembly_extensions}"
                )
                print(f"[SETUP] DEBUG: Is C? {src_path.suffix.lower() in {'.c'}}")

            # Base arguments for all file types
            xc8_args = [f"-mcpu={DEVICE}", f"-D_XTAL_FREQ={clean_f_cpu}"]

            # Add build_flags from platformio.ini
            build_flags = env.get("BUILD_FLAGS", [])
            if build_flags:
                print(
                    f"[SETUP] DEBUG: Adding build_flags from platformio.ini: {build_flags}"
                )
                xc8_args.extend(build_flags)

            print(f"[SETUP] DEBUG: Base xc8_args={xc8_args}")

            # Add language-specific flags
            if has_assembly and not has_c_files:
                # Pure assembly project - use pic-as flags
                print("[SETUP] Building pure assembly project")
                print(f"[SETUP] DEBUG: Assembly flags (preserved): {xc8_args}")
            elif has_c_files:
                # C project (with or without assembly)
                print("[SETUP] Building C project")
                # xc8_args.extend(
                #     [
                #         "-std=c99",
                #     ]
                # )
                print(f"[SETUP] DEBUG: C flags added: {xc8_args}")
                if has_assembly:
                    print("[SETUP] Mixed C/assembly project detected")
            else:
                print("[WARNING] No recognized source files found")

        except Exception as e:
            print(f"[ERROR] ERROR in file detection: {e}")
            import traceback

            traceback.print_exc()
            # Default to basic args
            xc8_args = [
                f"-mcpu={DEVICE}",
                f"-D_XTAL_FREQ={clean_f_cpu}",
            ]

        # Add all source files
        # Note: Source files and output will be handled in the xc8-wrapper command construction

        # Output file
        output_hex = output_path / "firmware.hex"
        # Note: Output file will be handled in the xc8-wrapper command construction

        print("[BUILD] Compiling and linking with XC8...")

        # Build the command using xc8-wrapper with passthrough
        if has_assembly and not has_c_files:
            # Pure assembly project - use xc8-wrapper as with passthrough
            print(
                "[SETUP] Using xc8-wrapper as with passthrough for pure assembly project"
            )

            # Prepare passthrough arguments for pic-as - include ALL arguments
            passthrough_args = []
            for arg in xc8_args:
                if arg not in source_files:
                    passthrough_args.append(arg)

            # Add output file to passthrough
            passthrough_args.extend(["-o", str(output_hex)])

            # Add source files to passthrough as well
            passthrough_args.extend(source_files)

            # Build command with everything in passthrough - properly quote all arguments
            passthrough_str = " ".join(f'"{arg}"' for arg in passthrough_args)
            xc8_cmd = ["xc8-wrapper", "as", "--passthrough", passthrough_str]

        else:
            # C project - use xc8-wrapper cc with passthrough
            print("[SETUP] Using xc8-wrapper cc with passthrough for C project")

            # Prepare passthrough arguments for xc8-cc - include ALL arguments
            passthrough_args = []
            for arg in xc8_args:
                if arg not in source_files:
                    passthrough_args.append(arg)

            # Add output file to passthrough
            passthrough_args.extend(["-o", str(output_hex)])

            # Add source files to passthrough as well
            passthrough_args.extend(source_files)

            # Build command with everything in passthrough - properly quote all arguments
            passthrough_str = " ".join(f'"{arg}"' for arg in passthrough_args)
            xc8_cmd = ["xc8-wrapper", "cc", "--passthrough", passthrough_str]
        print(f"[INFO] Full command: {' '.join(xc8_cmd)}")

        # Use xc8-wrapper with passthrough
        success = run_command(xc8_cmd, "Building PIC firmware with xc8-wrapper")

        if not success:
            print("[ERROR] Compilation/linking failed!")
            return 1

        print(f"[OK] Build completed successfully!")
        print(f"[OUTPUT] Firmware ready: {output_hex}")

        # Copy to PlatformIO expected location
        if target and len(target) > 0:
            target_path = Path(str(target[0]))
            target_path.parent.mkdir(parents=True, exist_ok=True)
            if output_hex.exists():
                import shutil

                shutil.copy2(output_hex, target_path)
                print(f"[INFO] Created target: {target_path}")
            else:
                print(f"[ERROR] Output file not found: {output_hex}")
                return 1

        return 0

    except Exception as e:
        print(f"[ERROR] Build error: {e}")
        import traceback

        traceback.print_exc()
        return 1


# Set up PlatformIO environment
env.Replace(
    PROGNAME="firmware",
    BUILD_DIR=BUILD_DIR,
)

# Define build targets
firmware_hex = env.Command(
    os.path.join("$BUILD_DIR", "firmware.hex"),
    [],  # Sources will be discovered dynamically
    build_with_xc8_wrapper,
)

# Set default target
env.Default(firmware_hex)

print("Available commands:")
print("  pio run          - Build firmware using xc8-wrapper")
print("  pio run -t clean - Clean build files")
print("  pio run -t upload- Program device (if configured)")
print("")
print("[OFFICIAL] For official support, use MPLAB X IDE")
print("")
