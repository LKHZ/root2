from astropy.io import fits
from astropy.wcs import WCS
from copy import deepcopy
from astropy import units as u
from astropy.coordinates import SkyCoord
import matplotlib.pyplot as plt
import numpy as np


hdu = fits.open(r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/image_0.fits')[0]
data = hdu.data

wcs = WCS(hdu.header)
print(hdu.header)
print(wcs.sub(2))
#print(wcs.pixel_to_world(4096,4096))
phase_centre_world = wcs.sub(2).pixel_to_world_values(4096,4096) 
print(phase_centre_world[0])

seg_size = 1024

header0 = hdu.header
#print(header0['CRVAL1'],header0['CRVAL2'])
phase_centre_world_ra = header0['CRVAL1']
phase_centre_world_dec = header0['CRVAL2']
phase_centre_pixel_x = header0['CRPIX1']
phase_centre_pixel_y = header0['CRPIX2']
#print(phase_centre_world_ra)

for row in range(0,16384,1024):
    for column in range(0,16384,1024):

        #phase_centre_pixel_x = seg_size/2 + row
        header0['CRPIX1'] = seg_size/2 + row
        #phase_centre_pixel_y = seg_size/2 + column   
        header0['CRPIX2']  = seg_size/2 + column 
        phase_centre_world = wcs.sub(2).pixel_to_world_values(phase_centre_pixel_x,phase_centre_pixel_y)  
        #phase_centre_world_ra = phase_centre_world[0]
        header0['CRVAL1'] = phase_centre_world[0]
        #phase_centre_world_dec = phase_centre_world[1]
        header0['CRPIX2'] = phase_centre_world[1]

        newdata = data[column :column+seg_size, row :row+seg_size]


		hdu = fits.PrimaryHDU(newdata)
		hdu.header = header0
		hdul = fits.HDUList([hdu])

		hdul.writeto(savepath)