import unittest
from sonance import *

def testCommands(cmd):

    # Turn on zones 1-6
    print cmd.poweron(SonanceZone.OFFICE)
    print cmd.poweron(SonanceZone.LIVING_ROOM)
    print cmd.muteoff(SonanceZone.OFFICE)
    print cmd.muteoff(SonanceZone.LIVING_ROOM)

    print cmd.source(SonanceZone.LIVING_ROOM,SonanceSource.AIRPORT)
    print cmd.volume(SonanceZone.OFFICE,SonanceVolume.NORMAL)
    print cmd.volume(SonanceZone.LIVING_ROOM,SonanceVolume.LOW)

    # Set Source to 3
    #print remote.send_command(SonanceCommand.source(SonanceZone.OFFICE,SonanceSource.AIRPORT))

    # Set Volume to 20
    #print remote.send_command(SonanceCommand.volume(SonanceZone.OFFICE, SonanceVolume.LOW))

class TestCommands(unittest.TestCase):

    def setUp(self):
        self.r = SonanceRemote()
        self.r.connect()

    def tearDown(self):
        self.r.disconnect()

    def test_connect(self):
        self.assertTrue(self.r.connect())

    def test_poweron(self):
        c = SonanceCommand(self.r)
        self.assertTrue(c.poweron(SonanceZone.OFFICE).status, SonanceCommandResponse.SONANCE_OK)

    def test_poweroff(self):
        c = SonanceCommand(self.r)
        self.assertTrue(c.poweroff(SonanceZone.OFFICE).status, SonanceCommandResponse.SONANCE_OK)

    def test_source(self):
        c = SonanceCommand(self.r)
        self.assertTrue(c.source(SonanceZone.OFFICE, SonanceSource.AIRPORT).status, SonanceCommandResponse.SONANCE_OK)

    def test_volume(self):
        c = SonanceCommand(self.r)
        self.assertTrue(c.muteoff(SonanceZone.OFFICE).status, SonanceCommandResponse.SONANCE_OK)

    def test_muteon(self):
        c = SonanceCommand(self.r)
        self.assertTrue(c.muteon(SonanceZone.OFFICE).status, SonanceCommandResponse.SONANCE_OK)


def testQueries(r):

    print r.send_query(":Z%d?" % SonanceZone.OFFICE)
    print r.send_query(":S%d?" % SonanceZone.OFFICE)
    print r.send_query(":V%d?" % SonanceZone.OFFICE)
    print r.send_query(":G%d?" % SonanceZone.OFFICE)
    print r.send_query(":M%d?" % SonanceZone.OFFICE)
    print r.send_query(":B%d?" % SonanceZone.OFFICE)
    print r.send_query(":L%d?" % SonanceZone.OFFICE)
    print r.send_query(":H%d?" % SonanceZone.OFFICE)

    print "running queries..."
    query = SonanceQuery(r)
    query.zonePower(SonanceZone.OFFICE)
    query.anyZonesOn()
    query.source(SonanceZone.OFFICE)
    query.volume(SonanceZone.OFFICE)
    query.mute(SonanceZone.OFFICE)

    print cmd.poweroff(SonanceZone.OFFICE)
    print cmd.poweroff(SonanceZone.LIVING_ROOM)


#r = SonanceRemote()

# Connect to the serial server
#r.connect()
#cmd = SonanceCommand(r)
#testCommands(cmd)
#testQueries(r)