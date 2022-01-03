"""
Pairvalue handler
@auth: Yu-Hsiang Fu
@date: 2014/09/27
"""


# 讀取成對數值: pair = (key or value1, value2)
def read_pairvalue(file_path, is_edge=False):
    pair_value = {}
    try:
        with open(file_path, mode="r") as f:
            for line in f:
                # 邊的pairvalue
                if is_edge is True:
                    line = line.strip()
                    index = line.rindex(' ')
                    part1 = line[0:index+1].strip()
                    part1 = part1[1:-1].strip().split(', ')
                    part2 = line[index+1:len(line)].strip()
                    key = tuple([int(part1[0]), int(part1[1])])
                    value = None
                    # 如果不能轉換成數字, 則轉換成文字
                    try:
                        value = float(part2)
                    except:
                        value = str(part2)
                    pair_value[key] = value
                # 節點的pairvalue
                else:
                    pair = line.strip().split(' ')
                    key = int(pair[0])
                    value = float(pair[1])
                    pair_value[key] = value
            f.close()
    except:
        print('[Error] The file can not be read ...')
        print('[Error] Please check this:  ' + str(file_path))
    return pair_value


# 輸出成對數值
def write_pairvalue(pair_value, file_path):
    # 輸出成對數值至檔案
    try:
        with open(file_path, mode="w") as f:
            for k in pair_value.keys():
                key = k
                value = pair_value[key] if k in pair_value.keys() else 0
                f.write(str(key) + ' ' + str(value) + '\n')
            f.flush()
            f.close()
    except:
        print('[Error] The file can not be writed ...')
        print('[Error] Please check this: ' + str(file_path))
