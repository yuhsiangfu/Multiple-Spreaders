# Multiple-Spreaders
The information about this repository is as follows.

## Citation
Fu, Y. H., Huang, C. Y., & Sun, C. T. (2016). Using a two-phase evolutionary framework to select multiple network spreaders based on community structure. Physica A: Statistical Mechanics and its Applications, 461, 840-853.

## Abstract
Using network community structures to identify multiple influential spreaders is an appropriate method for analyzing the dissemination of information, ideas and infectious diseases. For example, data on spreaders selected from groups of customers who make similar purchases may be used to advertise products and to optimize limited resource allocation. Other examples include community detection approaches aimed at identifying structures and groups in social or complex networks. However, determining the number of communities in a network remains a challenge. In this paper we describe our proposal for a two-phase evolutionary framework (TPEF) for determining community numbers and maximizing community modularity. Lancichinetti–Fortunato–Radicchi benchmark networks were used to test our proposed method and to analyze execution time, community structure quality, convergence, and the network spreading effect. Results indicate that our proposed TPEF generates satisfactory levels of community quality and convergence. They also suggest a need for an index, mechanism or sampling technique to determine whether a community detection approach should be used for selecting multiple network spreaders.

The url of the paper is https://doi.org/10.1016/j.physa.2016.06.042.

## Setting of the execution environment
In this paper, we used Python 3.4, NetworkX 1.9.1, Numpy 1.9.2 and Scipy 0.15.1 for programming. Also, for the IDE of Python, we recommend the PyCharm community version.

However, the Python 3.4 is no longer compatible for `Conda` to create the `env` environment. Therefore, you coulde add the mirror channel to `Conda` by using `conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/`. Then, you could use `conda create -n Python34 python=3.4 anaconda` to create the `Conda env` of Python3.4.

## Simple code usage
For real-world datasets:
1. TBD
2. use `experiment1_execution time analysis, real.py` to run performance analysis of different evolutionary algorithms and create `file\*.pickle`, e.g. `dolphins_gcc, experiment1-real-lga.pickle`, `dolphins_gcc, experiment1-real-sga.pickle` and `dolphins_gcc, experiment1-real-tpef.pickle`.
3. use `figure1_execution time analysis, real.py` to draw plots `image\*.png` and save tables of community information `image\*.txt`, e.g., `dolphins_gcc, experiment1-real-convertence.png`, `dolphins_gcc, experiment1-real-lga-fitness.png`, `dolphins_gcc, experiment1-real-lga-network.png`, `table1, community number-real.txt`, `table1, execution time analysis-real.txt` and `table1, modularity analysis-real.txt`.
4. use `table6_network statistics, real.py` to create table of network statistics `image\*.txt`, e.g., `table6, network statistics.txt`

For LFR behcnmark datasets:
1. TBD
2. use `experiment1_execution time analysis, LFR.py` to run performance analysis of different evolutionary algorithms and create `file\*.pickle`, e.g., `LFR_benchmark_1000_u=0.01_net-1, experiment1-LFR-lga.pickle`, `LFR_benchmark_1000_u=0.01_net-1, experiment1-LFR-sga.pickle` and `LFR_benchmark_1000_u=0.01_net-1, experiment1-LFR-tpef.pickle`.
3. 

## Notification
1. You are free to use the codes for educational purposes.
2. Our coding style may not as good as you expect, but it works.
3. We are glad to hear your improvements of the codes.
4. Any questions please contact yuhisnag.fu@gmail.com.

Best regards,
Yu-Hsiang Fu 20220103 updated.
