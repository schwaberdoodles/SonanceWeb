from bottle import route, run, template, install, response
from bottle import static_file
from SonanceClient import *

sonance_remote = SonanceRemote()

@route('/',method='GET')
def index():
    return static_file(filename="index.html", root="app/")

@route('/sonance/zones',method='GET')
def zones():
    sonance_remote.connect()
    zone_states = "["
    for zone_id in range(1,6):
        zone_states += SonanceQuery(sonance_remote).zoneState(int(zone_id)).__str__()
    zone_states += "]"
    sonance_remote.disconnect()
    return zone_states

@route('/sonance/zones/<zone_id>',method='GET')
def zone_index(zone_id):
    sonance_remote.connect()
    zone_state = SonanceQuery(sonance_remote).zoneState(int(zone_id))
    sonance_remote.disconnect()
    return zone_state.__str__()

@route('/sonance/zones/<zone_id>/power/on',method='GET')
def zone_power_on(zone_id):
    sonance_remote.connect()
    res = SonanceCommand(sonance_remote).poweron(int(zone_id))
    sonance_remote.disconnect()
    return res.__str__()

@route('/sonance/zones/<zone_id>/power/off',method='GET')
def zone_power_off(zone_id):
    sonance_remote.connect()
    res = SonanceCommand(sonance_remote).poweroff(int(zone_id))
    sonance_remote.disconnect()
    return res.__str__()

@route('/sonance/zones/<zone_id>/source/<source_id>',method='GET')
def zone_source(zone_id,source_id):
    sonance_remote.connect()
    res = SonanceCommand(sonance_remote).source(int(zone_id),int(source_id))
    sonance_remote.disconnect()
    return res.__str__()

@route('/sonance/zones/<zone_id>/source/<source_id>',method='GET')
def zone_source(zone_id,source_id):
    sonance_remote.connect()
    res = SonanceCommand(sonance_remote).source(int(zone_id),int(source_id))
    sonance_remote.disconnect()
    return res.__str__()

@route('/sonance/zones/<zone_id>/volume/<volume_level>',method='GET')
def zone_volume(zone_id,volume_level):
    sonance_remote.connect()
    res = SonanceCommand(sonance_remote).volume(int(zone_id),int(volume_level))
    sonance_remote.disconnect()
    return res.__str__()

run(host="0.0.0.0",port=8080,debug=True)
