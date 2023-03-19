from flask import Flask, request, make_response
from flask import render_template
from config import debug, bdName
from bd import SQLighter
import requests
import json
from time import time
from random import randint

app = Flask(__name__)


def uniqid(prefix=''):
    return prefix + hex(int(time()) * randint(1000, 100000))[2:10] + hex(
        int(time() * randint(1000000, 2000000)) % 0x100000)[2:7]

@app.route("/index")
@app.route("/index.html")
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/secondpage")
def second():
    data = {'token': ''}
    for key in data:
        data[key] = request.args.get(key, "")
    if debug == 1: print(data)
    url = 'https://dt.miet.ru/ppo_it_final'
    param = {'X-Auth-Token': data['token']}
    resp = requests.get(url=url, headers=param)
    if debug == 1: print(resp.json())
    if resp.json()['message'] != 'No Token':
        cases = []
        for i in range(len(resp.json()['message'])):
            cases.append(uniqid(prefix="case_"))
        bd = SQLighter(bdName)
        for case in cases:
            bd.insert_data_cases(NameCase=case)
        for indx, case in enumerate(resp.json()['message']):
            for point in case:
                bd.insert_data_routers(case=cases[indx],  S=point['distance'], SHcount=point['SH'])
        bd.close()

        return f'у вас есть {len(cases)} заданий: {cases}'
    return 'Не верный токен'

if __name__ == '__main__':
    app.run(debug=True)