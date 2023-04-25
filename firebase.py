from pyrebase import pyrebase

config = {
  "apiKey": "AIzaSyDaE95odjfdU3oVP80ZRUBQQbOwDhXCJ0c",
  "authDomain": "iotproject-d8301.firebaseapp.com",
  "databaseURL": "https://iotproject-d8301-default-rtdb.asia-southeast1.firebasedatabase.app",
  "storageBucket": "iotproject-d8301.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

data = {
    "name" : "zhongliang"
}

db.push(data)