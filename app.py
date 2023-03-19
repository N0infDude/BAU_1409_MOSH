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
    return "first page"

@app.route("/secondpage")
def index():
    data = {'key': ''}
    for key in data:
        data[key] = request.args.get(key)
    url = 'https://dt.miet.ru/ppo_it_final'
    param = {'X-Auth-Token': 'v9khcqgk'}
    resp = requests.get(url=url, headers=param)


    return "second page"
