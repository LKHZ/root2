#-*-codeing = utf-8 -*-
#@Time : 2022/5/18 20:45
#@Author : LichunSun
#@File : Engineering_cluster.py

import pandas as pd
import os
import cv2
import numpy as np
from astropy.io import fits
import h5py
import datetime
import matplotlib.pyplot as plt
from astropy.wcs import WCS
from copy import deepcopy
from sklearn.cluster import DBSCAN

def open_mulfits(fitsfile):
    hdu = fits.open(fitsfile)
    img = hdu[0].data
    wcs = WCS(hdu[0].header)
    hdu.close()
    return img,wcs

def cluster_DBSCAN(img,num_point):
    new = np.empty((1,3))
    for z in range(img.shape[0]):
        data = img[z, ::]
        sort = np.argsort(data.flatten(), kind='mergesort')
        samples = np.empty((num_point, 3))
        for i in range(1, num_point + 1):
            x = int(sort[-i] / img.shape[1])
            y = sort[-i] % (img.shape[1])
            samples[i - 1, 0] = y  # x与y互换
            samples[i - 1, 1] = x
            samples[i - 1, 2] = z

        clustering = DBSCAN(eps=r, min_samples=min_num).fit(samples[:,:2])
        sample_indices = clustering.core_sample_indices_
        single_sample = np.array([samples[sample_indice] for sample_indice in sample_indices])
        if single_sample.any():
            new = np.vstack((single_sample,new))
    new = np.delete(new,-1,0)
    return new

def Load_16kfits_wcs(fits16kpath):
    hdu16k = fits.open(fits16k)
    wcs16k = WCS(hdu16k[0].header)
    hdu16k.close()
    return wcs16k

def GLEAM(gleampath):
    gleam_path = gleampath
    df = pd.read_csv(gleam_path, header=1)
    postion = df[["# RA (deg)", " Dec (deg)"]]
    RAS = postion["# RA (deg)"]
    DECS = postion[" Dec (deg)"]
    return RAS,DECS

def Load_1kfits_wcs(fitsfile):
    hdu = fits.open(fitsfile)
    wcs = WCS(hdu[0].header)
    hdu.close()
    return wcs

def Matching(ras, decs, error):
    target_ra = []
    target_dec = []
    for i, ra in enumerate(ras):

        for I, RA in enumerate(RAS):
            if abs(ra - RA) <= error and abs(decs[i] - DECS[I]) <= error:
                # print('match',RAS[I],DECS[I])
                target_ra.append(RAS[I])
                target_dec.append(DECS[I])
    target_radec = list(zip(target_ra, target_dec))
    unique_target_radec = list(set(list(target_radec)))
    return unique_target_radec

def Plt_allcluster_pixel(all_cluster_xy,savepath,error):
    plt.style.use('classic')
    plt.figure(figsize=(20, 20))
    plt.scatter(all_cluster_xy[:, 0], all_cluster_xy[:, 1], s=50, c='#2e317c', label='error='.format(error))
    plt.xlim(-1024, 1024 * 18)
    plt.ylim(-1024, 1024 * 18)
    plt.grid()
    plt.legend(loc='best')
    plt.xticks(range(-1024, 18 * 1024, 1024))
    plt.yticks(range(-1024, 18 * 1024, 1024))
    plt.xlabel('ra (pixels)', fontsize=20)
    plt.ylabel('dec (pixels)', fontsize=20)
    plt.title('gleam/clsuter', fontsize=20)
    plt.savefig(savepath + '/' + 'all_cluster_pixel{}.png'.format(error))
    plt.close()

def Plt_single_pixel(x,y,savepath,file,error):
    plt.style.use('classic')
    plt.figure(figsize=(10, 10))
    plt.title(file.split(".fits")[0] + 'cluster' + '_' + 'error{}'.format(error))
    plt.scatter(x,y,label='error='.format(error))
    plt.xlim(0, 1024)
    plt.ylim(0, 1024)
    plt.grid()
    plt.legend(loc='best')
    plt.xticks(range(0, 1024, 128))
    plt.yticks(range(0, 1024, 128))
    plt.xlabel('x', fontsize=20)
    plt.ylabel('y', fontsize=20)
    plt.savefig(savepath + '/' + 'kdtree_{}_{}_{}.png'.format(file.split(".fits")[0],num_point,error))
    #plt.savefig('/home/lab30201/sdd/slc/SKAData/SKA_algorithm/cluster/xy0_5120.png')
    plt.close()

if __name__ == '__main__':

    starttime = datetime.datetime.now()
    print('start time:', datetime.datetime.now())

    inputdir = r'/home/lab30201/sdd/slc/SKAData/Faster_mulchannel/datafits1'
    gleampath = r"/home/lab30201/sdd/slc/SKAData/CIPdata/image/GLEAM_filtered.txt"
    fits16k = r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/image_0.fits'
    savepath = r'/home/lab30201/sdd/slc/SKAData/SKA_algorithm/cluster/test1'
    filelist = os.listdir(inputdir)
    filelist = [file for file in filelist if file.endswith('.fits')]

    r = 10
    min_num = 200
    num_point = 5000

    error = 5*(10**-3)
    wcs16k = Load_16kfits_wcs(fits16k)
    RAS,DECS = GLEAM(gleampath)
    all_xy = np.empty((1, 2))

    for file in filelist:
        print(file)
        img,wcs1k = open_mulfits(inputdir + '/' + file)
        '''
        numpoint ???????
        '''
        print('cluster',datetime.datetime.now())
        result = cluster_DBSCAN(img,num_point)

        if result.any():

            cluster_xy = result[:,:2]
            #np.savetxt(savepath + '/' + 'kdtree_{}_{}_{}.txt'.format(file.split(".fits")[0], num_point,error), result)
            #print('savetxt:',datetime.datetime.now())
            #Plt_single_pixel(cluster_xy[:,0],cluster_xy[:,1],savepath,file,error)
            #去掉重复点
            cluster_xy = np.array(list(set([tuple(uniquexy) for uniquexy in cluster_xy])))
            

            #wcs1k = Load_1kfits_wcs(inputdir + '/' + file)
            # print('load 1kwcs',datetime.datetime.now())
            cluster_pixel_wcs = wcs1k.sub(2).all_pix2world(cluster_xy, 0)
            ras = cluster_pixel_wcs[:, 0]
            decs = cluster_pixel_wcs[:, 1]

            match_radec = Matching(ras, decs, error)
            print('matching',datetime.datetime.now())
            match_xy = wcs16k.sub(2).all_world2pix(match_radec, 0)
            print(type(match_xy))
            if isinstance(match_xy, list):
                continue
            all_xy = np.vstack((match_xy, all_xy))
    all_xy = np.delete(all_xy, -1, 0)
    np.savetxt(savepath + '/' + 'all_cluster_pixel_wcs_{}.txt'.format(error), all_xy)

    Plt_allcluster_pixel(all_xy,savepath,error)

    print('end time :', datetime.datetime.now())
    print('It“s running {}'.format(datetime.datetime.now()-starttime))