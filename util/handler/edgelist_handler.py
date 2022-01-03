"""
Edgelist handler
@auth: Yu-Hsiang Fu
@date: 2014/09/27
"""


# 讀取連結清單：edgelist
def read_edgelist(file_path):
    # 匯入套件及模組
    import os
    import os.path

    # 從檔案讀取edge_pair = (start, end)及建立連結清單
    edge_list = []
    try:
        # 確認檔案是否存在及是否可以存取
        if os.path.isfile(file_path) and os.access(file_path, os.R_OK):
            with open(file_path, mode="r") as f:
                for line in f:
                    edge_list.append(line.strip())
                f.close()
        else:
            raise
    except:
        print('[Error] The file can not be read ...')
        print('[Error] Please check this file:  ' + str(file_path))
    return edge_list


# 輸出連結清單
def write_edgelist(G, file_path):
    # 匯入套件及模組
    import networkx as nx

    # 輸出連結清單至檔案
    try:
        nx.write_edgelist(G, path=file_path, data=False)
    except:
        print('[Error] The file can not be writed ...')
        print('[Error] Please check this file:  ' + str(file_path))
