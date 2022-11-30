#-*-codeing = utf-8 -*-
#@Time : 2022/5/18 20:45
#@Author : LichunSun
#@File : Engineering_cluster.py


import sys
import os
sys.path.append(os.path.abspath("../.."))
import pandas as pd
import datetime
import glob
import cv2
import numpy as np
from astropy.io import fits
import h5py
import datetime
import matplotlib.pyplot as plt
from astropy.wcs import WCS
from copy import deepcopy
from sklearn.cluster import DBSCAN

#from MultiExposurePhotoPipline.base.base_port import PipelinePort
from SKA_pipeline.base.base_port import PipelinePort

class Cluster(PipelinePort):
    """docstring for StarSperate"""
    def __init__(self, file, **kwargs):
        super().__init__(file, **kwargs)
        self.file = file
        self.filelist = glob.glob(os.path.join(self.input_dir,"*.fits"))
        self.gleam_path = os.path.join(self.input_dir, self.file_name+".txt")
        try:
            self.r = kwargs['r']
            self.min_num = kwargs['min_num']
            self.num_point = kwargs['num_point']

        except Exception as e:
            raise e
    
    def open_mulfits(fitsfile):
        hdu = fits.open(fitsfile)
        img = hdu[0].data
        wcs = WCS(hdu[0].header)
        hdu.close()
        return img,wcs

    def cluster_DBSCAN(self,img,r,min_num,num_point):
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


    def Reg_ori_size(self,file,result):
        x = int(os.path.basename(file).split('_')[2])
        y = int(os.path.basename(file).split('_')[3].split('.fits')[0])
        result[:,0] = result[:,0]+ x
        result[:,1] = result[:,1] +y

        return result

    def _execute_function(self):

        starttime = datetime.datetime.now()
        print('start time:', datetime.datetime.now())

        all_xy = np.empty((1, 2))
        for file in self.filelist:
            print(file)
            img,wcs1k = self.load(file,file_format='fits')
            print('cluster',datetime.datetime.now())
            result = self.cluster_DBSCAN(img,self.r,self.min_num,self.num_point)

            if result.any():
                cluster_xy = np.unique(result[:,:2],axis=0)
                np.savetxt(self.output_dir + '/' + 'dbscan_random_{}_{}.txt'.format(os.path.basename(file).split(".fits")[0], self.num_point), result)
                reg_ori_xy = self.Reg_ori_size(file,cluster_xy)
                all_xy = np.vstack((reg_ori_xy, all_xy))

        #all_xy = np.delete(all_xy, -1, 0)
        np.savetxt(self.output_dir + '/' + 'all_cluster_pixel_wcs.txt', all_xy)

        #Plt_allcluster_pixel(all_xy,savepath,error)

        print('end time :', datetime.datetime.now())
        print('It“s running {}'.format(datetime.datetime.now()-starttime))
