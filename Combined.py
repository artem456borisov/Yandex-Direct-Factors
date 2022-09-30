import requests
import json
import time
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
from pathlib import Path

token = "Enter a Token"
link4 = "https://api.direct.yandex.ru/v4/json/"
link4_live = "https://api.direct.yandex.ru/live/v4/json/"

def read_json(filename: str) -> dict:  #used to convert a json file into a python dict
    try:
        with open(filename, "r") as f:
            data = json.loads(f.read())
    except:
        raise Exception(f"Reading {filename} file encountered an error")

    return data

def create_dataframe(data: list) -> pd.DataFrame:
    # Declare an empty dataframe to append records
    dataframe = pd.DataFrame()

    # Looping through each record
    for d in data:
        # Normalize the column levels
        record = json_normalize(d)

        # Append it to the dataframe
        dataframe = dataframe.append(record, ignore_index=True)

    return dataframe


def Get_Words(main_key): #Crete a new Wordstat report and store the result in Wordstat_report.json
    report_id = 0

    filepath_minus = Path('Files/Minus_Keywords')
    lines = filepath_minus.read_text()
    main_key = main_key + lines

    body_create_report = { #ask the server to create a report
        "method": "CreateNewWordstatReport",
        "param": {
            'Phrases': [main_key],
            'GeoID': [213]
        },
        "token": token
    }

    r1 = requests.post(link4, json.dumps(body_create_report, ensure_ascii=False).encode('utf8'))
    r1 = r1.json()
    report_id = r1['data']

    body_get_report = { #ask the server to retrieve the report, based onn id
        "method": "GetWordstatReport",
        "param": report_id,
        "token": token
    }

    time.sleep(10) #server needs time to complete the request

    r1 = requests.post(link4, json.dumps(body_get_report, ensure_ascii=False).encode('utf8'))
    r1 = r1.json()

    with open('Files/Wordstat_report.json', 'w', encoding='utf-8') as f:
        json.dump(r1, f, ensure_ascii=False, indent=4)

def Wordstat_to_csv (file_name):
    data = read_json(filename=file_name)

    dataframe = create_dataframe(data=data['data'])
    # dataframe = create_dataframe(data=dataframe['SearchedAlso']+dataframe['SearchedWith'])
    dataframe = create_dataframe(data=dataframe['SearchedWith'])
    dataframe = dataframe.drop(1)
    dataframe.to_csv('Files/Wordstat_report.csv', index=False)

def Make_forecast (file_name): #parses the csv file for api call and returns a price forecast
    file = open(file_name)
    headers = ['keywords', 'shows']
    dtypes = {'keywords': 'str', 'shows': 'int'}
    parse_dates = ['keywords', 'shows']
    data = pd.read_csv(file, sep=',', header=None, names=headers, dtype=dtypes, parse_dates=parse_dates, skiprows=1)
    data['shows'] = pd.to_numeric(data['shows'])
    data = data.sort_values(by= 'shows') #sort values by shows to get the most meaningful data
    forcast_keys = np.array(data['keywords'], dtype=str)
    forcast_keys = forcast_keys[:100]
    forcast_keys = forcast_keys.tolist()

    body_for_forecast = {
        "method": "CreateNewForecast",
        "param": {
            'Phrases': forcast_keys,  # массив со словами
            'GeoID': [213],
            'Currency': "RUB",
        },
        "token": token
    }

    r1 = requests.post(link4_live, json.dumps(body_for_forecast, ensure_ascii=False).encode('utf8'))
    r1 = r1.json()
    forecast_id = r1['data']

    time.sleep(20)  # server needs time to complete the request

    body_get_forecasts = {
        "method": "GetForecast",
        "param": forecast_id,
        "token": token
    }

    r1 = requests.post(link4_live, json.dumps(body_get_forecasts, ensure_ascii=False).encode('utf8'))
    r1 = r1.json()
    with open('Files/Forecast_report.json', 'w', encoding='utf-8') as f:
        json.dump(r1, f, ensure_ascii=False, indent=4)

def Forecast_json_to_csv(file_name):
    data = read_json(filename=file_name)
    print(data)
    dataframe = create_dataframe(data=data['data']['Phrases'])

    dataframe.to_csv("Files/Forecast_report.csv", index=False)
    return dataframe


#Actual code:
Get_Words('nike air jordan')
Wordstat_to_csv('Files/Wordstat_report.json')
Make_forecast('Files/Wordstat_report.csv')
temp = Forecast_json_to_csv('Files/Forecast_report.json')

