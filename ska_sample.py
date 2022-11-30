#-*-codeing = utf-8 -*-
#@Time : 2022/5/3 16:38
#@Author : LichunSun
#@File : ska_sample.py


import os
import cv2
import numpy as np
from astropy.io import fits
import h5py


class hd5:

    def read(file):
        hd5_file = h5py.File(file, 'r')
        return hd5_file

    def write_hd5(self, file, data, datasetname: str):
        '''
        Create new file to write info
        :param file:
        :param data:
        :param datasetname:
        :return:
        '''
        hd5_file = h5py.File(file, 'w')
        hd5_file.create_dataset(datasetname, data=data)

def Single_sample(hd5_path,reshapesize):
    '''
    针对hd5文件
    :param hd5_path:
    :return:
    '''

    hd5file = hd5.read(hd5_path)
    channel = hd5file.keys()
    channels = [key for key in channel]
    channels.sort(key=lambda x: int(x[8:]))


    data = hd5file['{}'.format(channels[0])][:]
    data = data.reshape(reshapesize,reshapesize)

    X = []
    Y = []
    Z = []
    print(data.shape)
    #num_point = int(img.shape[1] / 3)
    num_point = 1000
    sort = np.argsort(data.flatten())
    for i in range(1, num_point):
        x = int(sort[-i] / data.shape[1])
        y = sort[-i] % (data.shape[1])
        X.append(x)
        Y.append(y)
    Z.append(0)

    ALL = list(zip(X, Y, Z*num_point))
    Txt_save(ALL, 'all_part_t1_16k_16k_1000.txt')
    #np.savetxt('part_t1_16k_16k_1000.txt',ALL)
    hd5file.close()

def ALL_sample(hd5_path, reshapesize):
    '''

    :param hd5_path:
    :param reshapesize:
    :return:
    '''

    hd5file = hd5.read(hd5_path)
    channel = hd5file.keys()
    channels = [key for key in channel]
    channels.sort(key=lambda x: int(x[8:]))

    X = []
    Y = []
    Z = []
    for z,channel in enumerate(channels):
        print(z,channel)
        data = hd5file['{}'.format(channel)][:]
        data = data.reshape(reshapesize, reshapesize)

        print(data.shape)
        # num_point = int(img.shape[1] / 3)
        num_point = 1000
        sort = np.argsort(data.flatten())
        for i in range(1, num_point):
            x = int(sort[-i] / data.shape[1])
            y = sort[-i] % (data.shape[1])
            X.append(x)
            Y.append(y)
        Z.append(z)

    ALL = list(zip(X, Y, Z * num_point))
    Txt_save(ALL,'all_part_t1_16k_16k_1000.txt')
    #np.savetxt('all_part_t1_16k_16k_1000.txt', ALL)
    hd5file.close()

def ALL_sample_1(hd5_path, reshapesize):
    '''

    :param hd5_path:
    :param reshapesize:
    :return:
    '''

    X = []
    Y = []
    Z = []


    hd5file = hd5.read(hd5_path)
    channel = hd5file.keys()
    channels = [key for key in channel]
    channels.sort(key=lambda x: int(x[8:]))

    for z,channel in enumerate(channels):

        print(z,channel)
        data = hd5file['{}'.format(channel)][:]
        data = data.reshape(reshapesize, reshapesize)

        print(data.shape)
        num_point = 1000

        for i in range(num_point):
            max_index = np.where(data == np.max(data))
            X.append(max_index[0])
            Y.append(max_index[1])
            data[max_index[0],max_index[1]] = np.min(data)
        Z.append(z)

    ALL = list(zip(X, Y, Z * num_point))
    Txt_save(ALL,'all_part_t1_16k_16k_1000_new.txt')
    #np.savetxt('all_part_t1_16k_16k_1000.txt', ALL)
    hd5file.close()

def Txt_save(data,txtsavepath):

    np.savetxt(txtsavepath, data)

if __name__ == '__main__':
    hd5_path = r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/part_t1.hdf5'
    reshapesize = 16384
    #Single_sample(hd5_path,reshapesize)
    ALL_sample_1(hd5_path,reshapesize)