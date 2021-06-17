import json
import requests
import mysql.connector
from datetime import datetime
import time
import dbinfo


def initiate_db():
    '''This function creates the tables that will store current/future weather data'''
    try:
        print('testing db')
        mydb = mysql.connector.connect(
            host=dbinfo.myhost,
            user=dbinfo.myuser,
            passwd=dbinfo.mypasswd,
            database=dbinfo.mydatabase,
            charset=dbinfo.mycharset
        )

        # Check if both tables exist. If they don't, create them.
        mycursor = mydb.cursor(dictionary=False)
        mycursor.execute(" SELECT count(*) FROM information_schema.tables WHERE table_name = 'weather_hist'")
        if (mycursor.fetchone()[0] == 0):
            mycursor.execute("CREATE TABLE weather_hist (timestamp VARCHAR(30), "
                             "time VARCHAR(30), longitude DOUBLE, "
                             "latitude DOUBLE, temp_val DOUBLE, uvi DOUBLE, feels_like DOUBLE, "
                             "pressure DOUBLE, humidity DOUBLE, wind_speed DOUBLE, "
                             "cloudy DOUBLE, visibility DOUBLE, "
                             "main_weather VARCHAR(30), "
                             "descript VARCHAR(30), time_added INT ) ")

        mycursor.execute(" SELECT count(*) FROM information_schema.tables WHERE table_name = 'weather_forecast'")
        if (mycursor.fetchone()[0] == 0):
            mycursor.execute("CREATE TABLE weather_forecast (time VARCHAR(30), "
                             "longitude DOUBLE, "
                             "latitude DOUBLE, temp_val DOUBLE,  feels_like DOUBLE, "
                             "pressure DOUBLE, humidity DOUBLE, wind_speed DOUBLE,  "
                             "cloudy DOUBLE, "
                             "main_weather VARCHAR(30), "
                             "time_added INT ) ")

        mydb.commit()

    except Exception as e:
        print(e)
        print('Failed to create tables')


def collect_weather(lati, longi):
    '''This function gathers current weather data'''

    URL = "https://api.openweathermap.org/data/2.5/onecall?lat=" + str(lati) + "&lon=" + str(
        longi) + "&exclude=minutely&appid=c0df90e98d85453f86f46197e2a4c551"

    response = requests.get(URL)
    weather_obj = json.loads(response.text)
    weather_info = ()
    try:
        long = weather_obj['lon']
        lat = weather_obj['lat']
        today = weather_obj['current']
        date1 = today['dt']
        timestamp = str(datetime.fromtimestamp(date1))
        temp = today['temp']
        feels_like = today['feels_like']
        pressure = today['pressure']
        humidity = today['humidity']
        uvi = today['uvi']
        wind_speed = today['wind_speed']
        clouds = today['clouds']
        visibility = today['visibility']
        weather_detail = today['weather']
        for i in weather_detail:
            for value in i:
                if value == 'main':
                    main = i[value]
                elif value == 'description':
                    desc = i[value]

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        time_added = time.time()

        weather_info = weather_info + (
            (timestamp, current_time, long, lat, temp, uvi, feels_like, pressure, humidity, wind_speed,
             clouds, visibility, main, desc, time_added),)

        initiate_db()
        # call for weather forecast collection
        collect_weather_forecast(lati, longi)

        # send current weather info to database function
        send_weather(weather_info, "current")

    except Exception as e:
        print(e)
        print('error')


def collect_weather_forecast(lati, longi):
    '''function that takes long at lat as parameters and gathers future weather data'''

    URL = "https://api.openweathermap.org/data/2.5/forecast?lat=" + str(lati) + "&lon=" + str(
        longi) + "&cnt=96&appid=c0df90e98d85453f86f46197e2a4c551"

    response = requests.get(URL)
    obj = json.loads(response.text)

    try:
        for j in range(0, 38):
            per_day = obj['list'][j]
            ft_date = per_day['dt']
            main = per_day['main']
            dt = per_day['dt_txt']
            weather = per_day['weather']
            clouds = per_day['clouds']
            winds = per_day['wind']
            timestamp = datetime.fromtimestamp(ft_date)
            timestamp = timestamp.strftime('%d-%m-%Y %H:%M:%S')

            # varibales
            ft_temp = main['temp']
            ft_feels_like = main['feels_like']
            ft_pressure = main['pressure']
            ft_humidity = main['humidity']
            ft_clouds = clouds['all']
            ft_main = weather[0]['main']
            ft_wind_speed = winds['speed']
            data = (
            (dt, longi, lati, ft_temp, ft_feels_like, ft_pressure, ft_humidity, ft_clouds, ft_wind_speed, ft_main),)

            # send to database function with command
            send_weather(data, 'future')
    except Exception as e:
        print(e)
        print('error')


def send_weather(data, command):
    '''This function takes weather data and a command of which table to send the data to'''

    try:
        mydb = mysql.connector.connect(
            host=dbinfo.myhost,
            user=dbinfo.myuser,
            passwd=dbinfo.mypasswd,
            database=dbinfo.mydatabase,
            charset=dbinfo.mycharset
        )
        mycursor = mydb.cursor(dictionary=False)
        if command == "current":
            sql = "INSERT INTO weather_hist VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        else:
            sql = "INSERT INTO weather_forecast (time, longitude, latitude, temp_val, feels_like, " \
                  "pressure, humidity, wind_speed, cloudy, main_weather) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        mycursor.executemany(sql, data)
        print('done')
        mydb.commit()

    except Exception as e:
        print(e)
        print("ERROR: Sending data to database failed!")
        return


## function to go down here to gather station co-ords to send back to weather function
collect_weather(53, 6)
