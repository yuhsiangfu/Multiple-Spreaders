"""
Network analysis: measure nodes' attritubes
@auth: Yu-Hsiang Fu
@date: 2016/05/03
"""
# ###
# 1.Imoprt packages and modulars
# ###
# import packages
import copy as c
import networkx as nx
# import numpy as np
# import random as r
import sys
import time

# import modulars
import util.handler.gpickle_handler as gh
import util.handler.pickle_handler as ph

# import constants
from util.constant.constant_folder import FOLDER_FILE
from util.constant.constant_folder import FOLDER_IMAGE
from util.constant.constant_graph import NODE_BETWEENNESS
from util.constant.constant_graph import NODE_CLOSENESS
from util.constant.constant_graph import NODE_DEGREE
from util.constant.constant_graph import NODE_K_SHELL
from util.constant.constant_graph import NODE_PAGERANK
from util.constant.constant_graph import GRAPH_THEORETICAL_THRESHOLD


# ###
# 2.Declare variables
# ###
PAGERANK_ALPHA = 0.85    # Google uses this value
PAGERANK_MAX_ITER = 100  # It's could be enough


# ###
# 3.Define functions
# ###
def show_msg(msg, newline=True):
    if newline:
        print(msg)
    else:
        print(msg, end='', flush=True)


def measure_node_attribute(G, show_progress=False):
    if show_progress:
        show_msg(" ---- compute betweenness")
    betweenness = nx.betweenness_centrality(G, normalized=True, weight=None)

    if show_progress:
        show_msg(" ---- compute closeness")
    closeness = nx.closeness_centrality(G, normalized=True)

    if show_progress:
        show_msg(" ---- compute degree")
    degree = nx.degree(G)

    if show_progress:
        show_msg(" ---- compute k-core")
    k_core = nx.core_number(G)

    if show_progress:
        show_msg(" ---- compute pagerank")
    page_rank = nx.pagerank(G, alpha=PAGERANK_ALPHA, max_iter=PAGERANK_MAX_ITER)

    # assign all above attribute
    if show_progress:
        show_msg(" ---- assign all above attributes to nodes")

    avg_k = 0
    avg_k2 = 0

    for i in G:
        G.node[i][NODE_BETWEENNESS] = betweenness[i]
        G.node[i][NODE_CLOSENESS] = closeness[i]
        G.node[i][NODE_DEGREE] = degree[i]
        G.node[i][NODE_K_SHELL] = k_core[i]
        G.node[i][NODE_PAGERANK] = page_rank[i]

        # calculate threshold
        avg_k += degree[i]
        avg_k2 += pow(degree[i], 2)

    # calculate theoretical-threshold
    G.graph[GRAPH_THEORETICAL_THRESHOLD] = round((avg_k / avg_k2), 8)
    return G


# ###
# 4.main function
# ###
def main_function():
    initial_time = time.time()
    # FILENAME_LIST = [('LFR_benchmark_1000_u=0.01', 26)]
    #
    # LFR benchmark, 10 network for each "u"
    FILENAME_LIST = [('LFR_benchmark_1000_u=0.01', 26),  # |C| = 26
                     ('LFR_benchmark_1000_u=0.05', 37),  # |C| = 37
                     ('LFR_benchmark_1000_u=0.1', 37),   # |C| = 37
                     ('LFR_benchmark_1000_u=0.2', 40),   # |C| = 40
                     ('LFR_benchmark_1000_u=0.3', 40),   # |C| = 40
                     ('LFR_benchmark_1000_u=0.4', 40),   # |C| = 40
                     ('LFR_benchmark_1000_u=0.5', 40),   # |C| = 40
                     ('LFR_benchmark_1000_u=0.6', 40)]   # |C| = 40

    # Overall parameters
    num_network = 10
    folder_LFR = 'LFR_benchmark_1000\\'

    for net in FILENAME_LIST:
        start_time = time.time()
        show_msg(' - [Net] ' + net[0] + ':')

        # ex: LFR_benchmark_1000_u=0.01_net-1.pickle
        for i in range(0, num_network):
            show_msg(' -- Network-{0}:'.format(i + 1))
            net_name = net[0] +'_net-' + str(i + 1)

            # read gpickle file
            show_msg(' --- Read gpickle file')
            read_time = time.time()
            pickle_path = FOLDER_FILE + folder_LFR + net_name + '.pickle'
            G = ph.read_pickle_file(pickle_path)
            show_msg(' ---- Time: {0:^8} sec.'.format(str(round(time.time() - read_time, 4))))

            # measure node attributes
            show_msg(" --- Measure node's attributes")
            measure_time = time.time()
            G = measure_node_attribute(G, show_progress=True)
            show_msg(' ---- Time: {0:^8} sec.'.format(str(round(time.time() - measure_time, 4))))

            # save gpickle file
            show_msg(" --- Save measured result")
            save_time = time.time()
            gpickle_path = FOLDER_FILE + net_name + ', analysis.gpickle'
            gh.write_gpickle_file(G, gpickle_path)
            show_msg(' ---- Time: {0:^8} sec.'.format(str(round(time.time() - save_time, 4))))

            # for i in G:
            #     print(i, G.node[i])
            # print(G.graph[GRAPH_THEORETICAL_THRESHOLD])

        show_msg(' - [Net] Time: {0:^8} sec.'.format(str(round(time.time() - start_time, 4))))
    show_msg(' Total time: {0:^4} seconds'.format(round(time.time() - initial_time, 4)))

if __name__ == '__main__':
    main_function()
