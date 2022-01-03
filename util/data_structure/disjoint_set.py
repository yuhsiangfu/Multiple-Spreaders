"""
Disjoint set data structure with rank & path compression
@auth: Yu-Hsiang Fu
@date: 2014/12/11
"""
# Disjoint Set資料結構
class disjoint_set:
    # 初始化
    def __init__(self, N):
        self._parent = list(range(N))
        self._rank   = [0] * N

    # 尋找集合
    def find_set(self, x):
        # 如果自已不是自已的parent, 表示parent是其他節點, 則往上找根節點
        if x != self._parent[x]:
            self._parent[x] = self.find_set(self._parent[x])
        # 找到根節點
        return self._parent[x]

    # 合併集合
    def union(self, x, y):
        # 找出x, y的根節點ri, rj
        ri = self.find_set(x)
        rj = self.find_set(y)
        # 如果i, j在同一個集合則不合併, 否則合併x, y的集合
        if ri == rj:
            return
        # 將rank大
        if self._rank[ri] > self._rank[rj]:
            self._parent[rj] = ri
        else:
            self._parent[ri] = rj
            if self._rank[ri] == self._rank[rj]:
                self._rank[rj] = self._rank[rj] + 1
