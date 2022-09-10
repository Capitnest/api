import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import auth
import requests
import json
import sys
sys.path.append('./..')
from config import *

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

gumroad_token = gumroad_access_token

def validate_license_gumroad(uid = None, license = None):
  if(uid == None or license == None):
    message = {
      "Success": False,
      "Message": "Invalid Arguments (uid or license"
    }
    return json.dumps(message)

  data = {
    'product_permalink': 'pro',
    'license_key': f'{license}'
  }

  response = requests.post('https://api.gumroad.com/v2/licenses/verify', data=data)
  gumroad_response = response.json()

  if (gumroad_response["success"] == False):
    message = {
      "Success": False,
      "Message": "Invalid License!"
    }
    return json.dumps(message)
 
  try:

    #check if the user already has the pro plan
    ref = db.reference(f'/users/{uid}/plan')
    current_plan = ref.get() #the current plan of the user

    if(current_plan == "pro"):
      message = {
      "Success": False,
      "Message": "The user already has the pro plan!"
      }
      return json.dumps(message)
    
    #update the plan to pro
    ref = db.reference(f'/users/{uid}')
    ref.update({
      'plan': 'pro'
    })

    data = {
      'access_token': f'{gumroad_token}',
      'product_permalink': 'pro',
      'license_key': f'{license}'
    }

    response = requests.put('https://api.gumroad.com/v2/licenses/disable', data=data)
   
    message = {
    "Success": True,
    "Message": "The Pro Plan has been activated!"
    }
    return json.dumps(message)
    
  except:
    message = {
      "Success": False,
      "Message": "Invalid UID!"
    }
    return json.dumps(message)