import cv2
import numpy as np
from datetime import *

# Load Yolo
net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")
classes = []
with open("yolov3_classes.txt", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Set minimum confidence level and non-maximum suppression threshold
conf_threshold = 0.3
nms_threshold = 0.1

# Load video
cap = cv2.VideoCapture(0)

#path = "/home/pi/motionCapture/detect_%s.avi" % dt_string
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output = None
recording = False
last_motion_time = 0

while True:
    ret, frame = cap.read()

    # Detect objects in the current frame
    blob = cv2.dnn.blobFromImage(frame, 1/255, (416, 416), (0,0,0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(net.getUnconnectedOutLayersNames())

    # Extract bounding boxes, confidences, and class IDs
    boxes = []
    confidences = []
    class_ids = []
    h, w = frame.shape[:2]

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > conf_threshold:
                center_x = int(detection[0] * w)
                center_y = int(detection[1] * h)
                width = int(detection[2] * w)
                height = int(detection[3] * h)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                boxes.append([left, top, width, height])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Apply non-maximum suppression to eliminate redundant overlapping boxes
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    # Draw the final detections on the frame
    for i in indices:
        i = indices[0]
        if classes[class_ids[i]] in ['person', 'human']:
            box = boxes[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            cv2.rectangle(frame, (left, top), (left+width, top+height), (0,255,0), 2)
            cv2.putText(frame, classes[class_ids[i]], (left, top-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)   
            # If a person is detected, set the recording flag to True
            # Create VideoWriter object
            recording = True
            detection = True
        else:
            detection = False
                
    if recording:
        # If motion was detected, start recording video
        if output is None:
            # use new path for saving video
            dt_string = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            path = "detect_%s.avi" % dt_string
            output = cv2.VideoWriter(path, fourcc, 10.0, (640, 480))
            print("new recording")
        output.write(frame)

    if detection is True:
        last_motion_time = datetime.now()
    else:
            if last_motion_time != 0:
                elapsed_time = (datetime.now() - last_motion_time).total_seconds()
                 # If motion was not detected for 5 seconds, stop recording video
                if elapsed_time >= 5:
                    output = None
                    recording = False
                    print("stop recording")
                    last_motion_time = 0
          
    # Display the resulting frame
    cv2.imshow("frame", frame)
   
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
