#-*-codeing = utf-8 -*-
#@Time : 2022/7/20 15:58
#@Author : LichunSun
#@File : Cal_recall_cluster.

import os
import numpy as np
import matplotlib.pyplot as plt

def Cal_distance_2(point_a,point_b):
    p1 = point_a
    p2 = point_b
    squared_dist = np.sum((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 ,axis=0)
    dist = np.sqrt(squared_dist)
    return dist

def Cal_recall(labelpath,clusterpath):
    filelist = os.listdir(clusterpath)
    print(filelist)
    filelist = [file for file in filelist if file.endswith('.txt')]
    count = 0
    all_i = []
    n = 0
    for file in filelist:
        print(n)
        print('all_i',len(all_i))
        n+=1
        field = int(file.split('_')[2].split('d')[1])
        x = int(file.split('_')[4])
        y = int(file.split('_')[5])
        cluster = np.loadtxt(clusterpath + '/' + file)[:,:2]
        cluster_unique = np.unique(cluster,axis=0)
        truelabel = np.loadtxt(labelpath + '/' + 'image_field{}_random_{}_{}.list'.format(field,x,y))
        truelabel = truelabel.reshape((-1,4))
        record = [0] * truelabel.shape[0]
        for i in range(truelabel.shape[0]):
            for j in range(cluster_unique.shape[0]):
                dist = Cal_distance_2(truelabel[i,1:3], cluster_unique[j])
                if dist < 20:
                    record[i] = 1
                    all_i.append(truelabel[i,3])
                    break
        count+=record.count(1)
    return count,all_i

if __name__ == '__main__':
    labelpath ='/home/dell460/slc/sdd_01/SKAData/CIP_random2/data/10field/label_I'
    clusterpath = '/home/dell460/slc/sdd_01/SKAData/CIP_random2/data/cluster'
    count,all_target_i = Cal_recall(labelpath,clusterpath)
    #print(count)
    print(all_target_i)
    true_i = np.loadtxt('/home/dell460/slc/sdd_01/SKAData/CIP_random2/data/all_label_I.txt')
    nums, bins = np.histogram(np.log2(true_i[:, 2]), bins=20)
    target_nums, target_bins = np.histogram(np.log2((all_target_i)), bins=bins)
    pre_plot = []
    print(nums)
    print(target_nums)
    # print(np.arange(np.min(bins),np.max(bins),(np.max(bins)-np.min(bins))/20))
    for i in range(len(target_nums)):
        if target_nums[i] == nums[i]:
            pre_plot.append(1)
        else:
            pre_plot.append(target_nums[i] / nums[i])
    plt.plot((np.arange(np.min(bins), np.max(bins), (np.max(bins) - np.min(bins)) / 20)), pre_plot)
    plt.grid()
    plt.title('cluster')
    plt.ylabel('recall')
    plt.xlabel('log_I(Jy)')
    plt.savefig('/home/dell460/slc/sdd_01/SKAData/CIP_random2/data/random2_cluster_recall.png')
    # path = '/home/lab30201/sdd/slc/SKAData/CIP_random/CIP_random/CIPdata/image/part1/t1/1l_cluster/' \
    #        'kdtree_randoom_image_random_0_0_5000_0.005.txt'
    # x = int(os.path.basename(path).split('_')[4])
    # y = int(os.path.basename(path).split('_')[5])
    # truepath = '/home/lab30201/sdd/slc/SKAData/CIP_random/CIP_random/CIPdata/image/part1/t1/label'+ '/' \
    #        + 'image_random_{}_{}.list'.format(x,y)
    # cluster = np.loadtxt(path)
    # truelabel = np.loadtxt(truepath)[:,1:3]
    # cluster_xy = cluster[:,:2]
    # print(cluster_xy.shape)
    # cluster_xy = np.unique(cluster_xy,axis=0)
    # record = [0]*truelabel.shape[0]
    # for i in range(truelabel.shape[0]):
    #     for j in range(cluster_xy.shape[0]):
    #         dist = Cal_distance_2(truelabel[i],cluster_xy[j])
    #         if dist<20:
    #             record[i] = 1
    # print(record.count(1))