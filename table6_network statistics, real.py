"""
Experiment1: execution time analysis, real network
@auth: Yu-Hsiang Fu
@date: 2016/05/03
"""
# ###
# 1.Imoprt packages and modulars
# ###
# import packages
import copy as c
import networkx as nx
import numpy as np
import sys
import time

# import modulars
import util.handler.gpickle_handler as gh
import util.handler.pickle_handler as ph

# import constants
from util.constant.constant_folder import FOLDER_FILE
from util.constant.constant_folder import FOLDER_IMAGE
from util.constant.constant_graph import NODE_DEGREE


# ###
# 2.Define functions
# ###
def show_msg(msg, newline=True):
    if newline:
        print(msg)
    else:
        print(msg, end='', flush=True)


def save_statistics_results(file_path, folder_real, net_list):
    with open(file_path, mode="w") as f:
        f.write('Network\t|N|\t|E|\tK\t<Cc>\tk_max\t<k>\tr\n')

        templete = '{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\n'
        for net in net_list:
            net_path = FOLDER_FILE + folder_real + net[0] + ', analysis.gpickle'
            G = gh.read_gpickle_file(net_path)

            # collect info.
            degree_list = list(nx.degree(G).values())
            clustering_list = list(nx.clustering(G).values())

            N = G.number_of_nodes()
            E = G.number_of_edges()
            K = net[1]
            k_max = max(degree_list)
            k_avg = round(np.mean(degree_list), 4)
            C_avg = round(np.mean(clustering_list), 4)
            R = round(nx.degree_assortativity_coefficient(G), 4)

            # write info.
            f.write(templete.format(net[0], N, E, K, C_avg, k_max, k_avg, R))

        f.close


# ###
# 3.main function
# ###
def main_function():
    initial_time = time.time()

    # real social network
    FILENAME_LIST = [('dolphins_gcc', 2),   # |C| = 2
                     ('football_gcc', 12),  # |C| = 12
                     ('karate_gcc', 2),     # |C| = 2
                     ('polblogs_gcc', 2),   # |C| = 2
                     ('polbooks_gcc', 3),   # |C| = 3
                     ('santafe_gcc', 4),    # |C| = 4
                     ]

    # folder of real networks
    folder_real = 'real_network\\'

    # save statistics results
    show_msg(' - Save statistics results')
    save_time = time.time()
    file_path = FOLDER_IMAGE + 'table6, network statistics.txt'
    save_statistics_results(file_path, folder_real, FILENAME_LIST)
    show_msg(' -- Time: {0:^8} sec.'.format(str(round(time.time() - save_time, 4))))

    show_msg(' Total time: {0:^4} seconds'.format(round(time.time() - initial_time, 4)))

if __name__ == '__main__':
    main_function()
