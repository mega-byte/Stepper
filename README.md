# Stepper
Project to control a stepper motor using an IR remote control.
This project uses a raspberry pi connected to an IR receiver as input and a stepper motor as an output device.
The IR decoding and configuration to a particular commercial IR remote controller is dealt with by the LIRC project.
There are two programs, a client and a server which can be on separate computers but must be on the same network.
The client receives the IR commands from the Remote control and sends them to the server using the Socket method of
inter process communication. The server receives the key presses made and has the logic to interpret and act on them.
Required other modules to import are: os, sys, pylirc, time, subprocess, socket, psutil# temp
