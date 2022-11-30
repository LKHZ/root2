#-*-codeing = utf-8 -*-
#@Time : 2022/5/26 21:50
#@Author : LichunSun
#@File : evaluation.py

import numpy as np
import os
import matplotlib.pyplot as plt
def Plt(x,y,color,file):
    X = int(file.split('_')[2])
    Y = int(file.split('_')[3])
    plt.style.use('classic')
    plt.figure(figsize=(15,15))
    plt.scatter(x, y, s=30, c=color, label='dis_20', marker='x')
    #plt.scatter(x[743:], y[743:], s=80, c=color[743:], label='dis_15', marker='x')
    plt.xlim(X, X+1024 )
    plt.ylim(Y, Y+1024 )
    plt.grid()
    plt.title(file.split('.txt')[0],fontsize=20)
    plt.legend(loc='upper center')
    plt.xticks(range(X, X+1024, 128))
    plt.yticks(range(Y, Y+1024, 128))
    plt.xlabel('X(pixels)', fontsize=20)
    plt.ylabel('Y(pixels)', fontsize=20)
    #plt.title('gleam/all_cluster', fontsize=20)
    plt.savefig('/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cluster/cal_1k_class/' + file.split('.txt')[0] + '.png')
    plt.close()

def Cal_distance(point_a,point_b):
    p1 = point_a
    p2 = point_b
    squared_dist = np.sum((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 ,axis=0)
    dist = np.sqrt(squared_dist)
    return dist

def Evaluation(cluster_xy,dis,file,savepath):
    X = int(file.split('_')[2])
    Y = int(file.split('_')[3])
    cluster_xy[:, 0] = cluster_xy[:, 0] + X
    cluster_xy[:, 1] = cluster_xy[:, 1] + Y
    truelabel = np.loadtxt(labellist + '/' + 'image_{}_{}.list'.format(file.split('_')[2], file.split('_')[3]))
    truelabel = truelabel.reshape((-1, 3))
    truelabel = truelabel[:, 1:]
    truelabel[:, 0] = truelabel[:, 0] + X
    truelabel[:, 1] = truelabel[:, 1] + Y
    num = 0
    for i in range(cluster_xy.shape[0]):
        for j in range(truelabel.shape[0]):
            if Cal_distance(cluster_xy[i, :2], truelabel[j, :]) <= dis:
                num += 1
                a = 1
                cluster_xy[i, 2] = j
                break
            else:
                a = 0
        if a == 0:
            cluster_xy[i, 2] = -1

    if float(num / cluster_xy.shape[0]) != 1:
        print(file)
        print(truelabel.shape)
        print('{:.2f}%'.format(float(num / cluster_xy.shape[0]) * 100))
        Plt(cluster_xy[:, 0], cluster_xy[:, 1], cluster_xy[:, 2], file)

    cluster_xy = np.array(list(set([tuple(uniquexy) for uniquexy in cluster_xy])))
    np.savetxt(savepath + '/' + file.split('.txt')[0] + '_cal_{}_class.txt'.format(dis), cluster_xy)
    return cluster_xy

if __name__ == '__main__':

    inputdir = r'/home/lab30201/sdd/slc/SKAData/SKA_algorithm/cluster/test1'
    labellist = r'/home/lab30201/sdd/slc/SKAData/Faster_mulchannel/datafits1'
    savepath = r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cluster/cal_1k_class'
    filelist = os.listdir(inputdir)
    filelist = [file for file in filelist if file.endswith('txt') and  file.split('_')[0] == 'kdtree']
    dis = 20
    all_xy = np.empty((1, 3))
    for file in filelist:
        #print(file)
        txtpath = inputdir + '/' + file
        cluster_xy = np.loadtxt(txtpath)
        x = int(file.split('_')[2])
        y = int(file.split('_')[3])
        #print(x,y)
        # print(cluster_xy[0,:])
        cluster_xy[:,0] = cluster_xy[:,0]+ x
        cluster_xy[:,1] = cluster_xy[:,1] +y
        # print(cluster_xy[0, :])
        truelabel = np.loadtxt(labellist + '/' + 'image_{}_{}.list'.format(file.split('_')[2],file.split('_')[3]))
        truelabel = truelabel.reshape((-1,3))
        truelabel = truelabel[:,1:]
        truelabel[:,0] = truelabel[:,0] + x
        truelabel[:,1] = truelabel[:,1] + y
        # print(truelabel[0,:])
        a = 0
        num = 0
        for i in range(cluster_xy.shape[0]):
            for j in range(truelabel.shape[0]):
                if Cal_distance(cluster_xy[i,:2],truelabel[j,:])<=dis:
                    num+=1
                    a=1
                    cluster_xy[i, 2] = j
                    break
                #     break
                else:
                     a=0
            if a == 0 :
                cluster_xy[i, 2] = -1
                #     continue
            #cluster_xy[i,2] = a



        if float(num/cluster_xy.shape[0]) != 1:
            print(file)
            #print('True sources')
            print(truelabel.shape)
            print('{:.2f}%'.format(float(num/cluster_xy.shape[0])*100))
            Plt(cluster_xy[:,0],cluster_xy[:,1],cluster_xy[:,2],file)
        #cluster_xy = np.array(list(set([tuple(uniquexy) for uniquexy in cluster_xy])))
        #np.savetxt(savepath + '/' +file.split('.txt')[0] + '_cal_{}_class.txt'.format(dis),cluster_xy)
        #all_xy = np.vstack((cluster_xy, all_xy))

    # all_xy = np.delete(all_xy, -1, 0)
    # all_xy = np.array(list(set([tuple(uniquexy) for uniquexy in all_xy])))
    # np.savetxt(savepath + '/' + 'all_cal_{}.txt'.format(dis),all_xy)