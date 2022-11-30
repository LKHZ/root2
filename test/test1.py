#-*-codeing = utf-8 -*-
#@Time : 2022/5/9 10:52
#@Author : LichunSun
#@File : test1.py


import numpy as np
import matplotlib.pyplot as plt
import os
import h5py
from astropy.io import fits
import datetime

if __name__ == '__main__':
    f = open(r"/home/lab30201/sdd/slc/SKAData/SKA_algorithm/test/text.txt",'w')
    hdu = fits.open('/home/lab30201/sdd/slc/SKAData/Faster_mulchannel/traindata300-300/image_0_0.fits')
    hdr = hdu[0].header
    data = hdu[0].data
    print(hdr,file=f)
    print(data.shape,file=f)
    f.close()
    # starttime = datetime.datetime.now()
    # print('初始时间：',starttime)
    # inputdir = '/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1'

    # filelist = os.listdir(inputdir)
    # filelist = [file  for file in filelist if file.endswith('.fits') ]
    # filelist.sort(key=lambda x: int(x[6:-5]))

    # h5_file = h5py.File(inputdir + '/' + 'part1_t1.hdf5','w')
    # t1_96channel = h5_file.create_dataset('t1_96channel',(96,2**14,2**14), chunks=True)
    # for channel,file in enumerate(filelist):
    #     file = inputdir +'/' + file
    #     print(file)
    #     img = fits.open(file)[0].data
    #     new_img = img.reshape(16384,16384)
    #     t1_96channel[channel,::] = new_img
    #     print(datetime.datetime.now())
    # h5_file.close()
    # print('结束时间：',datetime.datetime.now())
    # print('程序执行了：',datetime.datetime.now()-starttime)