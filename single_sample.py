#-*-codeing = utf-8 -*-
#@Time : 2022/5/3 15:25
#@Author : LichunSun
#@File : single_sample.py

import os
import cv2
import numpy as np
from astropy.io import fits
import h5py
import datetime
import matplotlib.pyplot as plt
from ds9_similar import fits_jpg
from astropy.wcs import WCS
from copy import deepcopy

class hd5:
    def __init__(self):
        self.read = hd5.read()
        self.write_hd5 = hd5.write_hd5()
        self.close = hd5.close()

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

    def close(file):
        file.close()

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

    ALL = list(zip(X, Y, Z ))
    Txt_save(ALL,'all_part_t1_16k_16k_1000.txt')
    #np.savetxt('all_part_t1_16k_16k_1000.txt', ALL)
    hd5file.close()

def cube16k_4k(fitspath):
    data = fits.open(fitspath)[0].data
    data = data.reshape(reshapesize,reshapesize)
    print(data.shape)
    seg_size = 1024
    for row in range(0, reshapesize, seg_size):
        for column in range(0, reshapesize, seg_size):
            print(row,column)
            newdata = data[column :column+seg_size, row :row+seg_size]
            Create_newFits(newdata,savepath=r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cube_1k/1k_fits/image_{}_{}.fits'.format(row, column))

def ALL_sample_1(hd5_path, reshapesize):
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
    for z, channel in enumerate(channels):
        print(z, channel)
        data = hd5file['{}'.format(channel)][:]
        data = data.reshape(reshapesize, reshapesize)
        print(data.shape)
        # num_point = int(img.shape[1] / 3)
        num_point = 1000
        print('寻找最大点前:', datetime.datetime.now())
        sort = np.argsort(data.flatten())
        print('执行np.argsort:', datetime.datetime.now())
        for i in range(num_point):
            x = int(sort[-i] / data.shape[1])
            y = sort[-i] % (data.shape[1])
            X.append(x)
            Y.append(y)
            Z.append(z)
            with open('all_part_t1_16k_16k_1000.txt', mode="a") as f:
                Txt_save(list(zip(X, Y, Z)), 'all_part_t1_16k_16k_1000.txt')
        print('执行np.argsort-写文件:', datetime.datetime.now())


    #ALL = list(zip(X, Y, Z))
    #Txt_save(ALL, 'all_part_t1_16k_16k_1000.txt')
    # np.savetxt('all_part_t1_16k_16k_1000.txt', ALL)
    hd5file.close()

def ALL_sample_seg(hd5_path, reshapesize,seg_size):
    '''
    :param hd5_path:
    :param reshapesize:
    :return:
    '''

    hd5file = hd5.read(hd5_path)
    channel = hd5file.keys()
    channels = [key for key in channel]
    channels.sort(key=lambda x: int(x[8:]))

    for row in range(0, reshapesize, seg_size):
        for column in range(0, reshapesize, seg_size):

            X = []
            Y = []
            Z = []

            for z,channel in enumerate(channels):
                print(z,channel)
                print(datetime.datetime.now())
                data = hd5file['{}'.format(channel)][:]
                data = data.reshape(reshapesize, reshapesize)

                #print(data.shape)
                # num_point = int(img.shape[1] / 3)
                num_point = 1000
                newdata = data[column :column+seg_size, row :row+seg_size]

                sort = np.argsort(newdata.flatten(),kind='mergesort')
                # X = [int(sort[-i] / data.shape[1]) for i in range(1, num_point)]
                # Y = [sort[-i] % (data.shape[1]) for i in range(1, num_point)]
                # Z = [z] * len(X)
                for i in range(1, num_point+1):
                    x = int(sort[-i] / newdata.shape[1])
                    y = sort[-i] % (newdata.shape[1])
                    X.append(x)
                    Y.append(y)
                    Z.append(z)

            ALL = list(zip(X, Y, Z))
            Txt_save(txtsavepath + '/' + 'part_t1_4k_4k_{}_{}.txt'.format(row,column),ALL)
            print('part_t1_4k_4k_{}_{}.txt save successful'.format(row,column))
            print(datetime.datetime.now())
            #np.savetxt('all_part_t1_16k_16k_1000.txt', ALL)
    hd5file.close()

def final_sample(hd5_path, reshapesize,seg_size):
    '''
    :param hd5_path:
    :param reshapesize:
    :return:
    '''

    hd5file = hd5.read(hd5_path)
    channel = hd5file.keys()
    channels = [key for key in channel]
    channels.sort(key=lambda x: int(x[8:]))

    for row in range(0, reshapesize, seg_size):
        for column in range(0, reshapesize, seg_size):

            X = []
            Y = []
            Z = []

            for z,channel in enumerate(channels):
                print(z,channel)
                print(datetime.datetime.now())
                data = hd5file['{}'.format(channel)][:]
                data = data.reshape(reshapesize, reshapesize)

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

            ALL = list(zip(X, Y, Z))
            Txt_save(txtsavepath + '/' + 'part_t1_{}_{}_{}.txt'.format(seg_size,row,column),ALL)
            swap_ALL = list(zip(Y, X, Z))
            Txt_save(txtsavepath + '/' + 'swap_part_t1_{}_{}_{}.txt'.format(seg_size,row,column),swap_ALL)
            print('part_t1_{}_{}_{}.txt save successful'.format(seg_size,row,column))
            print(datetime.datetime.now())
            #np.savetxt('all_part_t1_16k_16k_1000.txt', ALL)
    hd5file.close()

def final_sample_2(hd5_path, reshapesize,seg_size):
    '''
    :param hd5_path:
    :param reshapesize:
    :return:
    '''

    # hd5file = hd5.read(hd5_path)
    # channel = hd5file.keys()
    # channels = [key for key in channel]
    # channels.sort(key=lambda x: int(x[8:]))

    for row in range(0, reshapesize, seg_size):
        for column in range(0, reshapesize, seg_size):

            X = []
            Y = []
            Z = []

            for channel in range(96):
                print(channel)
                hd5file = hd5.read(hd5_path)
                data = hd5file['channel_{}'.format(channel)][:]
                hd5file.close()

                print("channel is {}".format(channel))
                print(datetime.datetime.now())
                #data = hd5file['{}'.format(channel)][:]
                data = data.reshape(reshapesize, reshapesize)

                #num_point = 5000
                newdata = data[column :column+seg_size, row :row+seg_size]
                num_point = int(len(newdata.flatten())/3)
                sort = np.argsort(newdata.flatten(),kind='mergesort')
                for i in range(1, num_point):
                    x = int(sort[-i] / newdata.shape[1]) + row
                    y = sort[-i] % (newdata.shape[1]) + column
                    X.append(x)
                    Y.append(y)
                    Z.append(channel)

            ALL = list(zip(X, Y, Z))
            Txt_save(txtsavepath + '/' + 'part_t1_256_256_{}_{}.txt'.format(row,column),ALL)
            swap_ALL = list(zip(Y, X, Z))
            Txt_save(txtsavepath + '/' + 'swap_part_t1_256_256_{}_{}.txt'.format(row,column),swap_ALL)
            print('part_t1_1k_1k_{}_{}.txt save successful'.format(row,column))
            print(datetime.datetime.now())
            #np.savetxt('all_part_t1_16k_16k_1000.txt', ALL)
    #hd5file.close()

def Create_newFits(data,savepath):

    hdu = fits.PrimaryHDU(data)
    hdul = fits.HDUList([hdu])
    hdul.writeto(savepath)

def Create_newFits_wcs(data,savepath,header):

    hdu = fits.PrimaryHDU(data)
    hdu.header = header
    hdul = fits.HDUList([hdu])
    hdul.writeto(savepath)

def Txt_save(txtsavepath,data):

    np.savetxt(txtsavepath, data)

def hd5_mulchannel_fits(hd5_path,savefitspath,fits_channel):

    '''
    改channel 需要修改z
    '''
    seg_size = 1024
    mulchannel_data = np.empty((fits_channel,seg_size,seg_size))

    hd5file = hd5.read(hd5_path)
    channel = hd5file.keys()
    channels = [key for key in channel]
    channels.sort(key=lambda x: int(x[8:]))

    for row in range(0, reshapesize, seg_size):
        for column in range(0, reshapesize, seg_size):

            for z,channel in enumerate(channels):

                data = hd5file['{}'.format(channel)][:]
                data = data.reshape(reshapesize, reshapesize)
                newdata = data[column :column+seg_size, row :row+seg_size]
                mulchannel_data[z,::] = newdata
            Create_newFits(mulchannel_data,savefitspath + '/' +'image_{}_{}.fits'.format(row, column))
            print('image_{}_{}.fits save successful'.format(row, column))

    hd5file.close()

def hd5_mulchannel_fits_wcs(hd5_path,savefitspath,fits_channel):

    '''
    改channel 需要修改z
    '''
    seg_size = 1024
    mulchannel_data = np.empty((fits_channel,seg_size,seg_size))

    hd5file = hd5.read(hd5_path)
    channel = hd5file.keys()
    channels = [key for key in channel]
    channels.sort(key=lambda x: int(x[8:]))

    hdu = fits.open(r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/image_0.fits')[0]
    wcs = WCS(hdu.header)
    hdr0 = deepcopy(hdu.header)


    for row in range(4096, reshapesize, seg_size):
        for column in range(0, reshapesize, seg_size):


            for z,channel in enumerate(channels):

                data = hd5file['{}'.format(channel)][:]
                data = data.reshape(reshapesize, reshapesize)
                newdata = data[column :column+seg_size, row :row+seg_size]
                mulchannel_data[z,::] = newdata

            new_hdr = save_wcsinfo(hdr0,seg_size,wcs,row,column)
            Create_newFits_wcs(mulchannel_data,savefitspath + '/' +'image_{}_{}.fits'.format(row, column),new_hdr)
            print('image_{}_{}.fits save successful'.format(row, column))

    hd5file.close()

def save_wcsinfo(header,seg_size,wcs,row,column):

    header0 = header
    header0['NAXIS1'] = seg_size
    header0['NAXIS2'] = seg_size
    #pixel center
    header0['CRPIX1'] = seg_size/2          
    header0['CRPIX2'] = seg_size/2

    phase_centre_pixel_x = seg_size/2 + row
    phase_centre_pixel_y = seg_size/2 + column
    #wcs phase center
    phase_centre_world = wcs.sub(2).pixel_to_world_values(phase_centre_pixel_x, phase_centre_pixel_y)
    header0['CRVAL1'] = float(phase_centre_world[0])
    header0['CRVAL2'] = float(phase_centre_world[1])
    
    return header0

def hd5cube_cubefits_wcs(inputdir,cubesize,savefitspath):
    h5_file = hd5.read(inputdir)
    key = [key for key in h5_file.keys()]
    print('读取前',datetime.datetime.now())
    bigcube = h5_file['{}'.format(key[0])][:]
    print('读取后', datetime.datetime.now())
    print(bigcube.shape)

    field = 10
    hdu = fits.open('/home/dell460/slc/sdd_01/SKAData/CIP_random2/data/10field/field10/\
CIP_8K_skymodel_field_number_1059_170.0_-10.0_2.73_fov_2_73_nmoment3_cip.taylor.0.restored.fits')[0]
    wcs = WCS(hdu.header)
    hdr0 = deepcopy(hdu.header)

    for row in range(0, bigcube.shape[1], cubesize):
        for column in range(0, bigcube.shape[1], cubesize):

            cube = bigcube[:,column :column+cubesize, row :row+cubesize]
            new_hdr = save_wcsinfo(hdr0, cubesize, wcs, row, column)
            Create_newFits_wcs(cube, savefitspath + '/' + 'image_field{}_random_{}_{}.fits'.format(field,row, column), new_hdr)
            print('image_field{}_random_{}_{}.fits save successful'.format(field,row, column))
            print(datetime.datetime.now)


    h5_file.close()

def Bigfits_littlefits(fitspath,seg_size,savefitspath):
        hdu = fits.open(fitspath)
        hdr = hdu[0].header
        hdr0 = deepcopy(hdr)
        data = hdu[0].data
        print(data.shape)
        hdu.close()
        wcs = WCS(hdr)
        newdata = data.reshape(data.shape[2],data.shape[2])
        for row in range(0,newdata.shape[0],seg_size):
            for column in range(0,newdata.shape[0],seg_size):
                littlefits = newdata[column :column+seg_size, row :row+seg_size]
                new_hdr = save_wcsinfo(hdr0,seg_size,wcs,row,column)
                Create_newFits_wcs(littlefits,savefitspath + '/' + 'image_random_{}_{}.fits'.format(row, column), new_hdr)
                print('image_random_{}_{}.fits save successful'.format(row, column))
                print(datetime.datetime.now)

if __name__ == '__main__':

    starttime = datetime.datetime.now()
    print('start time:', datetime.datetime.now())

    hd5_path = r'/home/dell460/slc/sdd_01/SKAData/CIP_random2/data/10field/field10/field10.hdf5'
    txtsavepath = r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cluster/sample_256'
    fitspath = r'/home/lab30201/sdd/slc/SKAData/CIP_random/CIP_random/CIPdata/image/part1/t1/image_0.fits'
    savefitspath = r'/home/dell460/slc/sdd_01/SKAData/CIP_random2/data/all_seg_fits'
    reshapesize = 8192
    seg_size = 1024
    cubesize = 1024
    #Single_sample(hd5_path,reshapesize)
    #ALL_sample_seg(hd5_path,reshapesize,seg_size)
    #cube16k_4k(fitspath)
    #final_sample(hd5_path,reshapesize,seg_size)
    #hd5_mulchannel_fits(hd5_path,savefitspath,96)
    #hd5_mulchannel_fits_wcs(hd5_path,savefitspath,96)
    #fits_jpg(savefitspath)
    hd5cube_cubefits_wcs(hd5_path,cubesize,savefitspath)
    #Bigfits_littlefits(fitspath,seg_size,savefitspath)

    print('end time :', datetime.datetime.now())
    print('It“s running {}'.format(datetime.datetime.now()-starttime))