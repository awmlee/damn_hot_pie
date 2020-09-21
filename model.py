from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
import sqlite3
import json
import os

print("db setup code executed")
app = Flask(__name__)
script_path = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+script_path+'/dht_database.db'
db = SQLAlchemy(app)
print(app.config['SQLALCHEMY_DATABASE_URI'])
print("db setup code executed done")

class DHTRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    humidity = db.Column(db.Integer())
    temperature = db.Column(db.Integer())
    PM1_0 = db.Column(db.Integer())
    PM2_5 = db.Column(db.Integer())
    PM10 = db.Column(db.Integer())
    date = db.Column(db.DateTime())

    def __init__(self, humidity, temperature,PM1_0,PM2_5,PM10, date):
        self.humidity = humidity
        self.temperature = temperature
        self.PM1_0 = PM1_0
        self.PM2_5=PM2_5
        self.PM10=PM10
        self.date = date

    def __repr__(self):
        return 'H:{0},T:{1},PM1:{2},PM2_5:{3},PM10:{4},DateTime:{5}\n'.format(self.humidity, self.temperature,self.PM1_0,self.PM2_5,self.PM10, self.date)

    def to_dict(self):
        d = {}
        d["id"] = self.id
        d["humidity"] = self.humidity
        d["temperature"] = self.temperature
        d["PM1_0"]=self.PM1_0
        d["PM2_5"]=self.PM2_5
        d["PM10"]=self.PM10
        d["date"] = str(self.date)
        return d

    def to_json(self):
        d = self.to_dict()
        return json.dumps(d)

try:
    DHTRecord.query.first()
except sqlalchemy.exc.OperationalError as e:
    #print app.config['SQLALCHEMY_DATABASE_URI']
    db.create_all()
