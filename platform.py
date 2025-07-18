# Copyright 2025 Sebastien Celles
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
⚠️  UNOFFICIAL MICROCHIP PIC SUPPORT ⚠️

This platform provides UNOFFICIAL support for Microchip PIC microcontrollers
in PlatformIO using the XC8 compiler through xc8-wrapper.

IMPORTANT DISCLAIMERS:
- This is NOT an official Microchip platform
- This is NOT officially supported by PlatformIO
- This is an EXPERIMENTAL community project
- Use at your own risk for production projects

For official support, use MPLAB X IDE from Microchip.

Platform: PIC 8-bit microcontrollers
Website: https://github.com/s-celles/platform-pic8bit
Documentation: https://github.com/s-celles/platform-pic8bit/blob/main/README.md
"""

from platformio.platform.base import PlatformBase


class Pic8bitPlatform(PlatformBase):
    """
    ⚠️  UNOFFICIAL PLATFORM ⚠️

    This platform supports Microchip PIC 8-bit microcontrollers using:
    - XC8 compiler (via xc8-wrapper)
    - Separate compilation support
    - SCons-based build system

    DISCLAIMER: This is NOT official Microchip or PlatformIO support!
    """

    def configure_default_packages(self, variables, targets):
        """Configure default packages for PIC development"""

        # We don't use pre-built packages, everything is handled by xc8-wrapper
        # which finds and uses the locally installed XC8 compiler
        return PlatformBase.configure_default_packages(self, variables, targets)

    def get_boards(self, id_=None):
        """Get available boards for this platform"""

        # Load boards from boards/ directory
        result = PlatformBase.get_boards(self, id_)
        if not result:
            return result

        # Add platform-specific board configurations
        # Handle both single board (when id_ is specified) and multiple boards
        if id_:
            # Single board case - result is a single board config object
            if hasattr(result, "update"):
                result.update("build.flags", ["-std=c99", "-Wall"])
        else:
            # Multiple boards case - result is a dictionary of board configs
            if hasattr(result, "values"):
                for board_config in result.values():
                    board_config.update("build.flags", ["-std=c99", "-Wall"])

        return result

    def configure_debug_session(self, debug_config):
        """Configure debug session (placeholder for future MPLAB integration)"""

        # Debug support would require MPLAB X IDE integration
        # This is a placeholder for future development
        raise NotImplementedError(
            "Debug support not implemented. "
            "Use MPLAB X IDE for debugging PIC microcontrollers."
        )

    def on_installed(self):
        """Called after platform installation"""

        print("🔧 PIC 8-bit platform installed!")
        print("")
        print("⚠️  IMPORTANT DISCLAIMERS:")
        print("   - This is UNOFFICIAL Microchip PIC support")
        print("   - NOT officially supported by Microchip or PlatformIO")
        print("   - Experimental community project - use at your own risk")
        print("")
        print("📋 Requirements:")
        print("   - Microchip XC8 compiler must be installed")
        print("   - xc8-wrapper Python module required")
        print("")
        print("📚 Documentation:")
        print("   https://github.com/s-celles/platform-pic8bit")
        print("")
        print("🏭 For official support, use MPLAB X IDE")

        return PlatformBase.on_installed(self)
