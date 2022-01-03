"""
Figure4: community effect, LFR_benchmark, with tables
@auth: Yu-Hsiang Fu
@date: 2016/05/05
"""
# import packages
import copy as c
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
# figure function
# ###
def draw_effect_figure(image_path, spread_avg, mu_list, image_save=False, image_show=False):
    # calculate community effect
    community_effect = {}
    community_avg = spread_avg[COMMUNITY_BASED]
    overall_avg = [0] * len(mu_list)

    for measure in MEASUREMENT_LIST:
        if measure is COMMUNITY_BASED:  # skip to next
            continue

        mi = COMMUNITY_BASED.split('_')
        mi = mi[0] + '-' + mi[1]
        mj = measure.split('node_')[1]
        key = '{0} vs. {1}'.format(mi, mj)

        community_effect[key] = []
        for i in range(0, len(mu_list)):
            diff = community_avg[i] - spread_avg[measure][i]
            community_effect[key].append(diff)
            overall_avg[i] += diff

    # calculate overall avg.
    for i in range(0, len(mu_list)):
        overall_avg[i] /= (len(MEASUREMENT_LIST) - 1)

    # create figure
    fig, ax_main = plt.subplots(figsize=(PLOT_X_SIZE, PLOT_Y_SIZE), facecolor='w')
    cm_index = 0

    # draw figure
    for i in sorted(community_effect.keys()):
        ax_main.plot(community_effect[i], linewidth=PLOT_LINE_WIDTH, marker=MARKER_LIST[cm_index], markersize=5, fillstyle='none', alpha=0.5)
        cm_index += 1
    ax_main.plot(overall_avg, color='k', linestyle='--', linewidth=PLOT_LINE_WIDTH)

    # figure setting
    legen_text = [i for i in sorted(community_effect.keys())]
    legen_text.append('overall-avg')
    ax_main.grid()
    ax_main.set_xlabel('Mixing parameter u',    fontdict={'fontsize': 10})
    ax_main.set_ylabel('Avg. community effect', fontdict={'fontsize': 10})
    ax_main.set_xticklabels(mu_list)
    ax_main.set_ylim(0, 0.45)
    ax_main.tick_params(axis='both', which='major', labelsize=8)
    ax_main.tick_params(axis='both', which='minor', labelsize=8)
    ax_main.legend(legen_text, loc=0, fontsize='small', prop={'size': 5})

    # save figure
    plt.tight_layout()
    if image_save:
        plt.savefig(image_path, dpi=PLOT_DPI, format=PLOT_FORMAT, bbox_inches='tight', pad_inches=0.05)
    if image_show:
        plt.show()
    plt.close(fig)


# ###
# table function
# ###
def save_community_effect_table(file_path, spread_avg, mu_list):
    # calculate community effect
    community_effect = {}
    community_avg = spread_avg[COMMUNITY_BASED]
    overall_avg = [0] * len(mu_list)

    for measure in MEASUREMENT_LIST:
        if measure is COMMUNITY_BASED:  # skip to next
            continue

        mi = COMMUNITY_BASED.split('_')
        mi = mi[0] + '-' + mi[1]
        mj = measure.split('node_')[1]
        key = '{0} vs. {1}'.format(mi, mj)

        community_effect[key] = []
        for i in range(0, len(mu_list)):
            diff = community_avg[i] - spread_avg[measure][i]
            community_effect[key].append(diff)
            overall_avg[i] += diff

    # calculate overall avg.
    for i in range(0, len(mu_list)):
        overall_avg[i] /= (len(MEASUREMENT_LIST) - 1)

    # save table
    with open(file_path, mode="w") as f:
        # title: mu
        f.write('Mixing parameter\t')
        for mu in mu_list:
            table_title = '{0}\t'.format(mu)
            f.write(table_title)
        f.write('\n')

        # content
        for i in sorted(community_effect.keys()):
            f.write('{0}\t'.format(i))

            for j in community_effect[i]:
                f.write('{0}\t'.format(round(j, 4)))
            f.write('\n')

        # overall
        f.write('Overall-avg\t')
        for i in overall_avg:
            f.write('{0}\t'.format(round(i, 4)))
        f.write('\n')
        f.close


# ###
# 4.main function
# ###
def main_function():
    initial_time = time.time()

    # LFR_benchmark parameters
    # mu_list = ['0.01', '0.05', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6']
    mu_list = ['0.01', '0.05', '0.1']
    folder_LFR = 'LFR_benchmark_1000\\'
    num_network    = 1
    num_simulation = 1000
    num_time_step  = 50

    # prepare data
    show_msg(' - Read pickle file')
    spread_avg = {}
    # spread_std = {}

    for measure in MEASUREMENT_LIST:
        show_msg(' -- [Measure]: {0}'.format(measure))
        measure_time = time.time()
        spread_avg[measure] = []
        # spread_std[measure] = []

        for mu in mu_list:
            show_msg(' --- [u={0}]'.format(mu))
            mu_time = time.time()
            data_list = []

            for i in range(0, num_network):
                # pickle: LFR_benchmark_1000_u=0.01_net-1, experiment2-LFR.pickle
                pickle_path = FOLDER_FILE
                pickle_path += 'LFR_benchmark_1000_u=' + mu + '_net-' + str(i + 1) + ', experiment2-LFR.pickle'
                pickle_file = ph.read_pickle_file(pickle_path)

                for j in range(0, num_simulation):
                    data_list.append(pickle_file[measure][j][num_time_step])

            spread_avg[measure].append(np.mean(data_list))
            # spread_std[measure].append(np.std(data_list))

            show_msg(' ---- Time: {0:^8} sec.'.format(str(round(time.time() - mu_time, 4))))
        show_msg(' -- [/Measure] Time: {0:^8} sec.'.format(str(round(time.time() - measure_time, 4))))

    # draw figure of community effect
    show_msg(' - Draw figure of community effect')
    draw_time = time.time()
    image_path = FOLDER_IMAGE + 'figure4, community effect-LFR.png'
    draw_effect_figure(image_path, spread_avg, mu_list, image_save=True, image_show=False)
    show_msg(' -- Time: {0:^8} sec.'.format(str(round(time.time() - draw_time, 4))))

    # save table of community effect
    show_msg(' - Save community effect table')
    save_time = time.time()
    table_path = FOLDER_IMAGE + 'table4, community effect-LFR.txt'
    save_community_effect_table(table_path, spread_avg, mu_list)
    show_msg(' -- Time: {0:^8} sec.'.format(str(round(time.time() - save_time, 4))))    

    show_msg(' Total time: {0:^4} seconds'.format(round(time.time() - initial_time, 4)))

if __name__ == '__main__':
    main_function()
