 #!/usr/bin/env python

import numpy
import numpy as np
import scipy
import img_scale
from scipy import misc
from astropy.io import fits
import glob
import os
import imageio


def bytescale(data, cmin=None, cmax=None, high=255, low=0):
    """
    Byte scales an array (image).

    Byte scaling means converting the input image to uint8 dtype and scaling
    the range to ``(low, high)`` (default 0-255).
    If the input image already has dtype uint8, no scaling is done.

    Parameters
         
    data : ndarray
        PIL image data array.
    cmin : scalar, optional
        Bias scaling of small values. Default is ``data.min()``.
    cmax : scalar, optional
        Bias scaling of large values. Default is ``data.max()``.
    high : scalar, optional
        Scale max value to `high`.  Default is 255.
    low : scalar, optional
        Scale min value to `low`.  Default is 0.

    Returns
       -
    img_array : uint8 ndarray
        The byte-scaled array.

    Examples
    #
    # >>> img = array([[ 91.06794177,   3.39058326,  84.4221549 ],
    #                  [ 73.88003259,  80.91433048,   4.88878881],
    #                  [ 51.53875334,  34.45808177,  27.5873488 ]])
    # >>> bytescale(img)
    # array([[255,   0, 236],
    #        [205, 225,   4],
    #        [140,  90,  70]], dtype=uint8)
    # >>> bytescale(img, high=200, low=100)
    # array([[200, 100, 192],
    #        [180, 188, 102],
    #        [155, 135, 128]], dtype=uint8)
    # >>> bytescale(img, cmin=0, cmax=255)
    # array([[91,  3, 84],
    #        [74, 81,  5],
    #        [52, 34, 28]], dtype=uint8)

    """
    if data.dtype == np.uint8:
        return data

    if high < low:
        raise ValueError("`high` should be larger than `low`.")

    if cmin is None:
        cmin = data.min()
    if cmax is None:
        cmax = data.max()

    cscale = cmax - cmin
    if cscale < 0:
        raise ValueError("`cmax` should be larger than `cmin`.")
    elif cscale == 0:
        cscale = 1

    scale = float(high - low) / cscale
    bytedata = (data * 1.0 - cmin) * scale + 0.4999
    bytedata[bytedata > high] = high
    bytedata[bytedata < 0] = 0
    return np.cast[np.uint8](bytedata) + np.cast[np.uint8](low)



# path = r'F:\VMwaresharefiel\yangwang_result\V_1s_wcs\astrometry_result_all\fits_list_jpg\small_fits_list'
#path = r'F:\VMwaresharefiel\PreprocessResult'
#path = r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cube_1k/1k_fits'
def fits_jpg(fitspath):

    path = fitspath
    path_fits_list = glob.glob(os.path.join(path, "*.fits"))


    for fits_path in path_fits_list:
        # Parameters
        # red_fn = green_fn = blue_fn = r"C:\Users\sun\Desktop\label_data\test" + str(i) + ".fits"
        red_fn = green_fn = blue_fn = fits_path
        # red_fn = green_fn = blue_fn = r"C:\Users\sun\Desktop\a_label\Cluster_" + str(i) + ".fits"
        sig_fract = 5.0
        per_fract = 5.0-2
        max_iter = 20
        sub_size_fract = 0.3
        min_val = 0.0
        red_factor = 1.0
        green_factor = 1.0
        blue_factor = 1.0
        red_non_linear_fact = 0.005
        green_non_linear_fact = 0.005
        blue_non_linear_fact = 0.005


        # Read red image
        hdulist = fits.open(red_fn)
        img_header = hdulist[0].header
        #img_data = hdulist[0].data[0, :, :]
        img_data = hdulist[0].data
        print("aaa", img_data.shape)
        hdulist.close()
        img_data_r = numpy.array(img_data, dtype=float)
    #    img_data_r = np.transpose(img_data_r, (1, 2, 0))
        img_data_r = np.flip(img_data_r,0)
        width=img_data_r.shape[0]
        height=img_data_r.shape[1]
        print ("Red file = ", red_fn, "(", width, ",", height, ")")

        # jpg = numpy.empty((width, height, 3), numpy.uint8)
        # jpg = np.transpose(img_data, (1,2,0))
        # scipy.misc.imsave('test' + str(i) + '.png', jpg)

        #sky = numpy.median(numpy.ravel(img_data_r))
        #sky = numpy.mean(numpy.ravel(img_data_r))
        #sky, num_iter = img_scale.sky_median_sig_clip(img_data_r, sig_fract, per_fract, max_iter)
        #print "sky = ", sky, "(", num_iter, ") for red image \
        #(", numpy.max(img_data_r), ",", numpy.min(img_data_r), ")"
        #img_data_r = img_data_r - sky
        ##### find sub-samples for zscale
        # flat_img_data_r = numpy.ravel(img_data_r)
        # size_r = width * height
        # sub_img_ind = numpy.random.randint(0, size_r, size=int(sub_size_fract*size_r))
        # sub_img_ind = numpy.unique(sub_img_ind)
        # sub_img_data_r = flat_img_data_r[sub_img_ind]
        # print ("size of the sample image = ", len(sub_img_data_r))
        # min_r, max_r, num_iter = img_scale.range_from_zscale(sub_img_data_r)
        # min_r, max_r, num_iter = img_scale.range_from_zscale(img_data_r,contrast = 0.2, sig_fract = 2, percent_fract = 0.01, max_iter=1, low_cut=True, high_cut=True)
        # print ("zscale = ", min_r, max_r, " (", num_iter, ")")


        # Read green image
        hdulist = fits.open(green_fn)
        img_header = hdulist[0].header
        #img_data = hdulist[0].data[0, :, :]
        img_data = hdulist[0].data
        hdulist.close()
        img_data_g = numpy.array(img_data, dtype=float)
    #    img_data_g = np.transpose(img_data_g, (1, 2, 0))
        img_data_g = np.flip(img_data_g,0)
        width=img_data_g.shape[0]
        height=img_data_g.shape[1]
        print ("Green file = ", green_fn, "(", width, ",", height, ")")

        #sky = numpy.median(numpy.ravel(img_data_g))
        #sky = numpy.mean(numpy.ravel(img_data_g))
        #sky, num_iter = img_scale.sky_median_sig_clip(img_data_g, sig_fract, per_fract, max_iter)
        #print "sky = ", sky, "(", num_iter, ") for green image \
        #(", numpy.max(img_data_g), ",", numpy.min(img_data_g), ")"
        #img_data_g = img_data_g - sky
        ##### find sub-samples for zscale
        # flat_img_data_g = numpy.ravel(img_data_g)
        # size_g = width * height
        # sub_img_ind = numpy.random.randint(0, size_g, size=int(sub_size_fract*size_g))
        # sub_img_ind = numpy.unique(sub_img_ind)
        # sub_img_data_g = flat_img_data_g[sub_img_ind]
        # print ("size of the sample image = ", len(sub_img_data_g))
        # min_g, max_g, num_iter = img_scale.range_from_zscale(sub_img_data_g)

        # min_g, max_g, num_iter = img_scale.range_from_zscale(img_data_g)
        # print ("zscale = ", min_g, max_g, " (", num_iter, ")")


        # Read blue image
        hdulist = fits.open(blue_fn)
        img_header = hdulist[0].header
        #img_data = hdulist[0].data[0, :, :]
        img_data = hdulist[0].data
        hdulist.close()
        img_data_b = numpy.array(img_data, dtype=float)
     #   img_data_b = np.transpose(img_data_b, (1, 2, 0))
        img_data_b = np.flip(img_data_b,0)
        width=img_data_b.shape[0]
        height=img_data_b.shape[1]
        print ("Blue file = ", blue_fn, "(", width, ",", height, ")")

        #sky = numpy.median(numpy.ravel(img_data_b))
        #sky = numpy.mean(numpy.ravel(img_data_b))
        #sky, num_iter = img_scale.sky_median_sig_clip(img_data_b, sig_fract, per_fract, max_iter)
        #print "sky = ", sky, "(", num_iter, ") for blue image \
        #(", numpy.max(img_data_b), ",", numpy.min(img_data_b), ")"
        #img_data_b = img_data_b - sky
        ##### find sub-samples for zscale
        # flat_img_data_b = numpy.ravel(img_data_b)
        # size_b = width * height
        # sub_img_ind = numpy.random.randint(0, size_b, size=int(sub_size_fract*size_b))
        # sub_img_ind = numpy.unique(sub_img_ind)
        # sub_img_data_b = flat_img_data_b[sub_img_ind]
        # print ("size of the sample image = ", len(sub_img_data_b))
        # min_b, max_b, num_iter = img_scale.range_from_zscale(sub_img_data_b)

        # min_b, max_b, num_iter = img_scale.range_from_zscale(img_data_b)
        # print ("zscale = ", min_b, max_b, " (", num_iter, ")")


        # Apply scaling relations
        # r = red_factor * img_scale.asinh(img_data_r, scale_min = min_r, scale_max = max_r, non_linear=red_non_linear_fact)
        # g = green_factor * img_scale.asinh(img_data_g, scale_min = min_g, scale_max = max_g, non_linear=green_non_linear_fact)
        # b = blue_factor * img_scale.asinh(img_data_b, scale_min = min_b, scale_max = max_b, non_linear=blue_non_linear_fact)

        # 这是ds9的linear-zscale的效果
        min_r, max_r, num_iter = img_scale.range_from_zscale(img_data_r, contrast=0.165, sig_fract=3.0, percent_fract=0.01,
                                                             max_iter=100, low_cut=True, high_cut=True)
        min_g, max_g, num_iter = img_scale.range_from_zscale(img_data_g, contrast=0.165, sig_fract=3.0, percent_fract=0.01,
                                                             max_iter=100, low_cut=True, high_cut=True)
        min_b, max_b, num_iter = img_scale.range_from_zscale(img_data_b, contrast=0.165, sig_fract=3.0, percent_fract=0.01,
                                                             max_iter=100, low_cut=True, high_cut=True)
        r = red_factor * img_scale.power(img_data_r, power_index=1,scale_min = min_r, scale_max = max_r)
        g = green_factor * img_scale.power(img_data_g, power_index=1,scale_min = min_g, scale_max = max_g)
        b = blue_factor * img_scale.power(img_data_b, power_index=1,scale_min = min_b, scale_max = max_b)


        # # 这类似ds9的log-minmax的效果
        # r = red_factor * img_scale.histeq(img_data_r,)
        # g = red_factor * img_scale.histeq(img_data_g,)
        # b = red_factor * img_scale.histeq(img_data_b,)


        # 这类似于histogram-mimax效果
        # min_r, max_r, num_iter = img_scale.range_from_zscale(img_data_r, contrast=0.2, sig_fract=2, percent_fract=0.01,
        #                                                      max_iter=1, low_cut=True, high_cut=True)
        # r = red_factor * img_scale.power(img_data_r, power_index=6.7,scale_min = min_r, scale_max = max_r)
        #
        # min_g, max_g, num_iter = img_scale.range_from_zscale(img_data_g, contrast=0.2, sig_fract=2, percent_fract=0.01,
        #                                                      max_iter=1, low_cut=True, high_cut=True)
        # g = green_factor * img_scale.power(img_data_g, power_index=6.7,scale_min = min_g, scale_max = max_g)
        #
        # min_b, max_b, num_iter = img_scale.range_from_zscale(img_data_b, contrast=0.2, sig_fract=2, percent_fract=0.01,
        #                                                      max_iter=1, low_cut=True, high_cut=True)
        # b = blue_factor * img_scale.power(img_data_b, power_index=6.7,scale_min = min_b, scale_max = max_b)

        # RGB image with SciPy
        print ("image size ", width, height )
        rgba_array = numpy.empty((width,height,3), numpy.uint8) # assuming 8 bits per channnel
        rgba_array[:,:,0] = bytescale(r) # red
        rgba_array[:,:,1] = bytescale(g) # green
        rgba_array[:,:,2] = bytescale(b) # blue
        # rgba_array[:,:,3] = 255 # Alpha transparency
        print(rgba_array.shape)
        # scipy.misc.imsave(r"E:\b_label_jpg\aaaCluster_" + str(i) + ".png", rgba_array)
        imageio.imsave(fits_path.split(".fi")[0] + ".jpg", rgba_array)
        # scipy.misc.imsave(r"C:\Users\sun\Desktop\a_label_jpg\Cluster_" + str(i) + ".png", rgba_array)


def main():
    fits_jpg(fitspath)

if __name__ == '__main__':
    fitspath = '/home/lab30201/sdd/slc/SKAData/CIP_random/CIP_random/CIPdata/image/part1/t1/local_area'
    main()