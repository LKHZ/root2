import numpy as np
import matplotlib.pyplot as plt

label_xy = np.loadtxt('/home/lab30201/sdd/slc/SKAData/CIP_random/CIP_random/CIPdata/image/part1/t1/1l_cluster/label_gleam_pixel_random.txt')
all_xy = np.loadtxt('/home/lab30201/sdd/slc/SKAData/CIP_random/CIP_random/CIPdata/image/part1/t1/1l_cluster/ALL_cluster_unique_random.txt')
all_xy = np.array(list(set([tuple(uniquexy) for uniquexy in all_xy])))
#all_xy_cal = np.loadtxt('/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cluster/cal_1k/all_cal.txt')
# cluster_xy1 = np.loadtxt('/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cluster/cluster_pixel_wcs_0.2.txt')
# cluster_xy2 = np.loadtxt('/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cluster/cluster_pixel_wcs_0.15.txt')
# cluster_xy3 = np.loadtxt('/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cluster/cluster_pixel_wcs_0.05.txt')
# cluster_xy4 = np.loadtxt('/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cluster/cluster_pixel_wcs_0.03.txt')
# cluster_xy5 = np.loadtxt('/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cluster/cluster_pixel_wcs_0.0004.txt')
# cluster_xy6 = np.loadtxt('/home/lab30201/sdd/slc/SKAData/SKA_algorithm/cluster/test1/all_cluster_pixel_wcs_0.005.txt')
def exceed(cluster_xy):
	temp = []
	for i in range(cluster_xy.shape[0]):
		if cluster_xy[i,0]<0 or cluster_xy[i,0]>16*1024 or cluster_xy[i,1]<0 or cluster_xy[i,1]>16*1024:
			temp.append(cluster_xy[i,:])
	temp = np.array(temp)
	return temp


# cluster_xy1 = exceed(cluster_xy1)
# cluster_xy2 = exceed(cluster_xy2)
# cluster_xy3 = exceed(cluster_xy3)
# cluster_xy4 = exceed(cluster_xy4)
# cluster_xy5 = exceed(cluster_xy5)
plt.style.use('classic')
plt.figure(figsize=(20,20))
plt.scatter(label_xy[:,0],label_xy[:,1],s=120,c='#2c9678',label='gleam')
# plt.scatter(cluster_xy1[:,0],cluster_xy1[:,1],s=50,c='#c04851',label='error=0.2',marker='x')
# plt.scatter(cluster_xy2[:,0],cluster_xy2[:,1],s=50,c='#621d34',label='error=0.15',marker='+')
# plt.scatter(cluster_xy3[:,0],cluster_xy3[:,1],s=50,c='#310f1b',label='error=0.05',marker='8')
# plt.scatter(cluster_xy4[:,0],cluster_xy4[:,1],s=150,c='#2e317c',label='error=0.03',marker='x')
#plt.scatter(all_xy[:,0],all_xy[:,1],s=30,c='red',label='all_cluster',marker='x')
plt.scatter(all_xy[:,0],all_xy[:,1],s=30,label='all_cluster',c='red',marker='x')
#plt.scatter(cluster_xy6[:,0],cluster_xy6[:,1],s=80,c='red',label='error=0.005',marker='x')

plt.xlim(0,1024*8)
plt.ylim(0,1024*8)
plt.grid()
plt.legend(loc='upper center')
plt.xticks(range(0,8*1024,1024))
plt.yticks(range(0,8*1024,1024))
plt.xlabel('X(pixels)',fontsize=20)
plt.ylabel('Y (pixels)',fontsize=20)
plt.title('gleam/all_cluster',fontsize=20)
#plt.savefig('/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cluster/label_GLEAM_pixel.png')
#plt.savefig('/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cluster/all.png')
#plt.savefig('/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cluster/exceed_cluster_0.001.png')

# plt.savefig('/home/lab30201/sdd/slc/SKAData/SKA_algorithm/cluster/GLEAM_ALL_cluster_unique.png')
plt.savefig('/home/lab30201/sdd/slc/SKAData/CIP_random/CIP_random/CIPdata/image/part1/t1/1l_cluster/GLEAM_ALL_cluster_unique_random.png')