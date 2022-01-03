"""
Standard Genetic Algorithm (SGA)
@auth: Yu-Hsiang Fu
@date: 2016/04/28
"""
# ###
# 1.Imoprt packages and modulars
# ###
# import packages
import copy as c
import numpy as np
import random as r
import sys
import time

# import constants
from util.constant.constant_graph import NODE_DEGREE


# ###
# 2.Declare variables
# ###
# porgram variables
GENE_TO_NODE = {}
NODE_TO_GENE = {}
NEIGHBOR_LIST = {}
NUMBER_COMMUNITY = 2

# GA variables
INDV_LENGTH = 0
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


def initialization(G, indv):
    global GENE_TO_NODE, NODE_TO_GENE
    global INDV_LENGTH, NEIGHBOR_LIST, NUMBER_COMMUNITY

    INDV_LENGTH = c.copy(G.number_of_nodes())
    NUMBER_COMMUNITY = c.copy(len(indv[INDV_PHENOTYPE]))

    # mapping gene-to-node and node-to-gene
    gene_index = 0
    for i in G:
        GENE_TO_NODE[gene_index] = i
        NODE_TO_GENE[i] = gene_index
        gene_index += 1

    # create neighbor list
    for i in G:
        NEIGHBOR_LIST[i] = list(G.neighbors(i))
        G.node[i][NODE_DEGREE] = len(NEIGHBOR_LIST[i])
    return(G)


# ###
# generate function
# ###
def generate_genotype():
    genotype = [r.randint(1, NUMBER_COMMUNITY) for i in range(0, INDV_LENGTH)]
    return genotype


def generate_phenotype(indv):
    # create community list, map node_index to node_id
    community_list = {}
    for i in range(INDV_LENGTH):
        node_id = GENE_TO_NODE[i]
        ci = indv[INDV_GENOTYPE][i]

        if ci in community_list:
            community_list[ci].append(node_id)
        else:
            community_list[ci] = [node_id]
    return list(community_list.values())


def generage_an_individual():
    individual = {}
    individual[INDV_GENOTYPE] = generate_genotype()
    return individual


def generate_two_individuals(indv_pool, rate_crossover=0.5):
    # random select parent
    parent_x = {}
    parent_y = {}
    pool_size = len(indv_pool)

    if pool_size == 1:
        parent_x = c.deepcopy(indv_pool[0][INDV_GENOTYPE])
        parent_y = generage_an_individual()
    else:
        parent_index = r.sample(range(0, pool_size), 2)
        parent_x = c.deepcopy(indv_pool[parent_index[0]][INDV_GENOTYPE])
        parent_y = c.deepcopy(indv_pool[parent_index[1]][INDV_GENOTYPE])

    # uniform corssover
    new_indv1 = {}
    new_indv2 = {}
    new_indv1[INDV_GENOTYPE] = []
    new_indv2[INDV_GENOTYPE] = []

    # assign gene value
    if r.random() <= rate_crossover:
        for i in range(0, INDV_LENGTH):
            # mask == 0, px[i] -> idv1[i], py[i] -> idv2[i]
            if r.randint(0, 1) == 0:
                new_indv1[INDV_GENOTYPE].append(parent_x[i])
                new_indv2[INDV_GENOTYPE].append(parent_y[i])
            # mask == 1, px[i] -> idv2[i], py[i] -> idv1[i]
            else:
                new_indv1[INDV_GENOTYPE].append(parent_y[i])
                new_indv2[INDV_GENOTYPE].append(parent_x[i])
    else:
        new_indv1[INDV_GENOTYPE] = parent_x
        new_indv2[INDV_GENOTYPE] = parent_y
    return new_indv1, new_indv2


def initial_population(p1_best, size_population=100, rate_mutation=0.05):
    # transform locus-based encode to straightforward encode
    com_index = 1
    new_indv = {}
    new_indv[INDV_GENOTYPE] = [0] * INDV_LENGTH
    for com in sorted(p1_best[INDV_PHENOTYPE]):
        for g in com:
            new_indv[INDV_GENOTYPE][NODE_TO_GENE[g]] = c.copy(com_index)
        com_index += 1

    # initial population
    indv_pool = [c.deepcopy(new_indv)]
    for i in range(1, size_population):
        tmp_indv = c.deepcopy(new_indv)
        for j in range(0, INDV_LENGTH):
            if r.random() <= rate_mutation:
                tmp_indv[INDV_GENOTYPE][j] = r.randint(1, NUMBER_COMMUNITY)
            else:
                pass
        indv_pool.append(tmp_indv)
    return indv_pool


# ###
# modularity function
# ###
def modularity(G, community_list):
    # check empty
    if len(community_list) != NUMBER_COMMUNITY:
        return 0

    # ls, ds variables
    intra_degree = {i: 0 for i in range(0, len(community_list))}  # ds
    intra_edges  = {i: 0 for i in range(0, len(community_list))}  # ls

    # calculate ds, time complexity: O(V)
    community_index = 0
    community_id = {}

    for com in community_list:
        tmp_index = c.copy(community_index)
        for i in com:
            intra_degree[tmp_index] += G.node[i][NODE_DEGREE]
            community_id[i] = tmp_index
        community_index += 1

    # calculate ls, time complexity: O(E)
    for (ei, ej) in G.edges():
        if community_id[ei] == community_id[ej]:
            intra_edges[community_id[ei]] += 1
        else:
            pass

    # calculate modularity Q, time complexity: O(C)
    modularity = 0
    num_edges = G.number_of_edges()
    for i in range(0, len(community_list)):
        ls = intra_edges[i] / num_edges
        ds = pow((intra_degree[i] / (2 * num_edges)), 2)
        modularity += (ls - ds)
    return modularity


# ###
# genetic operatin function
# ###
def selection(indv_pool, size_population=100, rate_selection=0.1):
    # truncate selection
    cut_index = int(rate_selection * size_population)
    indv_pool = indv_pool[0:cut_index]
    return indv_pool


def crossover(indv_pool, size_population=100, rate_crossover=0.8):
    pool_size = len(indv_pool)
    empty_size = size_population - len(indv_pool)
    new_pool = c.deepcopy(indv_pool)

    if (empty_size % 2) == 0:
        for i in range(pool_size, size_population, 2):
            new_indv1, new_indv2 = generate_two_individuals(indv_pool, rate_crossover)
            new_pool.append(new_indv1)
            new_pool.append(new_indv2)
    else:
        for i in range(pool_size, size_population - 1, 2):
            new_indv1, new_indv2 = generate_two_individuals(indv_pool, rate_crossover)
            new_pool.append(new_indv1)
            new_pool.append(new_indv2)
        new_pool.append(generate_two_individuals(indv_pool, rate_crossover)[r.randint(0, 1)])
    return new_pool


def mutation(indv_pool, size_population=100, rate_mutation=0.05):
    # bit-by-bit mutation based on distribution of neighbors' community_id
    for i in range(0, size_population):
        indv = indv_pool[i][INDV_GENOTYPE]

        for j in range(0, INDV_LENGTH):
            if r.random() <= rate_mutation:
                node_id = GENE_TO_NODE[j]
                indv[j] = r.choice([indv[NODE_TO_GENE[nb]] for nb in NEIGHBOR_LIST[node_id]])
            else:
                pass
    return indv_pool


# ###
# major function
# ###
def evaluation(G, indv_pool, size_population=100):
    for i in range(0, size_population):
        indv = indv_pool[i]
        indv[INDV_PHENOTYPE] = generate_phenotype(indv)
        indv[INDV_FITNESS] = modularity(G, indv[INDV_PHENOTYPE])
    indv_pool = sorted(indv_pool, key=lambda x: x[INDV_FITNESS], reverse=True)
    return indv_pool


def standard_genetic_algorithm(G, p1_best, num_generation=100, size_population=100, rate_selection=0.1, rate_crossover=0.5, rate_mutation=0.05, show_progress=False):
    if show_progress:
        show_msg(' ----- Phase 2: maximize modularity')
    else:
        pass

    # initial variables
    fitness_avg = []
    fitness_best = []
    G = initialization(G, p1_best)

    # initial individual pool by p1_best
    indv_pool = initial_population(p1_best, size_population, rate_mutation)

    # genetic operation
    indv_best = {}

    for j in range(0, num_generation):
        # show_progress: generateion number
        if show_progress:
            if j is 0:
                show_msg(' ------ Generation {0}'.format(j+1))
            elif ((j + 1) % 10) is 0:
                show_msg(' ------ Generation {0}'.format(j+1))
            else:
                pass
        else:
            pass

        # evuluate individuals
        indv_pool = evaluation(G, indv_pool, size_population)

        # maintain indv_best
        if not indv_best:
            indv_best = c.deepcopy(indv_pool[0])
        elif indv_pool[0][INDV_FITNESS] > indv_best[INDV_FITNESS]:
            indv_best = c.deepcopy(indv_pool[0])
        else:
            pass

        # record fitness_avg and fitness_best
        fitness_avg.append(np.mean([indv[INDV_FITNESS] for indv in indv_pool]))
        fitness_best.append(indv_best[INDV_FITNESS])

        # stop condition
        if (j + 1) == num_generation:
            break
        else:
            pass

        # genetic operation: selection, crossover and mutation
        indv_pool = selection(indv_pool, size_population, rate_selection)
        indv_pool = crossover(indv_pool, size_population, rate_crossover)
        indv_pool = mutation(indv_pool, size_population, rate_mutation)
    return [indv_best, fitness_avg, fitness_best]
