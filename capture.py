import cv2
import urllib.request
import numpy as np


stream = urllib.request.urlopen('http://192.168.225.139/mjpeg/1')
bytes = bytes()
img_counter = 0

while True:
    bytes += stream.read(1024)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    if a != -1 and b != -1:
        jpg = bytes[a:b+2]
        bytes = bytes[b+2:]
        i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow('i', i)
        if cv2.waitKey(1) == 27:
            # SPACE pressed
            img_name = "opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(img_name, i)
            print("{} written!".format(img_name))
            img_counter += 1

cv2.destroyAllWindows()
