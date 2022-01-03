"""
Figure2: multiple spreading, LFR_benchmark, with tables
@auth: Yu-Hsiang Fu
@date: 2016/05/04
"""
# ###
# 1.Imoprt packages and modulars
# ###
# import packages
# import copy as c
import matplotlib.pyplot as plt
import numpy as np
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


# ###
# 2.Declare variables
# ###
# measurement variables
COMMUNITY_BASED  = 'community_based'
MEASUREMENT_LIST = [NODE_BETWEENNESS, NODE_CLOSENESS, NODE_DEGREE,
                    NODE_K_SHELL, NODE_PAGERANK, COMMUNITY_BASED]

# figure variables
COLOR_LIST      = ['gray', 'orange', 'y', 'b', 'c', 'm', 'r', 'k']
MARKER_LIST     = ['^', 'v', '8', 'H', 's', 'D']
PLOT_LINE_WIDTH = 1
PLOT_X_SIZE     = 3
PLOT_Y_SIZE     = 3
PLOT_DPI        = 300
PLOT_FORMAT     = 'png'


# ###
# 3.Define functions
# ###
def show_msg(msg, newline=True):
    if newline:
        print(msg)
    else:
        print(msg, end='', flush=True)


# ###
# major function
# ###
def draw_figure(net_name, spread_result, num_simulation=1000, num_time_step=50, image_save=False, image_show=False):
    # prepare data
    num_network = len(spread_result)
    spread_avg = {}
    spread_std = {}

    for measure in MEASUREMENT_LIST:
        simulation_avg = [[] for i in range(0, (num_time_step + 1))]
        simulation_std = [0] * (num_time_step + 1)

        for i in range(0, num_network):
            for j in range(0, num_simulation):
                for k in range(0, (num_time_step + 1)):
                    simulation_avg[k].append(spread_result[i][measure][j][k])

        # calculate avg. and std
        for i in range(0, (num_time_step + 1)):
            simulation_std[i] = np.std(simulation_avg[i])
            simulation_avg[i] = np.mean(simulation_avg[i])

        spread_avg[measure] = simulation_avg
        spread_std[measure] = simulation_std

    # draw figure
    fig, axes = plt.subplots(figsize=(PLOT_X_SIZE, PLOT_Y_SIZE), facecolor='w')
    cm_index = 0
    legen_text = []

    for measure in MEASUREMENT_LIST:
        # errbar
        # x = range(0, num_time_step + 1)
        # y = spread_avg[measure]
        # axes.errorbar(x, y, yerr=spread_std[measure], marker=MARKER_LIST[cm_index], linewidth=1, markersize=3, markevery=3, fillstyle='none')

        # line
        axes.plot(spread_avg[measure], color=COLOR_LIST[cm_index], linewidth=PLOT_LINE_WIDTH, marker=MARKER_LIST[cm_index], markersize=4, markevery=2, fillstyle='none')
        cm_index += 1

        if measure is COMMUNITY_BASED:
            txt = measure.split('_')
            legen_text.append(txt[0] + '-' + txt[1])
        else:
            legen_text.append(measure.split('_')[1])

    # figure setting
    axes.grid()
    axes.set_xlabel('Time step',             fontdict={'fontsize': 10})
    axes.set_ylabel('Avg. % infected-nodes', fontdict={'fontsize': 10})
    axes.set_ylim(0, 0.8)
    axes.tick_params(axis='both', which='major', labelsize=8)
    axes.tick_params(axis='both', which='minor', labelsize=8)
    axes.legend(legen_text, loc=0, fontsize='small', prop={'size': 5}, ncol=2)

    # save figure
    image_path = '{0}{1}, {2}.{3}'.format(FOLDER_IMAGE, 'figure2, multiple spreading', net_name, PLOT_FORMAT)
    plt.tight_layout()
    if image_save:
        plt.savefig(image_path, dpi=PLOT_DPI, format=PLOT_FORMAT, bbox_inches='tight', pad_inches=0.05)
    if image_show:
        plt.show()
    plt.close(fig)


# ###
# 4.main function
# ###
def main_function():
    initial_time = time.time()
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
    folder_LFR = 'LFR_benchmark_1000\\'
    num_simulation = 1000
    num_time_step  = 50
    num_network    = 1

    for net in FILENAME_LIST:
        start_time = time.time()
        show_msg(' - [Net] ' + net[0] + ':')
        spread_result = {}
        
        show_msg(' -- Read spreading result')
        read_time = time.time()
        for i in range(0, num_network):
            show_msg(' --- Network-{0}:'.format(i + 1))
            # ex: LFR_benchmark_1000_u=0.01_net-1, analysis.gpickle
            net_name = net[0] + '_net-' + str(i + 1)

            # read pickle file of spreading results
            pickle_path = FOLDER_FILE + net_name + ', experiment2-LFR.pickle'
            spread_result[i] = ph.read_pickle_file(pickle_path)
        show_msg(' --- Time: {0:^8} sec.'.format(str(round(time.time() - read_time, 4))))

        # draw ans save figure of spreading results
        show_msg(' -- Draw and save figure of spreading result')
        draw_time = time.time()
        draw_figure(net[0], spread_result, num_simulation, num_time_step, image_save=True, image_show=False)
        show_msg(' --- Time: {0:^8} sec.'.format(str(round(time.time() - draw_time, 4))))

        show_msg(' - [Net] Time: {0:^8} sec.'.format(str(round(time.time() - start_time, 4))))
    show_msg(' Total time: {0:^4} seconds'.format(round(time.time() - initial_time, 4)))

if __name__ == '__main__':
    main_function()
