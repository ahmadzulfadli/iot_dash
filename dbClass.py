'''
http://127.0.0.1:7008/input_sensor?temperature=30&humidity=79
'''

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for, request, flash

# objek flask
app = Flask(__name__)

# api-key
app.secret_key = "djfljdfljfnkjsfhjfshjkfjfjfhjdhfdjhdfu"

# koneksi ke database
userpass = "mysql+pymysql://root:Kucinghitam123@"
basedir = "127.0.0.1"
dbname = "/iot_db"

app.config["SQLALCHEMY_DATABASE_URI"] = userpass + basedir + dbname
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# tabel komposter


class Komposter(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    temperature = db.Column(db.Float, nullable=False)
    moisture = db.Column(db.Float, nullable=False)
    ph_meter = db.Column(db.Float, nullable=False)
    count_day = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.TIMESTAMP, nullable=False,
                          server_default=db.func.current_timestamp())

    def __init__(self, temperature, moisture, ph_meter, count_day):
        self.temperature = temperature
        self.moisture = moisture
        self.ph_meter = ph_meter
        self.count_day = count_day
