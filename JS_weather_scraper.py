import time
import datetime
import requests
import traceback
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, String, DateTime

weather_key = "836e60d545402f71b66015366f7b8997"
weather_URI = "https://api.openweathermap.org/data/2.5/weather"

host = "dublinbus.csy6fo0e4c6z.us-east-1.rds.amazonaws.com"
db = "dublinbus"
username = "admin"
password = "dublinbus99"

engine = create_engine(f"mysql+mysqlconnector://{username}:{password}@{host}:3306/{db}", echo=True)

def write_to_file(string, obj):
    '''Write data to file'''
    title = string
    current_time = datetime.datetime.now()
    timestamp = datetime.datetime.timestamp(current_time)
    with open("{}{}".format(title, timestamp), "w") as f:
        f.write(obj)

def get_stops():
    pass

def get_weather(lon, lat, stop_num):
    '''Request weather data for specific geographic coordinates'''
    def get_each_weather(obj, station_num):
        '''Pull weather data from JSON object'''
        return {"date_created": datetime.datetime.now().replace(microsecond=0),
                "stop_number": stop_num,
                "pos_lng": obj["coord"]["lon"],
                "pos_lat": obj["coord"]["lat"],
                "weather_id": obj["weather"][0]["id"],
                "main": obj["weather"][0]["main"],
                "description": obj["weather"][0]["description"],
                "icon": obj["weather"][0]["icon"],
                "base": obj["base"],
                "temp": obj["main"]["temp"],
                "feels_like": obj["main"]["feels_like"],
                "temp_min": obj["main"]["temp_min"],
                "temp_max": obj["main"]["temp_max"],
                "pressure": obj["main"]["pressure"],
                "humidity": obj["main"]["humidity"],
                "visibility": obj["visibility"],
                "wind_speed": obj["wind"]["speed"],
                "wind_deg": obj["wind"]["deg"],
                "clouds_all": obj["clouds"]["all"],
                "last_update": datetime.datetime.fromtimestamp(int(obj["dt"] / 1e3)),
                "sys_type": obj["sys"]["type"],
                "sys_id": obj["sys"]["id"],
                "sunrise": datetime.datetime.fromtimestamp(int(obj["sys"]["sunrise"] / 1e3)),
                "sunset": datetime.datetime.fromtimestamp(int(obj["sys"]["sunset"] / 1e3)),
                "timezone": obj["timezone"],
                "id": obj["id"],
                "cod": obj["cod"],
                }

    weather_request = requests.get(weather_URI, params={"APPID": weather_key, "lon": lon, "lat": lat})
    write_to_file("weather", weather_request.text)
    # Pull weather data from JSON object returned for each set of coordinates
    weather_data = get_each_weather(weather_request.json(), station_num)
    return weather_data

def create_and_fill_stops():
    pass

def create_and_fill_weather(obj):
    '''Create weather table if doesn't exist, add weather data to table using get_weather function'''
    meta = MetaData()

    weather = Table(
        "weather", meta,
        Column("date_created", DateTime),
        Column("stop_number", Integer),
        Column("pos_lng", Float),
        Column("pos_lat", Float),
        Column("weather_id", String(128)),
        Column("main", String(128)),
        Column("description", String(128)),
        Column("icon", String(128)),
        Column("base", String(128)),
        Column("temp", Float),
        Column("feels_like", Float),
        Column("temp_min", Float),
        Column("temp_max", Float),
        Column("pressure", Float),
        Column("humidity", Float),
        Column("visibility", Float),
        Column("wind_speed", Float),
        Column("wind_deg", Float),
        Column("clouds_all", Float),
        Column("last_update", DateTime),
        Column("sys_type", Integer),
        Column("sys_id", Integer),
        Column("sunrise", DateTime),
        Column("sunset", DateTime),
        Column("timezone", Integer),
        Column("name", String(128)),
        Column("id", Integer),
        Column("cod", Integer),
    )
    # Create tables
    meta.create_all(engine)
    # Insert data into availability table
    stop_values = obj
    for i in stop_values:
        stop_num = i["number"]
        longitude = i["pos_lng"]
        latitude = i["pos_lat"]
        weather_values = get_weather(*(str(longitude), str(latitude), stop_num))
        # Insert data into weather table
        ins_weather = weather.insert().values(weather_values)
        engine.execute(ins_weather)

def main():
    '''Call functions to create and write to tables every 5 minutes'''
    while True:
        try:
            stop_values = create_and_fill_stops()
            create_and_fill_weather(stop_values)
            time.sleep(60 * 60)
        except:
            print(traceback.format_exc())

if __name__ == "__main__":
    main()