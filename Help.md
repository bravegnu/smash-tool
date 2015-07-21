# Smash User Manual #

## In-System Programming ##

Many Philips/NXP microcontrollers have an internal boot monitor, which
allows code to be downloaded into the Flash, by communicating through
the serial port. The method of downloading code is called In-System
Programming (ISP). ISP involves two software components -- 1. the boot
monitor running in the micro-controller 2. PC software to communicate
with the boot monitor and download code. Smash is one such software
that can communicate with the boot monitor.

The procedure for entering into ISP mode, is documented in the
corresponding micro-controller data-sheet.

## Configuring Smash ##

<img src='http://wiki.smash-tool.googlecode.com/hg/config-shot.png' align='right' />

Smash has to be configured, before it can be used for communicating
with the microcontroller. Click on the "Config." toolbar button, to
display the configuration form. The configuration form, contains a
handful of configuration options. The configuration options and their
meaning are given below.

Configuration can be preserved across invocations of Smash by saving
it. The configuration is saved in a configuration file located in
`~/.smashrc`. Click on the "Save" button to save the configuration to
the configuration file.

### Micro. Type ###
This option specifies the type of the microcontroller to program.

### Osc. Freq. (MHz) ###
This option specifies the microcontroller oscillator frequency in
MHz. The oscillator frequency is provided to the microcontroller so
that it can accurately configure the serial port baudrate generator.

## Bps ##
This option specifies the serial port baudrate, to be used for
communicating with the microcontroller.

### Enable reset and ISP entry using RTS/DTR toggling ###
In some development kits, the RTS and DTR signals of the serial port
are connected to the Reset and PSEN signals of the
microcontroller. This allows the microcontroller to be put in the ISP
mode, by appropriately toggling the RTS and DTR signals. This option
specifies whether RTS/DTR toggling should be used to automatically put
the microcontroller in ISP mode.

## Programming a Hex File ##

<img src='http://wiki.smash-tool.googlecode.com/hg/prog-shot.png' align='right' />

The steps for programming a Hex file is given below.

  1. If automatic ISP entry is not enabled, manual enter into ISP mode first.
  1. Click on the "Program" toolbar button, to display the program form.
  1. Select the serial device, from the "Serial Device" combo.
  1. Select the hex file to be programmed, from the "Hex File" combo.
  1. Make sure the checkbox "Erase blocks used in Hex file", is selected.
  1. Click "Program".

The blocks to erase can also be specified manually, by unselecting the
"Erase blocks used in Hex file" checkbox, and the selecting the blocks
to be erased from the "Select blocks to erase" list box.

Program verification, can be specified by selecting the "Verfiy after
programming" checkbox.

## Dumping Contents ##

The contents of the microcontroller flash memory can be view using
Smash. The steps for viewing the flash contents are given below.

  1. Click on the "Dump" toolbar button, to display the dump form.
  1. Select the serial device, from the "Serial Device" combo.
  1. Specify the start address, and the end address of the locations to be viewed.
  1. Click on the "Dump" button.
  1. The contents of the flash are shown in the text area.

## Reading and Changing Security Bits ##

Security bits can be used to "protect" the code located within the
Flash. Write Protect prohibits further block erase and program. Read
Protect prohibits further reading of user code memory. External
Execution Inhibit prohibits execution of instruction from external
code memory. 6x Clock Mode bit can be used to select between 6 and 12
clocks per machine cycle. All protection bits and clock mode bit can
be cleared only by a chip erase operation.

  1. Click on "Security Bits and Clock Mode" toolbar button.
  1. Click on "Read Bits" button read the status of all security and clock mode bits.
  1. Click on the corresponding "Set" buttons to enable the security bit.
  1. Click on the "Erase Code Memory and Security Bits", to erase all the security bits.

## Eavesdropping ##

The hex records and responses exchanged between PC and microcontroller
can be viewed using the Eavesdropping feature.

Click on the "Eavesdrop" toolbar button. The text area contains the
data sent/received to/from the microcontroller. The text in blue, is
the data sent to the microcontroller. The text in red, is the data
received from the microcontroller. The contents of the text area can
be cleared using the "Clear" button, and can be saved using the "Save"
button.