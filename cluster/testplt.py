import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.cluster import DBSCAN
from astropy.io import fits

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


if __name__ == '__main__':
    r = 10
    min_num = 200
    num_point = 5000

    path = '/home/lab30201/sdd/slc/SKAData/Faster_mulchannel/datafits1/image_3072_15360.fits'
    img = fits.open(path)[0].data
    result = cluster_DBSCAN(img, num_point)
    plt.scatter(result[:,0],result[:,1])
    plt.savefig('/home/lab30201/sdd/slc/SKAData/Faster_mulchannel/datafits1/image_3072_15360.png')