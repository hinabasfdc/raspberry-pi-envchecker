import urllib.request
import json

DEVICE_ID = "m5stick001"
URL_GET = "http://********"
URL_PUT = "https://********/v2/entities/%s/attrs" % DEVICE_ID

####
def getM5StickSensorData():
  req = urllib.request.Request(URL_GET)
  try:
    with urllib.request.urlopen(req) as res:
      return res.read().decode("utf-8")

  except urllib.error.HTTPError as err:
    print(err.code)
    return None

  except urllib.error.URLError as err:
    print(err.reason)
    return None

####
def updateEntityData(s):
  if s is None:
    return None
  
  j = json.loads(s)
  data = {
    "temperature": {
      "value": j["temperature"]["value"],
      "type": "Float"
    },
    "humidity": {
      "value": j["humidity"]["value"],
      "type": "Float"
    },
    "pressure": {
      "value": j["pressure"]["value"],
      "type": "Float"
    },
    "captureddatetime": {
      "value": j["captureddatetime"]["value"] + '+09:00',
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

###
def main():
  updateEntityData(getM5StickSensorData())

if __name__ == "__main__":
    main()
