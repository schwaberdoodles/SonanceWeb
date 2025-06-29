#SonanceWeb

Provides an HTML5 interface to the Sonance DAB1 (http://www.soundandvision.com/content/sonance-dab1-distributed-audio-system)

* Assumes you have a raspberry pi, or something running python 2.7, attached via RS232 serial null modem cable to a Sonance DAB1.

* Uses the sonance serial port and serial protocol to control the DAB1

* SonanceClient assumes that the serial server is listening on localhost:7777, or another hostname and port defined the SONANCE_SERVER_HOSTNAME and SONANCE_SERVER_PORT environment variables.

##Requirements

* Python 2.7
* Pyserial 2.7

##Notes

* Communication with the sonance device is accomplished using the pyserial tcp_serial_redirect capability. SonanceWeb uses a TCP socket to communicate with pyserial.

* No longer maintained
