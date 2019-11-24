import os
import sys
import glob
import cv2.cv2 as cv2
import numpy as np

class BBox():
    def __init__(self, x, y, h, w):
        self.x = x
        self.y = y
        self.h = h
        self.w = w

#所有的bbox
boxes = [] 
SampleClass = ['broken','insect','normal']
labelRootPath = './dataset/'
imageHeight = 3456
imageWidth = 4608
'''
計算某一軸重疊的長度
p1,p2為bbox中心點的座標
len1,len2為該軸的長度
'''
def axisOverlap(p1,len1,p2,len2):
    len1_h = len1 / 2
    len2_h = len2 / 2

    left = max(p1 - len1_h, p2 - len2_h)
    right = min(p1 + len1_h, p2 + len2_h)

    return right - left    

#兩個bbox間的交集（重疊的部份）
def iou_overlap(b1,b2):
    x = axisOverlap(b1.x, b1.w, b2.x, b2.w)
    y = axisOverlap(b1.y, b1.h, b2.y, b2.h)
    
    if x < 0 or y < 0:
        return 0
    return x * y

#兩個bbox的聯集
def iou_unity(b1,b2):
    overlap = iou_overlap(b1,b2)
    unity = b1.w*b1.h + b2.w*b2.h - overlap
    return unity

#bbox間的iou
def iou(b1, b2):
    return iou_overlap(b1,b2)/iou_unity(b1,b2)

#yolo9000中定義的距離
def iou_distance(b1,b2):
    return 1- iou(b1,b2)


def kpp_init(anchor_num):
    #建立一個list儲存每個cluster的中心點
    centroids = []
    #先隨機選出一個當作中心點
    boxes_num = len(boxes)
    centroid_index = int(np.random.choice(boxes_num,1))
    centroids.append(boxes[centroid_index])
    
    for centroid_index in range(0, anchor_num-1):
        sum_distance = 0
        distance_thresh = 0
        distance_list = []
        cur_sum = 0
        for b in boxes:
            min_distance = 1
        
            for idx, centroid in enumerate(centroids):
                distance = iou_distance(b ,centroid)
                #print(distance)
                if  distance < min_distance:
                    min_distance = distance
            sum_distance += min_distance
            distance_list.append(min_distance) 
        distance_thresh = sum_distance * np.random.random_sample()

        for i in range(0, boxes_num):
            cur_sum += distance_list[i]
            if cur_sum > distance_thresh:
                centroids.append(boxes[i])
                break
    return centroids

def kmeans(n_anchors, centroids):
    loss = 0
    groups = []
    new_centroids = []
    for i in range(n_anchors):
        groups.append([])
        new_centroids.append(BBox(0, 0, 0, 0))

    for box in boxes:
        min_distance = 1
        group_index = 0
        for centroid_index, centroid in enumerate(centroids):
            distance = (1 - iou(box, centroid))
            if distance < min_distance:
                min_distance = distance
                group_index = centroid_index
        groups[group_index].append(box)
        loss += min_distance
        new_centroids[group_index].w += box.w
        new_centroids[group_index].h += box.h

    for i in range(n_anchors):
        new_centroids[i].w /= len(groups[i])
        new_centroids[i].h /= len(groups[i])

    return new_centroids, groups, loss


def getBBox():

    for c in SampleClass:
        #找出所有儲存label的txt file
        labelsfiles = glob.glob(labelRootPath+c+'/*.txt') 
        for file in labelsfiles:
            with open(file) as f:
                #取出所有bbox
                labelBbox = f.readlines()
                for i in labelBbox:
                    curbbox = i.strip().split(' ')
                    x = 0
                    y = 0
                    w = float(curbbox[3]) * imageWidth
                    h = float(curbbox[4]) * imageHeight
                    boxes.append(BBox(x,y,w,h))
def area(elem):
    return elem[0]*elem[1]
if __name__ == "__main__":
    anchor_num = 9
    iterations_num = 100
    loss_convergence = 1e-6
    getBBox()
    centroids = kpp_init(anchor_num)
    
    # iterate k-means
    centroids, groups, old_loss = kmeans(anchor_num, centroids)
    iterations = 1
    while (True):
        centroids, groups, loss = kmeans(anchor_num, centroids)
        iterations = iterations + 1
        print("loss = %f" % loss)
        if abs(old_loss - loss) < loss_convergence or iterations > iterations_num:
            break
        old_loss = loss

        for centroid in centroids:
            print(centroid.w , centroid.h)
    
    area = []
    # print result

    centroids.sort(key = lambda x : x.w*x.h)
    for centroid in centroids:
        area = centroid.w * centroid.h
        if area == centroids[-1].w* centroids[-1].h:
            print("{0:.2f},{1:.2f}".format(centroid.w, centroid.h, area))
        else:
            print("{0:.2f},{1:.2f},".format(centroid.w, centroid.h, area), end=' ')