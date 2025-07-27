#!/usr/bin/env python3
"""
Installation script for platform-pic8bit dependencies

This script can be run manually if automatic installation fails:
python setup_dependencies.py

Or as a console script (if package is installed):
setup-pic8bit-deps

This script reads dependencies from pyproject.toml if available,
otherwise falls back to hardcoded list.
"""

import subprocess
import sys
import os
from pathlib import Path


def read_dependencies_from_pyproject():
    """Read dependencies from pyproject.toml if available"""
    try:
        # Try to use tomllib (Python 3.11+) or tomli (fallback)
        try:
            import tomllib
        except ImportError:
            try:
                import tomli as tomllib
            except ImportError:
                return None

        pyproject_path = Path(__file__).parent / "pyproject.toml"
        if not pyproject_path.exists():
            return None

        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)

        # Extract dependencies from pyproject.toml
        dependencies = []
        for dep in data.get("project", {}).get("dependencies", []):
            if "git+" in dep and "@" in dep:
                # Parse format: "package-name @ git+https://..."
                parts = dep.split(" @ ")
                if len(parts) == 2:
                    package_name = parts[0].strip()
                    package_url = parts[1].strip()
                    module_name = package_name.replace("-", "_")
                    dependencies.append((package_url, package_name, module_name))

        return dependencies if dependencies else None

    except Exception as e:
        print(f"[DEBUG] Could not read pyproject.toml: {e}")
        return None


def get_dependencies():
    """Get dependencies from pyproject.toml or fallback to hardcoded list"""
    # Try to read from pyproject.toml first
    deps = read_dependencies_from_pyproject()
    if deps:
        print("[INFO] Using dependencies from pyproject.toml")
        return deps

    # Fallback to hardcoded list
    print("[INFO] Using fallback dependency list")
    return [
        (
            "git+https://github.com/s-celles/xc8-wrapper.git",
            "xc8-wrapper",
            "xc8_wrapper",
        ),
        (
            "git+https://github.com/s-celles/ipecmd-wrapper.git",
            "ipecmd-wrapper",
            "ipecmd_wrapper",
        ),
    ]


def install_dependency(package_url, package_name):
    """Install a single dependency via pip"""
    print(f"[INSTALL] Installing {package_name}...")

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package_url],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode == 0:
            print(f"[INSTALL] ✓ Successfully installed {package_name}")
            return True
        else:
            print(f"[INSTALL] ✗ Failed to install {package_name}")
            print(f"[INSTALL]   Error: {result.stderr.strip()}")
            return False

    except Exception as e:
        print(f"[INSTALL] ✗ Exception installing {package_name}: {e}")
        return False


def check_dependency(module_name):
    """Check if a dependency is already installed"""
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False


def main():
    """Main installation function"""
    print("=" * 60)
    print("PIC 8-bit Platform Dependencies Installer")
    print("=" * 60)
    print()

    # Get dependencies from pyproject.toml or fallback
    dependencies = get_dependencies()

    success_count = 0

    for package_url, package_name, module_name in dependencies:
        print(f"[CHECK] Checking {package_name}...")

        if check_dependency(module_name):
            print(f"[CHECK] ✓ {package_name} is already installed")
            success_count += 1
        else:
            print(f"[CHECK] - {package_name} not found, installing...")
            if install_dependency(package_url, package_name):
                success_count += 1

        print()

    print("=" * 60)
    print(
        f"Installation Summary: {success_count}/{len(dependencies)} packages installed"
    )

    if success_count == len(dependencies):
        print("[SUCCESS] All dependencies installed successfully!")
        print()
        print("[NEXT STEPS]:")
        print("1. Ensure XC8 compiler is installed from Microchip")
        print("2. Create a PlatformIO project with platform: pic8bit")
        print("3. Choose board: pic16f876a or pic16f877")
        print("4. Set framework: pic-xc8")
        print()
        print("[EXAMPLES] Check platform-pic8bit/examples/ for sample projects")
        print("[INSTALL] You can also install in development mode with:")
        print("          pip install -e .")
    else:
        print("[WARNING] Some dependencies failed to install")
        print("You may need to install them manually:")
        for package_url, package_name, module_name in dependencies:
            if not check_dependency(module_name):
                print(f"  pip install {package_url}")
        print()
        print("[ALTERNATIVE] Try installing the whole package:")
        print("              pip install -e .")

    print("=" * 60)


if __name__ == "__main__":
    main()
