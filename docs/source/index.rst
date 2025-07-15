Welcome to PIC8bit Platform Documentation!
===========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   platforms/pic8bit
   examples/index
   boards/index
   troubleshooting

Overview
--------

The PIC8bit platform provides support for Microchip's 8-bit PIC microcontrollers
in the PlatformIO ecosystem. This unofficial platform enables developers to use
modern development tools and workflows with classic PIC microcontrollers.

.. warning::
    ⚠️ UNOFFICIAL PLATFORM - NOT SUPPORTED BY MICROCHIP ⚠️

    This is an unofficial, community-maintained PlatformIO platform for Microchip PIC 8-bit microcontrollers.

    It is experimental and not endorsed or supported by Microchip. Use at your own risk.

    Features may change and stability is not guaranteed.

.. note::
    **Notes**

    - This platform is unofficial and not supported by Microchip.
    - Make sure XC8 compiler is installed for compiling.
    - Make sure MPLAB X and IPECMD are installed for uploading.
    - See requirements.txt for Python dependencies.

Quick Start
-----------

1. Install PlatformIO
2. Install the platform: ``pio platform install s-celles/pic8bit``
3. Create a new project: ``pio project init --board pic16f876a``
4. Start coding!

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`