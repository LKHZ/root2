# -*- coding: utf-8 -*-
# @Author: Yzm
# @Date:   2021-11-09 10:03:01
# @Last Modified by:   Yzm
# @Last Modified time: 2022-05-02 21:00:09
import pandas as pd
import numpy as np
import sys
import os
import math
import time
import matplotlib.pyplot as plt
# from dataload import FitsLoad
from astropy.io import fits
from PIL import Image, ImageDraw

class FitsLoad(object):
	"""
	docstring for FitsLoad
	实现功能：1.创建实例的同时判断文件类型是否有错
			 2.返回关键信息
			 3.后续可以添加多次曝光信息
	读取图像，并返回关键信息
		包括 array， shape，曝光次数？ 其他？
	单个读入
	批量读入
	"""
	def __init__(self, path):
		super(FitsLoad, self).__init__()
		self.path = path
		# self.times = 0
		# self.name = os.path.basename(self.path)

	@property
	def name(self):
		return os.path.basename(self.path)

	@property
	def array(self):
		with fits.open(self.path) as hdu:
			return hdu[0].data	

	@property
	def header(self):
		with fits.open(self.path) as hdu:
			return hdu[0].header	

	def __enter__(self):
		return None

	def __exit__(self):
		pass

class SExtractor(object):
	'''[summary]
	
	[description]
	'''
	def __init__(self):
		# super(SExtractor, self).__init__()
		super(SExtractor, self).__init__()
		self.sexPath = './image.list'
		#self.sexPath = txtpath
		self.configFile = './default.sex'
		self.paramFile = './default.param'

		self.int_switch = False

		# self.password = password

	@property
	def password(self):
		return self._password

	@password.setter
	def password(self, password):
		if not isinstance(password, str):
			raise TypeError('Expected is str')
		self._password = password	

	@property
	def read_configue(self):
		'''[读SExtractor配置文件(*.sex)参数信息并转为Dataframe]
		
		[description]
		
		Returns:
			[Dataframe] -- [Dataframe的shape：（配置文件行数，3）
							第一列'line'：对应.sex文件的行号，
							第二列'param'：为参数keyworld
							第三列'value'：为参数取值]
		'''
		conf_list = []
		with open(self.configFile, 'r') as f:
			context = f.readlines()
		for index, line in enumerate(context):
			if len(line) < 10 or line[0] == '#' or line.split()[0] == '#':
				pass
			else:
				info = line.split('#')[0].split()
				conf_dict = {}
				# print(line.split('#')[0].split())
				conf_dict['line'] = index
				conf_dict['param'] = info[0]
				conf_dict['value'] = ''.join(info[1:])
				conf_list.append(conf_dict)
		# pprint(conf_list)
		return pd.DataFrame(conf_list, columns=['line', 'param', 'value'])

	@property
	def read_param(self):
		'''[读SExtractor配置文件(*.param)参数信息并转为Dataframe]
		
		[description]
		
		Returns:
			[Dataframe] -- [Dataframe的shape：（配置文件行数，3）
							第一列'line'：对应.param文件的行号，
							第二列'param'：keyworld
							第三列'value'：true/false 是否开启]
		'''
		param_list = []
		with open(self.paramFile, 'r') as f:
			text = f.readlines()
		for index, line in enumerate(text):
			if len(line) > 2:
				info = line.split()[0].split('#')
				# print(info)
				param_dict = {}
				param_dict['line'] = index
				param_dict['param'] = info[-1]
				param_dict['value'] = True if len(info[0]) > 1 else False
				# print(param_dict)
				param_list.append(param_dict)

		# pprint(conf_list)
		return pd.DataFrame(param_list, columns=['line', 'param', 'value'])

	@property
	def show_on_param(self):
		'''[summary]
		
		[description]
		显示开启状态的参数
		'''
		df = self.read_param
		param_on = df[df.value == True]  # 必须是等号，不能是is
		return param_on

	def cat_keyworld(self, keyworld, flag):
		'''[查看指定参数的信息]
		
		[description]
		
		Arguments:
			keyworld {[str]} -- [参数关键字]
			flag {[str]} -- [配置或参数标志]
		
		Returns:
			[list] -- [指定参数的信息['line', 'param', 'value']]
		'''
		if flag == 'sex':
			df = self.read_configue
			infor = df[df.param == keyworld].values.tolist()
			# print(infor)
			return infor
		elif flag == 'param':
			df = self.read_param
			infor = df[df.param == keyworld].values.tolist()
			return infor
		else:
			print('flag input error！！')
			return None
		
	def set_configue_old(self, keys, values):
		'''[设置参数]
		
		[description]
		
		Arguments:
			keys {[list]} -- [需修改的参数关键字列表]
			values {[list]} -- [对应的修改的参数取值]
		'''
		with open(self.configFile, 'r') as f:
			context = f.readlines()
		for key, value in zip(keys, values):
			line = self.cat_keyworld(key, 'sex')[0][0]
			# print('修改参数所在行', line)
			# print('切的结果', context[line].split('#', 1))
			info, annotation = context[line].split('#', 1)
			column1 = format(key, '<17')
			column2 = format(str(value), '<15')
			column3 = '#'+annotation
			context[line] = "{}{}{}".format(column1, column2, column3)
			# print('新行', context[line])
		# pprint(context)
		with open(self.configFile, 'w') as f:
			f.write(''.join(context))
		
	def set_configue(self, config):
		'''[设置参数]
		
		[description]
		
		Arguments:
			keys {[list]} -- [需修改的参数关键字列表]
			values {[list]} -- [对应的修改的参数取值]
		'''
		with open(self.configFile, 'r') as f:
			context = f.readlines()
		for key, value in config.items():
			line = self.cat_keyworld(key, 'sex')[0][0]
			# print('修改参数所在行', line)
			# print('切的结果', context[line].split('#', 1))
			info, annotation = context[line].split('#', 1)
			column1 = format(key, '<17')
			column2 = format(str(value), '<15')
			column3 = '#'+annotation
			context[line] = "{}{}{}".format(column1, column2, column3)
			# print('新行', context[line])
		# pprint(context)
		with open(self.configFile, 'w') as f:
			f.write(''.join(context))
		
	def set_param(self, key, state):
		'''[设置参数]
		
		[description]
		
		Arguments:
			key {[str]} -- [需修改的参数关键字]
			state {[bool]} -- [参数状态]
		'''
		with open(self.paramFile, 'r') as f:
			context = f.readlines()
		# if key in context.split():
		print(self.read_param.param)
		if key in np.array(self.read_param.param):
			line, _, value = self.cat_keyworld(key, 'param')[0]
			# print(type(state), type(value))
			if value == state:
				print('***param do not need modify!!***')
				return None
			context[line] = key+'\n' if state is True else '#{}\n'.format(key)
			with open(self.paramFile, 'w') as f:
				f.write(''.join(context))
		else:
			if state is False:
				print('***param do not exist!!!, do not need set to False***', '\n你在淦神魔？')
				return None
			with open(self.paramFile, 'a') as f:
				f.write(key)

	def judge_param(self, param_list):
		'''判断SExtractor配置文件采参数是否齐全'''
		judge_condition = [x for x in param_list if x not in self.row_info]
		if judge_condition == []:
			pass
		else:
			print('请在SExtractor配置文件中添加%s参数' % judge_condition)
			sys.exit()
		
class SExDetect(SExtractor):
	"""docstring for SExDetect"""
	def __init__(self, file):
		super(SExDetect, self).__init__()
		self.file = file
		
	def call_sex(self):
		'''调用SExtractor'''
		# 加异常处理
		# os.system('echo %s | sudo -S %s' % (self.password, 'sextractor -c ' + self.configFile + self.file_path))
		os.system('echo %s | sudo -S sextractor -c %s %s' % (self.password, self.configFile, self.file.path))

	def get_stamp(self, image, X, Y, RADIUS):
		return image[(round(Y) - math.ceil(RADIUS)):(round(Y) + math.ceil(RADIUS) + 1), 
					 (round(X) - math.ceil(RADIUS)):(round(X) + math.ceil(RADIUS) + 1)]

	def array_type(self):
		# 结构化矩阵自定义dtype
		params = self.show_on_param.param.tolist()
		type_list = []
		for index, param in enumerate(params):
			if index <= 1:
				type_list.append((param, 'int'))
			else:
				type_list.append((param, 'f4'))

		return np.dtype(type_list)

	def read_catalog(self):
		'''提取image.sex文件的坐标和列信息'''
		self.call_sex()
		# sextr(self.file_path, self.configFile, 741236985)
		coords = [] 
		with open(self.sexPath, 'r') as sex_file:
			old = sex_file.readlines()
		raw_info = [line.split()[2] for line in old if line[0] == '#']
		# print('让我看看raw_info', raw_info)
		old = old[len(raw_info):]
		# print('坐标第一行', old[0])

		if self.int_switch is True:
			# coords = [list(map(int, map(float, line.split()))) for line in old if line[0] != '#']
			coords = [tuple(map(int, map(float, line.split()))) for line in old if line[0] != '#']
		elif self.int_switch is False:
			# coords = [list(map(float, line.split())) for line in old if line[0] != '#']
			coords = [tuple(map(float, line.split())) for line in old if line[0] != '#']

		return coords
		# return np.asarray(coords, self.array_type())

	def list2array(self):
		return np.asarray(self.read_catalog(), self.array_type())

	def fiter(self, R, ellipse, snr):
		start = time.time()
		# 读fits
		array = self.file.array
		print(array.shape)

		# 将SExtractor扫描结果作为结构化数组
		catalog = self.list2array()
		print('pre-fitter: ', catalog.shape)

		# catalog[catalog[:, 0] < 20] = float('nan')

		catalog = catalog[
			(catalog['FLUX_RADIUS'] > R) &
			(catalog['CXX_IMAGE']/catalog['CYY_IMAGE'] < ellipse) & 
			(catalog['CXX_IMAGE']/catalog['CYY_IMAGE'] > 1/ellipse) &
			(catalog['FLUX_AUTO']/(catalog['BACKGROUND']*catalog['FLUX_RADIUS']*catalog['FLUX_RADIUS']*math.pi) > snr)]

		print('after-fitter', catalog.shape)
		end = time.time()
		print('扫描时间', round(end-start))
		return catalog

	def bbox_by_kron(self, image, starList, R, color, Width, save):
		fig = plt.figure(figsize=(80, 80))  # 单位为100
		# ax = fig.add_subplot(1,1,1)
		ax = plt.gca()

		for index, each in enumerate(starList):
			top_left_x, top_left_y = each['X_IMAGE']-R-4, each['Y_IMAGE']-R-4
			bottom_left_x, bottom_left_y = each['X_IMAGE']-R-4, each['Y_IMAGE']+R+4
			rect = plt.Rectangle((top_left_x, top_left_y), R*2+6, R*2+6, fill=False, edgecolor=color, linewidth=Width)

			ax.add_patch(rect)
			# ax.text(top_left_x, top_left_y, each[3], fontsize=16, color="r", style="italic", weight="light", verticalalignment='center', horizontalalignment='right', rotation=0)
			# ax.text(bottom_left_x, bottom_left_y, t1[index], fontsize=16, color="r", style="italic", weight="light", verticalalignment='center', horizontalalignment='right', rotation=0)

		plt.imshow(image, cmap='gray')
		plt.axis('off')
		plt.savefig(save)
		# plt.show()

	def draw_bbox(self, jpg, starList, R, color, lineWidth, save):
		'''根据坐标绘制bbox，由于fits图像与jpg图像原点不同，需要两次翻转'''
		print('draw start')
		Image.MAX_IMAGE_PIXELS = 1000000000
		with Image.open(jpg) as image:
			out = image.transpose(Image.FLIP_TOP_BOTTOM)
			draw = ImageDraw.Draw(out)
			for i in starList:
				bbox = [i['X_IMAGE']-R-4, i['Y_IMAGE']-R-4, i['X_IMAGE']+R+4, i['Y_IMAGE']+R+4]
				draw.rectangle([bbox[0], bbox[1], bbox[2], bbox[3]], outline=color, width=lineWidth)
			del draw
			out2 = out.transpose(Image.FLIP_TOP_BOTTOM)
		#save = os.path.join(save, self.file.name+".jpg")
########################################################################################################
		save = os.path.join(save, self.file.name.split('.fits')[0] + '_bbox' + ".jpg")
########################################################################################################
		out2.save(save, overwrite=True)
		print('draw complete')
		
def save_label(catalog,labelpath,labelname,img_size):
	x = []
	y = []
	for label in catalog:
		x.append(label['X_IMAGE'])
		temp_y = abs(label['Y_IMAGE'] - img_size)
		y.append(temp_y)

	ALL = list(zip(x,y))
	np.savetxt(labelpath + '/' + labelname.split('.fits')[0] + '.list',ALL)


def Remove_empty(labelpath,jpgpath):
	'''
	删除没有源的label文件
	'''
	labellist = os.listdir(labelpath)
	for labelfile in labellist:
		data = np.loadtxt(labelpath + '/' + labelfile)
		if not len(data):
			print('Remove {}'.format(labelfile))
			os.remove(labelpath + '/' + labelfile)
			os.remove(jpgpath + '/' + labelfile.split('.list')[0] + '.jpg')


def main():
	#path = r"/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/4k_fits/iamge_00_0_0.fits"
	#jpg = r"/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/4k_jpg/image_00_0_0.jpeg"
	#save = r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/sex'
	img_size = 1024*4
	save = r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cube_4k/4k_bbox'
	fitspath = r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cube_4k/4k_fits'
	jpgpath = r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cube_4k/4k_jpg'
	labelpath = r'/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/cube_4k/4k_label'

	fitslist = os.listdir(fitspath)
	jpglist = os.listdir(jpgpath)

	#for fitsfile in fitslist:
	for num,fitsfile in enumerate(fitslist):

		path = fitspath + '/' +fitsfile
		jpg = jpgpath + '/' + fitsfile.split('.fits')[0] + '.jpg'
		#txtpath = labelpath + '/' + fitsfile.split('.fits')[0] + '.list'

		SEx = SExtractor()
		config = {
			'DETECT_MINAREA': 16,
			'DETECT_THRESH': 20, 
			'ANALYSIS_THRESH': 20
		}

		SEx.set_configue(config)

		file = FitsLoad(path)

		deal = SExDetect(file)
		deal.password = '741236985'

		catalog = deal.list2array()
		#np.save(labelpath + '/' + fitsfile.split('.fits')[0] + '.list',catalog)
		
		# deal.bbox_by_kron(file.array, catalog, 5, 'red', 2, save)
		deal.draw_bbox(jpg, catalog, 5, 'red', 3, save)
		save_label(catalog,labelpath,fitsfile,img_size)
		
	Remove_empty(labelpath,jpgpath)







if __name__ == '__main__':
	main()