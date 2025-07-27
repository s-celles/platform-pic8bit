"""
Advanced platform configuration and hooks

This module provides additional platform configuration
and installation hooks for platform-pic8bit.
"""

import os
import sys
import subprocess
from pathlib import Path


class PlatformInstaller:
    """Handle platform installation and dependency management"""
    
    def __init__(self):
        self.installed_count = 0
        self.failed_count = 0
        self.dependencies = self._load_dependencies()
    
    def _load_dependencies(self):
        """Load dependencies from pyproject.toml or use fallback"""
        try:
            # Try to load from pyproject.toml
            from .setup_dependencies import get_dependencies
            deps_tuples = get_dependencies()
            
            # Convert to our internal format
            dependencies = []
            for url, name, module in deps_tuples:
                dependencies.append({
                    "url": url,
                    "name": name,
                    "module": module,
                    "description": f"{name} for PIC microcontroller development"
                })
            return dependencies
            
        except Exception:
            # Fallback to hardcoded dependencies
            return [
                {
                    "url": "git+https://github.com/s-celles/xc8-wrapper.git",
                    "name": "xc8-wrapper",
                    "module": "xc8_wrapper",
                    "description": "XC8 compiler wrapper for secure compilation"
                },
                {
                    "url": "git+https://github.com/s-celles/ipecmd-wrapper.git", 
                    "name": "ipecmd-wrapper",
                    "module": "ipecmd_wrapper",
                    "description": "IPECMD wrapper for device programming"
                }
            ]
    
    def check_dependency(self, module_name):
        """Check if a Python module is installed"""
        try:
            __import__(module_name)
            return True
        except ImportError:
            return False
    
    def install_dependency(self, dep_info):
        """Install a single dependency"""
        print(f"[INSTALL] Installing {dep_info['name']}...")
        print(f"[INSTALL]   {dep_info['description']}")
        
        try:
            # Try to install with pip
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", dep_info["url"]],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                print(f"[INSTALL] ✓ Successfully installed {dep_info['name']}")
                self.installed_count += 1
                return True
            else:
                print(f"[INSTALL] ✗ Failed to install {dep_info['name']}")
                if result.stderr:
                    print(f"[INSTALL]   Error: {result.stderr.strip()}")
                self.failed_count += 1
                return False
                
        except subprocess.TimeoutExpired:
            print(f"[INSTALL] ✗ Timeout installing {dep_info['name']}")
            self.failed_count += 1
            return False
        except Exception as e:
            print(f"[INSTALL] ✗ Exception installing {dep_info['name']}: {e}")
            self.failed_count += 1
            return False
    
    def install_all_dependencies(self):
        """Install all required dependencies"""
        print("[SETUP] Checking and installing Python dependencies...")
        print("")
        
        for dep_info in self.dependencies:
            print(f"[CHECK] Checking {dep_info['name']}...")
            
            if self.check_dependency(dep_info["module"]):
                print(f"[CHECK] ✓ {dep_info['name']} is already installed")
                self.installed_count += 1
            else:
                print(f"[CHECK] - {dep_info['name']} not found, installing...")
                self.install_dependency(dep_info)
            
            print("")
        
        return self.installed_count, self.failed_count
    
    def print_summary(self):
        """Print installation summary"""
        total = len(self.dependencies)
        print("=" * 60)
        print(f"Dependency Installation Summary:")
        print(f"  ✓ Installed: {self.installed_count}/{total}")
        if self.failed_count > 0:
            print(f"  ✗ Failed: {self.failed_count}/{total}")
        print("=" * 60)
        
        if self.failed_count > 0:
            print("[WARNING] Some dependencies failed to install.")
            print("You can install them manually using:")
            for dep_info in self.dependencies:
                if not self.check_dependency(dep_info["module"]):
                    print(f"  pip install {dep_info['url']}")
            print("")
            print("Or install the whole package:")
            print("  pip install -e .")
            print("")
    
    def verify_external_tools(self):
        """Verify external tools are available"""
        print("[VERIFY] Checking external tool requirements...")
        
        tools_status = {}
        
        # Check XC8 compiler
        xc8_paths = [
            "C:\\Program Files\\Microchip\\xc8",
            "C:\\Program Files (x86)\\Microchip\\xc8"
        ]
        
        xc8_found = False
        for path in xc8_paths:
            if Path(path).exists():
                print(f"[VERIFY] ✓ XC8 compiler found at: {path}")
                xc8_found = True
                break
        
        if not xc8_found:
            print("[VERIFY] ⚠ XC8 compiler not found in standard locations")
            print("[VERIFY]   Please install XC8 from Microchip website")
        
        tools_status["xc8"] = xc8_found
        
        # Check MPLAB X / IPECMD
        mplab_paths = [
            "C:\\Program Files\\Microchip\\MPLABX",
            "C:\\Program Files (x86)\\Microchip\\MPLABX"
        ]
        
        mplab_found = False
        for path in mplab_paths:
            if Path(path).exists():
                print(f"[VERIFY] ✓ MPLAB X found at: {path}")
                mplab_found = True
                break
        
        if not mplab_found:
            print("[VERIFY] ⚠ MPLAB X not found in standard locations")
            print("[VERIFY]   Please install MPLAB X IDE from Microchip website")
        
        tools_status["mplab"] = mplab_found
        
        return tools_status


def run_platform_setup():
    """Main setup function called during platform installation"""
    installer = PlatformInstaller()
    
    # Install Python dependencies
    installed, failed = installer.install_all_dependencies()
    installer.print_summary()
    
    # Verify external tools
    tools_status = installer.verify_external_tools()
    
    # Final recommendations
    print("")
    print("[SETUP] Platform installation completed!")
    print("")
    
    if failed == 0:
        print("[SUCCESS] All Python dependencies installed successfully!")
    else:
        print(f"[WARNING] {failed} dependencies failed to install")
    
    print("")
    print("[NEXT STEPS]:")
    
    if not tools_status.get("xc8", False):
        print("  1. Install XC8 compiler from Microchip website")
    
    if not tools_status.get("mplab", False):
        print("  2. Install MPLAB X IDE from Microchip website")
    
    print("  3. Create a new PlatformIO project:")
    print("     pio project init --board pic16f876a --project-option \"framework=pic-xc8\"")
    print("  4. Check examples in platform-pic8bit/examples/")
    print("")
    print("[HELP]:")
    print("  - Documentation: https://github.com/s-celles/platform-pic8bit")
    print("  - Issues: https://github.com/s-celles/platform-pic8bit/issues")
    print("")
    
    return installed, failed
