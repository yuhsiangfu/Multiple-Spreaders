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
1. use `experiment1_execution time analysis, real.py` to run performance analysis of different evolutionary algorithms and create `file\*.pickle`, e.g. <br>
`dolphins_gcc, experiment1-real-lga.pickle`, <br>
`dolphins_gcc, experiment1-real-sga.pickle` and <br>
`dolphins_gcc, experiment1-real-tpef.pickle`.
2. use `figure1_execution time analysis, real.py` to draw plots `image\*.png` and save tables of community information `image\*.txt`, e.g., <br>
`dolphins_gcc, experiment1-real-convertence.png`, <br>
`dolphins_gcc, experiment1-real-lga-fitness.png`, <br>
`dolphins_gcc, experiment1-real-lga-network.png`, <br>
`table1, community number-real.txt`, <br>
`table1, execution time analysis-real.txt` and <br>
`table1, modularity analysis-real.txt`.
3. use `table6_network statistics, real.py` to create table of network statistics `image\*.txt`, e.g., `table6, network statistics.txt`
4. please see example files in `image\example_real`.

For LFR behcnmark datasets:
1. use `experiment1_execution time analysis, LFR.py` to run performance analysis of different evolutionary algorithms and create `file\*.pickle`, e.g., <br>
`LFR_benchmark_1000_u=0.01_net-1, experiment1-LFR-lga.pickle`, <br>
`LFR_benchmark_1000_u=0.01_net-1, experiment1-LFR-sga.pickle` and <br>
`LFR_benchmark_1000_u=0.01_net-1, experiment1-LFR-tpef.pickle`.
2. use `figure1_execution time analysis, LFR.py` to draw plots `image\*.png` and save tables of community information `image\*.txt`, e.g., <br>
`figure1, execution time analysis-LFR.png`, <br>
`figure1, modularity analysis-LFR.png`, <br>
`LFR_benchmark_1000_u=0.01, experiment1-LFR-convergence.png`, <br>
`table1, community number-LFR.txt`, <br>
`table1, execution time analysis-LFR.txt` and <br>
`table1, modularity analysis-LFR.txt`.
3. use `figure3_normalized mutual information, LFR.py` to save the table of normalized mutual information (NMI) `image\*.txt`, e.g., ``.
 `image\*.txt`, e.g., `table3, normalized mutual information-LFR.txt`.
4. use `experiment2_multiple spreading, LFR.py` to run SIR simulations `file\*.pickle`, e.g., `LFR_benchmark_1000_u=0.01_net-1, experiment2-LFR.pickle`.
5. use `figure2_multiple spreading, LFR.py` to draw plots of SIR simulations `image\*.png`, e.g., `figure2, multiple spreading, LFR_benchmark_1000_u=0.01.png`.
6. use `figure4_community effect.py` to draw a plot `image\*.png` and save a table `image\*.txt` about community effect, e.g., `figure4, community effect-LFR.png` and `table4, community effect-LFR.txt`.
7. please see example in `image\example_LFR`.
 
## Notification
1. You are free to use the codes for educational purposes.
2. Our coding style may not as good as you expect, but it works.
3. We are glad to hear your improvements of the codes.
4. Any questions please contact yuhisnag.fu@gmail.com.

Best regards,
Yu-Hsiang Fu 20220103 updated.
