import socket
import cv2.cv2 as cv2
from cameraTest import *
import traceback
import sys
sys.path.insert(0,'/home/leeyihan/b03/darknet')
from darknet import *
import darknet
signal(SIGPIPE, SIG_IGN)
class SocketServer():
    def __init__(self, HOST, PORT, SIZE):
        self.SIZE = SIZE
        self.HOST = HOST
        self.PORT = PORT
        self.net = load_net(b'/home/leeyihan/b03/darknet/cfg/yolov3_b03.cfg', b'/home/leeyihan/b03/darknet/backup1/yolov3_b03.backup', 0)
        self.meta = load_meta(b"/home/leeyihan/b03/darknet/coffee.data")

        self.camera = Camera(608,608,'./imageLog/')
        self.Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Server.bind((HOST, PORT))
        print('socket is ready')
    def Run(self):
        try:
            self.Server.listen(1)
            conn, addr = self.Server.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                       break
                    if data == b'camera':
                        self.camera.Shot()
                        self.imgdata = cv2.imencode('.jpg',self.camera.curImg)[1].tostring()
                        imgsize = str(len(self.imgdata)).encode()
                        conn.sendall(imgsize)
                    if data == b'getImg':
                        conn.sendall(self.imgdata)
                    if data == b'close':
                        break
            self.Server.close()
        except Exception:
            traceback.print_exc()
            self.Server.close()
        
if __name__ == "__main__":
    server = SocketServer('127.0.0.1',50000,1024)
    server.Run()