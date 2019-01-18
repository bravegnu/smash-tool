# Smash

<img src='icons/logo-128.png' align='right'/>

Smash is an 8051 microcontroller In-System Programming (ISP) tool, for
Philips and NXP microcontrollers. It is a replacement for FlashMagic
tool, which is distributed under a non-free license and runs only on
Windows.

Smash is written in Python has both a command line interface and GUI
interface. The GUI interface uses the GTK+ toolkit, and is designed to
work in both Windows and Linux.

## Features

  * Hex file programming
  * Verification after programming
  * Reset and automatic entry into ISP mode, using DTR, RTS
  * Setting and clearing security bits
  * Dumping contents of micro-controller memory
  * Command-line and GUI interface
  * Works on Windows and Linux

## Supported Microcontrollers

| **Microcontroller** | **Supported?** |
| ------------------- | -------------- |
| P89V660             | Yes	       |
| P89V662             | Yes	       |
| P89V664             | Yes	       |
| P89V51RB2 	      | Development    |
| P89V51RC2           | Development    |
| P89V51RD2           | Development    |

## Installation

<img src='docs/prog-screen.png' align='right'/>

  * Please ensure the following packages are available before
    installing smash.

    - python >= 2.4
    - pyserial / python-serial >= 2.2
    - pygtk >= 2.8 (for GUI)
    - python-dbus >= 0.71 (for GUI)

  * Note that it is possible to run smash without the GUI interface,
    in which case pygtk and python-dbus are not required.

  * Run the following command from the smash package root
    directory. (You will require root privileges to install smash in
    the system directories)

```
# python setup.py install
```

## Maintainer

Smash is developed and maintained by [Zilogic Systems](http://zilogic.com).

<img src='docs/zilogic-logo.png'/>
