"""
Pos-file handler
@auth: Yu-Hsiang Fu
@date  2014/09/27
"""


# 讀取pos檔案：
def read_pos_file(file_path):
    # 匯入套件及模組
    import os
    import os.path

    # 從檔案讀取網絡節點的pos資訊
    pos = {}
    try:
        # 確認檔案是否存在及是否可以存取
        if os.path.isfile(file_path) and os.access(file_path, os.R_OK):
            with open(file_path, mode="r") as f:
                for line in f:
                    pos_items = line.strip().split(' ')
                    pos_id = int(pos_items[0])
                    pos[pos_id] = tuple([float(l) for l in pos_items[1:3]])
                f.close()
        else:
            raise
    except:
        print('[Error] The file can not be read ...')
        print('[Error] Please check this: ' + str(file_path))
    return pos


# 輸出pos檔案
def write_pos_file(pos, file_path):
    try:
        with open(file_path, mode="w") as f:
            for i in pos.keys():
                pos_id = str(i)
                pos_x = str(pos[i][0])
                pos_y = str(pos[i][1])
                f.write(pos_id + ' ' + pos_x + ' ' + pos_y + '\n')
            f.flush()
            f.close()
    except:
        print('[Error] The file can not be writed...')
        print('[Error] Please check this: ' + str(file_path))
