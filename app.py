from flask import Flask, jsonify
from flask import request
from flask_limiter import Limiter
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
limiter = Limiter(app, key_func=get_remote_address)

@app.route('/')
@limiter.limit('2 per minute')
def main():
    return "Capitnest API is live!"

# @app.route('/test', methods = ['GET', 'POST'])
# def handle_request():
#     text = str(request.args.get('input')) # ?input= a
#     character_count = len(text)

#     data_set = {'input': text, 'timestamp': time.time(), 'character_count': character_count}
#     json_dump = json.dumps(data_set)
#     return json_dump

@app.route('/feeds/general', methods = ['GET'])
@limiter.limit('50 per minute')
def feeds_general():

    f = open('posts/general.json', 'r')
    data = json.load(f)
    return jsonify(data) 

@app.route('/feeds/bitcoin', methods = ['GET'])
@limiter.limit('50 per minute')
def feeds_bitcoin():

    f = open('posts/bitcoin.json', 'r')
    data = json.load(f)
    return jsonify(data)

@app.route('/feeds/solana', methods = ['GET'])
@limiter.limit('50 per minute')
def feeds_solana():

    f = open('posts/solana.json', 'r')
    data = json.load(f)
    return jsonify(data)

@app.route('/feeds/cardano', methods = ['GET'])
@limiter.limit('50 per minute')
def feeds_cardano():

    f = open('posts/cardano.json', 'r')
    data = json.load(f)
    return jsonify(data)

@app.route('/feeds/ethereum', methods = ['GET'])
@limiter.limit('50 per minute')
def feeds_ethereum():

    f = open('posts/ethereum.json', 'r')
    data = json.load(f)
    return jsonify(data)

@app.route('/get-plan', methods = ['GET', 'POST'])
@limiter.limit('5 per minute')
def get_plan():
    uid = str(request.args.get('uid'))

    return getPlan(uid)

@app.route('/validate-license', methods = ['GET', 'POST'])
@limiter.limit('5 per minute')
def validate_license():

    license = str(request.args.get('license')) # ?input= a
    uid = str(request.args.get('uid'))

    return jsonify(validate_license_gumroad(license=license, uid=uid))

if __name__ == "__main__":
    app.run(debug=True)