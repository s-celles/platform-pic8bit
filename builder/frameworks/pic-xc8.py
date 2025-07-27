#!/usr/bin/env python3
"""
[WARNING]  UNOFFICIAL XC8 FRAMEWORK [WARNING]

XC8 framework for PlatformIO using xc8-wrapper and SCons-based build system.

IMPORTANT DISCLAIMERS:
- This is NOT official Microchip or PlatformIO support
- This is an EXPERIMENTAL community project
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

# Try to import Jinja2 for template rendering (required dependency)
from jinja2 import Environment, FileSystemLoader

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
        print("[C++] *** C++ FILES DETECTED - TRANSPILATION REQUIRED ***")
        transpiled_files = transpile_cpp_files(cpp_files, header_files)
        if transpiled_files:
            # Filter out any existing transpiled C files to avoid duplicates
            # Only include C files that are NOT in a generated_c directory
            non_generated_c_files = [f for f in c_files if "generated_c" not in str(f)]
            # Use only the transpiled files we just generated
            source_files = transpiled_files + non_generated_c_files
            print(
                f"[C++] Using {len(transpiled_files)} transpiled files + {len(non_generated_c_files)} other C files"
            )
        else:
            print("[ERROR] C++ transpilation failed!")
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


def generate_header_fallback(template_vars):
    """Generate PIC header content using Jinja2 template (required)"""
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


def transpile_cpp_files(cpp_files, header_files):
    """Transpile C++ files to C using xc8plusplus"""
    print("[C++] Starting C++ to C transpilation...")

    try:
        # Try to import xc8plusplus
        try:
            from xc8plusplus import XC8Transpiler

            print("[C++] xc8plusplus transpiler imported successfully")
        except ImportError:
            print(
                "[WARNING] xc8plusplus not available - attempting manual transpilation"
            )
            return attempt_manual_transpilation()

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
            f"[C++] Configured transpiler with XC8 include paths: {xc8_include_paths}"
        )

        # Create output directory for transpiled files
        cpp_dir = Path(cpp_files[0]).parent
        output_dir = cpp_dir / "generated_c"
        output_dir.mkdir(exist_ok=True)

        print(f"[C++] Transpiling to: {output_dir}")
        print(f"[C++] Target device: {DEVICE}")
        print(f"[C++] CPU frequency: {F_CPU}")

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
        print(f"[C++] Using Jinja2 template engine from: {templates_dir}")

        temp_header.write_text(pic_header_content)
        print(f"[C++] Created device-specific header: {temp_header}")
        print(f"[C++] Using universal stubs from: {stubs_file}")

        # Verify the stubs file exists
        if not stubs_file.exists():
            print(f"[ERROR] Universal stubs file not found: {stubs_file}")
            return None

        # Copy all header files to the output directory first
        print("[C++] Copying header files to output directory...")
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
                        print(
                            f"[C++] Skipped {header_path.name} (already in output directory)"
                        )

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
                        c_content = c_content.replace(
                            '#include "pic_includes.h"', "#include <xc.h>"
                        )
                        output_file.write_text(c_content)

                    # Only include main.c in the final compilation to avoid duplicates
                    # The xc8plusplus transpiler generates all dependencies in each file
                    if cpp_path.stem.lower() == "main":
                        transpiled_files.append(str(output_file))
                        main_file_found = True
                        print(
                            f"[C++] ✓ Success: {output_file.name} (included in build)"
                        )
                    else:
                        print(
                            f"[C++] ✓ Success: {output_file.name} (generated but excluded from build to avoid duplicates)"
                        )
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
            print(
                "[C++] Warning: No main.c file found. Using all transpiled files (may cause duplicates)"
            )
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
                        # Add standard main function (no template needed)
                        main_function = """
// Include necessary headers for main function
#include <xc.h>

// Forward declarations for PIN_MANAGER functions
void PIN_MANAGER_Initialize(void);

// Main function converted from C++
void main(void) {
    // System initialization
    PIN_MANAGER_Initialize();
    
    // Main loop
    while(1) {
        // Application logic goes here
        __delay_ms(10);
    }
}
"""
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

        print(
            f"[C++] Transpilation completed - {len(transpiled_files)} C files generated"
        )
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
            text=True,
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
    print("=" * 80)
    print("[BUILD] *** XC8 BUILD FUNCTION CALLED ***")
    print("[BUILD] *** PLATFORM FUNCTION *** Starting XC8 build with xc8-wrapper...")
    print("=" * 80)

    if not xc8_available:
        print("[ERROR] xc8-wrapper not available!")
        return 1

    try:
        # Get source files
        print("[BUILD] Getting project sources...")
        source_files = get_project_sources()
        if not source_files:
            print("[ERROR] No source files found!")
            return 1

        print(f"[BUILD] Source files to compile: {source_files}")

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
