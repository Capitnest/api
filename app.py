from flask import Flask, jsonify
from flask import request
from flask_limiter import Limiter
from flask_cors import CORS, cross_origin
from flask_limiter.util import get_remote_address
import json
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import auth

from config import *

from functions.gumroad import validate_license_gumroad
from functions.firebase import getPlan

cred = credentials.Certificate("service.json")
firebase_admin.initialize_app(cred, {
  "apiKey": firebase_apiKey,
  "authDomain": firebase_authDomain,
  "databaseURL": firebase_databaseURL,
  "projectId": firebase_projectId,
  "storageBucket": firebase_storageBucket,
  "messagingSenderId": firebase_messagingSenderId,
  "appId": firebase_appId
})

app = Flask(__name__)
CORS(app)
limiter = Limiter(app, key_func=get_remote_address)

@app.route('/')
@cross_origin()
@limiter.limit('2 per minute')
def main():
    return "Capitnest API is live!"

@app.route('/feeds/general', methods = ['GET'])
@cross_origin()
@limiter.limit('50 per minute')
def feeds_general():

    f = open('posts/general.json', 'r')
    data = json.load(f)
    return jsonify(data) 

@app.route('/get-plan', methods = ['GET', 'POST'])
@cross_origin()
@limiter.limit('50 per minute')
def get_plan():
    uid = str(request.args.get('uid'))

    print(getPlan(uid))

    return getPlan(uid)

@app.route('/feeds', methods = ['GET', 'POST'])
@cross_origin()
@limiter.limit('50 per minute')
def feeds():

    category = str(request.args.get('category')) # ?input= a
    date = str(request.args.get('date'))

    if(date == "general"):
        f = open(f'posts/{category}.json', 'r')
    else:
        f = open(f'posts/{category}_{date}.json', 'r')

    data = json.load(f)
    return jsonify(data)


@app.route('/validate-license', methods = ['GET', 'POST'])
@cross_origin()
@limiter.limit('5 per minute')
def validate_license():

    license = str(request.args.get('license')) # ?input= a
    uid = str(request.args.get('uid'))

    return jsonify(validate_license_gumroad(license=license, uid=uid))

if __name__ == "__main__":
    app.run(debug=True)
