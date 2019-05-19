#!/usr/bin/python2.7
#-*- coding: UTF-8 -*-
from urllib2 import Request, urlopen
from urllib import urlencode, quote_plus, unquote
import json
from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3
#import pandas as pd
#import numpy
#from langdetect import detect
home_dir ='/var/www/chatbot/'
app = Flask(__name__)
@app.route('/keyboard')
def Keyboard():
    dataSend = {
        "type" : "buttons",
        "buttons": ["    ^       ^ ", " ^   ^ ^  ^ ^      ^  ","  ^  ^ ^ "," ^ ^  ^ ^  ^ ^    "]
    }
    return jsonify(dataSend)
@app.route('/message')
def Message():
    dataReceive = request.get_json()
    content = dataReceive['content']
    user = dataReceive["user_key"]
    # ^    ^   ^   ^   ^     ^   ^  ^          ^
    if content == "    ^       ^ ":
        dataSend = {
            "message": {
                "text": " ^ ^   ^      ^ ^     ^       ^   ^ ^ ",
            }
        }
    elif content in area:
        returnstring= finedust(content)
        dataSend={
            "message": {
                "text": returnstring,
            }
        }


    return jsonify(dataSend)



def finedust (area):
    url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty'
    service_key = 'NiFhLcxn8s%2FB0XamZtDGo67i%2Bx84RAy5PRD0JjclZgxkWf7d3OZBRA3WESfu6hrel1Tx01yzI4%2F%2BAxubOLjgjQ%3D%3D'
    stationName = area

    decode_key = unquote(service_key)
    queryParams = '?' + urlencode({ quote_plus('ServiceKey') : decode_key, quote_plus('stationName'): stationName, quote_plus('dataTerm'): 'daily', quote_plus('_returnType'): 'json', quote_plus('ver'): '1.3', quote_plus('pageNo'): 1})

    request = Request(url + queryParams)
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read()

    response_body = json.loads(response_body)

    returnstring= "dataTime: {} \n pm10: {} \n pm2.5 :{}".format(response_body['list'][0]['dataTime'], response_body['list'][0]['pm10Value'], response_body['list'][0]['pm25Value'])
    return returnstring

if __name__ == "__main__":
    app.run( host = '0.0.0.0', port =5000)