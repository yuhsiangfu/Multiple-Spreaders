"""
Pickle file handler
@auth: Yu-Hsiang Fu
@date  2014/10/05
"""


# 讀取pickle檔案：
def read_pickle_file(file_path):
    # 匯入套件及模組
    import pickle
    import os
    import os.path

    # 從檔案讀取資訊
    try:
        # 確認檔案是否存在及是否可以存取
        if os.path.isfile(file_path) and os.access(file_path, os.R_OK):
            return pickle.load(open(file_path, 'rb'))
        else:
            raise
    except:
        print('[Error] The file can not be read ...')
        print('[Error] Please check this: ' + str(file_path))


# 輸出pickle檔案
def write_pickle_file(data, file_path):
    # 匯入套件及模組
    import pickle

    try:
        # 輸出資訊
        pickle.dump(data, open(file_path, 'wb'))
    except:
        print('[Error] The file can not be writed ...')
        print('[Error] Please check this: ' + str(file_path))
