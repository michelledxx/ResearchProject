import xmltodict
import requests
import json


def parse():
    '''This function takes the information from the AA incidents API, turns it
     into a json object and extracts the information place/indicent data'''
    URL = "https://www.theaa.ie/api/IncidentService.svc/GetIncidents"
    response = requests.get(URL)
    xmltxt = response.content

    x = xmltodict.parse(xmltxt)
    data_dict = json.dumps(x)

    road_obj = json.loads(data_dict)
    places = road_obj['Places']['Place']
    extract(places)


def extract(obj):
    '''This function extracts the report data per dublin location'''
    for i in range(0, len(obj)):
        if obj[i]['Area'] == 'Dublin':
            lat = obj[i]['Lat']
            long = obj[i]['Long']
            loc = obj[i]['Location']
            report = obj[i]['Report']
            print(lat, long, report, loc)

parse()