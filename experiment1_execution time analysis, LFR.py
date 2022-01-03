"""
Experiment1: execution time analysis, LFR benchmark
@auth: Yu-Hsiang Fu
@date: 2016/05/03
"""
# ###
# 1.Imoprt packages and modulars
# ###
# import packages
# import copy as c
# import numpy as np
# import random as r
import sys
import time

# import modulars
import util.ga.locus_ga as lga
import util.ga.standard_ga as sga
import util.ga.two_phase_ga as tpef
import util.handler.gpickle_handler as gh
import util.handler.pickle_handler as ph

# import constants
from util.constant.constant_folder import FOLDER_FILE
from util.constant.constant_folder import FOLDER_IMAGE


# ###
# 2.Declare variables
# ###
INDV_FITNESS = 'fitness'
INDV_GENOTYPE = 'genotype'
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
                     #('LFR_benchmark_1000_u=0.2', 40),   # |C| = 40
                     #('LFR_benchmark_1000_u=0.3', 40),   # |C| = 40
                     #('LFR_benchmark_1000_u=0.4', 40),   # |C| = 40
                     #('LFR_benchmark_1000_u=0.5', 40),   # |C| = 40
                     #('LFR_benchmark_1000_u=0.6', 40),   # |C| = 40
                     ]

    # Overall parameters
    num_network = 1
    num_evolution = 1

    # LGA parameters
    lga_num_generation = 100
    lga_size_population = 50
    lga_rate_selection = 0.1
    lga_rate_crossover = 0.8
    lga_rate_mutation = 0.05

    # SGA parameters
    sga_num_generation = 100
    sga_size_population = 50
    sga_rate_selection = 0.1
    sga_rate_crossover = 0.8
    sga_rate_mutation = 0.05

    # TPEF parameters
    p1_num_generation = 50
    p1_size_population = 25
    p1_rate_selection = 0.1
    p1_rate_crossover = 0.8
    p1_rate_mutation = 0.05

    p2_num_generation = 50
    p2_size_population = 25
    p2_rate_selection = 0.1
    p2_rate_crossover = 0.8
    p2_rate_mutation = 0.05

    # read gpickle file of network
    folder_LFR = 'LFR_benchmark_1000\\'

    for net in FILENAME_LIST:
        start_time = time.time()
        show_msg(' - [Net] ' + net[0] + ':')

        for i in range(0, num_network):
            show_msg(' -- Network-{0}:'.format(i + 1))
            net_name = net[0] +'_net-' + str(i + 1)

            # read gpickle file: LFR_benchmark_1000_u=0.01_net-1, analysis.gpickle
            show_msg(' --- Read gpickle file')
            read_time = time.time()
            g_path = FOLDER_FILE + folder_LFR + net_name + ', analysis.gpickle'
            G = ph.read_pickle_file(g_path)
            show_msg(' ---- Time: {0:^8} sec.'.format(str(round(time.time() - read_time, 4))))

            """
            LGA: [indv, fit_avg, fit_best, Q_avg, Q_std, Time_avg, Time_std]
            """
            show_msg(' --- Locus-based genetic algorithm (LGA)')
            lga_time = time.time()
            lga_result = lga.locus_based_genetic_algorithm(
                            G, num_evolution,
                            lga_num_generation, lga_size_population,
                            lga_rate_selection, lga_rate_crossover, lga_rate_mutation,
                            show_progress=False)
            show_msg(' ---- Time: {0:^8} sec.'.format(str(round(time.time() - lga_time, 4))))
            #
            lga_path = FOLDER_FILE + net_name + ', experiment1-LFR-lga.pickle'
            ph.write_pickle_file(lga_result, lga_path)

            """
            SGA: [indv, fit_avg, fit_best, Q_avg, Q_std, Time_avg, Time_std]
            """
            show_msg(' --- Standard genetic algorithm (SGA)')
            sga_time = time.time()
            sga_result = sga.standard_genetic_algorithm(
                            G, net[1], num_evolution,
                            sga_num_generation, sga_size_population,
                            sga_rate_selection, sga_rate_crossover, sga_rate_mutation,
                            show_progress=False)
            show_msg(' ---- Time: {0:^8} sec.'.format(str(round(time.time() - sga_time, 4))))
            #
            sga_path = FOLDER_FILE + net_name + ', experiment1-LFR-sga.pickle'
            ph.write_pickle_file(sga_result, sga_path)

            """
            TPEF: [[indv, fit_avg, fit_best], [indv, fit_avg, fit_best],
                   Q_avg, Q_std, Time_avg, Time_std]
            """
            show_msg(' -- Two-Phase Evolutionary Framework (TPEF)')
            tpef_time = time.time()
            tpef_result = tpef.two_phase_evolutionary_framework(
                            G, num_evolution,
                            p1_num_generation, p1_size_population,
                            p1_rate_selection, p1_rate_crossover, p1_rate_mutation,
                            p2_num_generation, p2_size_population,
                            p2_rate_selection, p2_rate_crossover, p2_rate_mutation,
                            show_progress=False)
            show_msg(' ---- Time: {0:^8} sec.'.format(str(round(time.time() - tpef_time, 4))))
            #
            tpef_path = FOLDER_FILE + net_name + ', experiment1-LFR-tpef.pickle'
            ph.write_pickle_file(tpef_result, tpef_path)

        show_msg(' - [Net] Time: {0:^8} sec.'.format(str(round(time.time() - start_time, 4))))
    show_msg(' Total time: {0:^4} seconds'.format(round(time.time() - initial_time, 4)))

if __name__ == '__main__':
    main_function()
