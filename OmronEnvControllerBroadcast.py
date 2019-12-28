import bluepy
import struct
import urllib.request
import datetime
import json

DEVICE_ID = "********"
URL_PUT = "https://********/v2/entities/%s/attrs" % DEVICE_ID

####
def updateEntityData(t, h, p):
  if t is None or h is None or p is None:
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
    "pressure": {
      "value": round(p, 1),
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
  scanner = bluepy.btle.Scanner(0)

  for i in range(11):
    #print('scan %i' % i)
    devices = scanner.scan(10)
    for device in devices:
      for (adtype, desc, value) in device.getScanData():
        if desc == 'Manufacturer' and value[0:4] == 'd502':
          (temp, humid, light, uv, press, noise, accelX, accelY, accelZ, batt) = struct.unpack('<hhhhhhhhhB', bytes.fromhex(value[6:]))
          #print(' (%3s) %s : %s ' % (adtype, desc, value))
          #print('%s %s %s %s %s %s %s %s %s %s' % (temp/100, humid/100, light, uv, press/10, noise/100, accelX, accelY, accelZ, (batt+100)/100))
          
          #print('temprature: %s' % round(temp/100, 1))
          #print('humidity: %s' % round(humid/100, 1))
          #print('pressure: %s' % round(press/10, 1))
          
          updateEntityData(temp/100, humid/100, press/10)
          break
      else:
        continue
      break
    else:
      continue
    break

if __name__ == "__main__":
  main()
