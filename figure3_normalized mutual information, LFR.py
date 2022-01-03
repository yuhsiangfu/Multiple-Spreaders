"""
Figure3: normailzed mutual information, LFR_benchmark, with tables
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
from sklearn.metrics.cluster import normalized_mutual_info_score as nmi

# import constants
from util.constant.constant_folder import FOLDER_FILE
from util.constant.constant_folder import FOLDER_IMAGE
from util.constant.constant_graph import NODE_COMMUNITY


# ###
# 2.Declare variables
# ###
# GA variable
INDV_FITNESS   = 'fitness'
INDV_GENOTYPE  = 'genotype'
INDV_PHENOTYPE = 'phenotype'

# figure variables
COLOR_LIST      = ['b', 'g', 'r', 'm']
MARKER_LIST     = ['^', 'v', '8', 'H', 's', 'D']
PLOT_LINE_WIDTH = 1.5
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
def draw_NMI_figure(image_path, NMI_avg, NMI_std, mu_list, ga_method, image_save=False, image_show=False):
    # create figure
    fig, axes = plt.subplots(figsize=(PLOT_X_SIZE, PLOT_Y_SIZE), facecolor='w')

    # draw figure
    cm_index = 0
    for method in ga_method:
        axes.plot(NMI_avg[method], color=COLOR_LIST[cm_index], linewidth=PLOT_LINE_WIDTH, marker=MARKER_LIST[cm_index], markersize=5, markevery=1, fillstyle='none')
        cm_index += 1

    # figure setting
    legend_text = [method.upper() for method in ga_method]
    xtick_list = mu_list
    axes.grid()
    axes.set_xlabel('Mixing parameter, u', fontdict={'fontsize': 10})
    axes.set_ylabel('Avg. NMI value',      fontdict={'fontsize': 10})
    axes.set_xlim(0, 7.02)
    axes.set_ylim(0, 1.02)
    axes.set_xticklabels(xtick_list)
    axes.tick_params(axis='both', which='major', labelsize=8)
    axes.tick_params(axis='both', which='minor', labelsize=8)
    axes.legend(legend_text, loc=0, fontsize='small', prop={'size': 7})

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
def save_NMI_table(file_path, NMI_max, NMI_avg, NMI_std, mu_list, ga_method):
    with open(file_path, mode="w") as f:
        # title: mu
        f.write('Mixing parameter\t')
        for mu in mu_list:
            table_title = '{0}\t{0}\t{0}\t'.format(mu)
            f.write(table_title)
        f.write('\n')

        # title: time_avg time_std
        f.write('NMI\t')
        for mu in mu_list:
            f.write('Max.\tAvg.\tStd.\t')
        f.write('\n')

        # content
        for method in ga_method:
            f.write('{0}\t'.format(method.upper()))

            for i in range(0, len(mu_list)):
                nmi_max = round(NMI_max[method][i], 4)
                nmi_avg = round(NMI_avg[method][i], 4)
                nmi_std = round(NMI_std[method][i], 4)
                f.write('{0}\t{1}\t{2}\t'.format(nmi_max, nmi_avg, nmi_std))
            f.write('\n')
        f.close


# ###
# 4.main function
# ###
def main_function():
    initial_time = time.time()

    # LFR_benchmark parameters
    # mu_list   = ['0.01', '0.05', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6']
    mu_list = ['0.01', '0.05', '0.1']
    ga_method = ['lga', 'sga', 'tpef']
    folder_LFR = 'LFR_benchmark_1000\\'
    num_network = 1

    # read gpickle and pickle files
    show_msg(' - Read gpickle and pickle files')
    NMI_max = {}
    NMI_avg = {}
    NMI_std = {}

    for method in ga_method:
        show_msg(' -- [Method]: {0}'.format(method))
        method_time = time.time()

        # calculate NMI_avg, NMI_std for each 'u'
        NMI_max[method] = []
        NMI_avg[method] = []
        NMI_std[method] = []

        for mu in mu_list:
            show_msg(' --- [u={0}]'.format(mu))
            mu_time = time.time()
            nmi_list = []

            # LGA:  [indv, fit_avg, fit_best, Q_avg, Q_std, Time_avg, Time_std]
            # SGA:  [indv, fit_avg, fit_best, Q_avg, Q_std, Time_avg, Time_std]
            # TPEF: [[indv, fit_avg, fit_best], [indv, fit_avg, fit_best],
            #        Q_avg, Q_std, Time_avg, Time_std]
            for i in range(0, num_network):
                show_msg(' ---- Network-{0}:'.format(i + 1))

                # gpickle: LFR_benchmark_1000_u=0.01_net-1, analysis.gpickle
                gpickle_path = FOLDER_FILE + folder_LFR
                gpickle_path += 'LFR_benchmark_1000_u=' + mu + '_net-' + str(i + 1) + ', analysis.gpickle'
                G = gh.read_gpickle_file(gpickle_path)

                # pickle: LFR_benchmark_1000_u=0.01_net-1, experiment1-LFR-lga.pickle
                pickle_path = FOLDER_FILE
                pickle_path += 'LFR_benchmark_1000_u=' + mu + '_net-' + str(i + 1) + ', experiment1-LFR-' + method + '.pickle'
                pickle_file = ph.read_pickle_file(pickle_path)

                # create true_community
                true_community = [G.node[i][NODE_COMMUNITY] for i in G]

                # create identified_community
                node_to_gene = {}
                gene_index = 0
                for i in G:
                    node_to_gene[i] = c.copy(gene_index)
                    gene_index += 1

                indf_community = [0] * G.number_of_nodes()
                community_list = []
                community_id = 1

                if method is 'tpef':
                    community_list = pickle_file[1][0][INDV_PHENOTYPE]
                else:
                    community_list = pickle_file[0][INDV_PHENOTYPE]

                for com in community_list:
                    for i in com:
                        indf_community[node_to_gene[i]] = c.copy(community_id)
                    community_id += 1

                # calculate NMI value
                nmi_list.append(nmi(true_community, indf_community))

            NMI_max[method].append(max(nmi_list))
            NMI_avg[method].append(np.mean(nmi_list))
            NMI_std[method].append(np.std(nmi_list))
            show_msg(' ---- Time: {0:^8} sec.'.format(str(round(time.time() - mu_time, 4))))
        show_msg(' -- [/Method] Time: {0:^8} sec.'.format(str(round(time.time() - method_time, 4))))

    # draw NMI figure
    show_msg(' - Draw figure of NMI value')
    draw_time = time.time()
    image_path = FOLDER_IMAGE + 'figure3, normalized mutual information-LFR.png'
    draw_NMI_figure(image_path,
                    NMI_avg, NMI_std,
                    mu_list, ga_method,
                    image_save=True, image_show=False)
    show_msg(' -- Time: {0:^8} sec.'.format(str(round(time.time() - draw_time, 4))))

    # save NMI table
    show_msg(' - Save NMI table')
    save_time = time.time()
    table_path = FOLDER_IMAGE + 'table3, normalized mutual information-LFR.txt'
    save_NMI_table(table_path, NMI_max, NMI_avg, NMI_std, mu_list, ga_method)
    show_msg(' -- Time: {0:^8} sec.'.format(str(round(time.time() - save_time, 4))))

    show_msg(' Total time: {0:^4} seconds'.format(round(time.time() - initial_time, 4)))

if __name__ == '__main__':
    main_function()