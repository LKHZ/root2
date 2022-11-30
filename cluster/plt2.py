#-*-codeing = utf-8 -*-
#@Time : 2022/5/27 21:55
#@Author : LichunSun
#@File : plt2.py

import os
import numpy as np
import matplotlib.pyplot as plt


def Plt(x,y,color):
    plt.style.use('classic')
    plt.figure(figsize=(20, 20))
    plt.scatter(x, y, s=30, c=color, label='dis_20', marker='x')
    #plt.scatter(x[743:], y[743:], s=80, c=color[743:], label='dis_15', marker='x')
    plt.xlim(2048, 2048+1024 )
    plt.ylim(8192, 8192+1024 )
    plt.grid()
    plt.legend(loc='upper center')
    plt.xticks(range(2048, 2048+1024, 128))
    plt.yticks(range(8192, 8192+1024, 128))
    plt.xlabel('X(pixels)', fontsize=20)
    plt.ylabel('Y (pixels)', fontsize=20)
    plt.title('gleam/all_cluster', fontsize=20)
    plt.savefig('/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cluster/cal_1k_class/kdtree_image_2048_8192_5000_cal_20_class.png')
    plt.close()


if __name__ == '__main__':

    txtpath = '/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cluster/cal_1k_class/kdtree_image_2048_8192_5000_cal_20_class.txt'
    clusterxy = np.loadtxt(txtpath)
    Plt(clusterxy[:,0],clusterxy[:,1],clusterxy[:,2])