#!/usr/bin/env python3
"""
[WARNING]  UNOFFICIAL ARDUINO FRAMEWORK FOR PIC [WARNING]

Arduino-style framework for PIC microcontrollers using XC8 compiler.
Provides setup() and loop() functions similar to Arduino IDE.

IMPORTANT DISCLAIMERS:
- This is NOT official Microchip, Arduino, or PlatformIO support
- This is an EXPERIMENTAL community project
- Uses xc8-wrapper to interface with XC8 compiler
- Requires XC8 compiler to be installed separately
- Provides Arduino-style programming model for PIC microcontrollers

For official support, use MPLAB X IDE or Arduino IDE with supported boards.
"""

import os
import sys
from pathlib import Path

from SCons.Script import (
    ARGUMENTS,
    COMMAND_LINE_TARGETS,
    DefaultEnvironment,
)

# Try to import Jinja2 for template rendering (required dependency)
from jinja2 import Environment, FileSystemLoader

# Initialize PlatformIO environment
env = DefaultEnvironment()

# Print framework info
print("")
print("[SETUP] Arduino Framework for PIC initialized (UNOFFICIAL)")
print("[WARNING] NOT officially supported by Microchip, Arduino, or PlatformIO")
print("[INFO] Provides Arduino-style setup() and loop() functions for PIC")
print("[INFO] Using xc8-wrapper to interface with XC8 compiler")
print("[TARGET] Target: PIC microcontrollers with Arduino-style programming")
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
    print("[SOURCES] *** COLLECTING SOURCE FILES ***")
    print("Collecting source files with build_src_filter support")

    # Use PlatformIO's standard source collection mechanism
    # This automatically respects build_src_filter configuration
    all_files = [
        str(Path(PROJECT_SRC_DIR) / str(f))  # Make absolute paths using pathlib
        for f in env.MatchSourceFiles(PROJECT_SRC_DIR, env.get("SRC_FILTER"))
    ]

    print(f"[SOURCES] Raw files found: {len(all_files)}")
    for f in all_files:
        print(f"[SOURCES]   - {f}")

    # Separate C++ and C source files
    cpp_files = [f for f in all_files if f.endswith((".cpp", ".cxx", ".cc"))]
    c_files = [f for f in all_files if f.endswith(".c")]
    header_files = [f for f in all_files if f.endswith((".h", ".hpp", ".hxx"))]

    print(f"[SOURCES] Found {len(all_files)} total files:")
    print(f"[SOURCES]   - C++ source files: {len(cpp_files)}")
    for f in cpp_files:
        print(f"[SOURCES]     * {f}")
    print(f"[SOURCES]   - C source files: {len(c_files)}")
    for f in c_files:
        print(f"[SOURCES]     * {f}")
    print(f"[SOURCES]   - Header files: {len(header_files)}")
    for f in header_files:
        print(f"[SOURCES]     * {f}")

    # If we have C++ files, transpile them
    if cpp_files:
        print("[ARDUINO] *** C++ FILES DETECTED - ARDUINO-STYLE TRANSPILATION ***")
        transpiled_files = transpile_arduino_cpp_files(cpp_files, header_files)
        if transpiled_files:
            # Filter out any existing transpiled C files to avoid duplicates
            # Only include C files that are NOT in a generated_c directory
            non_generated_c_files = [f for f in c_files if "generated_c" not in str(f)]
            # Use only the transpiled files we just generated
            source_files = transpiled_files + non_generated_c_files
            print(
                f"[ARDUINO] Using {len(transpiled_files)} transpiled files + {len(non_generated_c_files)} other C files"
            )
        else:
            print("[ERROR] Arduino-style C++ transpilation failed!")
            return []
    else:
        print("[SOURCES] No C++ files found - using C files only")
        # Only C files
        source_files = c_files

    # Remove duplicates and exclude header files from compilation
    source_files = list(
        set([f for f in source_files if not f.endswith((".h", ".hpp", ".hxx"))])
    )

    print(f"[SOURCES] *** FINAL SOURCE FILES FOR COMPILATION ({len(source_files)}) ***")
    for src in source_files:
        print(f"[SOURCES]   ✓ {src}")

    return source_files


def generate_arduino_header(template_vars):
    """Generate PIC header content using Jinja2 template for Arduino framework"""
    # Get framework directory from environment or use relative path
    framework_dir = (
        Path(__file__).parent
        if "__file__" in globals()
        else Path.cwd() / "platform-pic8bit" / "builder" / "frameworks"
    )
    templates_dir = framework_dir / "templates"

    # Use Jinja2 template engine (required dependency)
    env_jinja = Environment(loader=FileSystemLoader(str(templates_dir)))
    template = env_jinja.get_template("pic_includes.h.j2")
    return template.render(**template_vars)


def transpile_arduino_cpp_files(cpp_files, header_files):
    """Transpile Arduino-style C++ files to C using xc8plusplus with Arduino main() injection"""
    print("[ARDUINO] Starting Arduino-style C++ to C transpilation...")

    try:
        # Try to import xc8plusplus
        try:
            from xc8plusplus import XC8Transpiler

            print("[ARDUINO] xc8plusplus transpiler imported successfully")
        except ImportError:
            print(
                "[WARNING] xc8plusplus not available - Arduino framework requires transpiler"
            )
            return None

        # Create transpiler instance with XC8 include paths
        transpiler = XC8Transpiler()

        # Configure transpiler with XC8 include paths
        xc8_include_paths = [
            r"C:\Program Files\Microchip\xc8\v3.00\pic\include",
            r"C:\Program Files\Microchip\xc8\v3.00\pic\include\proc",
        ]

        # Add include paths to transpiler if it supports it
        if hasattr(transpiler, "add_include_path"):
            for path in xc8_include_paths:
                transpiler.add_include_path(path)
        elif hasattr(transpiler, "include_paths"):
            transpiler.include_paths.extend(xc8_include_paths)

        print(
            f"[ARDUINO] Configured transpiler with XC8 include paths: {xc8_include_paths}"
        )

        # Create output directory for transpiled files
        cpp_dir = Path(cpp_files[0]).parent
        output_dir = cpp_dir / "generated_c"
        output_dir.mkdir(exist_ok=True)

        print(f"[ARDUINO] Transpiling to: {output_dir}")
        print(f"[ARDUINO] Target device: {DEVICE}")
        print(f"[ARDUINO] CPU frequency: {F_CPU}")

        # Create header that includes universal PIC stubs and device configuration
        temp_header = output_dir / "pic_includes.h"

        # Get paths for template system
        # Handle SCons context where __file__ may not be available
        if "__file__" in globals():
            framework_dir = Path(__file__).parent
        else:
            # Fallback for SCons context - use platform directory
            platform_dir = Path(env.PioPlatform().get_dir())
            framework_dir = platform_dir / "builder" / "frameworks"

        stubs_file = framework_dir / "pic_universal_stubs.h"
        templates_dir = framework_dir / "templates"

        # Prepare template variables
        template_vars = {
            "device": DEVICE,
            "device_upper": DEVICE.upper(),
            "f_cpu": F_CPU,
            "clean_f_cpu": F_CPU.rstrip("LUlu"),
            "stubs_file_path": stubs_file.as_posix(),
        }

        # Generate header using Jinja2 template engine (required)
        env_jinja = Environment(loader=FileSystemLoader(str(templates_dir)))
        template = env_jinja.get_template("pic_includes.h.j2")
        pic_header_content = template.render(**template_vars)
        print(f"[ARDUINO] Using Jinja2 template engine from: {templates_dir}")

        temp_header.write_text(pic_header_content)
        print(f"[ARDUINO] Created device-specific header: {temp_header}")
        print(f"[ARDUINO] Using universal stubs from: {stubs_file}")

        # Verify the stubs file exists
        if not stubs_file.exists():
            print(f"[ERROR] Universal stubs file not found: {stubs_file}")
            return None

        # Copy all header files to the output directory first
        print("[ARDUINO] Copying header files to output directory...")
        for header_file in header_files:
            header_path = Path(header_file)
            if header_path.suffix in [".hpp", ".h", ".hxx"]:
                if header_path.suffix == ".hpp":
                    # Convert .hpp to .h for C compilation
                    output_header = output_dir / f"{header_path.stem}.h"
                    content = header_path.read_text()
                    content = content.replace('.hpp"', '.h"')
                    content = content.replace("_HPP", "_H")

                    # Add XC8 include at the top of converted headers
                    if not content.startswith("#include <xc.h>"):
                        content = "#include <xc.h>\n" + content

                    output_header.write_text(content)
                    print(f"[ARDUINO] Converted {header_path.name} -> {output_header.name}")
                else:
                    # Copy .h files directly (but only if not already in output_dir)
                    output_header = output_dir / header_path.name

                    # Check if source and destination are the same
                    if header_path.resolve() != output_header.resolve():
                        import shutil

                        shutil.copy2(header_path, output_header)
                        print(f"[ARDUINO] Copied {header_path.name}")
                    else:
                        print(
                            f"[ARDUINO] Skipped {header_path.name} (already in output directory)"
                        )

        transpiled_files = []
        arduino_main_file = None

        # Transpile C++ source files
        for cpp_file in cpp_files:
            cpp_path = Path(cpp_file)
            output_file = output_dir / f"{cpp_path.stem}.c"

            print(f"[ARDUINO] Transpiling {cpp_path.name} -> {output_file.name}")

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
                        c_content = c_content.replace(
                            '#include "pic_includes.h"', "#include <xc.h>"
                        )
                        
                        # Check if this file contains setup() and loop() functions (Arduino-style)
                        if cpp_path.stem.lower() == "main":
                            has_setup = "void setup(" in c_content
                            has_loop = "void loop(" in c_content
                            has_main = "void main(" in c_content or "int main(" in c_content
                            
                            if has_setup and has_loop and not has_main:
                                print(f"[ARDUINO] ✓ Arduino-style code detected: setup() and loop() found")
                                print(f"[ARDUINO] Adding Arduino framework main() function")
                                
                                # Add Arduino-style main function
                                arduino_main = '''

/**
 * @brief Main function - Arduino framework entry point
 * @details Calls setup() once, then loop() repeatedly
 * @note This function is automatically provided by the Arduino framework
 */
void main(void) {
    setup();
    while(1) {
        loop();
    }
}
'''
                                c_content += arduino_main
                                print(f"[ARDUINO] ✓ Arduino framework main() added to {output_file.name}")
                                arduino_main_file = str(output_file)
                            elif has_main:
                                print(f"[ARDUINO] ✓ Regular main() function found in {output_file.name}")
                                arduino_main_file = str(output_file)
                            else:
                                print(f"[WARNING] No main(), setup(), or loop() functions found in {output_file.name}")
                                print(f"[WARNING] The transpiler generated class definitions but not function implementations")
                                print(f"[ARDUINO] Attempting to create Arduino template stubs...")
                                
                                # Try to create basic Arduino template with empty implementations
                                arduino_template = '''

/**
 * @brief Setup function - Arduino framework initialization
 * @details This is a template stub - implement your initialization code here
 * @note Original C++ code was not transpiled by xc8plusplus
 */
void setup(void) {
    // TODO: Add your initialization code here
    // The transpiler failed to convert the C++ setup() function
    // You may need to manually port the C++ code to C
}

/**
 * @brief Loop function - Arduino framework main loop
 * @details This is a template stub - implement your main loop code here
 * @note Original C++ code was not transpiled by xc8plusplus
 */
void loop(void) {
    // TODO: Add your main loop code here
    // The transpiler failed to convert the C++ loop() function
    // You may need to manually port the C++ code to C
}

/**
 * @brief Main function - Arduino framework entry point
 * @details Calls setup() once, then loop() repeatedly
 * @note This function is automatically provided by the Arduino framework
 */
void main(void) {
    setup();
    while(1) {
        loop();
    }
}
'''
                                c_content += arduino_template
                                print(f"[ARDUINO] ✓ Arduino template stubs added to {output_file.name}")
                                print(f"[ARDUINO] ⚠️  You need to manually implement setup() and loop() functions")
                                print(f"[ARDUINO] ⚠️  The transpiler could not convert the C++ implementations")
                                arduino_main_file = str(output_file)
                        
                        output_file.write_text(c_content)

                    # Only include main.c in the final compilation
                    # The xc8plusplus transpiler should generate a complete main.c with all dependencies
                    if cpp_path.stem.lower() == "main":
                        transpiled_files.append(str(output_file))
                        print(
                            f"[ARDUINO] ✓ Success: {output_file.name} (main file - included in build)"
                        )
                    else:
                        print(
                            f"[ARDUINO] ✓ Success: {output_file.name} (generated for dependency resolution - not directly compiled)"
                        )
                else:
                    print(f"[ARDUINO] ✗ Failed: {cpp_path.name}")
                    return None
            except Exception as e:
                print(f"[ARDUINO] Exception during transpilation of {cpp_path.name}: {e}")
                return None
            finally:
                # Clean up temporary file
                if temp_cpp.exists():
                    temp_cpp.unlink()

        if not arduino_main_file:
            print("[ERROR] No main file found - Arduino framework requires a main.cpp file")
            print("[ERROR] The main.cpp file should contain either:")
            print("[ERROR] 1. setup() and loop() functions (Arduino-style)")
            print("[ERROR] 2. main() function (traditional)")
            return None

        # Clean up temporary PIC header
        if temp_header.exists():
            temp_header.unlink()

        print(
            f"[ARDUINO] Arduino transpilation completed - {len(transpiled_files)} C files generated"
        )
        return transpiled_files

    except Exception as e:
        print(f"[ERROR] Arduino C++ transpilation failed: {e}")
        import traceback

        traceback.print_exc()
        return None


# Build function using xc8-wrapper with Arduino support
def build_with_arduino_xc8_wrapper(target, source, env):
    """Build using xc8-wrapper integrated with PlatformIO for Arduino-style projects"""
    print("=" * 80)
    print("[BUILD] *** ARDUINO FRAMEWORK BUILD FUNCTION CALLED ***")
    print("[BUILD] *** ARDUINO PLATFORM FUNCTION *** Starting XC8 build with xc8-wrapper...")
    print("=" * 80)

    if not xc8_available:
        print("[ERROR] xc8-wrapper not available!")
        return 1

    try:
        # Get source files
        print("[BUILD] Getting Arduino project sources...")
        source_files = get_project_sources()
        if not source_files:
            print("[ERROR] No source files found!")
            return 1

        print(f"[BUILD] Arduino source files to compile: {source_files}")

        # Set build directory
        build_path = Path(BUILD_DIR)
        output_path = build_path / "output"
        output_path.mkdir(parents=True, exist_ok=True)

        print(f"[DIR] Build directory: {build_path}")
        print(f"[DIR] Output directory: {output_path}")

        print("[SETUP] Starting Arduino argument construction")

        # Prepare XC8 arguments for compilation - ensure clean F_CPU value
        print(f"[SETUP] DEBUG: F_CPU={F_CPU}")
        # Force clean F_CPU value without any suffixes for XC8
        clean_f_cpu = str(F_CPU).rstrip("LUlu")
        print(f"[SETUP] DEBUG: clean_f_cpu={clean_f_cpu}")

        # Base arguments for Arduino framework
        xc8_args = [f"-mcpu={DEVICE}", f"-D_XTAL_FREQ={clean_f_cpu}"]

        # Add build_flags from platformio.ini
        build_flags = env.get("BUILD_FLAGS", [])
        if build_flags:
            print(
                f"[SETUP] DEBUG: Adding build_flags from platformio.ini: {build_flags}"
            )
            xc8_args.extend(build_flags)

        print(f"[SETUP] DEBUG: Arduino base xc8_args={xc8_args}")

        # Arduino framework always uses C compilation (since we transpile C++ to C)
        print("[SETUP] Building Arduino-style C project (transpiled from C++)")

        # Output file
        output_hex = output_path / "firmware.hex"

        print("[BUILD] Compiling and linking with XC8 (Arduino framework)...")

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

        print(f"[INFO] Full Arduino command: {' '.join(xc8_cmd)}")

        # Use xc8-wrapper with passthrough
        success = run_command(xc8_cmd, "Building Arduino PIC firmware with xc8-wrapper")

        if not success:
            print("[ERROR] Arduino compilation/linking failed!")
            return 1

        print(f"[OK] Arduino build completed successfully!")
        print(f"[OUTPUT] Arduino firmware ready: {output_hex}")

        # Copy to PlatformIO expected location
        if target and len(target) > 0:
            target_path = Path(str(target[0]))
            target_path.parent.mkdir(parents=True, exist_ok=True)
            if output_hex.exists():
                import shutil

                shutil.copy2(output_hex, target_path)
                print(f"[INFO] Created Arduino target: {target_path}")
            else:
                print(f"[ERROR] Output file not found: {output_hex}")
                return 1

        return 0

    except Exception as e:
        print(f"[ERROR] Arduino build error: {e}")
        import traceback

        traceback.print_exc()
        return 1


# Set up PlatformIO environment for Arduino framework
env.Replace(
    PROGNAME="firmware",
    BUILD_DIR=BUILD_DIR,
)

# Define build targets
firmware_hex = env.Command(
    os.path.join("$BUILD_DIR", "firmware.hex"),
    [],  # Sources will be discovered dynamically
    build_with_arduino_xc8_wrapper,
)

# Set default target
env.Default(firmware_hex)

print("Arduino Framework Commands:")
print("  pio run          - Build Arduino-style firmware using xc8-wrapper")
print("  pio run -t clean - Clean build files")
print("  pio run -t upload- Program device (if configured)")
print("")
print("[ARDUINO] Arduino-style programming model for PIC microcontrollers")
print("[ARDUINO] Write setup() and loop() functions - main() is provided automatically")
print("[OFFICIAL] For official Arduino support, use Arduino IDE with supported boards")
print("[OFFICIAL] For official PIC support, use MPLAB X IDE")
print("")
