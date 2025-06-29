import unittest
from SonanceClient import *

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
        result = c.volume(SonanceZone.OFFICE, SonanceVolume.NORMAL)
        self.assertEqual(result.status, SonanceResponse.SONANCE_OK)

    def test_muteon(self):
        c = SonanceCommand(self.r)
        self.assertTrue(c.muteon(SonanceZone.OFFICE).status, SonanceCommandResponse.SONANCE_OK)

    def test_party_mode(self):
        c = SonanceCommand(self.r)
        # Turn on zones 1-6
        self.assertTrue(c.poweron(SonanceZone.OFFICE).status)
        self.assertTrue(c.poweron(SonanceZone.LIVING_ROOM).status)
        self.assertTrue(c.muteoff(SonanceZone.OFFICE).status)
        self.assertTrue(c.muteoff(SonanceZone.LIVING_ROOM).status)
        self.assertTrue(c.source(SonanceZone.LIVING_ROOM,SonanceSource.AIRPORT).status)
        self.assertTrue(c.volume(SonanceZone.OFFICE,SonanceVolume.NORMAL).status)
        self.assertTrue(c.volume(SonanceZone.LIVING_ROOM,SonanceVolume.LOW).status)

class TestQueries(unittest.TestCase):

    def setUp(self):
        self.r = SonanceRemote()
        self.r.connect()
        self.query = SonanceQuery(self.r)

    def tearDown(self):
        self.r.disconnect()

    def test_zonePower(self):
        self.assertTrue(self.query.zonePower(SonanceZone.OFFICE).get_status())

    def test_source(self):
        self.assertTrue(self.query.source(SonanceZone.OFFICE).get_status())

    def test_mute(self):
        self.assertTrue(self.query.mute(SonanceZone.OFFICE).get_status())

    def test_zone_state(self):
        print self.query.zoneState(SonanceZone.OFFICE)
        print self.query.zoneState(SonanceZone.LIVING_ROOM)
        print self.query.zoneState(SonanceZone.KITCHEN)
        print self.query.zoneState(SonanceZone.MASTER_BEDROOM)
        print self.query.zoneState(SonanceZone.AVAS_BEDROOM)
        print self.query.zoneState(SonanceZone.OUTDOOR)


