#-*-codeing = utf-8 -*-
#@Time : 2022/7/22 19:16
#@Author : LichunSun
#@File : test.py


import numpy as np

data = np.array([[1,10],[4,5]])
print(data)
print(data.flatten())
num_point = 2
sort = np.argsort(data.flatten(), kind='mergesort')
print(sort)
samples = np.empty((num_point, 2))
for i in range(1, num_point + 1):
    x = int(sort[-i] / data.shape[1])
    y = sort[-i] % (data.shape[1])
    samples[i - 1, 0] = x  # x与y互换
    samples[i - 1, 1] = y
print(samples)
