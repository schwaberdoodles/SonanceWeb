#SonanceWeb

Provides an HTML5 interface to the Sonance DAB1 (http://www.soundandvision.com/content/sonance-dab1-distributed-audio-system)

* Assumes you have a raspberryip, or something running python 2.7, attached via RS232 serial null modem cable to a Sonance DAB1.

* Uses the sonance serial port and serial protocol to control the DAB1

##Requirements

* Python 2.7
* Pyserial 2.7

##Notes

* Communication with the sonance device is accomplished using the pyserial tcp_serial_redirect capability. SonanceWeb uses a TCP socket to communicate with pyserial. 
# SonanceWeb
