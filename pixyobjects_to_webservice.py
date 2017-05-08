
import requests
import ujson as json
import serial
# Serial Information
serial_port = '/dev/cu.usbmodem1421'
baud_rate = 9600 #In arduino, Serial.begin(baud_rate)

serial_data = serial.Serial(serial_port, baud_rate)

#url to post data
url = "http://54.146.129.119:8080/blocks/"
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

with serial.Serial(serial_port, baud_rate) as ser:
    while True:
        line = serial_data.readline();
        line = line.decode("utf-8") #ser.readline returns a binary, convert to string
        pixy_data = line.strip(' \t\n\r')

        if pixy_data:
            print(pixy_data)
            try:
                # pixy_data = {"block_id": 2,"signature": 2,"x": 131,"y":55,"width": 15,"height": 15}
                 # needed to get data as json object
                requests.post(url, json=pixy_data, headers=headers)
            except requests.exceptions.ConnectionError as msg:
                print("{}".format(msg))
            except ValueError as msg:
                print("{}".format(msg))


