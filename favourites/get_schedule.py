import csv
import mysql
from pymysql import connect
from favourites import dbinfo
import datetime
import json
now = str(datetime.datetime.now().time())
nowh = now[0:2]
nowm = now[3:5]


import csv
from datetime import datetime

def difference(h1, m1, h2, m2):
    if h1 >= h2:
        if h1 == h2:
            if m1 >= m2:
                # convert into minutes
                t1 = int(h1) * 60 + int(m1)
                t2 = int(h2) * 60 + int(m2)
                if (t1 == t2):
                    #return False
                    return True
                else:
                    return True
    if int(h2) + 1 == int(h1):
        return True
    else:
        return False



def get_times(stop_id):
    #get updates for this stop
    data = []
    API_updates = get_API(stop_id)
    print('UPDATES', API_updates)
    #open schedule file
    with open('favourites/stop_times.csv', 'rt') as f2:
        reader2 = csv.reader(f2, delimiter=',')
        next(reader2)
        for row2 in reader2:
            #check if this bus in this row runs this day
            if check_day(row2[0]) == True:
                # check if this is the right stop
                if stop_id == str(row2[3]):
                    try:
                        #get the time from the row
                        #t = datetime.strptime(row2[1], '%H:%M:%S').time()
                        #t = row2[1]
                        h = row2[1][0:2]
                        m = row2[1][3:5]
                        #check if within he next hour
                        if difference(h, m, nowh, nowm) == True:
                            #check if API updated need to be applied
                            for i in range(0, len(API_updates)):
                                if row2[0] == API_updates[i][0]:
                                    print('match')
                                    new_times = calculate_new_time(row2, API_updates[i])
                                    print(new_times[0], 'new time index 1')
                                    print('old row', row2)
                                    row2[1] = new_times[0]
                                    row2[2] = new_times[1]
                                    data.append(row2)
                            data.append(row2)

                    #If the time goes past midnight eg (24:05)
                    except Exception as e:
                        if int(row2[1][0:2]) >= 24:
                            row2[1] = "0" + str(int(row2[1][0:2]) - 24) + row2[1][2:]
                            (datetime.strptime(row2[1], '%H:%M:%S'))
                            t = datetime.strptime(row2[1], '%H:%M:%S').time()
                            t = row2[1]
                            h = row2[1][0:2]
                            m = row2[1][3:5]

                            #repeat same as above with midnight accounted for
                            if difference(h, m, nowh, nowm) == True:
                                data.append(row2)
                                for i in range(0, len(API_updates)):
                                    if row2[0] == API_updates[i][0]:
                                        new_times = calculate_new_time(row2, API_updates[i])
                                        print(new_times)
                                        row2[1] = new_times[0]
                                        row2[2] = new_times[1]
                                        data.append(row2)

            else:
                continue

    return_json(data)


#get_times('8510B5550801')

def return_json(data):
    list = [{"route": x[0], "bus": x[0].split("-")[1], "arr_time": x[1], "dep_time": x[2], "stop": x[3], "seq": x[4]} for x in data]
    print(json.dumps(list))
    return json.dumps(list)

def get_API(stop_id):

    conn = connect(host=dbinfo.myhost, port=3306, user=dbinfo.myuser, password=dbinfo.mypasswd,
                   database=dbinfo.mydatabase,
                   charset="utf8")
    cs = conn.cursor()
    cs.execute("SELECT * from realtime_bus_data where stop_id = %s", stop_id)
    myresult = cs.fetchall()
    print(len(myresult))
    res = []
    for i in range(0, len(myresult)):
        res1 = []
        trip = str(myresult[i][2])
        route_id = myresult[i][5]
        stop_seq = myresult[i][6]
        arrival_delay = myresult[i][7]
        dep_delay = myresult[i][8]
        res1 += trip, route_id, stop_seq, arrival_delay, dep_delay
        res.append(res1)
    return res


def calculate_new_time(schedule, delays):
    """This function alters the scheduled times according to the API updates"""
    from datetime import timedelta as dt
    scheduled_arr = schedule[1]
    scheduled_dep = schedule[2]
    arr_delay = int(delays[3])
    dep_delay = int(delays[4])
    print(scheduled_arr, arr_delay)

    #code adapted from https://stackoverflow.com/questions/10663720/how-to-convert-a-time-string-to-seconds
    time1 = scheduled_arr
    time2 = scheduled_dep
    print(time2, time1)
    #chnage to seconds
    s1 = sum(x * int(t) for x, t in zip([3600, 60, 1], time1.split(":")))
    s2 = sum(x * int(t) for x, t in zip([3600, 60, 1], time2.split(":")))
    new_arr = s1 + int(arr_delay)
    new_dep = s2 + int(arr_delay)
    new_arr = str(dt(seconds=new_arr))
    new_dep = str(dt(seconds=new_dep))

    return new_arr, new_dep


import datetime as dd
def check_day(route):
    """This function checks if the route in the row is allowed today"""
    row_route = route.split(".")[1]
    routes = []
    today = str(dd.datetime.now().today().weekday())
    available = {
        "y1003" : ["0", "1", "2", "3", "4"],
         "y1004" : ["0", "6"],
        "y1005" : ["2", "3", "4"],
        "y1006" : ["5"]
    }
    for key, value in available.items():
        for day in value:
            if today == day:
                routes.append(key)

    if row_route in routes:
        return True
    else:
        return False


get_times('8250DB002008')

#check_day('5315.y1005.60-1-d12-1.1.O')