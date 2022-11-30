#-*-codeing = utf-8 -*-
#@Time : 2022/5/30 16:12
#@Author : LichunSun
#@File : reg_det.py

import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
def Plt(x):
    plt.style.use('classic')
    lenx = len(x)
    plt.plot(range(lenx),x)
    #plt.plot(range(lenx),y)
    plt.title('Square root error of center (cluster-truelabel)')
    plt.ylabel('sqrt(Center_cluuster-label)')
    plt.savefig(txtpath + '/' + 'error_sqrt.png')
    plt.close()

def Reg_det(xyclass,_class,file):
    X = int(file.split('_')[2])
    Y = int(file.split('_')[3])
    xy = xyclass[:,:2]
    x1 = np.min(xy[:,0]) -X
    y1 = np.max(xy[:,1]) -Y
    x2 = np.max(xy[:,0]) -X
    y2 = np.min(xy[:,1]) -Y
    #print((x2-x1)/2 + x1,(y1-y2)/2 + y2)
    #print(_class)
    return (x2-x1)/2 + x1,(y1-y2)/2 + y2
    #return np.array([x1,y1,x2,y2,_class])
def All_Reg_det(file,truelabel):

    data = np.loadtxt(txtpath + '/' + file)
    data = np.array([xy for j, xy in enumerate(data) if data[j, 2] != -1])
    _class = np.unique(data[:,2])
    #print(_class)
    for i in range(_class.shape[0]):
        #if _class[i]!=-1:
        xy = np.array([xy for j,xy in enumerate(data) if data[j,2]==_class[i]])

        poision = Reg_det(xy,_class[i],file)
        for j in range(truelabel.shape[0]):
            if abs(poision[0]-truelabel[j,1])<10 and abs(poision[1] - truelabel[j,2])<10:

                sqrt_x = (abs(poision[0] - truelabel[j, 1]))**2
                sqrt_y = (abs(poision[1] - truelabel[j, 2]))** 2

                errors_sqrt.append(np.sqrt(sqrt_x+sqrt_y))


if __name__ == '__main__':
    #txtpath = r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cluster/cal_1k_class/kdtree_image_5120_6144_5000_cal_20_class.txt'
    labellist = r'/home/lab30201/sdd/slc/SKAData/Faster_mulchannel/datafits1'
    txtpath = r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cluster/cal_1k_class'
    filelist = os.listdir(txtpath)
    filelist = [file for file in filelist if file.endswith('txt') and file.split('_')[0] == 'kdtree']
    error_xs = []
    error_ys = []
    errors_sqrt = []
    NUM = 0
    for file in filelist:
        #print(file)

        truelabel = np.loadtxt(labellist + '/' + 'image_{}_{}.list'.format(file.split('_')[2], file.split('_')[3]))
        truelabel = truelabel.reshape((-1, 3))
        NUM +=truelabel.shape[0]
        All_Reg_det(file,truelabel)
    print(NUM)
    print(len(errors_sqrt))
        #print('true',truelabel[:, 1:])
    #Plt(error_xs,error_ys)
    #Plt(errors_sqrt)
