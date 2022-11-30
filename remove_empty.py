import numpy as np
import os



def Remove_empty(labelpath,jpgpath):
	'''
	删除没有源的label文件
	'''
	labellist = os.listdir(labelpath)
	labellist = [label for label in labellist if label.endswith('.list')]
	for labelfile in labellist:
		data = np.loadtxt(labelpath + '/' + labelfile)
		print(len(data))
		if not len(data):
			print('Remove {}'.format(labelfile))
			#os.remove(bboxpath + '/' + labelfile.split('.list')[0] + '.fits' )
			#os.remove(labelpath + '/' + labelfile)
			#os.remove(jpgpath + '/' + labelfile.split('.list')[0] + '.fits')


def main():

	Remove_empty(labelpath = labelpath,jpgpath=jpgpath)

if __name__ == '__main__':

	# jpgpath = r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cube_1k/1k_jpeg'
	# labelpath = r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cube_1k/1k_label'
	# save = r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cube_1k/1k_bbox'
	labelpath = jpgpath = r'/home/lab30201/sdb/slc/sex_platform_V1/testdata300-300'

	main()