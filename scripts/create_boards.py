#!/usr/bin/env python3
"""
Create PlatformIO board configuration files from PIC device specifications

This script generates PlatformIO board JSON files from device specifications
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add atpack-python-parser src to path
atpack_parser_root = Path(__file__).parent.parent.parent.parent / "atpack-python-parser"
sys.path.insert(0, str(atpack_parser_root / "src"))

try:
    from atpack_parser import AtPackParser
except ImportError:
    print("❌ Error: atpack_parser module not found. Please ensure atpack-python-parser is available.")
    sys.exit(1)


class BoardGenerator:
    """Generate PlatformIO board configurations from PIC device specifications."""
    
    def __init__(self, output_dir: Path = None):
        """Initialize the board generator.
        
        Args:
            output_dir: Directory to output board JSON files (default: ../boards)
        """
        if output_dir is None:
            self.output_dir = Path(__file__).parent.parent / "boards"
        else:
            self.output_dir = Path(output_dir)
        
        self.output_dir.mkdir(exist_ok=True)
        
        # Default configuration templates
        self.pic16_protocols = ["pickit2", "pickit3", "pickit4", "mplab-ice", "custom"]
        self.pic24_protocols = ["GEN4", "pickit3", "pickit4", "mplab-ice", "custom"]
    
    def normalize_device_name(self, device_name: str) -> str:
        """Normalize device name for use in filenames and MCU fields."""
        return device_name.lower().replace("pic", "")
    
    def get_default_frequency(self, series: str, device_name: str) -> str:
        """Get default CPU frequency based on device series and name."""
        # Common default frequencies for different PIC series
        freq_map = {
            "PIC16": "4000000",  # 4 MHz
            "PIC18": "8000000",  # 8 MHz  
            "PIC24": "16000000", # 16 MHz
            "PIC32": "80000000", # 80 MHz
        }
        
        # Special cases for specific devices
        if "16F84" in device_name.upper():
            return "4000000"  # 4 MHz max for PIC16F84
        elif "16F877" in device_name.upper():
            return "20000000"  # 20 MHz max for PIC16F877A
        elif "24F" in device_name.upper():
            return "16000000"  # 16 MHz typical for PIC24F
        
        return freq_map.get(series, "4000000")
    
    def get_framework_from_series(self, series: str) -> List[str]:
        """Get appropriate framework based on device series."""
        framework_map = {
            "PIC16": ["pic-xc8"],
            "PIC18": ["pic-xc8"], 
            "PIC24": ["Baremetal"],
            "PIC32": ["arduino"],
        }
        return framework_map.get(series, ["pic-xc8"])
    
    def get_upload_protocol(self, series: str) -> str:
        """Get default upload protocol based on series."""
        protocol_map = {
            "PIC16": "pickit3",
            "PIC18": "pickit3",
            "PIC24": "GEN4",
            "PIC32": "pickit3",
        }
        return protocol_map.get(series, "pickit3")
    
    def get_protocols_list(self, series: str) -> List[str]:
        """Get supported protocols list based on series."""
        if series in ["PIC24", "PIC32"]:
            return self.pic24_protocols
        else:
            return self.pic16_protocols
    
    def create_pic16_board(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Create PIC16/PIC18 board configuration."""
        device_name = spec["device_name"]
        normalized_name = self.normalize_device_name(device_name)
        
        # Handle f_cpu - convert from spec or use default
        f_cpu_spec = spec.get("f_cpu", "User configurable")
        if f_cpu_spec == "User configurable" or not f_cpu_spec:
            f_cpu = self.get_default_frequency(spec["series"], device_name)
        else:
            # Try to extract numeric value if it's a string like "20000000L"
            f_cpu = str(f_cpu_spec).replace("L", "").replace("l", "")
            if not f_cpu.isdigit():
                f_cpu = self.get_default_frequency(spec["series"], device_name)
        
        board_config = {
            "build": {
                "core": normalized_name,
                "extra_flags": f"-D{device_name.upper()}",
                "f_cpu": f_cpu,
                "mcu": normalized_name,
                "variant": normalized_name
            },
            "debug": {
                "tools": {
                    "mplab-ice": {
                        "server": {
                            "executable": "bin/mplabx-ice",
                            "arguments": [
                                "--chip", device_name.upper()
                            ]
                        }
                    }
                }
            },
            "frameworks": self.get_framework_from_series(spec["series"]),
            "name": f"⚠️ UNOFFICIAL {device_name.upper()}",
            "upload": {
                "maximum_ram_size": spec.get("maximum_ram_size", 0),
                "maximum_size": spec.get("maximum_size", 0),
                "protocol": self.get_upload_protocol(spec["series"]),
                "protocols": self.get_protocols_list(spec["series"])
            },
            "url": f"https://www.microchip.com/en-us/product/{device_name.upper()}",
            "vendor": "Microchip",
            "disclaimers": {
                "unofficial": "⚠️ UNOFFICIAL board support - NOT officially supported by Microchip",
                "experimental": "Experimental community project - use at your own risk",
                "official_tools": "For official support, use MPLAB X IDE from Microchip"
            }
        }
        
        return board_config
    
    def create_pic24_board(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Create PIC24/PIC32 board configuration."""
        device_name = spec["device_name"]
        normalized_name = self.normalize_device_name(device_name)
        
        # Handle f_cpu
        f_cpu_spec = spec.get("f_cpu", "User configurable")
        if f_cpu_spec == "User configurable" or not f_cpu_spec:
            f_cpu = self.get_default_frequency(spec["series"], device_name)
        else:
            f_cpu = str(f_cpu_spec).replace("L", "").replace("l", "")
            if not f_cpu.isdigit():
                f_cpu = self.get_default_frequency(spec["series"], device_name)
        
        # Calculate flash end address (maximum_size is in words for PIC)
        flash_size_words = spec.get("maximum_size", 0)
        # For PIC24, each instruction word is 24 bits, but addresses are word-based
        flash_end = f"0x{flash_size_words:X}" if flash_size_words > 0 else "0x0"
        
        board_config = {
            "name": f"WizIO-{device_name.upper()}",
            "url": "https://github.com/Wiz-IO/XC16",
            "vendor": "Microchip",
            "frameworks": self.get_framework_from_series(spec["series"]),
            "build": {
                "category": spec["series"],
                "mcu": normalized_name,
                "f_cpu": f"{f_cpu}L"
            },
            "debug": {},
            "upload": {
                "maximum_ram_size": spec.get("maximum_ram_size", 0),
                "maximum_size": flash_size_words,
                "protocol": self.get_upload_protocol(spec["series"]),
                "device": device_name.upper(),
                "info": {
                    "DeviceID": "0x00000000",  # Would need additional parsing for real device ID
                    "FlashEnd": flash_end,
                    "Eeprom": spec.get("eeprom_addr", "0x0") if spec.get("eeprom_addr") else "0x0",
                    "EepromSize": spec.get("eeprom_size", 0),
                    "Config": spec.get("config_addr", "0x0") if spec.get("config_addr") else "0x0",
                    "ConfigSize": spec.get("config_size", 0)
                },
                "tool": {
                    "power": 1,
                    "release_power": 0,
                    "release_reset": 1,
                    "speed": 100
                }
            }
        }
        
        return board_config
    
    def create_board_config(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Create board configuration based on device specifications."""
        series = spec.get("series", "PIC16")
        
        if series in ["PIC24", "PIC32"]:
            return self.create_pic24_board(spec)
        else:
            return self.create_pic16_board(spec)
    
    def generate_board_file(self, spec) -> Path:
        """Generate a single board JSON file from device specifications.
        
        Args:
            spec: Device specification object from atpack_parser
            
        Returns:
            Path to the generated file
        """
        device_name = spec.device_name
        normalized_name = self.normalize_device_name(device_name)
        
        # Convert spec object to dict for processing
        spec_dict = {
            "device_name": spec.device_name,
            "f_cpu": spec.f_cpu,
            "maximum_ram_size": spec.maximum_ram_size,
            "maximum_size": spec.maximum_size,
            "eeprom_addr": spec.eeprom_addr,
            "eeprom_size": spec.eeprom_size,
            "config_addr": spec.config_addr,
            "config_size": spec.config_size,
            "gpr_total_size": spec.gpr_total_size,
            "architecture": spec.architecture,
            "series": spec.series,
        }
        
        # Create board configuration
        board_config = self.create_board_config(spec_dict)
        
        # Generate filename: pic + normalized device name + .json
        filename = f"pic{normalized_name}.json"
        filepath = self.output_dir / filename
        
        # Write JSON file with proper formatting
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(board_config, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def generate_from_atpack(self, atpack_path: str, device_filter: Optional[List[str]] = None, pic16f_only: bool = False) -> List[Path]:
        """Generate board files from AtPack file.
        
        Args:
            atpack_path: Path to the AtPack file
            device_filter: Optional list of device names to generate (if None, generates all)
            pic16f_only: If True, only generate PIC16F devices
            
        Returns:
            List of generated file paths
        """
        generated_files = []
        
        try:
            parser = AtPackParser(atpack_path)
            print(f"✅ Loaded AtPack: {Path(atpack_path).name}")
            print(f"🏷️  Device family: {parser.device_family}")
            
            # Get all device specifications
            all_specs = parser.get_all_device_specs()
            print(f"📋 Found {len(all_specs)} devices")
            
            # Apply PIC16F filter if requested
            if pic16f_only:
                all_specs = [spec for spec in all_specs if spec.device_name.upper().startswith("PIC16F")]
                print(f"🔍 Filtered to {len(all_specs)} PIC16F devices")
            
            # Filter devices if specified
            if device_filter:
                filtered_specs = [spec for spec in all_specs if spec.device_name in device_filter]
                print(f"🔍 Filtering to {len(filtered_specs)} devices: {device_filter}")
            else:
                filtered_specs = all_specs
            
            # Generate board files
            for spec in filtered_specs:
                try:
                    filepath = self.generate_board_file(spec)
                    generated_files.append(filepath)
                    print(f"  ✅ Generated: {filepath.name}")
                    
                except Exception as e:
                    print(f"  ❌ Failed to generate board for {spec.device_name}: {e}")
            
            print(f"\n🎉 Generated {len(generated_files)} board files in {self.output_dir}")
            
        except Exception as e:
            print(f"❌ Error processing AtPack file: {e}")
            raise
        
        return generated_files


def main():
    """Main function with command-line argument parsing."""
    parser = argparse.ArgumentParser(
        description="Generate PlatformIO board configurations from PIC device specifications",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all PIC16F devices from AtPack:
  python create_boards.py ../../../atpack-python-parser/atpacks/Microchip.PIC16Fxxx_DFP.1.7.162.atpack --pic16f-only
  
  # Generate all devices from AtPack:
  python create_boards.py ../../../atpack-python-parser/atpacks/Microchip.PIC16Fxxx_DFP.1.7.162.atpack
  
  # Generate specific devices only:
  python create_boards.py ../../../atpack-python-parser/atpacks/Microchip.PIC16Fxxx_DFP.1.7.162.atpack --devices PIC16F877A PIC16F84A
  
  # Specify custom output directory:
  python create_boards.py ../../../atpack-python-parser/atpacks/Microchip.PIC16Fxxx_DFP.1.7.162.atpack --output-dir /custom/boards/dir
        """
    )
    
    parser.add_argument(
        "atpack_path",
        help="Path to the AtPack file to process"
    )
    
    parser.add_argument(
        "--devices",
        nargs="*",
        help="Specific device names to generate (if not specified, generates all)"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Output directory for board files (default: ../boards)"
    )
    
    parser.add_argument(
        "--pic16f-only",
        action="store_true",
        help="Generate only PIC16F devices (filters out other series)"
    )
    
    args = parser.parse_args()
    
    print("🚀 PlatformIO Board Generator for PIC Devices")
    print("=" * 60)
    
    # Initialize generator with custom output directory if specified
    output_dir = Path(args.output_dir) if args.output_dir else None
    generator = BoardGenerator(output_dir)
    
    try:
        # Generate from AtPack file
        atpack_path = Path(args.atpack_path)
        if not atpack_path.exists():
            print(f"❌ Error: AtPack file not found: {atpack_path}")
            return 1
        
        print(f"📦 Processing AtPack file: {atpack_path}")
        
        # Apply PIC16F filter if requested
        device_filter = args.devices
        if args.pic16f_only:
            print("🔍 Filtering for PIC16F devices only")
        
        generated = generator.generate_from_atpack(
            str(atpack_path), 
            device_filter,
            pic16f_only=args.pic16f_only
        )
        
        print(f"\n✅ Successfully generated {len(generated)} board files!")
        print(f"📁 Output directory: {generator.output_dir}")
        
        if generated:
            print("\n📋 Generated files:")
            for path in generated[:10]:  # Show first 10
                print(f"  - {path.name}")
            if len(generated) > 10:
                print(f"  ... and {len(generated) - 10} more files")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
