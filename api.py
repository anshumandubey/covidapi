import flask
import os
from flask import request
from flask_cors import CORS
import pandas as pd
import json
import requests
import numpy as np
import time,threading
from threading import Timer

app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

class setInterval :
    def __init__(self,interval,action) :
        self.interval=interval
        self.action=action
        self.stopEvent=threading.Event()
        thread=threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self) :
        nextTime=time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()) :
            nextTime+=self.interval
            self.action()

    def cancel(self) :
        self.stopEvent.set()

def flatten_json(y):
    out = {}
    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x
    flatten(y)
    return out

df = pd.DataFrame(columns=['country', 'date', 'confirmed', 'deaths', 'recovered'])
df_totalCases = pd.DataFrame(columns=['country', 'date', 'confirmed', 'deaths', 'recovered'])

def data():
    global df,df_totalCases
    print("Updating data...")
    resp = requests.get(f"https://pomber.github.io/covid19/timeseries.json")
    data = json.loads(resp.text)
    df = df.iloc[0:0]
    df_totalCases = df = df.iloc[0:0]
    for key,value in data.items():
        dic_flattened = (flatten_json(d) for d in value)
        temp_df = pd.DataFrame(dic_flattened)
        temp_df.insert(0, 'country', key)
        df = df.append([temp_df],ignore_index=True)
        df_totalCases = df_totalCases.append([temp_df.tail(1)],ignore_index=True)

    df['country'] = df['country'].str.lower()
    df_totalCases['country'] = df_totalCases['country'].str.lower()

data()
inter = setInterval(14400, data)

@app.route('/')
def home():
    return "<h2>Covid Data API</h2><br>"+ \
        "<h4>Get all data: <a href='http://ec2-54-174-192-47.compute-1.amazonaws.com/api/all'>http://ec2-54-174-192-47.compute-1.amazonaws.com/api/all</a></h4><br>"+ \
            "<h4>Get all data for specfic country i.e. India: <a href='http://ec2-54-174-192-47.compute-1.amazonaws.com/api/all?country=india'>http://ec2-54-174-192-47.compute-1.amazonaws.com/api/all?country=india</a></h4><br>"+ \
                "<h4>Get all data for specfic date i.e. 22/3/2020: <a href='http://ec2-54-174-192-47.compute-1.amazonaws.com/api/all?date=22-3'>http://ec2-54-174-192-47.compute-1.amazonaws.com/api/all?date=<i>22-3</i></a></h4><br>"+ \
                    "<h4>Get last day data for all countries: <a href='http://ec2-54-174-192-47.compute-1.amazonaws.com/api/lastday'>http://ec2-54-174-192-47.compute-1.amazonaws.com/api/lastday</a></h4><br>"+ \
                        "<h4>Get last day data for specfic country i.e. India: <a href='http://ec2-54-174-192-47.compute-1.amazonaws.com/api/lastday?country=india'>http://ec2-54-174-192-47.compute-1.amazonaws.com/api/lastday?country=india</a></h4><br>"+ \
                            "<h4>Get total cases till today: <a href='http://ec2-54-174-192-47.compute-1.amazonaws.com/api/total'>http://ec2-54-174-192-47.compute-1.amazonaws.com/api/total</a></h4><br>"

@app.route('/api/all', methods=['GET'])
def api_all():
    # Check if a country was provided in the url
    if 'country' in request.args:
        country = str(request.args['country'])
        df_country = df.where(df['country']==country.lower())
        df_country.dropna(axis = 0, how ='all',inplace=True)
        return df_country.to_json(orient='records')
    elif 'date' in request.args:                # Date in ?date=dd-mm
        date = str(request.args['date'])
        df_date = df.where(df['date']=='2020-{}-{}'.format(date.split("-")[1],date.split("-")[0]))
        df_date.dropna(axis = 0, how ='all',inplace=True)
        return df_date.to_json(orient='records')
    else:
        return df.to_json(orient='records')


@app.route('/api/lastday', methods=['GET'])
def api_lastday():
    if 'country' in request.args:
        country = str(request.args['country'])
        df_totalCountry = df_totalCases.where(df_totalCases['country']==country.lower())
        df_totalCountry.dropna(axis = 0, how ='all',inplace=True)
        return df_totalCountry.to_json(orient='records')
    else:
        return df_totalCases.to_json(orient='records')

@app.route('/api/total', methods=['GET'])
def api_total():
    df_total = df_totalCases[['confirmed','recovered','deaths']].sum()
    return df_total.to_json(orient='index')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
