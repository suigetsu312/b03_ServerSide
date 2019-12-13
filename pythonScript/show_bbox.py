import cv2
import glob

imgs = glob.glob('/home/Bo3admin/b03/b03_ServerSide/dataset/mixing/*jpg')

for img in imgs:
    frame = cv2.imread(img)
    f = open(img[:-3]+ 'txt')
    lines = f.readlines()
    for line in lines:
        box =[int(float(x)*608) for x in line.split(' ')[1:]]
        print('line : {0}, box : {1}'.format(line, box))
        x_center = box[0]
        y_center = box[1]
        w = box[2]
        h = box[3]
        x_u = int(x_center-int(w/2))
        y_u = int(y_center-int(h/2))

        cv2.rectangle(frame, (x_u,y_u), (x_u+w,y_u+h), (255,255,0), 2)
        
    cv2.imwrite(img.split('.')[0]+'_testbox.jpg',frame)
    