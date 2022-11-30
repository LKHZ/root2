import os


# filelist = os.listdir(path)
# #labellist = [label for label in filelist if label.endswith('.list')]
# fitslist = [fitsfile for fitsfile in filelist if fitsfile.endswith('.fits')]

# for fitsfile in fitslist:
# 	filename = fitsfile.split('.fits')[0]
# 	if not os.path.exists(path + '/' + filename + '.list'):
# 		os.remove(path + '/' + fitsfile)
# 		print(path + '/' + fitsfile + ' is remove')


def Remove_fits(path):
	#对所有的fits处理 如果fits没有对应的label 删除fits 一个文件内包含所有fits和有源的label
	filelist = os.listdir(path)
	fitslist = [fitsfile for fitsfile in filelist if fitsfile.endswith('.fits')]

	for fitsfile in fitslist:
		filename = fitsfile.split('.fits')[0]
		if not os.path.exists(path + '/' + filename + '.list'):
			os.remove(path + '/' + fitsfile)
			print(path + '/' + fitsfile + ' is remove')

def Remove_fits2(inputpath,removepath):
	#对所有的fits处理  删除没有源的fits 两个文件夹 针对：在原始数据的基础上生成新的数据，比如加噪声等
	filelist = os.listdir(removepath)
	fitslist = [fitsfile for fitsfile in filelist if fitsfile.endswith('.fits')]

	for fitsfile in fitslist:
		x = fitsfile.split('_')[1]
		y = fitsfile.split('_')[2]
		if not os.path.exists(inputpath + '/' + 'image_{}_{}'.format(x,y) + '.list'):
			os.remove(removepath + '/' + fitsfile)
			os.remove(removepath + '/' + fitsfile.split('.fits')[0] + '.jpg')
			print(removepath + '/' + fitsfile + ' is remove')
if __name__ == '__main__':
	path = r'/home/dell460/slc/sdd_01/SKAData/CIP_random2/data/fits_label'
	removepath = r'/home/lab30201/sdd/slc/SKAData/Faster_mulchannel/testdata300-300'
	Remove_fits(path)
	#Remove_fits(path,removepath)