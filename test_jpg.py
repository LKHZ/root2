#-*-codeing = utf-8 -*-
#@Time : 2022/5/2 16:24
#@Author : LichunSun
#@File : test_jpg.py

import matplotlib.pyplot as plt
from astropy.io import fits
import h5py
import datetime
import numpy as np
from single_sample import hd5,Txt_save

def sample(hd5_path,reshapesize,seg_size,txtsavepath):
    hd5file = hd5.read(hd5_path)
    channel = hd5file.keys()
    channels = [key for key in channel]
    channels.sort(key=lambda x: int(x[8:]))

    for row in range(0, reshapesize, seg_size):
        for column in range(0, reshapesize, seg_size):

            X = []
            Y = []
            Z = []
            get_channel_time = []
            print('一个采样开始时间：',datetime.datetime.now())
            starttime = datetime.datetime.now()
            for z,channel in enumerate(channels):

                print(z,channel)
                #print(datetime.datetime.now())
                time = datetime.datetime.now()
                data = hd5file['{}'.format(channel)][:]
                print("取一个channel",datetime.datetime.now()-time)
                get_channel_time.append(datetime.datetime.now() - time)
                data = data.reshape(reshapesize, reshapesize)
                #print('hd5取一个channel：', datetime.datetime.now())
                #num_point = 5000
                newdata = data[column :column+seg_size, row :row+seg_size]
                num_point = 500
                sort = np.argsort(newdata.flatten(),kind='mergesort')


                for i in range(1, num_point+1):
                    x = int(sort[-i] / newdata.shape[1]) + row
                    y = sort[-i] % (newdata.shape[1]) + column
                    X.append(x)
                    Y.append(y)
                    Z.append(z)
                print('取完数据后采样：', datetime.datetime.now())
            ALL = list(zip(X, Y, Z))
            np.savetxt(txtsavepath + '/' + 'get_channel_time{}_{}_{}.txt'.format(seg_size,row,column),get_channel_time,fmt = '%s')
            #Txt_save(txtsavepath + '/' + 'part_t1_{}_{}_{}.txt'.format(seg_size,row,column),ALL)
            swap_ALL = list(zip(Y, X, Z))
            #Txt_save(txtsavepath + '/' + 'swap_part_t1_{}_{}_{}.txt'.format(seg_size,row,column),swap_ALL)
            print('part_t1_{}_{}_{}.txt save successful'.format(seg_size,row,column))
            print('一个采样结束时间：',datetime.datetime.now())
            print('一个采样消耗的时间：', datetime.datetime.now()-starttime)
            #np.savetxt('all_part_t1_16k_16k_1000.txt', ALL)
    hd5file.close()


def main():
    sample(hd5_path,reshapesize,seg_size,txtsavepath)

if __name__ == '__main__':

    print('start time:', datetime.datetime.now())
    hd5_path = r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/part_t1.hdf5'
    txtsavepath = r'/home/lab30201/sdd/slc/SKAData/SKA_algorithm/testsmple'
    reshapesize = 16384
    seg_size = 256
    main()