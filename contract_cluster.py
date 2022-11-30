import numpy as np
import matplotlib.pyplot as plt
import cv2
import os

def contra():
	cluster = np.loadtxt('/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/SKA_sample/4k/part_t1_4k_4k_0_0.txt')
#label
	sextrator = np.loadtxt('/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cube_4k/4k_label/iamge_00_0_0.list')
	print(sextrator[:,:1])
	cluster = cluster[:1000,:2]

	#print(cluster[:,:1])
	cluster_x = cluster[:,:1]
	cluster_y = cluster[:,1:]

	sextrator_x = sextrator[:,:1]
	sextrator_y = sextrator[:,1:]

	plt.scatter(cluster_x,cluster_y,c='b')
	plt.scatter(sextrator_x,sextrator_y,c='r')
	plt.savefig('/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cube_4k/contra.png')

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


if __name__ == '__main__':

	box_halfweigh = 3
    #savepath = r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cube_4k/box.png'
	label = np.loadtxt(r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/SKA_sample/4k/part_t1_4k_4k_0_0.txt')
	filelist = os.listdir(r"/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cube_4k/4k_jpg")
	for file in filelist:
		filepath = r"/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cube_4k/4k_jpg" + '/' + file
		img = cv2.imread(filepath)
		savepath = r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cube_4k/' + file.split('.jpg')[0] + '.png'
		#img = cv2.imread(r"/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cube_4k/4k_jpg/iamge_00_0_0.jpg")
		#img = cv2.flip(img, 1)
		# label = np.loadtxt(r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/SKA_sample/4k/part_t1_4k_4k_0_0.txt')
		bbox(img,label,savepath,box_halfweigh)
	