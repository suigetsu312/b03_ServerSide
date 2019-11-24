import socket
import cv2.cv2 as cv2
import traceback
import time
import numpy as np
from signal import signal, SIGPIPE, SIG_DFL, SIG_IGN
signal(SIGPIPE, SIG_IGN)

HOST = '140.137.132.172'
PORT = 2002
SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:

    s.connect((HOST, PORT))
    s.sendall(b'camera')
    time.sleep(1)
    IMGSIZE = int(s.recv(SIZE).decode())

    s.sendall(b'getImg')
    time.sleep(1)
    data = s.recv(IMGSIZE)
    data_encode = np.array(data)
    str_encode = data_encode.tostring()
    nparr = np.fromstring(str_encode, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    print('Received')
    cv2.imshow('receiced', img)
    cv2.waitKey(0)
except Exception:
    traceback.print_exc()
    s.close()
