import serial
import time
import string
import pynmea2
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.exceptions import PubNubException
from decouple import config

pnChannel = "raspi-tracker"

pnconfig = PNConfiguration()
pnconfig.subscribe_key = config('subscribe_key')
pnconfig.publish_key = config('publish_key')
pnconfig.ssl = False

pubnub = PubNub(pnconfig)
pubnub.subscribe().channels(pnChannel).execute()
time.sleep(20)

while True:
    port = "/dev/ttyAMA0"
    ser = serial.Serial(port, baudrate=9600, timeout=0.5)
    dataout = pynmea2.NMEAStreamReader()
    newdata = ser.readline()
    #print("valor: " , newdata.decode('utf-8', 'backslashreplace'))
    newdata = newdata.decode('utf-8', 'backslashreplace')

    if newdata[0:5] == "GPGLL" or newdata[0:6] == "$GPGLL" or newdata[0:6] == "$GPRMC" or newdata[0:5] == "GPRMC":
        newmsg = pynmea2.parse(newdata)
        lat = newmsg.latitude
        lng = newmsg.longitude
        print('---------------------------------------------')
        gps = "LATITUD=" + str(lat) + " LONGITUD=" + str(lng)
        print(gps)
        print('---------------------------------------------')
        try:
            envelope = pubnub.publish().channel(pnChannel).message({
                'lat': lat,
                'lng': lng
            }).sync()
            time.sleep(10)
        except PubNubException as e:
            handle_exception(e)
