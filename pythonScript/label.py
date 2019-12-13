import numpy
import cv2.cv2 as cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
import sys
import os
from Sample.SampleImage import SampleImage

positiveSampleClass = ['mixing']
#negativeSampleClass = ['broken','insect']
sampleRootPath = '/home/Bo3admin/b03/b03_ServerSide/coffee'
sampleinfo = []
def getSampleImagesByClass(sampleClass:str):
    print(sampleRootPath+'/'+sampleClass+'/*.jpg')
    SampleImages = glob.glob(sampleRootPath+'/'+sampleClass+'/*.jpg')
    if(len(SampleImages) == 0):
        print('{} image is not found.'.format(sampleClass))
    else:
        print('{}:{}.'.format(sampleClass,str(len(SampleImages))))

    return SampleImages

def img_threadhold(frame):
    #轉灰階
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #平滑化
    gray_img = cv2.GaussianBlur(gray_img, (3, 3), 0)

    #依照區域亮度做二值化
    gray_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, blockSize = 321, C = 14)
    
    #膨脹
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(1, 1))
    gray_img = cv2.erode(gray_img,kernel)
    
    return gray_img

def cleanFolder(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

def getBBox(c:str, obClass:int):
      
    folderPath = './dataset/'+c
    if os.path.exists(folderPath) is False:
        os.makedirs(folderPath)
    cleanFolder(folderPath)
    count = 0
    SampleImages = getSampleImagesByClass(c)
    for SI in SampleImages:
      
        SampleImg = SampleImage(SI)
        f = open(folderPath + '/' + SampleImg.name +'.txt', 'w+')

        frame = cv2.imread(SampleImg.filePath)
        #frame = np.uint8(np.clip((frame * 1.7 + 40),0,255))
        dis = frame.copy()
        height, width, _ = frame.shape
        #二值化
        gray_img = img_threadhold(frame)
        #取得輪廓
        contours, _ = cv2.findContours(gray_img.copy(), cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
        rects = [cv2.boundingRect(contour) for contour in contours]
        rects = [rect for rect in rects if rect[2] >= 8 and rect[3] >= 24]
        count +=len(rects)
        for rect in rects:        
                
            #紀錄生豆在圖片上的位置
            x,y,w,h = rect
            #cv2.rectangle(dis, (x, y), (x + w, y + h), (255,255,0), 5)
            xmin = x
            xmax = x+w
            ymin = y
            ymax = y+h
            recx = int(x)
            recy = int(y)
            recw = int(w)
            rech = int(h)
            cv2.rectangle(dis, (recx,recy),(recx+recw,recy+rech),color=(255,255,0))
            #類別
            c = obClass
            #長寬及高度 bbox : image
            x = (xmin +(xmax-xmin)/2*1.0)/width
            y = (ymin +(ymax-ymin)/2*1.0)/height
            w = (xmax-xmin)*1.0/width
            h = (ymax-ymin)*1.0/height
            #write bbox info to txt file
            if rect == rects[-1]:
                f.writelines('{} {:.6f} {:.6f} {:.6f} {:.6f}'.format(c,x,y,w,h))
            else:
                f.writelines('{} {:.6f} {:.6f} {:.6f} {:.6f}\n'.format(c,x,y,w,h))
            #cv2.putText(dis, str(c), (recx+recw,recy+rech), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
                
            #print to CLI
            #print('{} {:.6f} {:.6f} {:.6f} {:.6f}'.format(c,x,y,w,h))
        cv2.imwrite(folderPath + '/' + SampleImg.name +'.jpg',dis)
        sampleinfo.append(SampleImages)
        f.close()
    print(count)

if __name__ == "__main__":
    idx = 1
    '''for i in negativeSampleClass:
        getBBox(i,idx)
        idx+=1
    '''
    getBBox(positiveSampleClass[0],0)
    


        




        
    
    
    
    


