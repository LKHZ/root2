#-*-codeing = utf-8 -*-
#@Time : 2022/4/29 16:04
#@Author : LichunSun
#@File : fits_hd5.py

import h5py
from astropy.io import fits
import numpy as np
import datetime
import os

def Sort_file(inputdir):
    filelist = os.listdir(inputdir)
    filelist = [file  for file in filelist if file.endswith('.fits') ]
    filelist.sort(key=lambda x: int(x[6:-5]))
    print(filelist)
    return filelist

def Fits_cube_hd5(inputdir,hd5filename,datasetname,outputdir,cubeshape):
    filelist = Sort_file(inputdir)
    h5_file = h5py.File(outputdir + '/' + hd5filename, 'w')
    t1_96channel = h5_file.create_dataset(datasetname, cubeshape, chunks=True)
    for channel,file in enumerate(filelist):
        file = inputdir +'/' + file
        print(file)
        img = fits.open(file)[0].data
        new_img = img.reshape(img.shape[2],img.shape[2])
        t1_96channel[channel,::] = new_img
        print(datetime.datetime.now())
    h5_file.close()

def Hd5cube_192(hd51_dir,hd52_dir,hd53_dir,hd55_dir,hd56_dir,hd57_dir,outputdir,hd5filename,datasetname,cubeshape):

    hd51_file = h5py.File(hd51_dir, 'r')
    hd51_key = [key for key in hd51_file.keys()]
    hd51 = hd51_file['{}'.format(hd51_key[0])][:]
    hd51_file.close()
    print('t1 read end ')

    hd52_file = h5py.File(hd52_dir, 'r')
    hd52_key = [key for key in hd52_file.keys()]
    hd52 = hd52_file['{}'.format(hd52_key[0])][:]
    hd52_file.close()
    print('t2 read end ')

    hd53_file = h5py.File(hd53_dir, 'r')
    hd53_key = [key for key in hd53_file.keys()]
    hd53 = hd53_file['{}'.format(hd53_key[0])][:]
    hd53_file.close()
    print('t3 read end ')

    hd55_file = h5py.File(hd55_dir, 'r')
    hd55_key = [key for key in hd55_file.keys()]
    hd55 = hd55_file['{}'.format(hd55_key[0])][:]
    hd55_file.close()
    print('t5 read end ')

    hd56_file = h5py.File(hd56_dir, 'r')
    hd56_key = [key for key in hd56_file.keys()]
    hd56 = hd56_file['{}'.format(hd56_key[0])][:]
    hd56_file.close()
    print('t6 read end ')

    hd57_file = h5py.File(hd57_dir, 'r')
    hd57_key = [key for key in hd57_file.keys()]
    hd57 = hd57_file['{}'.format(hd57_key[0])][:]
    hd57_file.close()
    print('t7 read end ')

    
    h5_file = h5py.File(outputdir + '/' + hd5filename, 'w')
    t1_t7channel = h5_file.create_dataset(datasetname, cubeshape, chunks=True)

    t1_t7channel[:96,::] = hd51
    print('t1 successful')
    t1_t7channel[96:96*2,::] = hd52
    print('t2 successful')
    t1_t7channel[96*2:96*3,::] = hd53
    print('t3 successful')
    t1_t7channel[96*3:96*4,::] = hd55
    print('t5 successful')
    t1_t7channel[96*4:96*5,::] = hd56
    print('t6 successful')
    t1_t7channel[96*5:,::] = hd57
    print('t7 successful')

    h5_file.close()
    

if __name__ == '__main__':

    starttime = datetime.datetime.now()
    print('初始时间：',starttime)
    for i in range(5,11):

    ##############################################################################################
        inputdir = r'/home/dell460/slc/sdd_01/SKAData/CIP_random2/data/10field/field{}/t5'.format(i)
        outputdir = r'/home/dell460/slc/sdd_01/SKAData/CIP_random2/data/10field/field{}'.format(i)
        cubeshape = (96, 2 ** 13, 2 ** 13)
        #hd5filename = 'part2_t7.hdf5'
        hd5filename = 'field{}.hdf5'.format(i)
        datasetname = 't5'
        Fits_cube_hd5(inputdir,hd5filename,datasetname,outputdir,cubeshape)
    #############################################################################################

    # cubeshape = (96*6, 2 ** 13, 2 ** 13)
    # hd51_dir = '/home/dell460/slc/sdd_01/SKAData/CIP_random/CIP_random/CIPdata/image/part1/t1/t1_random_.hdf5'
    # hd52_dir = '/home/dell460/slc/sdd_01/SKAData/CIP_random/CIP_random/CIPdata/image/part1/t2/t2_random_.hdf5'
    # hd53_dir = '/home/dell460/slc/sdd_01/SKAData/CIP_random/CIP_random/CIPdata/image/part1/t3/t3_random_.hdf5'

    # hd55_dir = '/home/dell460/slc/sdd_01/SKAData/CIP_random/CIP_random/CIPdata/image/part2/t5/t5_random_.hdf5'
    # hd56_dir = '/home/dell460/slc/sdd_01/SKAData/CIP_random/CIP_random/CIPdata/image/part2/t6/t6_random_.hdf5'
    # hd57_dir = '/home/dell460/slc/sdd_01/SKAData/CIP_random/CIP_random/CIPdata/image/part2/t7/t7_random_.hdf5'

    # outputdir = '/home/dell460/slc/sdd_01/SKAData/CIP_random/CIP_random/CIPdata/image'
    # hd5filename = 'CIPdata_t1_t7.hdf5'
    # datasetname = 'random_t1_t7'

    # Hd5cube_192(hd51_dir,hd52_dir,hd53_dir,hd55_dir,hd56_dir,hd57_dir,outputdir,hd5filename,datasetname,cubeshape)


    print('结束时间：',datetime.datetime.now())
    print('程序执行了：',datetime.datetime.now()-starttime)




