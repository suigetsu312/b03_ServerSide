# 該檔案用來提取訓練log，去除不可解析的log後使log檔案格式化，生成新的log檔案供視覺化工具繪圖
import inspect
import os
import random
import sys
def extract_log(log_file,new_log_file,key_word):
    with open(log_file, 'r') as f: 
      with open(new_log_file, 'w') as train_log:   
  #f = open(log_file)
    #train_log = open(new_log_file, 'w')
        for line in f:
    # 去除多gpu的同步log
          if 'Syncing' in line:
            continue
    # 去除除零錯誤的log
          if 'nan' in line:
            continue
          if key_word in line:
            train_log.write(line)
    f.close()
    train_log.close()

extract_log('/home/leeyihan/b03/darknet/testTraining1027_1.log','train_log_loss.txt','images')
extract_log('/home/leeyihan/b03/darknet/testTraining1027_1.log','train_log_iou.txt','IOU')
