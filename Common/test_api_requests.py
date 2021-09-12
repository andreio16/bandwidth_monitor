from flask_restful.fields import Integer
import requests
from datetime import datetime

BASE = "http://127.0.0.1:5000/"

data = [{"date_created": datetime.now().strftime("%d %b %Y, %H:%M:%S"), "mega_bits_per_second": 0.50},
        {"date_created": datetime.now().strftime("%d %b %Y, %H:%M:%S"), "mega_bits_per_second": 0.55},
        {"date_created": datetime.now().strftime("%d %b %Y, %H:%M:%S"), "mega_bits_per_second": 0.90},
        {"date_created": datetime.now().strftime("%d %b %Y, %H:%M:%S"), "mega_bits_per_second": 0.90}]

for i in range(len(data)):
    response = requests.put(BASE + "resource/" + str(i), data[i])
    print(response.json())

input()
for i in range(len(data)):
    response = requests.get(BASE + "resource/" + str(i))
    print(response.json())

response = requests.get(BASE + "resource/10")
print(response.json())

response = requests.patch(BASE + "resource/1", {"mega_bits_per_second": 4.22})
print(response.json())

response = requests.delete(BASE + "resource/3")
print(response.json())

input()
for i in range(len(data)):
    response = requests.get(BASE + "resource/" + str(i))
    print(response.json())

input()
response = requests.get(BASE + "nr_resources")
print("Tot nr of db recordings : " + (str)(response.json()['nr_resources']))
