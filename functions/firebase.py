import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import auth
import requests
import json
import sys

def getPlan(uid=None):

    ref = db.reference(f'/users/{uid}/plan')

    print(uid)
    print(ref.get())

    if(uid == None):
        return("Permission denied.")

    try:
        current_plan = ref.get() #the current plan of the user

        if(current_plan == None):
            return("free")
        else:
            return(current_plan)

    except:
        return("Error.")