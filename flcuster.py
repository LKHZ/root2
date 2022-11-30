import os
import numpy as np
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import dendrogram, linkage,fcluster
import glob

def Fcluster(path,savepath):
	filelist = glob.glob(os.path.join(path,'*.txt'))
	all_flcuster = np.empty((1,2))

	for file in filelist:
		mul_flag = 0
		print(file)
		data = np.loadtxt(file)
		newdata = data[:, :2]
		pdist_data = pdist(newdata)
		Z = linkage(pdist_data, 'average')
		dn = dendrogram(Z)
		dis = np.array(dn['dcoord'])
		ori_class = 0
		record = []
		final = np.empty((1, 2))
		if int(np.max(dis[:, 2]))<50:
			np.savetxt(savepath + '/' + 'flcuster_' + os.path.basename(file), newdata)
			all_flcuster = np.vstack((newdata,all_flcuster))
			continue
		else:

			for i in range(int(np.max(dis[:, 2])), 0, -50):

				c = fcluster(Z, i, criterion='distance')
				class_num = np.unique(c)
				if len(class_num) != ori_class:
					ori_class = len(class_num)
					c = c.reshape((-1, 1))
					a = np.hstack((newdata, c))
					for j in range(class_num.shape[0]):
						newarray = np.array([data for n, data in enumerate(a) if a[n, 2] == j + 1])
						x_max = np.max(newarray[:, 0])
						x_min = np.min(newarray[:, 0])
						y_max = np.max(newarray[:, 1])
						y_min = np.min(newarray[:, 1])
						area = (x_max - x_min) * (y_max - y_min)
						if 10 < area < 1000:
							flag = 1
							record.append((i, j + 1, class_num.shape[0], area))

				else:
					mul_flag +=1 

			if mul_flag >=8:
				np.savetxt(savepath + '/' + 'flcuster_' + os.path.basename(file), newdata)
				all_flcuster = np.vstack((newdata,all_flcuster))
				# print(area)
			else:
				record = np.array(record)
				#print(record)
				a = np.unique(record[:, 3], return_index=True, return_counts=True)
				a_sets = list(set.difference(set(np.arange(0, record.shape[0])), set(a[1])))
				print(a_sets)

				for a_set in a_sets:
					# $print(record[a_set,:])
					thresh = record[a_set, :][0]
					cla = record[a_set, :][1]
					# print(cla)
					target_cla = np.array(fcluster(Z, thresh, criterion='distance'))
					target_cla = target_cla.reshape((-1, 1))
					# print(target_cla)
					newdata = np.hstack((newdata, target_cla))

					# print(newdata)
					for j in range(newdata.shape[0]):
						# print(newdata[j,2],cla)
						if cla == newdata[j, 2]:
							final = np.vstack((newdata[j, :2], final))
					newdata = np.delete(newdata, 2, axis=1)
				# print(final.shape)
				final = np.delete(final, -1, axis=0)
				all_flcuster = np.vstack((final,all_flcuster))
				# print(final.shape)
				# print(final)
				np.savetxt(savepath + '/' + 'flcuster_' + os.path.basename(file), final)

	all_flcuster = np.delete(all_flcuster,-1,axis=0)
	np.savetxt(savepath + '/' + 'all_flcuster.txt',all_flcuster)
if __name__ == '__main__':

	path = '/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cluster/cal_1k_class'
	savepath = '/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cluster/fcluster_1k'
	Fcluster(path,savepath)