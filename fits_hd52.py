#-*-codeing = utf-8 -*-
#@Time : 2022/10/27 15：25
#@Author : LichunSun
#@File : fits_hd5.py

import h5py
from astropy.io import fits
import numpy as np
import datetime
import os


if __name__ == '__main__':

    starttime = datetime.datetime.now()
    print('初始时间：',starttime)
    filelist = ['image_' + str(x) + '.fits' for x in range(96)]
    prefix1 = "/share/liuxh/SKA_eor/CIP_random/CIPdata/image/part1"
    prefix2 = "/share/liuxh/SKA_eor/CIP_random/CIPdata/image/part2"
    part1 = ["t1","t2","t3"]
    part2 = ["t5","t6","t7"]
    outputpath = '/home/zhengyitian/slc'
    hd5filename = 't123567_random_.hdf5'
    datasetname = 't123567'
    cubeshape = (96*6, 2 ** 13, 2 ** 13)

    channel = 0

    h5_file = h5py.File(outputpath + '/' + hd5filename, 'w')
    t123567_576channel = h5_file.create_dataset(datasetname, cubeshape, chunks=True)
    for i in range(len(part1)):
        inputpath = prefix1 + '/'+ part1[i]
        for file in filelist:
            filename = inputpath + '/' + file
            print(filename)
            img = fits.open(filename)[0].data
            new_img = img.reshape(img.shape[2],img.shape[2])
            t123567_576channel[channel,::] = new_img
            channel+=1

    for i in range(len(part2)):
        inputpath = prefix2 + '/'+ part2[i]
        for file in filelist:
            filename = inputpath + '/' + file
            print(filename)
            img = fits.open(filename)[0].data
            new_img = img.reshape(img.shape[2],img.shape[2])
            t123567_576channel[channel,::] = new_img
            channel+=1
    h5_file.close()

    print('结束时间：',datetime.datetime.now())
    print('程序执行了：',datetime.datetime.now()-starttime)
      