import sys
import os
sys.path.append(os.path.abspath("../.."))
from SKA_pipeline.Cluster.cluster import Cluster


if __name__ == '__main__':
    cluster_filepath = r'/home/lab30201/sdd/slc/SKAData/CIP_random/CIP_random/CIPdata/image/part1/t1/1k_mulchannel'
    gleampath = r"/home/lab30201/sdd/slc/SKAData/CIPdata/image/GLEAM_filtered.txt"
    cluster_savepath = r'/home/lab30201/sdd/slc/SKAData/SKA_algorithm/SKA_pipeline/datas/test_save'
    Cluster = Cluster(
        file='',
        input_dir = cluster_filepath,
        r=10,
        min_num = 200,
        num_point = 5000,
        output_dir = cluster_savepath)
    Cluster._execute_function()
    #Cluster.run()