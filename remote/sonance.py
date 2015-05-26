# connects to remote serial server

# Assumes you are running a remote serial server
# `python tcp_serial_redirect.py --spy --ser-nl=CRLF --net-nl=CRLF -c /dev/ttyUSB0 19200`
#

import socket

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
    TYPE_COMMAND = 1
    TYPE_QUERY = 2

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

    def append(self, message):
        self.msg.append(message)

    def set_code(self, code):
        self.rsp_code = code

    def status(self):
        if self.msg.body.endswith('+OK',0,-2):
            self.rsp_status = SonanceResponse.SONANCE_OK
        elif last_msg.message.endswith('+ERR',0,-2):
            self.rsp_status = SonanceResponse.SONANCE_ERROR
        return SonanceResponse.SONANCE_UNKNOWN

class SonanceCommandResponse(SonanceResponse):

    def __init__(self, message):
        self.message = message
        self.status()

class SonanceQueryResponse(SonanceResponse):

    def __init__(self, message):
        self.message = message
        # like command response but sonance query responses don't contain status codes
        self.rsp_status = SonanceResponse.SONANCE_OK
        self.rsp_code = 0
        self.qtype = ""
        self.zone = 0
        self.value = 0
        self.state = 0
        self.parse()

    def set_zone(self, zone):
        self.zone = zone

    def set_value(self, value):
        self.value = value

    def parse(self):
        if self.message.length == 3:
            self.qtype = self.message.message[1]
            self.zone = self.message.message[2]
            self.value = self.message.message[3]
        elif self.message.length == 5:
            self.state = self.message.message[3:5]
        else:
            # bad response message
            self.rsp_status = SonanceResponse.SONANCE_ERROR


class SonanceRemote:
    SOCK_RECV_BUFFER_SIZE = 32
    SOCK_TIMEOUT = 1

    host = "172.16.1.80"
    port = 7777
    _s = socket

    def __init__(self):
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.settimeout(SonanceRemote.SOCK_TIMEOUT)

    def __del__(self):
        self.disconnect()

    def connect(self,host="172.16.1.80",port=7777):
        try:
            self._s = socket.create_connection((host,port))
            return True
        except socket.error, v:
            errorcode=v[0]
            if errorcode==errno.ECONNREFUSED:
                print "Connection Refused"
            return False

    # Send a command message and receive the response
    def send_message(self, msg, msg_type):
        print "send_message(%s)" % msg
        self._s.sendall("%s%s" % (msg, SonanceMessage.TERMINATOR))
        msgs = []
        msgs.append(SonanceMessage())
        while True:
            buff = self._s.recv(SonanceRemote.SOCK_RECV_BUFFER_SIZE)
            if not buff:
                break
            else:
                msgs[-1].append(buff)
                if msg_type == SonanceMessage.TYPE_COMMAND:
                    if msgs[-1].status() != SonanceResponse.SONANCE_UNKNOWN:
                        return msgs
                    else:
                        msgs.append(SonanceMessage)
                elif msg_type == SonanceMessage.TYPE_QUERY:
                    if msgs[-1].received():
                        return msgs

    def send_command(self, cmd):
        #print "send_command(%s) = " % cmd
        return SonanceCommandResponse(self.send_message(cmd,SonanceMessage.TYPE_COMMAND).pop())

    def send_query(self, cmd):
        #print "send_query(%s) = " % cmd
        return SonanceQueryResponse(self.send_message(cmd,SonanceMessage.TYPE_QUERY).pop())

    def disconnect(self):
        self._s.close()

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
        rsp = self.r.send_query(":%s%d?" % (SonanceFunction.POWER, zone))
        print "queryPower (%s) = %s" % (rsp.zone, rsp.state)

    def source(self,zone):
        rsp = self.r.send_query(":%s%d?" % (SonanceFunction.SOURCE, zone))
        print "querySource (%s) = %s" % (rsp.zone, rsp.state)

    def volume(self,zone):
        rsp = self.r.send_query(":%s%d?" % (SonanceFunction.VOLUME, zone))
        print "queryVolume (%s) = %s" % (rsp.zone, rsp.state)

    def mute(self,zone):
        rsp = self.r.send_query(":M%d?" % zone)
        print "queryMute(%s) = %s" % (rsp.zone, rsp.state)

    def anyZonesOn(self):
        # broken
        rsp = self.r.send_query(":Z?")
        print "anyZonesOn() = %s" % rsp


