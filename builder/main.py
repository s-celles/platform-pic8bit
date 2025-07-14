#!/usr/bin/env python3
"""
PlatformIO Builder for PIC 8-bit microcontrollers

This is the main entry point for the PIC 8-bit platform builder.
All build logic is delegated to the framework-specific builders.

⚠️  UNOFFICIAL PLATFORM - NOT SUPPORTED BY MICROCHIP ⚠️
"""

import sys
from os.path import join
from pathlib import Path
from SCons.Script import ARGUMENTS, COMMAND_LINE_TARGETS, Default, DefaultEnvironment

ALLOWED_UPLOAD_PROTOCOLS = ["ipecmd-wrapper"]

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
    OPTIMIZATION_LEVEL=int(ARGUMENTS.get("optimization_level", "2")),
)

# Add board-specific defines
env.Append(CPPDEFINES=["$BOARD_MCU"])

# Note: _XTAL_FREQ is handled by the framework, not here


def upload_via_ipecmd(target, source, env):
    """Upload firmware via IPECMD wrapper"""
    print("📦 Starting upload via IPECMD...")

    try:
        # Import ipecmd-wrapper (now it should be installed)
        from ipecmd_wrapper.core import program_pic

        # Create args namespace similar to CLI
        class Args:
            def __init__(self):
                self.part = board.get("build.mcu", "pic16f876a").upper()
                upload_protocol = env.GetProjectOption("upload_protocol")
                assert upload_protocol in ALLOWED_UPLOAD_PROTOCOLS, (
                    f"Unknown upload protocol '{upload_protocol}' - must be in {ALLOWED_UPLOAD_PROTOCOLS}"
                )
                self.tool = self._get_upload_option("tool", None)
                self.file = str(source[0]) if source else None
                self.power = self._get_upload_option("power", None)
                self.memory = ""
                self.verify = ""
                self.erase = self._get_upload_option("erase", True, is_boolean=True)
                self.logout = True
                self.vdd_first = False
                self.test_programmer = False

                # Get ipecmd configuration from upload_flags
                self.ipecmd_version = self._get_upload_option("ipecmd-version", None)
                self.ipecmd_path = self._get_upload_option("ipecmd-path", None)

            def _get_upload_option(
                self, option_name: str, default=None, is_boolean=False
            ):
                """Extract options from upload_flags with proper parsing"""
                # Method 1: Use PlatformIO's built-in method
                upload_flags = env.GetProjectOption("upload_flags", [])

                if isinstance(upload_flags, str):
                    upload_flags = upload_flags.split()

                # Method 2: Alternative - use env.subst to resolve variables
                if not upload_flags or upload_flags == [""]:
                    try:
                        resolved_flags = env.subst("$UPLOAD_FLAGS")
                        if resolved_flags and resolved_flags != "$UPLOAD_FLAGS":
                            upload_flags = resolved_flags.split()
                    except:
                        pass

                # Look for --option=value format
                for flag in upload_flags:
                    if flag.startswith(f"--{option_name}="):
                        value = flag.split("=", 1)[1]
                        if is_boolean:
                            return value.lower() in ("true", "1", "yes", "on")
                        return value

                # Look for --option value format (separate arguments)
                for i, flag in enumerate(upload_flags):
                    if flag == f"--{option_name}" and i + 1 < len(upload_flags):
                        value = upload_flags[i + 1]
                        if is_boolean:
                            return value.lower() in ("true", "1", "yes", "on")
                        return value

                # Look for boolean flags (just --option without value)
                if is_boolean and f"--{option_name}" in upload_flags:
                    return True

                return default

        args = Args()

        print(f"🐛 DEBUG: IPECMD version from config: {args.ipecmd_version}")
        print(f"🐛 DEBUG: IPECMD path from config: {args.ipecmd_path}")

        if not args.file:
            print("❌ No HEX file to upload")
            return 1

        print(f"📦 Uploading {args.file} to {args.part} via {args.tool}")

        # Call the main programming function
        program_pic(args)

        print("✅ Upload completed successfully!")
        return 0

    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("❌ ipecmd-wrapper not found. Please ensure it's installed.")
        print("💡 Try: cd ipecmd-wrapper && pip install -e .")
        return 1
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        import traceback

        traceback.print_exc()
        return 1


# Load the selected framework
framework = env.get("PIOFRAMEWORK")
if framework:
    env.SConscript(
        join(platform.get_dir(), "builder", "frameworks", "%s.py" % framework[0])
    )
else:
    print("❌ No framework specified!")
    sys.stderr.write("Error: Please specify a framework (e.g., framework = pic-xc8)\n")
    env.Exit(1)


# Add upload target after framework is loaded
if "upload" in COMMAND_LINE_TARGETS:
    # Use the same target as defined in the framework
    firmware_hex = "$BUILD_DIR/firmware.hex"
    upload_target = env.Alias("upload", firmware_hex, upload_via_ipecmd)
    env.AlwaysBuild(upload_target)
