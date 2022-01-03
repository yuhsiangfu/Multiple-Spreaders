"""
Experiment2: multiple spreading, LFR_benchmark, using TPEF
@auth: Yu-Hsiang Fu
@date: 2016/05/03
"""
# ###
# 1.Imoprt packages and modulars
# ###
# import packages
# import copy as c
import sys
import time

# import modulars
import util.epidemic_model.sir_model as sir
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
# from util.constant.constant_graph import GRAPH_THEORETICAL_THRESHOLD


# ###
# 2.Declare variables
# ###
# measurement variables
COMMUNITY_BASED  = 'community_based'
MEASUREMENT_LIST = [NODE_BETWEENNESS, NODE_CLOSENESS, NODE_DEGREE,
                    NODE_K_SHELL, NODE_PAGERANK, COMMUNITY_BASED]

# GA variable
# INDV_FITNESS   = 'fitness'
# INDV_GENOTYPE  = 'genotype'
INDV_PHENOTYPE = 'phenotype'


# ###
# 3.Define functions
# ###
def show_msg(msg, newline=True):
    if newline:
        print(msg)
    else:
        print(msg, end='', flush=True)


# ###
# get function
# ### 
def get_topk_centers(G, community_list, num_spreader):
    topk_centers = []
    for com in community_list:
        node_list = []
        for i in com:
            numerator = pow(len(set(G.neighbors(i)) & set(com)), 2)
            denominator = G.node[i][NODE_DEGREE] * len(com)
            node_list.append((i, (numerator / denominator)))
        node_list = sorted(node_list, key=lambda x: x[1], reverse=True)
        topk_centers.append(node_list[0][0])
    return topk_centers


def get_topk_nodes(G, measure, num_spreader):
    topk_nodes = [(i, G.node[i][measure]) for i in G]
    topk_nodes = sorted(topk_nodes, key=lambda x: x[1], reverse=True)
    topk_nodes = [i for (i, w) in topk_nodes[0:num_spreader]]
    return topk_nodes


# ###
# major function
# ###
def generate_topk_spreader(G, community_list):
    num_spreader = len(community_list)
    topk_node = {}

    for measure in MEASUREMENT_LIST:
        if measure is COMMUNITY_BASED:
            topk_node[measure] = get_topk_centers(G, community_list, num_spreader)
        else:
            topk_node[measure] = get_topk_nodes(G, measure, num_spreader)
    return topk_node



def multiple_spreading(G, topk_spreader, num_simulation=1000, num_time_step=50, rate_infection=0.1, rate_recovery=1, show_progress=False, progress_gap=100):
    spread_result = {}

    for measure in MEASUREMENT_LIST:
        show_msg(' ----- Measure: {0}'.format(measure))

        # simulation result
        initial_node = topk_spreader[measure]
        sim_result = {}
        for i in range(0, num_simulation):
            if show_progress:
                if i is 0:
                    show_msg(' ------ Simulation {0}'.format(i + 1))
                elif ((i + 1) % progress_gap) is 0:
                    show_msg(' ------ Simulation {0}'.format(i + 1))
                else:
                    pass
            else:
                pass

            # spreading by SIR model
            sim_result[i] = sir.spreading(G, initial_node, num_time_step, rate_infection, rate_recovery)
        spread_result[measure] = sim_result
    return spread_result


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
                     # ('LFR_benchmark_1000_u=0.2', 40),   # |C| = 40
                     # ('LFR_benchmark_1000_u=0.3', 40),   # |C| = 40
                     # ('LFR_benchmark_1000_u=0.4', 40),   # |C| = 40
                     # ('LFR_benchmark_1000_u=0.5', 40),   # |C| = 40
                     # ('LFR_benchmark_1000_u=0.6', 40),   # |C| = 40
                     ]

    # spreading and sir model
    num_simulation = 1000
    num_time_step  = 50

    rate_infection = 0.08  # LFR_benchmark_1000_u=0.01~0.6
    rate_recovery  = 1

    # LFR_benchmark parameters
    folder_LFR  = 'LFR_benchmark_1000\\'
    num_network = 1

    for net in FILENAME_LIST:
        start_time = time.time()
        show_msg(' - [Net] ' + net[0] + ':')

        # ex: LFR_benchmark_1000_u=0.01_net-1, analysis.gpickle
        for i in range(0, num_network):
            show_msg(' -- Network-{0}:'.format(i + 1))
            net_name = net[0] +'_net-' + str(i + 1)

            # read gpickle file
            show_msg(' --- Read gpickle file')
            read_time = time.time()
            gpickle_path = FOLDER_FILE + folder_LFR + net_name + ', analysis.gpickle'
            G = gh.read_gpickle_file(gpickle_path)
            show_msg(' ---- Time: {0:^8} sec.'.format(str(round(time.time() - read_time, 4))))

            # read community detection results: TPEF
            # ex: LFR_benchmark_1000_u=0.01_net-1, experiment1-LFR-tpef.pickle
            show_msg(' --- Read community detection results')
            community_time = time.time()
            community_path = FOLDER_FILE + net_name + ', experiment1-LFR-tpef.pickle'
            community_list = ph.read_pickle_file(community_path)[1][0][INDV_PHENOTYPE]
            show_msg(' ---- Time: {0:^8} sec.'.format(str(round(time.time() - community_time, 4))))

            # get top-k spreaders
            show_msg(' --- Get top-k network spreaders')
            topk_time = time.time()
            topk_spreader = generate_topk_spreader(G, community_list)
            show_msg(' ---- Time: {0:^8} sec.'.format(str(round(time.time() - topk_time, 4))))

            # multiple network spreading
            show_msg(' --- Multiple spreading')
            spread_time = time.time()
            spread_result = multiple_spreading(
                            G,
                            topk_spreader,
                            num_simulation, num_time_step,
                            rate_infection, rate_recovery,
                            show_progress=False)
            show_msg(' ---- Time: {0:^8} sec.'.format(str(round(time.time() - spread_time, 4))))

            # save spreading results
            show_msg(' --- Save spreading result')
            save_time = time.time()
            save_path = FOLDER_FILE + net_name + ', experiment2-LFR.pickle'
            ph.write_pickle_file(spread_result, save_path)
            show_msg(' ---- Time: {0:^8} sec.'.format(str(round(time.time() - save_time, 4))))

        show_msg(' - [Net] Time: {0:^8} sec.'.format(str(round(time.time() - start_time, 4))))
    show_msg(' Total time: {0:^4} seconds'.format(round(time.time() - initial_time, 4)))

if __name__ == '__main__':
    main_function()
