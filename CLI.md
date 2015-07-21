# Smash Command Line Interface #

The general syntax when Smash is invoked from the command line is give
below.

```
smash [options] <serial-device>
```

Here, serial-device is the COM port name (`COMx`) in Windows and
the serial device filename (`/dev/ttySx`, `/dev/ttyUSBx`) in
Linux. In Windows the COM port name can be obtained from the Device
Manager.

## Programming a Hex File ##

The `-P` or `--prog` option is used to program a hex file. The
filename is to be passed as argument to the option.

```
$ smash --prog=file.hex COM3
```

If the program is to be verified by reading back and comparing with
file contents, use the `-V` or `--verify` option.

```
$ smash --verify --prog=file.hex COM3
```

## Reading and Changing Security Bits ##

Security bits can be used to "protect" the code located within the
Flash. Usually protection bits and clock mode bit can be cleared only
by a chip erase operation.

The `-S` or `--prog-sec` option can be used to set security
bits. The security bits to set are passed as an argument to the
option. Each security bit is given an alphabet

| **Bit** | **Meaning** | **Supported In** |
|:--------|:------------|:-----------------|
|W        |Write protect|P89V66x           |
|R        |Read protect |P89V66x           |
|X        |External Execution Inhibit|P89V66x           |
|P        |Parallel Program protect|P89V51Rx2         |

The read and write protect bit in the P89V664 can be enabled by using
the following command.

```
$ smash --prog-sec=RW COM3
```

Some microcontroller support 6x clock mode. In these microcontrollers,
the 6x clock mode can be enabled using `--prog-clock6` option. An
example invocation is shown below.

```
$ smash --prog-clock6 COM3
```

Usually security bits are cleared only by a chip erase operation. A
chip erase can be performed using the `-C` or `--chip-erase`
option. An example invocation is shown below.

```
$ smash --chip-erase COM3
```
