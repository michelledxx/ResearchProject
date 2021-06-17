import pandas as pd
import openpyxl

def create_Station_Per_Route_CSV():
    """This function creates a CSV file of stations per route from the
     file 'Routes serving at Bus Stops in Ireland' found on
     https://www.transportforireland.ie/transitData/PT_Data.html
    """
    read_file = pd.read_excel(r'route_sequences_report_20210511_ALL.xlsx')
    read_file.to_csv(r'StationToBus.csv', index = None, header=True)

    f=pd.read_csv("StationToBus.csv")
    keep_col = ['ShapeId','StopSequence','RouteName','RouteDescription', 'Direction',
            'Latitude', 'Longitude', 'ShortCommonName_en', 'HasPole', 'HasShelter', 'RouteData']
    new_f = f[keep_col]
    new_f.to_csv("StopAndStationToDB.csv", index=False)


create_Station_Per_Route_CSV()