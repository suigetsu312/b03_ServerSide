import socket
import cv2.cv2 as cv2
import traceback
import cameraTest
import random
import time
import numpy as np
from signal import signal, SIGPIPE, SIG_DFL, SIG_IGN
signal(SIGPIPE, SIG_IGN)
from cameraTest import *

class SocketClient():
    def __init__(self, HOST, PORT, SIZE, path):
        self.SIZE = SIZE
        self.HOST = HOST
        self.PORT = PORT
        self.camera = Camera(608,608,'./imageLog/')
        self.imgdata = None
        self.Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def Run(self):
        try:
            self.Client.connect((HOST, PORT))
            #shot image & send image size
            self.camera.Shot()
            curImg = cv2.imread('/home/leeyihan/b03/coffee/broken/trjfdrthjfhbnfj (2).JPG')
            self.imgdata = cv2.imencode('.jpg',curImg)[1].tostring()
            imgsize = ('IMGSIZE ' + str(len(self.imgdata))).encode()
            self.Client.sendall(imgsize)
            while True:
                data = self.Client.recv(1024)
                txt = data.decode()
                #send image data
                if txt == 'GOTSIZE':
                    self.Client.sendall(self.imgdata)
                
                elif txt == 'POSITION':
                    print('readey to get position')
                    self.Client.sendall(b'GETPOS')

                elif txt == 'NOTFOUND':
                    print('OBJECT NOT FOUND')
                    break
                elif txt.startswith('pos'):
                    print('position :', txt.split(','))
                    break
                elif data:
                    print('connection failed. get ', txt)
                    break
                elif not data:
                    break
                #get position
            self.Client.sendall(b'close')
            self.Client.close()
        except Exception:
            traceback.print_exc()
            self.Client.close()
        
if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 50000
    SIZE = 1024
    client = SocketClient(HOST,PORT,SIZE,'./imageLog/')
    client.Run()