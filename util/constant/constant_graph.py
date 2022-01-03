"""
Constant: graph
@auth: Yu-Hsiang Fu
@date: 2014/09/28
"""
# 節點變數
NODE_ID = 'node_id'
NODE_EGO_NETWORK = 'node_ego-network'
NODE_LAYOUT_XY = 'node_layout-xy'

# 節點屬性
NODE_BETWEENNESS = 'node_betweenness'
NODE_CLOSENESS = 'node_closeness'
NODE_CLUSTERING = 'node_clustering'
NODE_COMMUNITY = 'node_community'
NODE_DEGREE = 'node_degree'
NODE_K_SHELL = 'node_k-shell'
NODE_NEIGHBOR_CORE = 'node_neighbor-core'
NODE_PAGERANK = 'node_pagerank'
NODE_LOCAL_FEATURES = 'node_local-features'      # Li
NODE_GLOBAL_DIVERSITY = 'node_global-diversity'  # Ei
NODE_INFLUENCE = 'node_influence'                # IFi = Ei * Li

# 節點的鄰居屬性
NEIGHBORS_BETWEENNESS = 'neighbors_betweenness'
NEIGHBORS_CLOSENESS = 'neighbors_closeness'
NEIGHBORS_CLUSTERING = 'neighbors_clustering'
NEIGHBORS_DEGREE = 'neighbors_degree'
NEIGHBORS_K_SHELL = 'neighbors_k-shell'
NEIGHBORS_PAGERANK = 'neighbors_pagerank'
NEIGHBORS_GLOBAL_DIVERSITY = 'neighbors_global-diversity'
NEIGHBORS_LOCAL_FEATURES = 'neighbors_local-features'
NEIGHBORS_INFLUENCE = 'neighbors_influence'

# 網絡變數
GRAPH_NUM_EDGES = 'graph_num_edges'
GRAPH_NUM_NODES = 'graph_num_nodes'
GRAPH_DENSITY = 'graph_density'

# 網絡屬性: avg, max, min
GRAPH_AVG_BETWEENNESS = 'graph_avg-betweenness'
GRAPH_AVG_CLOSENESS = 'graph_avg-closeness'
GRAPH_AVG_CLUSTERING = 'graph_avg-clustering'
GRAPH_AVG_DEGREE = 'graph_avg-degree'
GRAPH_MAX_DEGREE = 'graph_max-degree'
GRAPH_AVG_DEGREE_SQUARE = 'graph_avg-degree-square'
GRAPH_AVG_K_SHELL = 'graph_avg-k-shell'
GRAPH_MAX_K_SHELL = 'graph_max-k-shell'
GRAPH_AVG_GLOBAL_DIVERSITY = 'graph_avg-global-diversity'
GRAPH_AVG_LOCAL_FEATURES = 'graph_avg-local-features'
GRAPH_AVG_ST_PATH = 'graph_avg-shortest-path'
GRAPH_DEGREE_ASSORTATIVITY = 'graph_degree-assortativity'
GRAPH_DEGREE_HETEROGENEITY = 'graph_degree-heterogeneity'
GRAPH_THEORETICAL_THRESHOLD = 'graph_theoretical-threshold'  # SIR threshold
