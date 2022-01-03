"""
Gpickle file handler
@auth: Yu-Hsiang Fu
@date  2014/09/28
"""


# 讀取gpickle檔案：
def read_gpickle_file(file_path):
    # 匯入套件及模組
    import networkx as nx
    import os
    import os.path

    # 從檔案讀取網絡的節點及連結資訊
    try:
        # 確認檔案是否存在及是否可以存取
        if os.path.isfile(file_path) and os.access(file_path, os.R_OK):
            return nx.read_gpickle(file_path)
        else:
            raise
    except:
        print('[Error] The file can not be read ...')
        print('[Error] Please check this: ' + str(file_path))


# 輸出gpickle檔案
def write_gpickle_file(G, file_path):
    # 匯入套件及模組
    import networkx as nx

    try:
        # 輸出圖形, 節點及連結資訊
        nx.write_gpickle(G, file_path)
    except:
        print('[Error] The file can not be writed ...')
        print('[Error] Please check this: ' + str(file_path))
