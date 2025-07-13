#!/usr/bin/env python3
"""
PlatformIO Builder for PIC 8-bit microcontrollers

This is the main entry point for the PIC 8-bit platform builder.
All build logic is delegated to the framework-specific builders.

⚠️  UNOFFICIAL PLATFORM - NOT SUPPORTED BY MICROCHIP ⚠️
"""

import sys
from os.path import join
from SCons.Script import (ARGUMENTS, COMMAND_LINE_TARGETS, Default, DefaultEnvironment)

# Initialize environment
env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()

print("🔧 PIC8bit platform builder initialized")
print(f"🎯 Target MCU: {board.get('build.mcu', 'pic16f876a').upper()}")
print(f"⚡ CPU Frequency: {board.get('build.f_cpu', '4000000L')}")
print("🔨 Build system: SCons + xc8-wrapper")

# Configure basic environment variables that frameworks might need
env.Replace(
    F_CPU=board.get("build.f_cpu", "4000000L"),
    BOARD_MCU=board.get("build.mcu", "pic16f876a").upper(),
    OPTIMIZATION_LEVEL=int(ARGUMENTS.get("optimization_level", "2"))
)

# Add board-specific defines
env.Append(
    CPPDEFINES=[
        "$BOARD_MCU"
    ]
)

# Note: _XTAL_FREQ is handled by the framework, not here

# Load the selected framework
framework = env.get("PIOFRAMEWORK")
if framework:
    env.SConscript(join(platform.get_dir(), "builder", "frameworks", "%s.py" % framework[0]))
else:
    print("❌ No framework specified!")
    sys.stderr.write("Error: Please specify a framework (e.g., framework = pic-xc8)\n")
    env.Exit(1)
