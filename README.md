# 🏗️ PIC 8-bit platform for PlatformIO

A PlatformIO platform for Microchip PIC microcontroller programming (8bit).

## 📚 Documentation

**For complete documentation, installation instructions, usage examples, and API reference, visit:**

**[https://s-celles.github.io/platform-pic8bit/](https://s-celles.github.io/platform-pic8bit/)**

## ✨ Features

- 🔧 Build and upload firmware for PIC 8-bit MCUs using PlatformIO
- ✅ Supports (at least partially) [XC8 toolchain](https://www.microchip.com/en-us/tools-resources/develop/mplab-xc-compilers/xc8) via [`xc8-wrapper`](https://s-celles.github.io/xc8-wrapper/)
- 🎯 Uploads HEX files using [`ipecmd-wrapper`](https://s-celles.github.io/ipecmd-wrapper/) and [MPLAB IPECMD](https://microchip.my.site.com/s/article/Automate-MPLAB-programming-process-using-command-lineIPECMD)

## ⚖️ Important Legal Notice

⚠️  UNOFFICIAL PLATFORM - NOT SUPPORTED BY MICROCHIP ⚠️

This is an unofficial, community-maintained PlatformIO platform for Microchip PIC 8-bit microcontrollers.

It is experimental and not endorsed or supported by Microchip (nor by PlatformIO team). Use at your own risk.

Features may change and stability is not guaranteed.

### 📦 What This Package Provides

This package provides a PlatformIO platform for PIC microcontrollers (8bit). It interfaces with Microchip's XC8 compiler and MPLAB IPE command-line tool (IPECMD). But it does NOT include the actual MPLAB IPE software nor XC8 compiler.


### 🏢 Microchip XC8 & MPLAB IPE License
The XC8 compiler & MPLAB IPE tools are **proprietary software owned exclusively by Microchip Technology Inc.** You must obtain proper licenses from Microchip to use these tools.

## 🔗 Links

- **[📚 Documentation](https://s-celles.github.io/platform-pic8bit/)** - Complete documentation
- **[💾 Repository](https://github.com/s-celles/platform-pic8bit/)** - Source code
- **[🐛 Issues](https://github.com/s-celles/platform-pic8bit/issues)** - Bug reports
- **[💡 Feature Requests](https://github.com/s-celles/platform-pic8bit/discussions)** - Discussions and feature requests
- **[📝 Changelog](https://s-celles.github.io/platform-pic8bit/changelog/)** - Release history

## 📄 License
**platform-pic8bit** is released under the **Apache Licence 2.0** (see [LICENSE](LICENSE) file).
**Microchip XC8 compiler & MPLAB IPE Tools**: Proprietary Microchip licenses (separate licensing required)

## Notes
- This platform is **unofficial** and not supported by Microchip.
- Make sure XC8 compiler is installed for compiling. 
- Make sure MPLAB X and IPECMD are installed for uploading.
- **Dependencies are automatically installed** when you install the platform

## 🚀 Quick Start

### Automatic Installation (Recommended)

When you install this platform, it will automatically install the required Python dependencies:

```bash
# Install platform (dependencies installed automatically)
pio platform install file://path/to/platform-pic8bit

# Or install from repository
pio platform install https://github.com/s-celles/platform-pic8bit.git
```

### Manual Installation

If automatic installation fails, you can install dependencies manually:

```bash
# Option 1: Install the whole package (recommended)
pip install -e .

# Option 2: Install individual dependencies
pip install git+https://github.com/s-celles/xc8-wrapper.git
pip install git+https://github.com/s-celles/ipecmd-wrapper.git

# Option 3: Use the setup script
python setup_dependencies.py

# Option 4: Use the console script (if package is installed)
setup-pic8bit-deps
```

### Development Installation

For development work:

```bash
# Clone and install in development mode
git clone https://github.com/s-celles/platform-pic8bit.git
cd platform-pic8bit
pip install -e .[dev]

# Run tests
pytest

# Format code
black .

# Type checking
mypy .
```

### Prerequisites

Before using this platform, ensure you have installed:

1. **XC8 Compiler** from Microchip (required for compilation)
2. **MPLAB X IDE** with IPECMD (required for uploading to device)

### Create Your First Project

```bash
# Create new project
pio project init --board pic16f876a --project-option "framework=pic-xc8"

# Build project
pio run

# Upload to device
pio run -t upload
```
- See `requirements.txt` for Python dependencies.

## 🤝 Contributing

Contributions welcome! See the [Contributing Guide](https://s-celles.github.io/platform-pic8bit/contributing/) for setup instructions and contribution guidelines.

---

<div align="center">

Made with ❤️ by [Sébastien Celles](https://github.com/s-celles) for the PIC developer community.

</div>
