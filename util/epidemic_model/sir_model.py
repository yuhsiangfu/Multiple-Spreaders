"""
SIR model (set ver.)
@auth:  Yu-Hsiang Fu
@date:  2014/10/02
@check: 2016/05/03
"""
# ###
# 1.Imoprt packages and modulars
# ###
# import packages
import copy as c
import numpy as np
import random as r
# import sys


# ###
# 2.Define functions
# ###
# convert S node: to I nodes: S -> I
def convert_susceptible_to_infected(G, susceptible_set, infected_set, rate_infection=0.1):
    current_infected = set()

    for ni in infected_set:
        # shuffle neighbors
        neighbor_list = G.neighbors(ni)
        np.random.shuffle(neighbor_list)

        # infect susceptible neighbors
        for nb in neighbor_list:
            if (nb in susceptible_set) and (r.random() < rate_infection):
                current_infected.add(nb)
    return current_infected


# convert I nodes to R nodes: I -> R
def convert_infected_to_recovered(infected_set, recovered_set, rate_recovery=1):
    current_recovered = set()

    # Case 1: if rate_recovery == 1, then move all I nodes to R state
    if rate_recovery == 1:
        current_recovered = current_recovered | infected_set # s.union(t)
    # Case 2: if move I nodes to R state by rate_recovery
    else:
        for ni in infected_set:
            if (r.random() <= rate_recovery):
                current_recovered.add(ni)
    return current_recovered


# spreading and infecting neighbor nodes
def spreading(G, initial_node, num_time_step=50, rate_infection=0.1, rate_recovery=1):
    # calculate avg. proportion of infected nodes
    num_node = c.copy(G.number_of_nodes())
    num_time_step += 1
    spreading_result = {}

    # create S, I and R states
    S = set() | set(G.nodes())  # S = S + G.node
    I = set()                   # I
    R = set()                   # R

    # total time steps of simulation: num_time_step
    for t in range(0, num_time_step):
        I_t = set()
        R_t = set()

        # Case 1：t == 0, move initial nodes to I state
        if t == 0:
            I = I | set(initial_node)  # I = I + I(t=0)
            S = S - I                  # S = S - I(t=0)
        # Case 2: t > 0, infect neighbors of I nodes
        else:
            # I(t), infected neighbor nodes
            I_t = convert_susceptible_to_infected(G, S, I, rate_infection)

            # R(t), nodes from I state to R state
            R_t = convert_infected_to_recovered(I, R, rate_recovery)

            # update all states
            R = R | R_t  # R = R + R(t)
            I = I | I_t  # I = I + I(t)
            I = I - R_t  # I = I - R(t)
            S = S - I_t  # S = S - I(t)

        # record current result: p(t) = R(t)/|V| or p(t) = 1 - S(t)/|V|
        # spreading_result[t] = np.divide(len(R), num_node)
        spreading_result[t] = (1 - np.divide(len(S), num_node))
    return spreading_result
