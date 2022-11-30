#-*-codeing = utf-8 -*-
#@Time : 2022/5/2 16:24
#@Author : LichunSun
#@File : test_jpg.py

import matplotlib.pyplot as plt
from astropy.io import fits
import os 
import numpy as np
import cv2
from single_sample import hd5
from astropy.wcs import WCS
from PIL import Image
# img = fits.open(r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/image_95.fits')[0].data
# img = img.reshape(16384,16384)

# plt.figure(figsize=(200,200))
# plt.imshow(img,cmap='gray')
# plt.savefig(r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/testimg1.jpg')
# plt.show()

def test1():
	label = np.loadtxt(r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cube_1k/1k_label/iamge_0_7168_10240.list')
	if len(label):
		print('true')
	else:
		print('false')

def bbox(img,label,savepath,box_halfweigh):
    for i in range(label.shape[0]):
        for j in range(label.shape[1]):
            if j ==0:
                x_left_top = int(label[i,j]-box_halfweigh)
                x_right_bottom = int(label[i,j] + box_halfweigh)
            if j == 1:
                y_left_top = int(label[i,j] + box_halfweigh)
                y_right_bottom = int(label[i,j] - box_halfweigh)

        cv2.rectangle(img,(x_left_top,y_left_top),(x_right_bottom,y_right_bottom),(0,255,0),2)
    cv2.imwrite(savepath, img)

def bbox1(img,label,savepath,box_halfweigh):
    for i in range(label.shape[0]):
        for j in range(label.shape[1]):
            if j ==0:
                x_left_top = int(label[i,j]-box_halfweigh)
                x_right_bottom = int(label[i,j] + box_halfweigh)
            if j == 1:
                y_left_top = int(label[i,j] + box_halfweigh)
                y_right_bottom = int(label[i,j] - box_halfweigh)

        cv2.rectangle(img,(x_left_top,y_left_top),(x_right_bottom,y_right_bottom),(0,255,0),2)
    cv2.imwrite(savepath, img)

def test2():

    hd5_path = r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/part_t1.hdf5'
    hd5file = hd5.read(hd5_path)
    data = hd5file['channel_0'][:]
    data = data.reshape(16384,16384)
    data = data[:1024*4,:1024*4]
    max_index = np.where(data == np.max(data))
    print(max_index)

def test3():

    hd5_path = r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/part_t1.hdf5'
    hd5file = hd5.read(hd5_path)
    data = hd5file['channel_0'][:]
    data = data.reshape(16384,16384)
    data = data[:1024*4,:1024*4]

    data = trans90(data)

    num_point = 5000
    X = []
    Y = []
    print(num_point)
    sort = np.argsort(data.flatten())
    for i in range(1, num_point):
        x = int(sort[-i] / data.shape[1])
        y = sort[-i] % (data.shape[1])
        X.append(x)
        Y.append(y)
    ALL = list(zip(X, Y))
    np.savetxt(r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cube_4k/4k_label/trans_part_t1_4k_4k_5000.txt',ALL)
    hd5file.close()

def test4():

    #cv2.imwrite(r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cube_4k/4k_jpg/cv2iamge_00_0_0.jpg',img)
    #max_index = np.where(img == np.max(img))
    #print(max_index)
    #print('cv2 max_index value:{}'.format(img[3652,1626]))
    
    fitsimg = fits.open(r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/image_0.fits')[0].data
    print(fitsimg.shape)
    print('FITS 大图里面的的最大值:{}'.format(fitsimg[:,:,3652,1626]))
    fitsimg = fitsimg.reshape(16384,16384)
    fitsimg = fitsimg[:1024*4,:1024*4]
    max_index_fits = np.where(fitsimg == np.max(fitsimg))
    print(max_index_fits)
    print('FITS 小图4k里面的的最大值:{}'.format(fitsimg[3652,1626]))

def trans90(matrix):
    matrix = matrix[::-1]   #先反转
    rows,cols = len(matrix),len(matrix[0])
    for i in range(rows):   #做转置，对角线不交换，把右上三角换到左下三角
        for j in range(i,cols):   #注意从i开始，不要换了又把左下三角换回去了
            if i==j:
                continue
            else:
                matrix[i][j],matrix[j][i]=matrix[j][i],matrix[i][j]
    return matrix
def Create_newFits_wcs(data,savepath,header):

    hdu = fits.PrimaryHDU(data)
    hdu.header = header
    hdul = fits.HDUList([hdu])
    hdul.writeto(savepath)

def test5():
    path = '/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1'
    filelist = os.listdir(path)
    fitslist = [file for file in filelist if file.endswith('.fits')]
    fitslist = [file for file in fitslist if file.split('_')[2]=='t1']
    #print(fitslist[1][-15:-14])
    print(fitslist)
    hdr = fits.open(path + '/'+ fitslist[0])
    header = hdr[0].header
    hdr.close()
    print(header)
    newdata = np.empty((3,16*1024,16*1024))
    fitslist.sort(key=lambda x: int(x[-15:-14]))
    for i,file in enumerate(fitslist):
        hdu = fits.open(path + '/' + file)
        data = hdu[0].data
        print(data.shape)
        data = data.reshape(16*1024,16*1024)
        print(data.shape)
        newdata[i,:,:] = data
        hdu.close()
    Create_newFits_wcs(newdata,'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/taylor_t1.fits',header)
    # path = '/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1'
    # t10 = fits.open(path + '/' + '/CIP_16K_t1_baseline_realistic_dipole_element_beams_gleam_96_200k_72_0-91_0_fov_5_5_nmoment3_cip.taylor.0.restored.fits')
    # t11 = fits.open(path + '/' + '/CIP_16K_t1_baseline_realistic_dipole_element_beams_gleam_96_200k_72_0-91_0_fov_5_5_nmoment3_cip.taylor.1.restored.fits')
    # t12 = fits.open(path + '/' + '/CIP_16K_t1_baseline_realistic_dipole_element_beams_gleam_96_200k_72_0-91_0_fov_5_5_nmoment3_cip.taylor.2.restored.fits')
    # hdr = t10[0].header
    # print(t10[0].data.shape)
    # print(hdr)


def save_wcsinfo(header, seg_size, wcs, row, column):
    header0 = header
    header0['NAXIS1'] = seg_size
    header0['NAXIS2'] = seg_size
    # pixel center
    header0['CRPIX1'] = seg_size / 2
    header0['CRPIX2'] = seg_size / 2

    phase_centre_pixel_x = seg_size / 2 + row
    phase_centre_pixel_y = seg_size / 2 + column
    # wcs phase center
    phase_centre_world = wcs.sub(2).pixel_to_world_values(phase_centre_pixel_x, phase_centre_pixel_y)
    header0['CRVAL1'] = float(phase_centre_world[0])
    header0['CRVAL2'] = float(phase_centre_world[1])

    return header0
def test6():
    hdu = fits.open('/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/taylor_t1.fits')
    savefitspath = '/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/taylor_t1'
    data = hdu[0].data
    hdr = hdu[0].header
    wcs = WCS(hdr)
    print(data.shape)
    seg_size = 1024
    hdu.close()
    for row in range(0, data.shape[1], seg_size):
        for column in range(0, data.shape[1], seg_size):
            cube = data[:,column :column+seg_size, row :row+seg_size]
            new_hdr = save_wcsinfo(hdr, seg_size, wcs, row, column)
            Create_newFits_wcs(cube, savefitspath + '/' + 'image_{}_{}.fits'.format(row, column), new_hdr)
            print('image_{}_{}.fits save successful'.format(row, column))

def test7():
    hdu = fits.open('/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/CIP_16K_t1_baseline_realistic_dipole_element_beams_gleam_96_200k_72_0-91_0_fov_5_5_nmoment3_cip.taylor.2.restored.fits')
    data = (hdu[0].data).reshape(16384,16384)
    hdr = hdu[0].header
    hdu.close()
    Create_newFits_wcs(data[:1024,:1024],'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t12_00.fits',hdr)

def Plot_highmean(labelpath,jpgpath,savepath):
    all =[]
    filelist = os.listdir(labelpath)
    point_size = 10
    point_color = (0, 0, 255)
    for file in filelist:
        label = np.loadtxt(labelpath + '/' + file)
        img =cv2.imread(jpgpath + '/' + file.split('.list')[0] + '.png')
        for i in range(label.shape[0]):
            if label[i, 3] > label[:, 3].mean():
                all.append(label[i,3])

                #img = cv2.circle(img, (int(label[i, 1]), int(abs(label[i, 2] - 1024))), radius=10,
                                 #color=point_color)
        #cv2.imwrite(savepath + '/' + "highmean_{}_circl.png".format(file.split('.list')[0]), img)
    print(all)
    print(len(all))
def main():
    #img = r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cube_4k/4k_jpg/iamge_00_0_0.jpg'
    # img = cv2.imread(r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cube_4k/4k_jpg/iamge_00_0_0.jpg')
    # # img = cv2.transpose(img)
    # # img = cv2.flip(img, 1)
    # #label = np.loadtxt(r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/SKA_sample/4k/part_t1_4k_4k_0_0.txt')
    # label = np.loadtxt(r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cube_4k/4k_label/trans_part_t1_4k_4k_5000.txt')
    # label = label[:,:2]
    # #savepath = r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cube_4k/4k_jpg/iamge_00_0_0_box.png'
    # savepath = r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cube_4k/4k_jpg/pixel_iamge_00_0_0_box5000.png'
    # box_halfweigh = 0.1
    labelpath = '/home/lab30201/sdd/slc/SKAData/CIP_random/CIP_random/CIPdata/image/part1/t1/label'
    jpgpath = '/home/lab30201/sdd/slc/SKAData/CIP_random/CIP_random/CIPdata/image/part1/t1/1k_single'
    savepath = '/home/lab30201/sdd/slc/SKAData/CIP_random/CIP_random/CIPdata/image/part1/t1/high_i_mean'
    Plot_highmean(labelpath,jpgpath,savepath)
    #bbox(img,label,savepath,box_halfweigh)

if __name__ == '__main__':
    main()