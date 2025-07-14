#!/usr/bin/env python3
"""
⚠️  UNOFFICIAL XC8 FRAMEWORK ⚠️

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

# Initialize PlatformIO environment
env = DefaultEnvironment()

# Print framework info
print("")
print("🔧 XC8 Framework initialized (UNOFFICIAL)")
print("⚠️  NOT officially supported by Microchip or PlatformIO")
print("📋 Using xc8-wrapper to interface with XC8 compiler")
print("🎯 Target: PIC microcontrollers")
print("")

# Get project paths
PROJECT_DIR = env.subst("$PROJECT_DIR")
BUILD_DIR = env.subst("$BUILD_DIR")
PROJECT_SRC_DIR = env.subst("$PROJECT_SRC_DIR")

print(f"📁 Project directory: {PROJECT_DIR}")
print(f"📁 Build directory: {BUILD_DIR}")
print(f"📁 Source directory: {PROJECT_SRC_DIR}")
print("")

try:
    from xc8_wrapper import run_command, get_xc8_tool_path, log

    print("✅ xc8-wrapper imported successfully")
    xc8_available = True
except ImportError as e:
    print(f"❌ Failed to import xc8-wrapper: {e}")
    print("📋 Make sure xc8-wrapper is installed or available in the project")
    xc8_available = False

# Configure compiler for PIC16F876A
DEVICE = env.BoardConfig().get("build.mcu", "pic16f876a")
OPTIMIZATION = env.GetProjectOption("optimization_level", "2")
F_CPU = env.BoardConfig().get("build.f_cpu", "4000000L")

print(f"🎯 Target device: {DEVICE}")
print(f"⚡ CPU frequency: {F_CPU}")
print(f"🔧 Optimization level: {OPTIMIZATION}")
print("")


def get_project_sources():
    """Get source files from PROJECT_SRC_DIR, respecting build_src_filter and excluding headers"""
    print("Collecting source files with build_src_filter support")
    
    # Use PlatformIO's standard source collection mechanism
    # This automatically respects build_src_filter configuration
    source_files = [
        str(Path(PROJECT_SRC_DIR) / str(f))  # Make absolute paths using pathlib
        for f in env.MatchSourceFiles(PROJECT_SRC_DIR, env.get("SRC_FILTER"))
        if not str(f).endswith(('.h', '.hpp'))  # Exclude header files
    ]
    
    print(f"📁 Found {len(source_files)} source files:")
    for src in source_files:
        print(f"  - {src}")
        
    return source_files


# Build function using xc8-wrapper
def build_with_xc8_wrapper(target, source, env):
    """Build using xc8-wrapper integrated with PlatformIO"""
    print("🔄 *** PLATFORM FUNCTION *** Starting XC8 build with xc8-wrapper...")

    if not xc8_available:
        print("❌ xc8-wrapper not available!")
        return 1

    try:
        # Get source files
        source_files = get_project_sources()
        if not source_files:
            print("❌ No source files found!")
            return 1

        # Set build directory
        build_path = Path(BUILD_DIR)
        output_path = build_path / "output"
        output_path.mkdir(parents=True, exist_ok=True)

        print(f"📁 Build directory: {build_path}")
        print(f"📁 Output directory: {output_path}")

        print("🔧 Starting argument construction")

        # Prepare XC8 arguments for compilation - ensure clean F_CPU value
        print(f"🔧 DEBUG: F_CPU={F_CPU}")
        # Force clean F_CPU value without any suffixes for XC8
        clean_f_cpu = str(F_CPU).rstrip("LUlu")
        print(f"🔧 DEBUG: clean_f_cpu={clean_f_cpu}")

        print("🔧 Starting argument construction")

        # Initialize variables
        has_assembly = False
        has_c_files = False
        
        try:
            # Detect if we have assembly files
            assembly_extensions = {'.s', '.asm', '.S', '.inc', '.as'}
            print(f"🔧 DEBUG: source_files={source_files}")
            print(f"🔧 DEBUG: assembly_extensions={assembly_extensions}")
            
            has_assembly = any(Path(src).suffix.lower() in assembly_extensions for src in source_files)
            has_c_files = any(Path(src).suffix.lower() in {'.c'} for src in source_files)
            
            print(f"🔧 DEBUG: has_assembly={has_assembly}, has_c_files={has_c_files}")
            
            # Check each file individually
            for src in source_files:
                src_path = Path(src)
                print(f"🔧 DEBUG: File: {src} -> suffix: '{src_path.suffix}' -> suffix.lower(): '{src_path.suffix.lower()}'")
                print(f"🔧 DEBUG: Is assembly? {src_path.suffix.lower() in assembly_extensions}")
                print(f"🔧 DEBUG: Is C? {src_path.suffix.lower() in {'.c'}}")

            # Base arguments for all file types
            xc8_args = [
                f"-mcpu={DEVICE}",
                f"-O{OPTIMIZATION}",
                f"-D_XTAL_FREQ={clean_f_cpu}",
                "-DDEBUG=1",
                "-Wall",
            ]

            print(f"🔧 DEBUG: Base xc8_args={xc8_args}")

            # Add language-specific flags
            if has_assembly and not has_c_files:
                # Pure assembly project - use pic-as flags
                print("🔧 Building pure assembly project")
                xc8_args = [
                    f"-mcpu={DEVICE}",
                    # pic-as specific flags
                    "-Wa,-a",  # Generate listing
                ]
                print(f"🔧 DEBUG: Assembly flags: {xc8_args}")
            elif has_c_files:
                # C project (with or without assembly)
                print("🔧 Building C project")
                xc8_args.extend([
                    "-std=c99",
                ])
                print(f"🔧 DEBUG: C flags added: {xc8_args}")
                if has_assembly:
                    print("🔧 Mixed C/assembly project detected")
            else:
                print("⚠️ No recognized source files found")
                
        except Exception as e:
            print(f"❌ ERROR in file detection: {e}")
            import traceback
            traceback.print_exc()
            # Default to basic args
            xc8_args = [
                f"-mcpu={DEVICE}",
                f"-O{OPTIMIZATION}",
                f"-D_XTAL_FREQ={clean_f_cpu}",
                "-DDEBUG=1",
                "-Wall",
            ]

        # Add all source files
        xc8_args.extend(source_files)

        # Output file
        output_hex = output_path / "firmware.hex"
        xc8_args.extend(["-o", str(output_hex)])

        print("🔨 Compiling and linking with XC8...")

        # Get appropriate compiler/assembler path based on project type
        try:
            if has_assembly and not has_c_files:
                # Pure assembly project - use pic-as assembler
                print("🔧 Using PIC assembler for pure assembly project")
                tool_path, version_info = get_xc8_tool_path("pic-as")
                print(f"📋 Using PIC assembler: {tool_path}")
            else:
                # C project (with or without assembly) - use xc8-cc compiler
                print("🔧 Using XC8 compiler for C project")
                tool_path, version_info = get_xc8_tool_path("cc")
                print(f"📋 Using XC8 compiler: {tool_path}")
            
            print(f"📋 Version: {version_info}")
        except Exception as e:
            print(f"❌ Failed to find XC8 tool: {e}")
            print("📋 Make sure XC8 compiler is installed from Microchip")
            print("📋 Expected locations: C:/Program Files/Microchip/xc8/v*/bin/")
            return 1

        # Build the complete command
        xc8_cmd = [tool_path] + xc8_args
        print(f"📋 Full command: {' '.join(xc8_cmd)}")

        # Use xc8-wrapper to compile and link
        if has_assembly and not has_c_files:
            success = run_command(xc8_cmd, "Assembling PIC firmware")
        else:
            success = run_command(xc8_cmd, "Compiling and linking PIC firmware")

        if not success:
            print("❌ Compilation/linking failed!")
            return 1

        print(f"✅ Build completed successfully!")
        print(f"📦 Firmware ready: {output_hex}")

        # Copy to PlatformIO expected location
        if target and len(target) > 0:
            target_path = Path(str(target[0]))
            target_path.parent.mkdir(parents=True, exist_ok=True)
            if output_hex.exists():
                import shutil

                shutil.copy2(output_hex, target_path)
                print(f"📋 Created target: {target_path}")
            else:
                print(f"❌ Output file not found: {output_hex}")
                return 1

        return 0

    except Exception as e:
        print(f"❌ Build error: {e}")
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
print("🏭 For official support, use MPLAB X IDE")
print("")
