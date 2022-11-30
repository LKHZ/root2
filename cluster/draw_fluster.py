from matplotlib import pyplot as plt
import numpy as np
import os
import glob

def draw(path):
	filelist = glob.glob(os.path.join(path,'*.txt'))
	for file in filelist:
		X = int(os.path.basename(file).split("_")[3])
		Y = int(os.path.basename(file).split("_")[4])
		data =np.loadtxt(file)
		plt.style.use('classic')
		plt.figure(figsize=(10, 10))
		plt.title(os.path.basename(file).split('.txt')[0])
		plt.scatter(data[:,0], data[:,1])
		plt.xlim(X, X+1024)
		plt.ylim(Y, Y+1024)
		plt.grid()
		#plt.legend(loc='best')
		plt.xticks(range(X, X+1024, 128))
		plt.yticks(range(Y, Y+1024, 128))
		plt.xlabel('x', fontsize=20)
		plt.ylabel('y', fontsize=20)
		#plt.savefig(savepath + '/' + 'kdtree_{}_{}_{}.png'.format(file.split(".fits")[0], num_point, error))
		plt.savefig(path + '/' + 'flcuster_' + os.path.basename(file).split('.txt')[0] + 'jpg')
		plt.close()

if __name__ == '__main__':
	path = '/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cluster/fcluster_1k'
	draw(path)