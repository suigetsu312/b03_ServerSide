import numpy as np
import glob
import sys
import os
import random 
import shutil
import cv2.cv2 as cv2

#建立儲存所有影像樣本檔案之路徑的變數
AllSampleImg = []
#建立儲存樣本種類的變數
SampleClass = [ 'mixing']
#以下為儲存樣本資料夾的變數
imgRootPath = '/home/Bo3admin/b03/b03_ServerSide/coffee/'
labelRootPath = '/home/Bo3admin/b03/b03_ServerSide/dataset/'

dataPath = '/home/Bo3admin/b03/b03_ServerSide/darknet/data/b03/'
trainPath = '/home/Bo3admin/b03/b03_ServerSide/darknet/data/b03/train/'
valPath = '/home/Bo3admin/b03/b03_ServerSide/darknet/data/b03/val/'
#取得某種樣本所有的影像檔案路徑
def getSampleImageByClass(sampleClass:str):
    #使用glob取得jpg檔的路徑
    SampleImages = glob.glob(imgRootPath+'/'+sampleClass+'/*.jpg')
    #將list串接
    AllSampleImg.extend(SampleImages)
    #顯示樣本數量
    if(len(SampleImages) == 0):
        print('{} image is not found.'.format(sampleClass))
    else:
        print('{}:{}.'.format(sampleClass,str(len(SampleImages))))

#清空特定資料夾之檔案
def cleanFolder(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
#將樣本的資料分成訓練集或驗證集移至另一個資料夾
def genDataset(datapath, basepath, lenth, mode):
    #使用mode來決定是哪個資料集
    if mode == 'train':
        filename = 'train'
    elif mode == 'val':
        filename = 'val'
    else:
        print('輸入了錯誤的模式')
        return
    #開啟紀錄資料集檔案的txt
    f = open(dataPath+'/'+filename+'.txt', 'w+')
    dataset = AllSampleImg[0:lenth]
    for img in dataset:

        fullimgpath = os.path.abspath(img)
        frame = cv2.imread(fullimgpath)
        cv2.imwrite(basepath + '/' + img.split('/')[-1], frame) 
        shutil.copyfile( labelRootPath+'/'+img.split('/')[-2]+'/'+img.split('/')[-1].split('.')[0] + '.txt', basepath + '/' + img.split('/')[-1].split('.')[0] + '.txt')
        fullimgpath = os.path.abspath(basepath + '/' + img.split('/')[-1])
        if img != dataset[-1] :
            fullimgpath = fullimgpath + '\n'
        f.writelines(fullimgpath)
        AllSampleImg.remove(img)
        print(fullimgpath)
    f.close()
if __name__ == "__main__":

    cleanFolder(trainPath)
    cleanFolder(valPath)

    for s in SampleClass:
        getSampleImageByClass(s)
    random.shuffle(AllSampleImg)

    train = int(len(AllSampleImg)*0.8//1)
    val = len(AllSampleImg) - train
    print('train: {} pics, val : {} pics'.format(train,val))

    genDataset(dataPath, trainPath, train, 'train')
    genDataset(dataPath, valPath, val, 'val')