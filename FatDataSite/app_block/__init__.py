from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("D:\FatData-analysis\FatData-analysis\FatDataSite\clever-analitics-text-22ccd-firebase-adminsdk-fi5io-02b5fa2422.json")
firebase_admin.initialize_app(cred)

firebaseConfig = {
  "apiKey": "AIzaSyCBlG_g1TaNtFxCMDNMAsXC1ijPyDBjgpQ",
  "authDomain": "clever-analitics-text-22ccd.firebaseapp.com",
  "databaseURL": "https://clever-analitics-text-22ccd-default-rtdb.firebaseio.com",
  "projectId": "clever-analitics-text-22ccd",
  "storageBucket": "clever-analitics-text-22ccd.appspot.com",
  "messagingSenderId": "384783073635",
  "appId": "1:384783073635:web:f512219aefc67aa90c5356"
};

firebase = pyrebase.initialize_app(firebaseConfig)

db = firestore.client()
auth = firebase.auth()

app = Flask(__name__)