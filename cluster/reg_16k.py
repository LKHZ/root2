import os
import numpy as np
import matplotlib.pyplot as plt

def Plt(x,y):
	plt.style.use('classic')
	plt.figure(figsize=(20, 20))
	plt.title('ALL_Cluster(pixel)')
	plt.scatter(x,y,label='cluster_resuult')
	plt.xlim(0, 16*1024)
	plt.ylim(0, 16*1024)
	plt.grid()
	plt.legend(loc='best')
	plt.xticks(range(0, 16*1024, 1024))
	plt.yticks(range(0, 16*1024, 1024))
	plt.xlabel('x', fontsize=20)
	plt.ylabel('y', fontsize=20)
	plt.savefig('/home/lab30201/sdd/slc/SKAData/SKA_algorithm/cluster/all_cluuster_unique.png')
	plt.close()


def Cal_ap(gleampath,clustertxt):
	clustert_xy = np.loadtxt(clustertxt)
	sort_xy = np.sort(clustert_xy[:,0])
	print(sort_xy)

if __name__ == '__main__':

	#gleampath = '/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cluster/label_GLEAM_pixel.txt'
	inputdir = '/home/lab30201/sdd/slc/SKAData/CIP_random/CIP_random/CIPdata/image/part1/t1/1l_cluster'
	#clustertxt = '/home/lab30201/sdd/slc/SKAData/SKA_algorithm/cluster/all_cluster_unique.txt'
	#Cal_ap(gleampath,clustertxt)
	filelist = os.listdir(inputdir)
	filelist = [file for file in filelist if file.endswith('txt')]
	all_x = []
	all_y = []
	all_xy = np.empty((1,2))
	for file in filelist:
		print(file)
		txtpath = inputdir + '/' + file
		if not os.path.getsize(txtpath):
			continue
		if (file.split('_')[0]) == 'kdtree':
			x = int(file.split('_')[4])
			y = int(file.split('_')[5])
			cluster_xy = np.loadtxt(txtpath)[:,:2]
			cluster_xy = np.array(list(set([tuple(uniquexy) for uniquexy in cluster_xy])))
			cluster_xy[:,0] = cluster_xy[:,0]+ x
			cluster_xy[:,1] = cluster_xy[:,1] +y
			all_xy = np.vstack((cluster_xy,all_xy))
	all_xy = np.delete(all_xy,-1,0)
	all_xy = np.array(list(set([tuple(uniquexy) for uniquexy in all_xy])))
	np.savetxt('/home/lab30201/sdd/slc/SKAData/CIP_random/CIP_random/CIPdata/image/part1/t1/1l_cluster/ALL_cluster_unique_random.txt',all_xy)
	#Plt(all_xy[:,0],all_xy[:,1])
