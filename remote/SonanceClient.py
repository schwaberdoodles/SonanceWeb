# connects to remote serial server

# Assumes you are running a remote serial server
# `python tcp_serial_redirect.py --spy --ser-nl=CRLF --net-nl=CRLF -c /dev/ttyUSB0 19200`
#

import socket
import json
import os

class SonanceSource:
    TUNER = 1
    AIRPORT = 2
    MOVIE = 3

class SonanceZone:
    OFFICE = 1
    KITCHEN = 2
    LIVING_ROOM = 3
    MASTER_BEDROOM = 4
    AVAS_BEDROOM = 5
    OUTDOOR = 6


class SonanceVolume:
    LOW = 10
    NORMAL = 20
    HIGH = 30
    LOUD = 40

class SonanceFunction:
    SOURCE = 'S'
    POWER = 'Z'
    VOLUME = 'V'
    MUTE = 'M'
    EQ_BASS = 'L'
    EQ_TREBLE = 'H'
    ON = 1
    OFF = 0

class SonanceMessage:
    TERMINATOR = '\r\n'

    def __init__(self):
        self.body = ""

    def append(self, message):
        self.body += message

    def received(self):
        if self.body.endswith(SonanceMessage.TERMINATOR):
            print "message received = %s" % self.body
            return True
        return False

    def status(self):
        if self.body.endswith('+OK',0,-2):
            return SonanceResponse.SONANCE_OK
        elif self.body.endswith('+ERR',0,-2):
            return SonanceResponse.SONANCE_ERROR
        else:
            return SonanceResponse.SONANCE_UNKNOWN

    def length(self):
        return len(self.body)

class SonanceResponse:

    SONANCE_UNKNOWN = -1
    SONANCE_ERROR = 0
    SONANCE_OK = 1
    SONANCE_BAD_MESSAGE = 2;

    def __init__(self):
        self.rsp_status = SonanceResponse.SONANCE_UNKNOWN
        self.msg = SonanceMessage()
        self.status()
        self.rsp_code = 0
        self.zone = 0
        self.value = 0

    def __str__(self):
        if self.rsp_status == SonanceResponse.SONANCE_OK:
            return "OK"
        else:
            return "ERR"

class SonanceZoneState:

    def __init(self,zone,source,power,volume):
        self.zone = zone
        self.source = source
        self.power = power
        self.volume = volume

    def __str__(self):
        return json.dumps({ 'zone': self.zone, 'source': self.source, 'power': self.power, 'volume': self.volume})

class SonanceCommandResponse(SonanceResponse):

    def __init__(self, cmd, status):
        self.cmd = cmd
        self.status = status

    def __str__(self):
        return json.dumps({'cmd': self.cmd, 'status': self.status})


class SonanceQueryResponse(SonanceResponse):

    def __init__(self, message):
        self.message = message
        # like command response but sonance query responses don't contain status codes
        self.status = SonanceResponse.SONANCE_OK
        self.qtype = ""
        self.zone = 0
        self.value = 0
        self.parse()
        #print "query_response->%s<-" % message

    def __str__(self):
        return json.dumps({'qtype': self.qtype, 'status': self._status, 'zone': self.zone, 'value': self.value})

    def set_zone(self, zone):
        self.zone = zone

    def set_value(self, value):
        self.value = value

    def get_status(self):
        return self.status

    def value(self):
        return self.value

    def parse(self):
        if self.message[0] != '+':
            self._status = SONANCE_BAD_MESSAGE
        elif len(self.message) >= 3:
            self.qtype = self.message[1]
            self.zone = self.message[2]
            self.value = self.message[3]
            if len(self.message) >= 4:
                self.value = self.message[3:5]
        else:
            # bad response message
            self.status = SonanceResponse.SONANCE_ERROR

class SonanceRemote:
    SOCK_RECV_BUFFER_SIZE = 32
    SOCK_TIMEOUT = 1

    def __init__(self):
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.settimeout(SonanceRemote.SOCK_TIMEOUT)

    def __del__(self):
        self.disconnect()

    def connect(self, host=os.getenv('SONANCE_SERVER_HOSTNAME', "127.0.0.1"), port=os.getenv('SONANCE_SERVER_PORT', "7777")):
        try:
            self._s = socket.create_connection((host,port))
            print "Connected to %s:%s" % (host, port)
            return True
        except socket.error, v:
            print "Connection Error..."
            return False

    def disconnect(self):
        self._s.close()

    def send_command(self, cmd):
        #print "send_command(%s)" % cmd
        self._s.sendall("%s%s" % (cmd, SonanceMessage.TERMINATOR))
        msg = ""
        while True:
            pkt = self._s.recv(SonanceRemote.SOCK_RECV_BUFFER_SIZE)
            if not pkt:
                break
            else:
                msg += pkt
                if msg.endswith('+OK',0,-2):
                    lines = msg.splitlines()
                    return SonanceCommandResponse(lines[0],SonanceResponse.SONANCE_OK)
                elif msg.endswith('+ERR',0,-2):
                    lines = msg.splitlines()
                    return SonanceCommandResponse(lines[0],SonanceResponse.SONANCE_ERROR)

    def send_query(self, cmd):
        #print "send_query(%s) = " % cmd
        self._s.sendall("%s%s" % (cmd, SonanceMessage.TERMINATOR))
        msg = ""
        while True:
            pkt = self._s.recv(SonanceRemote.SOCK_RECV_BUFFER_SIZE)
            if not pkt:
                break
            else:
                msg += pkt
                if msg.endswith(SonanceMessage.TERMINATOR):
                    return SonanceQueryResponse(msg.strip())

class SonanceCommand:

    def __init__(self,_remote):
        self.r = _remote

    def source(self, zone, source):
        return self.r.send_command(":%s%d%d" % (SonanceFunction.SOURCE, zone, source))

    def poweron(self, zone):
        return self.r.send_command(":%s%d%d" % (SonanceFunction.POWER, zone, SonanceFunction.ON))

    def poweroff(self, zone):
        return self.r.send_command(":%s%d%d" % (SonanceFunction.POWER, zone, SonanceFunction.OFF))

    def volume(self, zone, level):
        return self.r.send_command(":%s%d%d" % (SonanceFunction.VOLUME, zone, level))

    def muteon(self, zone):
        return self.r.send_command(":%s%d%d" % (SonanceFunction.MUTE, zone, SonanceFunction.ON))

    def muteoff(self, zone):
        return self.r.send_command(":%s%d%d" % (SonanceFunction.MUTE, zone, SonanceFunction.OFF))

    def basseq(self, zone, eqlevel):
        return self.r.send_command(":%s%d%d" % (SonanceFunction.EQ_BASS, zone, eqlevel))

    def treble(self, zone,eqlevel):
        return self.r.send_command(":%s%d%d" % (SonanceFunction.EQ_TREBLE, zone, eqlevel))

class SonanceQuery():

    def __init__(self,_remote):
        self.r = _remote

    def zonePower(self,zone):
        return self.r.send_query(":%s%d?" % (SonanceFunction.POWER, zone))

    def source(self,zone):
        return self.r.send_query(":%s%d?" % (SonanceFunction.SOURCE, zone))

    def volume(self,zone):
        return self.r.send_query(":%s%d?" % (SonanceFunction.VOLUME, zone))

    def mute(self,zone):
        return self.r.send_query(":M%d?" % zone)

    def zoneState(self,zone):
        state = SonanceZoneState()
        state.zone = zone
        state.power = self.zonePower(zone).value
        state.source = self.source(zone).value
        state.volume = self.volume(zone).value
        return state

    def zoneStates(self):
        foreach
