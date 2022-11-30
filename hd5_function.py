#-*-codeing = utf-8 -*-
#@Time : 2022/5/1 17:07
#@Author : LichunSun
#@File : hd5_function.py

import h5py

def read_hd5(file:str):
    hd5_file = h5py.File(file,'r')
    return hd5_file

def write_hd5(file,data,datasetname:str):
    if file[-4:] == "hdf5":
        file.create_dataset(datasetname, data=data)
    else:
        hd5_file = h5py.File(file, 'w')
        hd5_file.create_dataset(datasetname, data=data)

if __name__ == '__main__':

    hd5 = read_hd5('/home/lab30201/sdd/slc/SKAData/CIPdata/image/part1/t1/part_t1.hdf5')
    channel = hd5.keys()
    channels = [key for key in channel]
    channels.sort(key=lambda x: int(x[8:]))
    print(channels)
    data = hd5['{}'.format(channels[0])][:]
    print(data.reshape(16384,16384))
