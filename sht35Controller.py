import time
from grove.i2c import Bus
import urllib.request
import datetime
import json

DEVICE_ID = "********"
URL_PUT = "https://********/v2/entities/%s/attrs" % DEVICE_ID

####
def CRC(data):
  crc = 0xff
  for s in data:
    crc ^= s
    for i in range(8):
      if crc & 0x80:
        crc <<= 1
        crc ^= 0x131
      else:
        crc <<= 1
  return crc

####
class GroveTemperatureHumiditySensorSHT3x(object):

    def __init__(self, address=0x45, bus=None):
        self.address = address

        # I2C bus
        self.bus = Bus(bus)

    def read(self):
        # high repeatability, clock stretching disabled
        self.bus.write_i2c_block_data(self.address, 0x24, [0x00])

        # measurement duration < 16 ms
        time.sleep(0.016)

        # read 6 bytes back
        # Temp MSB, Temp LSB, Temp CRC, Humididty MSB, Humidity LSB, Humidity CRC
        data = self.bus.read_i2c_block_data(0x45, 0x00, 6)
        temperature = data[0] * 256 + data[1]
        celsius = -45 + (175 * temperature / 65535.0)
        humidity = 100 * (data[3] * 256 + data[4]) / 65535.0
        if data[2] != CRC(data[:2]):
            raise RuntimeError("temperature CRC mismatch")
        if data[5] != CRC(data[3:5]):
            raise RuntimeError("humidity CRC mismatch")
        return celsius, humidity

def updateEntityData(t, h):
  if t is None or h is None:
    return None
  
  data = {
    "temperature": {
      "value": round(t, 1),
      "type": "Float"
    },
    "humidity": {
      "value": round(h, 1),
      "type": "Float"
    },
    "captureddatetime": {
      "value": datetime.datetime.now().isoformat(timespec='seconds') + '+09:00',
      "type": "DateTime"
    }
  }
  headers = {
      'Content-Type': 'application/json',
  }
  
  req = urllib.request.Request(URL_PUT, json.dumps(data).encode(), headers, method='PUT')
  try:
    with urllib.request.urlopen(req) as res:
      print(res.info())
  except urllib.error.HTTPError as err:
    print(err.code)
  except urllib.error.URLError as err:
    print(err.reason)

####
def main():
    sensor = GroveTemperatureHumiditySensorSHT3x()
    temperature, humidity = sensor.read()
    updateEntityData(temperature, humidity)

'''
    print('Temperature in Celsius is {:.1f} C'.format(temperature))
    print('Relative Humidity is {:.1f} %'.format(humidity))
'''

if __name__ == "__main__":
  main()
