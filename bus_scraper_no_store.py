import requests
import json
from pymysql import connect

class BikeStationsSpider:
    def __init__(self):
        self.headers = {
        'Cache-Control': 'no-cache',
        'x-api-key': 'e31a714730e34d21a2dfcbc8de363774',
        }
        self.url = "https://api.nationaltransport.ie/gtfsrtest/?format=json"
    def parse_url(self):
        response = requests.get(self.url, headers=self.headers)
        content = json.loads(response.text)
        print(content["entity"])
    def run(self):
        self.parse_url()
if __name__ == "__main__":
    Bike = BikeStationsSpider()
    Bike.run()

