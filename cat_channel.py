# -*-codeing = utf-8 -*-
# @Time : 2022/9/16 16:02
# @Author : LichunSun
# @File : test.py

from astropy.io import fits
import os
import numpy as np

def Create_newFits(data,savepath):

    hdu = fits.PrimaryHDU(data)
    hdul = fits.HDUList([hdu])
    hdul.writeto(savepath)

def Normalization(img):
    return (img - img.min()) / (img.max() - img.min())

def cat_data_channel(input,final_channel,savepath):
    hdu = fits.open(input)
    filename = os.path.basename(input)
    img = hdu[0].data
    img_channel = img.shape[0]
    # 对每一个通道进行归一化（每个通道的最大最小值不一样）
    for channel in range(img_channel):
        img[channel,::] = Normalization(img[channel,::])

    cat_channel = int(img_channel/final_channel)
    tmp_data = np.zeros((final_channel,img.shape[1],img.shape[2]))
    for i in range(final_channel):
        tmp_data[i,::] = sum(img[i*cat_channel:(i+1)*cat_channel,::])

    Create_newFits(tmp_data,savepath + '/' + filename)
    hdu.close()

if __name__ == '__main__':

    final_channel = 8
    inputpath = '/home/dell460/slc/sdd_01/Faster_mul/traindata300-300'
    filelist = os.listdir(inputpath)
    filelist = [ file for file in filelist if file.endswith('.fits')]
    savepath = '/home/dell460/slc/CircleNet/data/monuseg/train'
    # inputpath = '/home/dell460/slc/sdd_01/Faster_mul/testdata300-300/image_random_5120_0.fits'
    # savepath  = '/home/dell460/slc/sdd_01/Faster_mul'
    for file in filelist:
        cat_data_channel(inputpath + '/' + file, final_channel, savepath)
        #cat_data_channel(inputpath,final_channel,savepath)