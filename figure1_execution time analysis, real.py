"""
Figure1: execution time analysis, real datasets, with tables
@auth: Yu-Hsiang Fu
@date: 2016/05/08
"""
# import packages
import copy as c
import matplotlib.pyplot as plt
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


# ###
# 2.Declare variables
# ###
# GA variable
INDV_FITNESS   = 'fitness'
INDV_GENOTYPE  = 'genotype'
INDV_PHENOTYPE = 'phenotype'

# figure variables
COLOR_BAR_LIST  = ['b', 'g', 'r', 'm']
COLOR_LIST      = ['gray', 'orange', 'y', 'b', 'c', 'm', 'r', 'k']
MARKER_LIST     = ['^', 'v', '8', 'H', 's', 'D']
PLOT_LINE_WIDTH = 1
PLOT_NODE_SIZE  = 25
PLOT_NET_X_SIZE = 4
PLOT_NET_Y_SIZE = 4
PLOT_X_SIZE     = 6
PLOT_Y_SIZE     = 3
PLOT_X2_SIZE    = 3
PLOT_Y2_SIZE    = 3
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
def draw_execution_time_figure(image_path, table_result, net_list, ga_method, image_save=False, image_show=False):
    # create figure
    fig, axes   = plt.subplots(figsize=(PLOT_X_SIZE, PLOT_Y_SIZE), facecolor='w')
    bar_ind     = np.arange(len(net_list))
    bar_alpha   = 0.85
    bar_counter = 0
    bar_width   = 0.25
    bar_err_cfg = {'ecolor': '0.0'}
    hatch_list  = {'SGA': '/', 'LGA': '//', 'TPEF': '+'}

    # draw figure
    for method in ga_method:
        time_avg = []
        time_std = []

        for net in net_list:
            time_avg.append(table_result[method][net[0]][3])
            time_std.append(table_result[method][net[0]][4])

        axes.bar(bar_ind + (bar_counter * bar_width), time_avg, bar_width, hatch=hatch_list[method.upper()], color=COLOR_BAR_LIST[bar_counter], yerr=time_std, alpha=bar_alpha, error_kw=bar_err_cfg)
        bar_counter += 1

    # figure setting
    xtick_list = [net[0].split('_gcc')[0] for net in net_list]
    axes.grid()
    axes.set_xlabel('', fontdict={'fontsize': 10})
    axes.set_ylabel('Avg. time (seconds)',  fontdict={'fontsize': 10})
    axes.set_xticks((bar_ind + bar_width * 1.5))
    axes.set_xticklabels(xtick_list)  #, rotation='vertical')
    axes.set_xlim(-0.3, len(xtick_list) + 0.0)
    # axes.set_ylim(0, 120)
    axes.tick_params(axis='x', which='major', labelsize=10)
    axes.tick_params(axis='y', which='major', labelsize=8)
    axes.tick_params(axis='both', which='minor', labelsize=8)
    axes.legend([method.upper() for method in ga_method], loc=0, fontsize='small', prop={'size': 8}, ncol=3)

    # save and show figure
    plt.tight_layout()
    if image_save:
        plt.savefig(image_path, dpi=PLOT_DPI, format=PLOT_FORMAT, bbox_inches='tight', pad_inches=0.05)
    if image_show:
        plt.show()
    plt.close(fig)


def save_modularity_figure(image_path, table_result, net_list, ga_method, image_save=False, image_show=False):
    # create figure
    fig, axes   = plt.subplots(figsize=(PLOT_X_SIZE, PLOT_Y_SIZE), facecolor='w')
    bar_ind     = np.arange(len(net_list))
    bar_alpha   = 0.85
    bar_counter = 0
    bar_width   = 0.25
    bar_err_cfg = {'ecolor': '0.0'}
    hatch_list  = {'SGA': '/', 'LGA': '//', 'TPEF': '+'}

    # draw figure
    legend_text = []
    for method in ga_method:
        q_avg = []
        q_std = []

        for net in net_list:
            q_avg.append(table_result[method][net[0]][1])
            q_std.append(table_result[method][net[0]][2])

        axes.bar(bar_ind + (bar_counter * bar_width), q_avg, bar_width, hatch=hatch_list[method.upper()], color=COLOR_BAR_LIST[bar_counter], yerr=q_std, alpha=bar_alpha, error_kw=bar_err_cfg)
        bar_counter += 1

        if method is 'sga':
            legend_text.append(method.upper() + '(baseline)')
        else:
            legend_text.append(method.upper())

    # figure setting
    xtick_list = [net[0].split('_gcc')[0] for net in net_list]
    axes.grid()
    axes.set_xlabel('', fontdict={'fontsize': 10})
    axes.set_ylabel('Avg. modularity',      fontdict={'fontsize': 10})
    axes.set_xticks((bar_ind + bar_width * 1.5))
    axes.set_xticklabels(xtick_list)
    axes.set_xlim(-0.3, len(xtick_list) + 0.0)
    axes.set_ylim(0, 1)
    axes.tick_params(axis='x', which='major', labelsize=10)
    axes.tick_params(axis='y', which='major', labelsize=8)
    axes.tick_params(axis='both', which='minor', labelsize=8)
    # axes.legend([method.upper() for method in ga_method], loc=0, fontsize='x-small', prop={'size': 8}, ncol=3)
    axes.legend(legend_text, loc=0, fontsize='small', prop={'size': 8}, ncol=3)

    # save and show figure
    plt.tight_layout()
    if image_save:
        plt.savefig(image_path, dpi=PLOT_DPI, format=PLOT_FORMAT, bbox_inches='tight', pad_inches=0.05)
    if image_show:
        plt.show()
    plt.close(fig)


def draw_fitness_and_network(net_list, ga_method, image_save=True, image_show=False):
    folder_real = 'real_network\\'

    for net in net_list:
        convergence_list = {}

        for method in ga_method:
            g_path = FOLDER_FILE + folder_real + net[0] + ', analysis.gpickle'
            G = gh.read_gpickle_file(g_path)

            # ex:  dolphins_gcc, experiment1-real-lga
            pickle_path = FOLDER_FILE + net[0] + ', experiment1-real-' + method + '.pickle'
            pickle_result = ph.read_pickle_file(pickle_path)
            community_list = []
            fitness_list = []

            if method is 'tpef':
                community_list = pickle_result[1][0]
                fitness_list.append(pickle_result[1][1])  # fit_avg
                fitness_list.append(pickle_result[1][2])  # fit_best
            else:
                community_list = pickle_result[0]
                fitness_list.append(pickle_result[1])  # fit_avg
                fitness_list.append(pickle_result[2])  # fit_best

            # draw networks
            image_path = FOLDER_IMAGE + net[0] + ', experiment1-real-' + method + '-network.png'
            community_list = community_list[INDV_PHENOTYPE]
            draw_network(image_path, G, community_list, image_save=True, image_show=False)

            image_path = FOLDER_IMAGE + net[0] + ', experiment1-real-' + method + '-fitness.png'
            draw_fitness(image_path, fitness_list, image_save=True, image_show=False)

            convergence_list[method] = fitness_list

        # craw convergence
        image_path = FOLDER_IMAGE + net[0] + ', experiment1-real-convertence.png'
        draw_convergence(image_path, convergence_list, ga_method, image_save=True, image_show=False)


def draw_network(image_path, G, com_list, image_save=False, image_show=False):
    # create pos
    pos = {u: v['node_layout-xy'] for (u, v) in G.nodes(data=True)}

    # create community_list
    com_index = 1
    community_list = {}
    for com in sorted(com_list):
        community_list[com_index] = com
        com_index += 1

    # create edge_list
    edge_list = {}
    edge_other = []
    for (ei, ej) in G.edges():
        ci = -1
        cj = -2

        for i in community_list:
            if ei in community_list[i]:
                ci = c.copy(i)
            if ej in community_list[i]:
                cj = c.copy(i)
            if (ci != -1) and (cj != -2):
                break

        if ci == cj:
            if ci in edge_list:
                edge_list[ci].append((ei, ej))
            else:
                edge_list[ci] = [(ei, ej)]
        else:
            edge_other.append((ei, ej))

    # create figure
    fig, axes = plt.subplots(figsize=(PLOT_NET_X_SIZE, PLOT_NET_Y_SIZE), facecolor='w')

    # draw colored edges
    plot_cmap = plt.cm.jet
    color_max = max(community_list)
    nx.draw_networkx_edges(G, pos=pos, edgelist=edge_other, edge_color='gray', width=1.0, alpha=0.5)
    for i in edge_list:
        edge_color = [i] * len(edge_list[i])
        nx.draw_networkx_edges(G, pos=pos, edgelist=edge_list[i], edge_color=edge_color, edge_cmap=plot_cmap, width=1.5, edge_vmin=0.9, edge_vmax=color_max+0.1, alpha=0.8)

    # draw colored nodes
    for i in community_list:
        node_color = [i] * len(community_list[i])
        nx.draw_networkx_nodes(G, pos=pos, nodelist=community_list[i], node_size=PLOT_NODE_SIZE, node_color=node_color, cmap=plot_cmap, vmin=0.9, vmax=color_max+0.1)

    # figure setting
    axes.xaxis.set_visible(False)
    axes.yaxis.set_visible(False)
    axes.axis('off')

    # save and show
    plt.tight_layout()
    if image_save:
        plt.savefig(image_path, dpi=PLOT_DPI, format=PLOT_FORMAT, bbox_inches='tight', pad_inches=0.05)
    if image_show:
        plt.show()
    plt.close(fig)


def draw_fitness(image_path, fitness_result, image_show=False, image_save=False):
    fitness_avg = fitness_result[0]
    fitness_best = fitness_result[1]
    num_generation = len(fitness_avg)

    # create figure
    fig, ax_main = plt.subplots(figsize=(PLOT_X2_SIZE, PLOT_Y2_SIZE), facecolor='w')

    # plot
    fitness_avg.insert(0, 0)
    fitness_best.insert(0, 0)
    # ax_main.plot(fitness_avg,  color='b', linewidth=PLOT_LINE_WIDTH)
    # ax_main.plot(fitness_best, color='r', linewidth=PLOT_LINE_WIDTH)
    ax_main.plot(fitness_avg,  color=COLOR_BAR_LIST[0], linewidth=PLOT_LINE_WIDTH, marker=MARKER_LIST[0], markersize=6, markevery=2, fillstyle='none')
    ax_main.plot(fitness_best, color=COLOR_BAR_LIST[2], linewidth=PLOT_LINE_WIDTH, marker=MARKER_LIST[1], markersize=6, markevery=2, fillstyle='none')

    # figure setting
    max_ylim = max(fitness_best) + 0.02 if max(fitness_best) != 1 else 1.01
    ax_main.grid()
    ax_main.set_xlabel('Generation', fontdict={'fontsize': 10})
    ax_main.set_ylabel('Modularity Q', fontdict={'fontsize': 10})
    ax_main.tick_params(axis='both', which='major', labelsize=8)
    ax_main.tick_params(axis='both', which='minor', labelsize=8)
    ax_main.set_xlim([0, num_generation])
    ax_main.set_ylim([0, max_ylim])
    legen_text = ['fit. avg', 'fit. best']
    ax_main.legend(legen_text, loc=4, fontsize='small', prop={'size': 7})

    # save and show figure
    plt.tight_layout()
    if image_save:
        plt.savefig(image_path, dpi=PLOT_DPI, format=PLOT_FORMAT, bbox_inches='tight', pad_inches=0.05)
    if image_show:
        plt.show()
    plt.close(fig)


def draw_convergence(image_path, convergence_list, ga_method, image_save=False, image_show=False):
    # create figure
    fig, ax_main = plt.subplots(figsize=(PLOT_X2_SIZE, PLOT_Y2_SIZE), facecolor='w')

    # draw figure
    cm_index = 0
    for method in ga_method:
        fitness_best = convergence_list[method][1]
        ax_main.plot(fitness_best, color=COLOR_BAR_LIST[cm_index], linewidth=PLOT_LINE_WIDTH, marker=MARKER_LIST[cm_index], markersize=6, markevery=2, fillstyle='none')
        cm_index += 1

    # figure setting
    ax_main.grid()
    ax_main.set_xlabel('Generation', fontdict={'fontsize': 10})
    ax_main.set_ylabel('Avg. modularity Q', fontdict={'fontsize': 10})
    ax_main.tick_params(axis='both', which='major', labelsize=8)
    ax_main.tick_params(axis='both', which='minor', labelsize=8)
    ax_main.set_xlim([0, 50])
    legen_text = [method.upper() for method in ga_method]
    ax_main.legend(legen_text, loc=0, fontsize='small', prop={'size': 7})

    # save and show figure
    plt.tight_layout()
    if image_save:
        plt.savefig(image_path, dpi=PLOT_DPI, format=PLOT_FORMAT, bbox_inches='tight', pad_inches=0.05)
    if image_show:
        plt.show()
    plt.close(fig)


# ###
# table function
# ###
def save_execution_time_table(file_path, table_result, net_list, ga_method):
    with open(file_path, mode="w") as f:
        # title: mu
        f.write('Network\t')
        for net in net_list:
            table_title = '{0}\t{0}\t'.format(net[0])
            f.write(table_title)
        f.write('\n')

        # title: time_avg time_std
        f.write('Execution time\t')
        for i in range(0, len(net_list)):
            table_title = 'Avg.\tStd.\t'
            f.write(table_title)
        f.write('\n')

        # content
        for method in ga_method:
            f.write('{0}\t'.format(method.upper()))

            for net in net_list:
                time_avg = round(table_result[method][net[0]][3], 4)
                time_std = round(table_result[method][net[0]][4], 4)
                f.write('{0}\t{1}\t'.format(time_avg, time_std))
            f.write('\n')
        f.close


def save_modularity_table(file_path, table_result, net_list, ga_method):
    with open(file_path, mode="w") as f:
        # title: mu
        f.write('Network\t')
        for net in net_list:
            table_title = '{0}\t{0}\t{0}\t'.format(net[0])
            f.write(table_title)
        f.write('\n')

        # title: time_avg time_std
        f.write('Modularity Q\t')
        for i in range(0, len(net_list)):
            f.write('Max.\tAvg.\tStd.\t')
        f.write('\n')

        # content
        for method in ga_method:
            f.write('{0}\t'.format(method.upper()))

            for net in net_list:
                q_max = round(table_result[method][net[0]][0], 4)
                q_avg = round(table_result[method][net[0]][1], 4)
                q_std = round(table_result[method][net[0]][2], 4)
                f.write('{0}\t{1}\t{2}\t'.format(q_max, q_avg, q_std))
            f.write('\n')
        f.close


def save_community_number_table(file_path, table_result, net_list, ga_method):
    with open(file_path, mode="w") as f:
        # title: mu
        f.write('Network\t')
        for net in net_list:
            table_title = '{0}\t'.format(net[0])
            f.write(table_title)
        f.write('\n')

        # content
        for method in ga_method:
            f.write('{0}\t'.format(method.upper()))

            for net in net_list:
                c_avg = round(table_result[method][net[0]][0], 4)
                f.write('{0}\t'.format(c_avg))
            f.write('\n')
        f.close


# ###
# 4.main function
# ###
def main_function():
    initial_time = time.time()

    # real social network
    FILENAME_LIST = [('karate_gcc', 2),      # |C| = 2
                     ('dolphins_gcc', 2),    # |C| = 2
                     #('football_gcc', 12),   # |C| = 12
                     #('polbooks_gcc', 3),    # |C| = 3
                     #('polblogs_gcc', 2),    # |C| = 2
                     #('santafe_gcc', 4),     # |C| = 4
                     ]

    # LFR_benchmark parameters
    ga_method   = ['lga', 'sga', 'tpef']
    folder_real = ''
    # folder_real = 'real_network\\'
    community_number = {}
    community_result = {}

    # read pickle files
    show_msg(' - Read pickle file')
    for method in ga_method:
        show_msg(' -- [Method]: {0}'.format(method))
        method_time = time.time()
        cluster_result = {}
        method_result = {}

        # karate_gcc, experiment1-real-lga.pickle
        # LGA:  [indv, fit_avg, fit_best, Q_avg, Q_std, Time_avg, Time_std]
        # SGA:  [indv, fit_avg, fit_best, Q_avg, Q_std, Time_avg, Time_std]
        # TPEF: [[indv, fit_avg, fit_best], [indv, fit_avg, fit_best],
        #        Q_avg, Q_std, Time_avg, Time_std]
        for net in FILENAME_LIST:
            show_msg(' ---- Network-{0}:'.format(net[0]))

            pickle_path = FOLDER_FILE + folder_real + net[0] + ', experiment1-real-' + method + '.pickle'
            pickle_file = ph.read_pickle_file(pickle_path)

            # for each method: Q_best, Q_avg, Q_std, time_avg, time_std
            cluster_result[net[0]] = []
            method_result[net[0]] = []

            if method is 'tpef':
                method_result[net[0]].append(pickle_file[1][0][INDV_FITNESS])
                method_result[net[0]].append(pickle_file[2])
                method_result[net[0]].append(pickle_file[3])
                method_result[net[0]].append(pickle_file[4])
                method_result[net[0]].append(pickle_file[5])
                cluster_result[net[0]].append(len(pickle_file[1][0][INDV_PHENOTYPE]))
            else:
                method_result[net[0]].append(pickle_file[0][INDV_FITNESS])
                method_result[net[0]].append(pickle_file[3])
                method_result[net[0]].append(pickle_file[4])
                method_result[net[0]].append(pickle_file[5])
                method_result[net[0]].append(pickle_file[6])
                cluster_result[net[0]].append(len(pickle_file[0][INDV_PHENOTYPE]))

        community_number[method] = cluster_result
        community_result[method] = method_result
        show_msg(' -- [/Method] Time: {0:^8} sec.'.format(str(round(time.time() - method_time, 4))))

    # draw figures
    # draw execution time figure
    show_msg(' - Draw figure of execution time analysis')
    draw_time = time.time()
    image_path = FOLDER_IMAGE + 'figure1, execution time analysis-real.png'
    draw_execution_time_figure(image_path, community_result,
                               FILENAME_LIST, ga_method,
                               image_save=True, image_show=False)
    show_msg(' -- Time: {0:^8} sec.'.format(str(round(time.time() - draw_time, 4))))

    # save modularity figure
    show_msg(' - Draw figure of modularity analysis')
    save_time = time.time()
    table_path = FOLDER_IMAGE + 'figure1, modularity analysis-real.png'
    save_modularity_figure(table_path, community_result,
                           FILENAME_LIST, ga_method,
                           image_save=True, image_show=False)
    show_msg(' -- Time: {0:^8} sec.'.format(str(round(time.time() - save_time, 4))))

    # draw networks
    show_msg(' - Draw networks')
    draw_time = time.time()
    draw_fitness_and_network(FILENAME_LIST, ga_method,
                             image_save=True, image_show=False)
    show_msg(' -- Time: {0:^8} sec.'.format(str(round(time.time() - draw_time, 4))))

    # save tables
    # save execution time table
    show_msg(' - Save execution time analysis table')
    save_time = time.time()
    table_path = FOLDER_IMAGE + 'table1, execution time analysis-real.txt'
    save_execution_time_table(table_path, community_result, FILENAME_LIST, ga_method)
    show_msg(' -- Time: {0:^8} sec.'.format(str(round(time.time() - save_time, 4))))

    # save modularity table
    show_msg(' - Save modularity analysis table')
    save_time = time.time()
    table_path = FOLDER_IMAGE + 'table1, modularity analysis-real.txt'
    save_modularity_table(table_path, community_result, FILENAME_LIST, ga_method)
    show_msg(' -- Time: {0:^8} sec.'.format(str(round(time.time() - save_time, 4))))

    # save community number table
    show_msg(' - Save community number table')
    save_time = time.time()
    table_path = FOLDER_IMAGE + 'table1, community number-real.txt'
    save_community_number_table(table_path, community_number, FILENAME_LIST, ga_method)
    show_msg(' -- Time: {0:^8} sec.'.format(str(round(time.time() - save_time, 4))))

    show_msg(' Total time: {0:^4} seconds'.format(round(time.time() - initial_time, 4)))

if __name__ == '__main__':
    main_function()
