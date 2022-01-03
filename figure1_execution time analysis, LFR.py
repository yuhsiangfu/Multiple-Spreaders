"""
Figure1: execution time analysis, LFR_benchmark, with tables
@auth: Yu-Hsiang Fu
@date: 2016/05/04
"""
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
PLOT_LINE_WIDTH = 1.5
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
def draw_execution_time_figure(image_path, table_result, mu_list, ga_method, image_save=False, image_show=False):
    # create figure
    fig, axes   = plt.subplots(figsize=(PLOT_X_SIZE, PLOT_Y_SIZE), facecolor='w')
    bar_ind     = np.arange(len(mu_list))
    bar_alpha   = 0.85
    bar_counter = 0
    bar_width   = 0.25
    bar_err_cfg = {'ecolor': '0.0'}
    hatch_list  = {'SGA': '/', 'LGA': '//', 'TPEF': '+'}

    # draw figure
    for method in ga_method:
        time_avg = []
        time_std = []

        for mu in mu_list:
            time_avg.append(table_result[method][mu][3])
            time_std.append(table_result[method][mu][4])

        axes.bar(bar_ind + (bar_counter * bar_width), time_avg, bar_width, hatch=hatch_list[method.upper()], color=COLOR_BAR_LIST[bar_counter], yerr=time_std, alpha=bar_alpha, error_kw=bar_err_cfg)
        bar_counter += 1

    # figure setting
    xtick_list = mu_list
    axes.grid()
    axes.set_xlabel('Mixing parameter (u)', fontdict={'fontsize': 10})
    axes.set_ylabel('Avg. time (seconds)',  fontdict={'fontsize': 10})
    axes.set_xticks((bar_ind + bar_width * 1.5))
    axes.set_xticklabels(xtick_list)
    axes.set_xlim(-0.3, len(mu_list) + 0.0)
    axes.set_ylim(0, 120)
    axes.tick_params(axis='both', which='major', labelsize=8)
    axes.tick_params(axis='both', which='minor', labelsize=8)
    axes.legend([method.upper() for method in ga_method], loc=0, fontsize='small', prop={'size': 8}, ncol=3)

    # save and show figure
    plt.tight_layout()
    if image_save:
        plt.savefig(image_path, dpi=PLOT_DPI, format=PLOT_FORMAT, bbox_inches='tight', pad_inches=0.05)
    if image_show:
        plt.show()
    plt.close(fig)


def save_modularity_figure(image_path, table_result, mu_list, ga_method, image_save=False, image_show=False):
    # create figure
    fig, axes   = plt.subplots(figsize=(PLOT_X_SIZE, PLOT_Y_SIZE), facecolor='w')
    bar_ind     = np.arange(len(mu_list))
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

        for mu in mu_list:
            q_avg.append(table_result[method][mu][1])
            q_std.append(table_result[method][mu][2])

        axes.bar(bar_ind + (bar_counter * bar_width), q_avg, bar_width, hatch=hatch_list[method.upper()], color=COLOR_BAR_LIST[bar_counter], yerr=q_std, alpha=bar_alpha, error_kw=bar_err_cfg)
        bar_counter += 1

        if method is 'sga':
            legend_text.append(method.upper() + '(baseline)')
        else:
            legend_text.append(method.upper())

    # figure setting
    xtick_list = mu_list
    axes.grid()
    axes.set_xlabel('Mixing parameter (u)', fontdict={'fontsize': 10})
    axes.set_ylabel('Avg. modularity: Q',   fontdict={'fontsize': 10})
    axes.set_xticks((bar_ind + bar_width * 1.5))
    axes.set_xticklabels(xtick_list)
    axes.set_xlim(-0.3, len(mu_list) + 0.0)
    axes.set_ylim(0, 1)
    axes.tick_params(axis='both', which='major', labelsize=8)
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


# def draw_fitness(image_path, fitness_result, image_show=False, image_save=False):
#     fitness_avg = fitness_result[0]
#     fitness_best = fitness_result[1]
#     num_generation = len(fitness_avg)

#     # create figure
#     fig, ax_main = plt.subplots(figsize=(PLOT_X2_SIZE, PLOT_Y2_SIZE), facecolor='w')

#     # plot
#     fitness_avg.insert(0, 0)
#     fitness_best.insert(0, 0)
#     ax_main.plot(fitness_avg,  color='b', linewidth=PLOT_LINE_WIDTH)
#     ax_main.plot(fitness_best, color='r', linewidth=PLOT_LINE_WIDTH)

#     # figure setting
#     max_ylim = max(fitness_best) + 0.02 if max(fitness_best) != 1 else 1.01
#     ax_main.grid()
#     ax_main.set_xlabel('Generation', fontdict={'fontsize': 10})
#     ax_main.set_ylabel('Fitness: Q',    fontdict={'fontsize': 10})
#     ax_main.tick_params(axis='both', which='major', labelsize=10)
#     ax_main.tick_params(axis='both', which='minor', labelsize=10)
#     ax_main.set_xlim([0, num_generation])
#     ax_main.set_ylim([0, max_ylim])
#     legen_text = ['fit. avg', 'fit. best']
#     ax_main.legend(legen_text, loc=0, fontsize='small', prop={'size': 10})

#     # save and show figure
#     plt.tight_layout()
#     if image_save:
#         plt.savefig(image_path, dpi=PLOT_DPI, format=PLOT_FORMAT, bbox_inches='tight', pad_inches=0.05)
#     if image_show:
#         plt.show()
#     plt.close(fig)


def draw_convergence_figure(num_network, num_generation, mu_list, ga_method, image_save=False, image_show=False):
    # folder_LFR = 'LFR_benchmark_1000\\'
    folder_LFR = ''

    for mu in mu_list:
        convergence_list = {}

        for method in ga_method:
            fit_best_avg = [0] * num_generation

            for i in range(0, num_network):
                pickle_path = FOLDER_FILE + folder_LFR + 'LFR_benchmark_1000_u=' + mu +'_net-' + str(i + 1) + ', experiment1-LFR-' + method + '.pickle'
                fitness_list = []

                if method is 'tpef':
                    fitness_list = ph.read_pickle_file(pickle_path)[1][2]
                else:
                    fitness_list = ph.read_pickle_file(pickle_path)[2]

                for j in range(0, num_generation):
                    fit_best_avg[j] += fitness_list[j]

            for i in range(0, num_generation):
                fit_best_avg[i] /= num_network

            fit_best_avg.insert(0, 0)
            convergence_list[method] = fit_best_avg

        # draw convergence figure
        image_path = FOLDER_IMAGE + 'LFR_benchmark_1000_u=' + mu + ', experiment1-LFR-convergence.png'
        draw_convergence(image_path, num_generation, convergence_list, ga_method, image_save=True, image_show=False)


def draw_convergence(image_path, num_generation, convergence_list, ga_method, image_save=False, image_show=False):
    # create figure
    fig, ax_main = plt.subplots(figsize=(PLOT_X2_SIZE, PLOT_Y2_SIZE), facecolor='w')

    # draw figure
    cm_index = 0
    for method in ga_method:
        fitness_best = convergence_list[method]
        ax_main.plot(fitness_best, color=COLOR_BAR_LIST[cm_index], linewidth=PLOT_LINE_WIDTH, marker=MARKER_LIST[cm_index], markersize=6, markevery=2, fillstyle='none')
        cm_index += 1

    # figure setting
    ax_main.grid()
    ax_main.set_xlabel('Generation', fontdict={'fontsize': 10})
    ax_main.set_ylabel('Avg. modularity Q', fontdict={'fontsize': 10})
    ax_main.tick_params(axis='both', which='major', labelsize=8)
    ax_main.tick_params(axis='both', which='minor', labelsize=8)
    ax_main.set_xlim([0, num_generation])
    legen_text = [method.upper() for method in ga_method]
    ax_main.legend(legen_text, loc=4, fontsize='small', prop={'size': 7})

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
def save_execution_time_table(file_path, table_result, mu_list, ga_method):
    with open(file_path, mode="w") as f:
        # title: mu
        f.write('Mixing parameter\t')
        for mu in mu_list:
            table_title = '{0}\t{0}\t'.format(mu)
            f.write(table_title)
        f.write('\n')

        # title: time_avg time_std
        f.write('Execution time\t')
        for mu in mu_list:
            table_title = 'Avg.\tStd.\t'
            f.write(table_title)
        f.write('\n')

        # content
        for method in ga_method:
            f.write('{0}\t'.format(method.upper()))

            for mu in mu_list:
                time_avg = round(table_result[method][mu][3], 4)
                time_std = round(table_result[method][mu][4], 4)
                f.write('{0}\t{1}\t'.format(time_avg, time_std))
            f.write('\n')
        f.close


def save_modularity_table(file_path, table_result, mu_list, ga_method):
    with open(file_path, mode="w") as f:
        # title: mu
        f.write('Mixing parameter\t')
        for mu in mu_list:
            table_title = '{0}\t{0}\t{0}\t'.format(mu)
            f.write(table_title)
        f.write('\n')

        # title: time_avg time_std
        f.write('Modularity Q\t')
        for mu in mu_list:
            f.write('Max.\tAvg.\tStd.\t')
        f.write('\n')

        # content
        for method in ga_method:
            f.write('{0}\t'.format(method.upper()))

            for mu in mu_list:
                q_max = round(table_result[method][mu][0], 4)
                q_avg = round(table_result[method][mu][1], 4)
                q_std = round(table_result[method][mu][2], 4)
                f.write('{0}\t{1}\t{2}\t'.format(q_max, q_avg, q_std))
            f.write('\n')
        f.close


def save_community_number_table(file_path, table_result, mu_list, ga_method):
    with open(file_path, mode="w") as f:
        # title: mu
        f.write('Mixing parameter\t')
        for mu in mu_list:
            table_title = '{0}\t'.format(mu)
            f.write(table_title)
        f.write('\n')

        # content
        for method in ga_method:
            f.write('{0}\t'.format(method.upper()))

            for mu in mu_list:
                c_avg = round(table_result[method][mu][0], 4)
                f.write('{0}\t'.format(c_avg))
            f.write('\n')
        f.close


# ###
# 4.main function
# ###
def main_function():
    initial_time = time.time()
    
    # LFR_benchmark parameters
    # mu_list     = ['0.01', '0.05', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6']
    mu_list     = ['0.01', '0.05', '0.1']
    ga_method   = ['lga', 'sga', 'tpef']
    # folder_LFR  = 'LFR_benchmark_1000\\'
    num_network    = 1
    num_generation = 50  # TPEF
    community_number = {}
    community_result = {}

    # read pickle files
    show_msg(' - Read pickle file')
    for method in ga_method:
        show_msg(' -- [Method]: {0}'.format(method))
        method_time = time.time()
        cluster_result = {}
        method_result = {}
        
        for mu in mu_list:
            show_msg(' --- [u={0}]'.format(mu))
            mu_time = time.time()
            LFR_name = FOLDER_FILE + 'LFR_benchmark_1000_u=' + mu
            c_list = []
            q_list = []
            time_list = []

            # LFR_benchmark_1000_u=0.01_net-1, experiment1-LFR-lga.pickle
            # LGA:  [indv, fit_avg, fit_best, Q_avg, Q_std, Time_avg, Time_std]
            # SGA:  [indv, fit_avg, fit_best, Q_avg, Q_std, Time_avg, Time_std]
            # TPEF: [[indv, fit_avg, fit_best], [indv, fit_avg, fit_best],
            #        Q_avg, Q_std, Time_avg, Time_std]
            for i in range(0, num_network):
                show_msg(' ---- Network-{0}:'.format(i + 1))
                pickle_path = LFR_name +'_net-' + str(i + 1) + ', experiment1-LFR-' + method + '.pickle'
                pickle_file = ph.read_pickle_file(pickle_path)

                if method is 'tpef':
                    c_list.append(len(pickle_file[1][0][INDV_PHENOTYPE]))
                    q_list.append(pickle_file[1][0][INDV_FITNESS])
                    time_list.append(pickle_file[4])
                else:
                    c_list.append(len(pickle_file[0][INDV_PHENOTYPE]))
                    q_list.append(pickle_file[0][INDV_FITNESS])
                    time_list.append(pickle_file[5])

            # for each method: Q_best, Q_avg, Q_std, time_avg, time_std
            method_result[mu] = []
            method_result[mu].append(max(q_list))
            method_result[mu].append(np.mean(q_list))
            method_result[mu].append(np.std(q_list))
            method_result[mu].append(np.mean(time_list))
            method_result[mu].append(np.std(time_list))
            # method_result[mu].append(np.mean(time_list))  # for normalize

            # community number
            cluster_result[mu] = []
            cluster_result[mu].append(np.mean(c_list))
            show_msg(' ---- Time: {0:^8} sec.'.format(str(round(time.time() - mu_time, 4))))

        community_number[method] = cluster_result
        community_result[method] = method_result
        show_msg(' -- [/Method] Time: {0:^8} sec.'.format(str(round(time.time() - method_time, 4))))

    # # normalize execution time
    # for mu in mu_list:
    #     time_max = 0
    #
    #     for method in ga_method:
    #         if community_result[method][mu][5] > time_max:
    #             time_max = community_result[method][mu][5]
    #         else:
    #             pass
    #
    #     for method in ga_method:
    #         community_result[method][mu][5] /= time_max

    # draw figures
    # draw execution time figure
    show_msg(' - Draw figure of execution time analysis')
    draw_time = time.time()
    image_path = FOLDER_IMAGE + 'figure1, execution time analysis-LFR.png'
    draw_execution_time_figure(image_path, community_result,
                               mu_list, ga_method,
                               image_save=True, image_show=False)
    show_msg(' -- Time: {0:^8} sec.'.format(str(round(time.time() - draw_time, 4))))

    # save modularity figure
    show_msg(' - Draw figure of modularity analysis')
    save_time = time.time()
    table_path = FOLDER_IMAGE + 'figure1, modularity analysis-LFR.png'
    save_modularity_figure(table_path, community_result,
                           mu_list, ga_method,
                           image_save=True, image_show=False)
    show_msg(' -- Time: {0:^8} sec.'.format(str(round(time.time() - save_time, 4))))

    # draw convergence
    show_msg(' - Draw figure of convergence')
    draw_time = time.time()
    draw_convergence_figure(num_network, num_generation,
                            mu_list, ga_method,
                            image_save=True, image_show=False)
    show_msg(' -- Time: {0:^8} sec.'.format(str(round(time.time() - draw_time, 4))))

    # save tables
    # save execution time table
    show_msg(' - Save execution time analysis table')
    save_time = time.time()
    table_path = FOLDER_IMAGE + 'table1, execution time analysis-LFR.txt'
    save_execution_time_table(table_path, community_result, mu_list, ga_method)
    show_msg(' -- Time: {0:^8} sec.'.format(str(round(time.time() - save_time, 4))))

    # save modularity table
    show_msg(' - Save modularity analysis table')
    save_time = time.time()
    table_path = FOLDER_IMAGE + 'table1, modularity analysis-LFR.txt'
    save_modularity_table(table_path, community_result, mu_list, ga_method)
    show_msg(' -- Time: {0:^8} sec.'.format(str(round(time.time() - save_time, 4))))

    # save community number table
    show_msg(' - Save community number table')
    save_time = time.time()
    table_path = FOLDER_IMAGE + 'table1, community number-LFR.txt'
    save_community_number_table(table_path, community_number, mu_list, ga_method)
    show_msg(' -- Time: {0:^8} sec.'.format(str(round(time.time() - save_time, 4))))

    show_msg(' Total time: {0:^4} seconds'.format(round(time.time() - initial_time, 4)))

if __name__ == '__main__':
    main_function()
