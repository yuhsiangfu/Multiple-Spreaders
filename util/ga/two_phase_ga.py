"""
Two-Phase Evolutionary Framework
@auth: Yu-Hsiang Fu
@date: 2016/05/02
"""
# ###
# 1.Imoprt packages and modulars
# ###
# import packages
# import copy as c
import numpy as np
# import random as r
import sys
import time

# import modulars
import util.ga.phase1_ga as p1ga
import util.ga.phase2_ga as p2ga


# ###
# 2.Declare variables
# ###
INDV_FITNESS = 'fitness'
INDV_GENOTYPE = 'genotype'
INDV_PHENOTYPE = 'phenotype'
# TPEF_PHASE1 = 'tpef-phase1'
# TPEF_PHASE2 = 'tpef-phase2'


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
def two_phase_evolutionary_framework(
    G, num_evolution=1,
    p1_num_generation=100, p1_size_population=50,
    p1_rate_selection=0.1, p1_rate_crossover=0.8, p1_rate_mutation=0.05,
    p2_num_generation=100, p2_size_population=50,
    p2_rate_selection=0.1, p2_rate_crossover=0.8, p2_rate_mutation=0.05,
    show_progress=False):

    # initial variables
    evo_best = {}
    best_list = []
    time_list = []

    for i in range(0, num_evolution):
        evo_time = time.time()

        show_msg(' ---- TPEF: evolution {0}'.format(i + 1))

        # phase-1: determine clusters
        p1_best = p1ga.locus_based_genetic_algorithm(
                    G,
                    p1_num_generation, p1_size_population,
                    p1_rate_selection, p1_rate_crossover, p1_rate_mutation,
                    show_progress)

        # phase-2: maximize modularity
        p2_best = p2ga.standard_genetic_algorithm(
                    G, p1_best[0],
                    p2_num_generation, p2_size_population,
                    p2_rate_selection, p2_rate_crossover, p2_rate_mutation,
                    show_progress)

        # maintain evo_best, 0: p1_best, 1: p2_best
        if not evo_best:
            evo_best = [p1_best, p2_best]
        elif p2_best[0][INDV_FITNESS] > evo_best[1][0][INDV_FITNESS]:
            evo_best = [p1_best, p2_best]
        else:
            pass

        best_list.append(p2_best[0][INDV_FITNESS])
        time_list.append(time.time() - evo_time)

    # calculate avg. and std. values of fintess and time
    evo_best.append(np.mean(best_list))
    evo_best.append(np.std(best_list))
    evo_best.append(np.mean(time_list))
    evo_best.append(np.std(time_list))
    return evo_best
