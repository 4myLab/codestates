from flask import Blueprint, render_template, request
import numpy as np
import sqlite3
import os
import pickle

with open('model/model.pkl','rb') as pickle_file:
    model =  pickle.load(pickle_file)

DB_FILENAME = 'project3.db'
# DB_FILEPATH = os.path.join(os.getcwd(), DB_FILENAME)

main_bp = Blueprint('main_page',__name__)

@main_bp.route('/', methods=['GET'])
def mainController():
    try:
        page = 'main'
        rMessage = render_template('%s.html' %page, data=y_pred)
        rCode = 200
    except:
        rMessage = '페이지를 찾을 수 없습니다.'
        rCode = 400
    finally:
        return rMessage, rCode

@main_bp.route('/result/<name_info>', methods=['GET','POST'])
def resultController(name_info):
    try:
        page = 'result'
        conn = sqlite3.connect(DB_FILENAME)
        cur = conn.cursor()

        result = []
        print(name_info)
        cur.execute('SELECT appid, name, positive, negative, price FROM game_info WHERE name= ? ;',[name_info])
        datum = cur.fetchone()
        print(datum)
        reviews = datum[2] + datum[3]
        odds = float((datum[2]+1)/(datum[3]+1))
        arr = np.array([[reviews, odds, datum[2]]])
        y_pred = model.predict(arr)
        result = [datum[1], datum[2], datum[3], reviews, odds, int(y_pred[0]), '$ '+str(round(y_pred[0]*datum[4]))]
        
        # for data in datum:
        #     reviews = data[2] + data[3]
        #     odds = float((data[2]+1)/(data[3]+1))
        #     arr = np.array([[reviews, odds, data[2]]])
        #     y_pred = model.predict(arr)
            # total = (data[0],data[1],y_pred)
            # result.append(total)
        cur.close()
        conn.close()
    except:
        data = '데이터가 없습니다.'
    finally:
        return render_template('%s.html'%page, data=result)