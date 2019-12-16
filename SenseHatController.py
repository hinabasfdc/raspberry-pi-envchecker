import json
import urllib.request
from sense_hat import SenseHat
import datetime

####
DEVICE_ID = "sensehat001"
URL_PUT = "https://********/v2/entities/%s/attrs" % DEVICE_ID
sense = SenseHat()
sense.clear()

####
def updateEntityData():
  data = {
    "temperature": {
      "value": round(sense.get_temperature(), 1),
      "type": "Float"
    },
    "humidity": {
      "value": round(sense.get_humidity(), 1),
      "type": "Float"
    },
    "pressure": {
      "value": round(sense.get_pressure(), 1),
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
  #print(data)

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
  updateEntityData()

if __name__ == "__main__":
    main()
