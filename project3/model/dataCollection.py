# https://api.steampowered.com/ISteamApps/GetAppList/v2
from ast import comprehension
from calendar import c
import pandas as pd
from pandas import json_normalize
import requests
import os
import time
import json
import sqlite3

from bs4 import BeautifulSoup

# try catch로 추가되는 데이터만 넣기 가능?

# 1. Collect Game to code info & Insert into database 
# Variable Info
DB_FILENAME = 'project3.db'
DB_FILEPATH = os.path.join(os.getcwd(), DB_FILENAME)
Total_count = 0 # Number of Data
Validate_count = 0

# Create Session 
conn = sqlite3.connect(DB_FILENAME)
cur = conn.cursor()

# Data collection 1 : basic data
# def basic_data():
url_gamecode = 'https://api.steampowered.com/ISteamApps/GetAppList/v2'
resp_gamecode = requests.get(url_gamecode)
json_gamecode = json.loads(resp_gamecode.content)

# cur.execute("""CREATE TABLE if not exists game_code_info(
#                     code VARCHAR(10) NOT NULL PRIMARY KEY,
#                     name VARCHAR(100) NOT NULL);""")
for info in json_gamecode['applist']['apps']:
    Total_count = Total_count + 1
    if ('test' not in info['name'].lower()) and (info['name'] != ''):
        Validate_count = Validate_count + 1
        cur.execute('REPLACE INTO game_code_info (code, name) VALUES (?,?);',
                    (str(info['appid']), info['name']))
conn.commit()
print('Total Number of Data : ',Total_count)
print('The Number of Validate Data : ',Validate_count)
    # pass

# Data collection 2 : code - real data
# def data_matching():
cur.execute("SELECT code FROM game_code_info gci ORDER BY code desc;")
count = 0
json_list = []
for i, code in enumerate(cur.fetchall()):
    url = f'https://steamspy.com/api.php?request=appdetails&appid={code[0]}'
    resp = requests.get(url)
    json_data = json.loads(resp.content)
    data_value = list(json_data.values())
    print(i,data_value[0])
    try:
        if (data_value[13] != 0):
            data_value[13] = float(data_value[13])/100
        else:
            data_value[13] = 0.0
        
        if (data_value[14] != 0):
            data_value[14] = float(data_value[14])/100
        else:
            data_value[14] = 0.0        

        if data_value[19]:
            data_value[19] = str(list(data_value[19].keys()))
        else:
            data_value[19] = ''
        
        if (type(data_value[13]) == int) or (type(data_value[13]) == float):
            cur.execute('REPLACE INTO game_info VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', data_value)
            count = count + 1
        if count%10 == 0:
            print("INSERTING # :", count,"/",Validate_count) 
            conn.commit()

    except:
        continue


# 게임 정보 url
# https://store.steampowered.com/api/appdetails?appids=1476090&l=korean
# https://steamspy.com/api.php?request=appdetails&appid=1426210
# https://partner.steamgames.com/doc/store/getreviews

cur.close()
conn.close()