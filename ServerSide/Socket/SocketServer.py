import socket
import codecs
import cv2.cv2 as cv2
import random
import time
import numpy as np
import traceback
import sys
sys.path.insert(0,'/home/leeyihan/b03/darknet')
from darknet import *
from signal import signal, SIGPIPE, SIG_DFL, SIG_IGN
signal(SIGPIPE, SIG_IGN)
class SocketServer():
    def __init__(self, HOST, PORT, SIZE, path):
        self.SIZE = SIZE
        self.HOST = HOST
        self.PORT = PORT
        self.PATH = path
        self.SIZE = 1024
        self.net = load_net(b'/home/leeyihan/b03/darknet/cfg/yolov3_b03.cfg', b'/home/leeyihan/b03/darknet/backup1/yolov3_b03.backup', 0)
        self.meta = load_meta(b"/home/leeyihan/b03/darknet/coffee.data")
        self.Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.position = ''
        self.Server.bind((HOST, PORT))
        print('socket is ready')

    def Run(self):
        try:
            self.Server.listen(1)
            conn, addr = self.Server.accept()
            with conn:
                print('Connected by', addr)
                notReaded = True
                while True:
                    data = conn.recv(self.SIZE)
                 
                    txt = data.decode(errors="ignore")

                    if len(txt)<9:
                        self.SIZE = 1024
                        print('txt=',txt)

                    if data and self.SIZE != 1024:
                        #print('GET IMAGE')
                        data_encode = np.array(data)
                        str_encode = data_encode.tostring()
                        nparr = np.fromstring(str_encode, np.uint8)
                        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                        filename = self.PATH + str(random.getrandbits(64))+'.jpg'
                        cv2.imwrite(filename, img)
                        #print('start yolodetect')
                        self.position = detect(self.net, self.meta, bytes(filename,encoding='utf-8'))
                        time.sleep(1)
                        #print('send position: ',self.position)
                        if len(self.position) == 0 :
                            print('not found ',len(self.position))
                            conn.sendall(b'NOTFOUND')
                        else: 
                            print('found ',len(self.position))
                            conn.sendall(b'POSITION')

                    elif txt.startswith('IMGSIZE'):
                        self.SIZE = int(txt.split(' ')[1])
                        conn.sendall(b'GOTSIZE')
                        #print('GOT SIZE')

                    elif txt == 'GETPOS':
                        str1 = ''
                        for i in self.position:
                            str1 += str(i) + ' '
                        conn.sendall(('pos,'+str1).encode())
                    
                    elif data == b'close':
                        break
            self.Server.close()
        except Exception:
            traceback.print_exc()
            self.Server.close()
        
if __name__ == "__main__":
    server = SocketServer('127.0.0.1', 50000, 1024, './imageLog/')
    server.Run()
    