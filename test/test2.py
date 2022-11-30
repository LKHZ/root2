import sys
sys.path.append('..')
import h5py
from astropy.io import fits 
from single_sample import hd5,save_wcsinfo,Create_newFits_wcs
import datetime
from astropy.wcs import WCS
from copy import deepcopy

def hd5cube_cubefits_wcs(inputdir,cubesize,savefitspath):
	h5_file = hd5.read(inputdir)
	key = [key for key in h5_file.keys()]
	print('读取前',datetime.datetime.now())
	bigcube = h5_file['{}'.format(key[0])][:]
	print('读取后', datetime.datetime.now())
	print(bigcube.shape)

	hdu = fits.open(r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/image_0.fits')[0]
	wcs = WCS(hdu.header)
	hdr0 = deepcopy(hdu.header)

	for row in range(0, bigcube.shape[1], cubesize):
		for column in range(0, bigcube.shape[1], cubesize):

			cube = bigcube[:,column :column+cubesize, row :row+cubesize]
			new_hdr = save_wcsinfo(hdr0, cubesize, wcs, row, column)
			Create_newFits_wcs(cube, savefitspath + '/' + 'image_{}_{}.fits'.format(row, column), new_hdr)
			print('image_{}_{}.fits save successful'.format(row, column))
			print(datetime.datetime.now)
			
	h5_file.close()

if __name__ == '__main__':

	starttime = datetime.datetime.now()
	print('start time:', datetime.datetime.now())

	inputdir = '/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/part1_t1.hdf5'
	savefitspath = r'/home/lab30201/sdd/slc/SKAData/Faster_mulchannel/datafits'
	cubesize = 1024

	hd5cube_cubefits_wcs(inputdir,cubesize,savefitspath)

	print('end time :', datetime.datetime.now())
	print('It“s running {}'.format(datetime.datetime.now() - starttime))

