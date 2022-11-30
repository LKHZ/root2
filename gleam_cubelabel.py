import os
import numpy as np

def gleam_label1k(X,Y,cubesize):
		save_x = int(X/cubesize)*cubesize
		save_y = int(Y/cubesize)*cubesize
		x = X%cubesize
		y = Y%cubesize
		return save_x,save_y,x,y



if __name__ == '__main__':
	
	gleampath = r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cluster/label_GLEAM_pixel.txt'
	savepath = r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cube_1k/cube_1klabel'
	gleam = np.loadtxt(gleampath)
	cubesize = 1024
	for i in range(gleam.shape[0]):
		save_x,save_y,x,y = gleam_label1k(gleam[i,0],gleam[i,1],cubesize)
		with open(savepath + '/' + 'image_{}_{}.list'.format(save_x,save_y),mode = 'a') as f:
			f.write(str(100) +' ' +  str(x) + ' ' + str(y))
			f.write('\n')

