import dlib
import cv2
import numpy as np
import imutils
import requests
import pyttsx3
import threading
import urllib
import time

engine = pyttsx3.init()

# webcam = cv2.VideoCapture('http://192.168.225.139/mjpeg/1')
stream = urllib.request.urlopen('http://192.168.225.139/mjpeg/1')
bytes = bytes()

forward_detector = dlib.simple_object_detector('model/forward.svm')
left_detector = dlib.simple_object_detector('model/left.svm')
right_detector = dlib.simple_object_detector('model/right.svm')
stop_detector = dlib.simple_object_detector('model/stop.svm')
uturn_detector = dlib.simple_object_detector('model/uturn.svm')

count = 0
label = ""

last_label = ""


def doReq(param):
    requests.request(url=f"http://192.168.225.184/{param}", method="GET")


# def sendCommand(param):
#     threading.Thread(target=doReq, args=(param,), daemon=True).start()


def speak1(thing):
    try:
        engine.say(thing)
        engine.runAndWait()
    except:
        pass


def speak(thing):
    threading.Thread(target=speak1, args=(thing,), daemon=True).start()


def check_label(lab):
    global count, label
    if lab == label:
        label = lab
        count += 1
    else:
        count = 1
        label = lab


while True:
    # _, image = webcam.read()
    ok = False
    bytes += stream.read(1024)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    if a != -1 and b != -1:
        jpg = bytes[a:b + 2]
        bytes = bytes[b + 2:]
        i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        # cv2.imshow('i', i)

        image = imutils.resize(i, width=400)
        bgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        gray = clahe.apply(bgray)
        nimage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        fd = forward_detector(nimage)
        ld = left_detector(nimage)
        rd = right_detector(nimage)
        sd = stop_detector(nimage)
        ud = uturn_detector(nimage)

        print('last_label:', last_label)

        for b in ud:
            if not ok:
                ok = True
            else:
                break

            if last_label != "uturn":
                last_label = "uturn"
            else:
                break
            (x, y, w, h) = (b.left(), b.top(), b.right(), b.bottom())
            cv2.putText(image, 'uturn', (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255, 0), 2)
            cv2.rectangle(image, (x, y), (w, h), (0, 255, 0), 2)
            speak('uturn')


        for b in fd:
            if not ok:
                ok = True
            else:
                break
            if last_label != "forward":
                last_label = "forward"
            else:
                break
            (x, y, w, h) = (b.left(), b.top(), b.right(), b.bottom())
            cv2.putText(image, 'forward', (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255, 0), 2)
            cv2.rectangle(image, (x, y), (w, h), (0, 255, 0), 2)
            speak('forward')
            doReq("F")

        for b in ld:
            if not ok:
                ok = True
            else:
                break
            if last_label != "left":
                last_label = "left"
            else:
                break
            (x, y, w, h) = (b.left(), b.top(), b.right(), b.bottom())
            cv2.putText(image, 'left', (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255, 0), 2)
            cv2.rectangle(image, (x, y), (w, h), (0, 255, 0), 2)
            speak('left')
            doReq("L")
            # time.sleep(0.05)
            # doReq("F")
            # time.sleep(2)
            # doReq("S")

        for b in rd:
            if not ok:
                ok = True
            else:
                break
            if last_label != "right":
                last_label = "right"
            else:
                break
            (x, y, w, h) = (b.left(), b.top(), b.right(), b.bottom())
            cv2.putText(image, 'right', (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255, 0), 2)
            cv2.rectangle(image, (x, y), (w, h), (0, 255, 0), 2)
            speak('right')
            doReq("R")
            # time.sleep(0.05)
            # doReq("F")
            # time.sleep(2)
            # doReq("S")

        for b in sd:
            if not ok:
                ok = True
            else:
                break
            if last_label != "stop":
                last_label = "stop"
            else:
                break
            (x, y, w, h) = (b.left(), b.top(), b.right(), b.bottom())
            cv2.putText(image, 'stop', (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255, 0), 2)
            cv2.rectangle(image, (x, y), (w, h), (0, 255, 0), 2)
            speak('stop')
            doReq("S")

        cv2.imshow("Image", np.hstack([image]))
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("Exiting..")
            cv2.destroyAllWindows()
            # webcam.release()
            break
