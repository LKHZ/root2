#-*-codeing = utf-8 -*-
#@Time : 2022/5/12 11:15
#@Author : LichunSun
#@File : kdtree2.py

from sklearn.cluster import DBSCAN
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import os


if __name__ == '__main__':

    r = 10
    min_num = 200
    
    inputdir = '/home/lab30201/sdd/slc/SKAData/Faster_mulchannel/datafits1'
    filelist = os.listdir(inputdir)

    for file in filelist:

        #hdu = fits.open(r"E:\A_Postgraduate\temp_ska\image_0_3072.fits")
        hdu = fits.open(inputdir + '/' + file)
        img = hdu[0].data
        num_point = 5000
        new = []
        len_point = []

        for z in range(img.shape[0]):
            data = img[z,::]
            sort = np.argsort(data.flatten(), kind='mergesort')
            samples = np.empty((num_point,3))
            for i in range(1, num_point + 1):
                x = int(sort[-i] / img.shape[1])
                y = sort[-i] % (img.shape[1])
                samples[i-1,0] = y              #x与y互换
                samples[i-1,1] = x
                samples[i-1,2] = z

            clustering = DBSCAN(eps=r, min_samples=min_num).fit(samples[:,:2])
            sample_indices = clustering.core_sample_indices_

            for num,sample_indice in enumerate(sample_indices):
                new.append(samples[sample_indice])

        print(len(new))
        len_point.append(new)
        #np.savetxt(r'E:\A_Postgraduate\temp_ska\1k_kdtree\kdtree_new_0_3072_{}.txt'.format(num_point),new)
        np.savetxt(r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cluster/1k_kdtree/kdtree_{}_{}.txt'.format(file.split(".fits")[0],num_point),new)
        hdu.close()


