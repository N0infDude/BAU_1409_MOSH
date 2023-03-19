from flask import Flask, request, make_response
from flask import render_template
from config import debug, bdName
from bd import SQLighter
import requests
import json

app = Flask(__name__)


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
    param = {'X-Auth-Token': 'v9khcqgk'}
    resp = requests.get(url=url, headers=param)
    if debug == 1: print(resp.json())

    return "second page"

if __name__ == '__main__':
    app.run(debug=True)