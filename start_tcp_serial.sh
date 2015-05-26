#!/bin/bash
PYSERIAL_EXAMPLES=/usr/share/doc/python-serial/examples
python $PYSERIAL_EXAMPLES/tcp_serial_redirect.py --spy --ser-nl=CRLF --net-nl=CRLF -c /dev/ttyUSB0 19200
