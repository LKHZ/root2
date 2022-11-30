#-*-codeing = utf-8 -*-
#@Time : 2022/5/16 20:51
#@Author : LichunSun
#@File : cluster_match_wcs.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.wcs import WCS
import os

def GLEAM(gleampath):
    gleam_path = gleampath
    df = pd.read_csv(gleam_path, header=1)
    postion = df[["# RA (deg)", " Dec (deg)"]]
    RAS = postion["# RA (deg)"]
    DECS = postion[" Dec (deg)"]
    return RAS,DECS

def Load_clustertxt(txtpath):
    sample = np.loadtxt(txtpath,encoding='utf-8')
    xy = sample[:, :2]
    cluster_xy = np.array(list(set([tuple(t) for t in xy])))
    return cluster_xy


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

def Save_plt(match,error,file):
    plt.style.use('classic')
    plt.figure(figsize=(10.24, 10.24))
    plt.xlim(0, 1024)
    plt.ylim(0, 1024)
    xa = []
    ya = []
    fina = []
    for i in range(len(match)):
        xy = wcs.sub(2).world_to_pixel_values(match[i][0], match[i][1])
        print(xy[0], xy[1])
        xa.append(xy[0])
        ya.append(xy[1])
    #     if 0 < xy[0] < 1024 and 0 < xy[1] < 1024:
    #         fina.append(match[i])
    # print(fina)
    plt.scatter(xa, ya, label="error={}".format(error))
    plt.legend(loc='best')
    plt.title('cluster_pixel_wcs_match_{}'.format(file.split(".txt")[0]))
    plt.savefig(clustertxt + '/' + '{}.png'.format(file.split(".txt")[0]))
    plt.close()
    #plt.show()
    return xy

def Match_fitswcs_load(fitsfile):
    hdu = fits.open(fitsfile)
    wcs = WCS(hdu[0].header)
    hdu.close()
    return wcs

def Load_16kfits_wcs(fits16kpath):
    hdu16k = fits.open(fits16k)
    wcs16k = WCS(hdu16k[0].header)
    hdu16k.close()
    return wcs16k


def Plt_contrac(x,y,error):
    label_xy = np.loadtxt('/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cluster/label_GLEAM_pixel.txt')
    plt.style.use('classic')
    plt.figure(figsize=(20,20))
    plt.scatter(label_xy[:,0],label_xy[:,1],s=80,c='#2c9678',label='gleam')
    plt.scatter(x,y,s=80,c='red',label='error={}'.format(error),marker='x')
    plt.xlim(-1024,1024*18)
    plt.ylim(-1024,1024*18)
    plt.grid()    
    plt.legend(loc='upper center')
    plt.xticks(range(-1024,18*1024,1024))
    plt.yticks(range(-1024,18*1024,1024))
    plt.xlabel('ra (pixels)',fontsize=20)
    plt.ylabel('dec (pixels)',fontsize=20)
    plt.title('gleam/clsuter',fontsize=20)
    plt.savefig('/home/lab30201/sdd/slc/SKAData/SKA_algorithm/cluster/cluster_{}.png'.format(error))
    plt.close()

if __name__ == '__main__':

    # hdu = fits.open(r"E:\A_Postgraduate\temp_ska\image_0_0.fits")
    # wcs = WCS(hdu[0].header)
    #gleampath = r"E:\A_Postgraduate\temp_ska\GLEAM_filtered.txt"
    #clustertxt = r'E:\A_Postgraduate\temp_ska\sample_1k_kdtree'
    gleampath = r"/home/lab30201/sdd/slc/SKAData/CIPdata/image/GLEAM_filtered.txt"
    clustertxt = r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cluster/1k_kdtree'
    fitspath = r'/home/lab30201/sdd/slc/SKAData/Faster_mulchannel/datafits'
    fits16k = r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/image_0.fits'
    hdu16k = fits.open(fits16k)
    wcs16k = WCS(hdu16k[0].header)
    hdu16k.close()

    RAS,DECS = GLEAM(gleampath)
    error = 4*(10**-3)
    txtfilelist = os.listdir(clustertxt)
    txtfilelist = [txt for txt in txtfilelist if txt.endswith('.txt')]
    all_xy = np.empty((1,2))

    for file in txtfilelist:
        print(file)

        txtpath = clustertxt + '/' + file
        if not os.path.getsize(txtpath):
            continue

        fitsfile = fitspath + '/' + 'image_{}_{}.fits'.format(file.split("_")[2],file.split("_")[3])
        wcs = Match_fitswcs_load(fitsfile)
        cluster_xy = Load_clustertxt(txtpath)
        
        cluster_pixel_wcs = wcs.sub(2).all_pix2world(cluster_xy, 0)
        ras = cluster_pixel_wcs[:, 0]
        decs = cluster_pixel_wcs[:, 1]

        match = Matching(ras, decs, error)
        #print(match)
        match_xy = wcs16k.sub(2).all_world2pix(match,0)
        # print('当前',match_xy)
        # print(type(match_xy))
        if isinstance(match_xy,list):
        #         print('ssssssss')
            continue
        all_xy = np.vstack((match_xy,all_xy))
    all_xy = np.delete(all_xy,-1,0)
        #pixelxy = Save_plt(match,error,file)
        #all_xy.append(pixelxy)
    np.savetxt('/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cluster/cluster_pixel_wcs_0.004.txt',all_xy)
    Plt_contrac(all_xy[:,0],all_xy[:,1],error)


