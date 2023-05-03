from time import *
from grovepi import *
import cv2
from pyrebase import pyrebase
import base64


ultrasonic = 3
buzzer = 2

config = {
  "apiKey": "AIzaSyBMBkDe6bnJ03kAmO6KsCgLV2RQo0yKVFs",
  "authDomain": "iot-asss.firebaseapp.com",
  "databaseURL": "https://iot-asss-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "storageBucket": "iot-asss.appspot.com"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password("cwh020812@gmail.com", "123456")
db = firebase.database()
storage = firebase.storage()

pinMode(ultrasonic, "INPUT")
pinMode(buzzer, "OUTPUT")
cap = cv2.VideoCapture(0)
def control_buzzer(value):
  
        if value:
            digitalWrite(buzzer, 1)
        else:
            digitalWrite(buzzer, 0)

while True:
    motion=db.child("Motion").get().val()
    ret, frame = cap.read()
        
    retval, buffer = cv2.imencode('.jpg', frame)
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')

    # Create a dictionary with a single key-value pair containing the byte string
    live_stream = {"live_stream": jpg_as_text}

    # Store the `live_stream` dictionary in the database
    db.child("Live_Stream").set(live_stream)

    
    try:
        sleep(0.2)
        distance = ultrasonicRead(ultrasonic)
        print(distance, "cm")
               
        if distance <= 50:
            filename = "images/{}.jpg".format(int(time.time()))                                       
            cv2.imwrite(filename,frame)                              
            control_buzzer(motion["Alarm"])
            Motion={
                "Detect" : 1,
                "Alarm" : 1
                }
            results = db.child("Motion").set(Motion)
        else:
            control_buzzer(motion["Alarm"])
            Motion={
                "Detect" : 0,
                "Alarm" : 0
                }
            results = db.child("Motion").set(Motion)
           
    except KeyboardInterrupt :
        control_buzzer(motion["Alarm"])
        break
    except TypeError:
        print("Type Error occurs")
    except IOError:
        print("IO Error occurs")
    
# release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
