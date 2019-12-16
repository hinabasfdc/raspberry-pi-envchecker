import bluepy
import struct
import datetime
import urllib.request
import json

####
DEVICE_ID = "omronenv001"
URL_PUT = "https://********/v2/entities/%s/attrs" % DEVICE_ID
DEVADDR = "********" # Omron 環境センサーの アドレス
HANDLE = 0x0019 # Latest data のハンドル

####
def main():

    try:
        peri = bluepy.btle.Peripheral()
        peri.connect(DEVADDR, bluepy.btle.ADDR_TYPE_RANDOM)
        data = peri.readCharacteristic(HANDLE)
        (seq, temperature, humidity, light, uv, pressure, noise, discom, heat, batt) = struct.unpack('<BhhhhhhhhH', data)
        peri.disconnect()

        data = {
            "temperature": {
            "value": round(temperature / 100, 1),
            "type": "Float"
            },
            "humidity": {
            "value": round(humidity / 100, 1),
            "type": "Float"
            },
            "pressure": {
            "value": round(pressure / 10, 1),
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

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
