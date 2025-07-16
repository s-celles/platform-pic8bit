..  Copyright (c) 2025 Sébastien Celles
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
       http://www.apache.org/licenses/LICENSE-2.0
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

.. _platform_pic8bit:

PIC8bit
=======

:Registry:
    `<https://registry.platformio.org/platforms/s-celles/pic8bit>`__ (not available yet)


:Configuration:
    .. code-block:: ini

        [env:myenv]
        platform = s-celles/pic8bit

PIC8bit is a series of low-cost, low-power 8-bit microcontrollers based on RISC architecture with Harvard memory organization. The PIC (Peripheral Interface Controller) microcontrollers are manufactured by Microchip Technology and feature FLASH memory technology, making them reprogrammable thousands of times. These microcontrollers are widely used in embedded systems due to their simplicity, reliability, and cost-effectiveness.

For more detailed information please visit `vendor site <https://www.microchip.com/?utm_source=platformio.org&utm_medium=docs>`__.

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

Examples
--------

Examples are listed from `PIC8bit development platform repository <https://github.com/s-celles/platform-pic8bit/tree/master/examples?utm_source=platformio.org&utm_medium=docs>`__:

* `c-simple <https://github.com/s-celles/PIC_Test_Project/tree/main/src/simple>`__
* `c-multi <https://github.com/s-celles/PIC_Test_Project/tree/main/src/multi>`__
* `asm-simple <https://github.com/s-celles/PIC_Test_Project/tree/main/src/asm-simple>`__

Debugging
---------

.. warning::
    Debugging support for PIC8bit microcontrollers requires external debug probes and specific hardware configurations. Please refer to Microchip's official documentation for debug probe compatibility.

Tools & Debug Probes
~~~~~~~~~~~~~~~~~~~~

Supported programming and debugging tools depend on the specific PIC microcontroller variant, available hardware and IPECMD compatibility. Common debug tools include:

* **PICkit™ 4**: Universal programmer and debugger for PIC microcontrollers
* **PICkit™ 3**: Universal programmer and debugger for PIC microcontrollers
* **PICkit™ 2**: Universal programmer and debugger for PIC microcontrollers
* ...

External Debug Tools
~~~~~~~~~~~~~~~~~~~~

All PIC8bit microcontrollers supported by this platform require **external debug probes** and are **NOT READY** for debugging out of the box. Please click on board name for further details.

.. list-table::
    :header-rows: 1

    * - Name
      - MCU
      - Frequency
      - Flash
      - RAM
      - Debug
    * - ``pic16f876a``
      - PIC16F876A
      - 20MHz
      - 8KB
      - 368B
      - External

Stable and upstream versions
----------------------------

You can switch between `stable releases <https://github.com/s-celles/platform-pic8bit/releases>`__ of PIC8bit development platform and the latest upstream version using :ref:`projectconf_env_platform` option in :ref:`projectconf` as described below.

Stable
~~~~~~

.. code-block:: ini

    ; Latest stable version, NOT recommended
    ; Pin the version as shown below
    [env:latest_stable]
    platform = s-celles/pic8bit
    board = ...

    ; Specific version
    [env:custom_stable]
    platform = s-celles/pic8bit@x.y.z
    board = ...

Upstream
~~~~~~~~

.. code-block:: ini

    [env:upstream_develop]
    platform = https://github.com/s-celles/platform-pic8bit.git
    board = ...

Packages
--------

.. list-table::
    :header-rows: 1

    * - Name
      - Description
    * - `xc8-wrapper <https://s-celles.github.io/xc8-wrapper/>`__
      - Python wrapper for Microchip XC8 Compiler for 8-bit PIC microcontrollers
    * - `ipecmd-wrapper <https://s-celles.github.io/ipecmd-wrapper/>`__
      - Python wrapper for Microchip IPECMD command to program PIC microcontrollers

.. warning::
    **Linux Users**:

    * Ensure proper USB permissions for PIC programmers/debuggers
    * Install libusb development libraries if required

    **Windows Users:**

    Please ensure you have the correct USB drivers for your PIC programmer/debugger from Microchip

Frameworks
----------

.. list-table::
    :header-rows: 1

    * - Name
      - Description
    * - :ref:`framework_pic_native`
      - Native PIC development using XC8 compiler with direct register access and Microchip's peripheral libraries for maximum performance and hardware control

Boards
------

.. note::
    * You can list pre-configured boards by :ref:`cmd_boards` command
    * For more detailed ``board`` information please scroll the tables below horizontally.

Microchip Technology
~~~~~~~~~~~~~~~~~~~~

.. list-table::
    :header-rows: 1

    * - Name
      - Debug
      - MCU
      - Frequency
      - Flash
      - RAM
      - EEPROM
    * - ``pic16f876a``
      - External
      - PIC16F876A
      - 20MHz
      - 8KB
      - 368B
      - 256B

Board Details
~~~~~~~~~~~~~

PIC16F876A
^^^^^^^^^^

* **Architecture**: 8-bit RISC with Harvard memory organization
* **Instruction Set**: 35 single-word instructions
* **Package**: 28-pin PDIP, SOIC, SSOP
* **Operating Voltage**: 4.0V to 5.5V
* **Peripherals**

  * 3 Timers (Timer0: 8-bit, Timer1: 16-bit, Timer2: 8-bit)
  * ...
  * (See datasheet for detailed specifications)


Configuration
-------------

Basic Project Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a ``platformio.ini`` file in your project root:

.. code-block:: ini

    [platformio]
    src_dir = src

    [env:c-simple]
    ; ⚠️  UNOFFICIAL PLATFORM - NOT SUPPORTED BY MICROCHIP ⚠️
    ; This platform is community-maintained and experimental
    ; Use at your own risk for development/testing purposes only
    ; Official Microchip tools: MPLAB X IDE, MPLAB XC8 compiler
    ; NOTE: Using local platform for testing - switch to GitHub URL once pushed
    ; Simple single-file project
    platform = file://./platform-pic8bit
    ; platform = https://github.com/s-celles/platform-pic8bit.git
    board = pic16f876a
    framework = pic-xc8

    ; Build configuration
    build_flags = 
        -DDEBUG=1
        -Wall
        -O2

    ; Source filter to include only simple subdirectory
    build_src_filter = -<*> +<simple/*>

    ; Upload configuration via IPECMD wrapper
    upload_protocol = ipecmd-wrapper
    upload_flags =
        --tool=PK4  ; Available: PK3, PK4, PK5, ICD3, ICD4, ICD5, ICE4, RICE, SNAP, PM3, PKOB, PKOB4, J32
        --power=5.0
        --ipecmd-version=6.20
    ;    --ipecmd-path=C:\Program Files\Microchip\MPLABX\v6.20\mplab_platform\mplab_ipe\bin\ipecmd.exe
    ;    --erase=true

    ; Custom build flags for XC8
    board_build.f_cpu = 4000000L
    board_build.mcu = pic16f876a

    ; Remove incompatible flags
    build_unflags = 
        -std=gnu11

Advanced Configuration
~~~~~~~~~~~~~~~~~~~~~~
For more complex projects, you can define multiple environments in your `platformio.ini` file. Each environment can have its own configuration, such as different boards, frameworks, and build flags.


Getting Started
---------------

1. Install PlatformIO
~~~~~~~~~~~~~~~~~~~~~

Follow the `PlatformIO installation guide <https://platformio.org/install>`__ for your operating system.

2. Create a New Project
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    pio project init --board pic16f876a --project-dir my-pic-project
    cd my-pic-project

3. Write Your First Program
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create ``src/main.c``:

.. code-block:: c

    /*
    * PIC 16F876A Project with PlatformIO
    * 4MHz Crystal - LED Blinking on PORTB
    */

    #include <xc.h>

    // Configuration bits for PIC16F876A with 4MHz crystal
    #pragma config FOSC = HS        // HS oscillator (high speed crystal)
    #pragma config WDTE = OFF       // Watchdog Timer disabled
    #pragma config PWRTE = OFF      // Power-up Timer disabled
    #pragma config BOREN = ON       // Brown-out Reset enabled
    #pragma config LVP = OFF        // Low Voltage Programming disabled
    #pragma config CPD = OFF        // Data EEPROM Memory Code Protection disabled
    #pragma config WRT = OFF        // Flash Program Memory Write Enable disabled
    #pragma config CP = OFF         // Flash Program Memory Code Protection disabled

    /** Define crystal frequency (4MHz) */
    #define _XTAL_FREQ 4000000

    #define LED4 PORTCbits.RC2
    #define LED3 PORTCbits.RC1
    #define LED2 PORTCbits.RC0
    #define LED1 PORTAbits.RA5
    #define LED0 PORTAbits.RA3

    #define BUT0 PORTAbits.RA2
    #define BUT1 PORTAbits.RA1
    #define BUT2 PORTAbits.RA4

    void main(void) {
        TRISC = 0b00100000;
        TRISA = 0b00010110;
        TRISB = 0b00000000;
        ADCON1 = 0b00000110;

        LED0 = 0;
        LED1 = 0;
        LED2 = 0;
        LED3 = 0;
        LED4 = 0;

        // Main loop
        while(1) {
            // Blinking sequence
            LED2 = !LED2;        
            __delay_ms(500);       // 500 ms before toggle
        }
    }


4. Build and Upload
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    pio run
    pio run --target upload

Features
--------

* **Comprehensive Toolchain**: Integrated XC8 compiler support
* **Multiple Programming Methods**: Support for various Microchip programmers
* **Rich Peripheral Support**: ADC, UART, SPI, I²C, PWM, and Timer libraries
* **Configuration Management**: Easy configuration bit management
* **Code Optimization**: Multiple optimization levels supported
* **Debugging Support**: Integration with Microchip debugging tools

Limitations
-----------

.. warning::
    This platform is currently in **Work In Progress (WIP)** (it's neither supported by Microchip nor by PlatformIO) status:

    * Limited board support (currently focusing on PIC16F8XX series)
    * Debugging features may require additional configuration
    * Some advanced PIC features may not be fully supported
    * Community-driven project with unofficial support

Community and Support
---------------------

* **GitHub Repository**: `s-celles/platform-pic8bit <https://github.com/s-celles/platform-pic8bit>`__
* **Issues and Feature Requests**: Use GitHub Issues for bug reports and feature requests
* **Documentation**: `PlatformIO PIC8bit Platform Docs <https://s-celles.github.io/platform-pic8bit/>`__
* **Microchip Official Resources**: `Microchip Developer Help <https://microchipdeveloper.com/>`__

Contributing
------------

This is a community-driven project. Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request with your improvements

Areas where contributions are particularly welcome:

* Additional board definitions
* Enhanced debugging support
* More comprehensive examples
* Documentation improvements
* Framework enhancements

License
-------

This platform follows the same licensing as PlatformIO Core. Please refer to the `LICENSE <https://github.com/s-celles/platform-pic8bit/blob/master/LICENSE>`__ file in the repository for details.

.. _projectconf_env_platform:

projectconf_env_platform
------------------------

This is a placeholder for the 'projectconf_env_platform' label.

.. _projectconf:

projectconf
-----------

This is a placeholder for the 'projectconf' label.

.. _framework_pic_native:

framework_pic_native
--------------------

This is a placeholder for the 'framework_pic_native' label.

.. _cmd_boards:

cmd_boards
----------

This is a placeholder for the 'cmd_boards' label.