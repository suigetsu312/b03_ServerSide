import sys
sys.path.insert(0,'/home/leeyihan/b03/darknet')
from darknet import *
from time import gmtime, strftime, localtime, sleep
import numpy as np
import json
import base64
import cv2
import requests
from PIL import Image
import os

def yolo(image_path):
    #([b.x, b.y, b.h, b.w, dets[j].prob[i]], meta.names[i])
    print('started detect')
    
    #因應相機位置將照片旋轉180度再儲存
    Rot_name = '/home/leeyihan/b03/socket_python/imageLog/rotate/rotate_' + strftime("%Y-%m-%d-%T", localtime())+'.jpg'
    pri_image = Image.open(image_path)
    pri_image.rotate(180).save(Rot_name)

    #yolo物件偵測
    trad_bbox = detect(net, meta, str.encode(Rot_name))

    #讀取旋轉後的相片
    frame = cv2.imread(Rot_name)

    #如果物件偵測結果沒有任何豆子就回傳None(null)
    if len(trad_bbox) == 0:
        return None

    #convert to numpy array
    trad_bbox = np.asarray(trad_bbox)
    #NMS
    trad_bbox = NMS(trad_bbox)
    #生豆列表
    defect_list=[]
    a=trad_bbox.tolist()
    for i in range(len(a)):
        #印出生豆資料
        print("x: {0:3f}, y: {1:3f}, prob: {2:3f}, class: {3:3f}".format(a[i][0],a[i][1],a[i][4],a[i][5]))
        #忽略prob被設定為-1的豆子和正常豆
        if a[i][4] == -1 or a[i][5] == 0:
            continue
        #加入瑕疵豆列表
        defect_list.append([a[i][0],a[i][1]])

    #點出瑕疵豆中心點並存成另一張圖
    for x in defect_list:
        center_y = int(x[1])
        center_x = int(x[0])
        cv2.circle(frame, (center_x,center_y), 3, (255,255,0), 3)
    cv2.imwrite('/home/leeyihan/b03/socket_python/imageLog/result/result_'+image_path.split('/')[-1], frame)

    return defect_list

#計算iou
def IoU(target,compare):
    target_l = target[0] - target[2]/2
    target_r = target[0] + target[2]/2
    target_d = target[1] - target[3]/2
    target_t = target[1] + target[3]/2

    compare_l = compare[0] - compare[2]/2
    compare_r = compare[0] + compare[2]/2
    compare_d = compare[1] - compare[3]/2
    compare_t = compare[1] + compare[3]/2


    inter_l = np.max([target_l,compare_l])
    inter_r = np.min([target_r,compare_r])
    inter_d = np.max([target_d,compare_d])
    inter_t = np.min([target_t,compare_t])

    interArea = (inter_r-inter_l) * (inter_t-inter_d)
    if ((target_r - compare_l > 0) and (compare_r - target_l > 0)) :
        interArea = interArea
    else:
        interArea = 0

    totalArea = (target_r-target_l) * (target_t-target_d) +    (compare_r-compare_l) * (compare_t-compare_d) - interArea
    return np.max([interArea / (totalArea + 1e-23),0])

#計算nms
def NMS(bbox):
    for i in range(bbox.shape[0]):
        target = i
        if bbox[target,4] != 0:
            for j in range(bbox.shape[0]-i-1):
                compare = j+i+1
                if bbox[target,5] == bbox[compare,5]:
                    iou = IoU(bbox[target],bbox[compare])
                    #如果iou大於0.3就比較prob將較低的刪除
                    if iou > 0.3:
                        if bbox[target,4] >= bbox[compare,4]:
                            bbox[compare,4] = -1
                        else:
                            bbox[target,4] = -1
                            break
    return bbox

#base64轉bytes後存成圖片
def save_img(base64data, img_name):
    with open(img_name, 'wb') as output:
        output.write(base64.b64decode(base64data))

#讀取網路資訊
net = load_net(b'/home/leeyihan/b03/darknet/cfg/yolov3_b03_1.cfg', b'/home/leeyihan/b03/darknet/backup/1027_1/yolov3_b03_1.backup', 0)
meta = load_meta(b"/home/leeyihan/b03/darknet/coffee.data")
#拍照
r = requests.get('http://140.137.132.172:2004/cur_shot')
data = r.json() # Check the JSON Response Content documentation below
img_name = '/home/leeyihan/b03/socket_python/imageLog/image/' + strftime("%Y-%m-%d-%T", localtime()) + '.jpg'
save_img(data['image'] , img_name)

#進行yolo物件偵測
trad_bbox = yolo(img_name)

if trad_bbox == None:
    print('not found')
else:
    #進行傳送前的type轉換
    for x in trad_bbox:
        x[0]=str(x[0])
        x[1]=str(x[1])

    data_dic = {}
    df = []
    for i in range(len(trad_bbox)):
        df = trad_bbox[i]
        data_dic[i] = df


    #將傳送資料轉成json格式
    data_json = json.dumps(data_dic)
    #發出request抓取瑕疵豆
    r = requests.post('http://140.137.132.172:2004/pick_bean', json=data_json)
    #將會回傳204 no content
    print(r.status_code)
