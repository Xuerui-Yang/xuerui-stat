import numpy as np
import pandas as pd
import random as ra
from collections import Counter

from .preprocessing import PreProcessing

class DecisionTree(PreProcessing):
    """
    创建决策树，用于对连续型数据建立分类模型。
    采用CART算法，即最小化GINI值的二叉决策树方法
    输入：
    - data 用于训练决策树的数据，类型为DataFrame
    - cat_name 类别特征名称
    输出：无
    可调用参数：无
    可调用函数：
    - train(max_depth,min_gini)
        用于生成决策树
        输出：
        - 一个dict类型的决策树，结构形如{'Info':info,'Left':left,'Right':right}
         其中Info包含两项：划分特征对应列标号以及划分的具体数值。
         Left和Right分别储存左右子树或最终划分结果
    - test(test_data)
        用于测试预测能力
        输出：
        - 记录混淆矩阵在self.confusion_matrix中，返回平均误差
    - predict(data)
        用于预测data对应类别
        输出；
        - 类别
    """

    def __init__(self, data, cat_name):
        super().__init__(data, cat_name)
        self.tree = None
        self.test_data = None
        self.confusion_matrix = None

    def _get_gini(self, data):
        """计算GINI值"""
        total = len(data)
        # 统计各类别概率
        if total:
            count = dict(Counter(data[:, -1]))
            count = list(count.values())
            f = lambda x: (x / total)**2
            pr2 = list(map(f, count))
            # 计算gini值
            gini = 1 - sum(pr2)
        else:
            gini = 0
        return gini

    def _split_gini(self, data, split_index):
        """计算排序后的数据在split_index前分成两份后的GINI值"""
        part_1 = data[:split_index]
        part_2 = data[split_index:]
        pr = split_index / len(data)
        gini = pr * self._get_gini(part_1) + \
            (1 - pr) * self._get_gini(part_2)
        return gini

    def _split_criteria(self, data, feature):
        """遍历index，获取数据对应特征的最佳划分点和最小GINI值"""
        smallest = 1
        # 将数据按对应特征从小到大排序
        sorted_data = data[np.argsort(data[:, feature])]
        for i in range(len(data) - 1):
            # 只在对应特征的值变化时考虑划分
            # 如果在第i个和第i+1个之间划分
            if sorted_data[i, feature] != sorted_data[i + 1, feature]:
                # 计算GINI函数
                f = self._split_gini(sorted_data, i + 1)
                # 保留最小的GINI和对应的划分点
                if f < smallest:
                    smallest = f
                    index = i
        if smallest == 1:
            # 说明没能划分（避免所有特征对应值都相同，但类别不同的数据的情况）
            split_criteria = 'none'
        else:
            # 对应的划分点为两相邻数据对应特征的中点
            split_criteria = (
                sorted_data[index, feature] + sorted_data[index + 1, feature]) / 2
        return split_criteria, smallest

    def _split_feature(self, data):
        """遍历特征，获取最佳划分特征和最佳划分点"""
        smallest = 1
        for element in range(self.columns_num - 1):
            # 获取element对应特征的最佳划分点和最小GINI
            (x, f) = self._split_criteria(data, element)
            # 保留最小的GINI和对应的划分点
            if f < smallest:
                smallest = f
                split_feature = element
                split_criteria = x
        if smallest == 1:
            # 说明没能划分（避免所有值都相同，但类别不同的数据的情况）
            split_feature, split_criteria = 'none', 'none'
        return split_feature, split_criteria

    def _split(self, data, info, left=True):
        """对传入数据在指定位置进行划分，根据True或False返回左侧或右侧数据"""
        feature, criteria = info
        if left:
            result = data[data[:, feature] < criteria]
        else:
            result = data[data[:, feature] >= criteria]
        return result

    def _classify(self, data):
        """为叶节点选择类别"""
        # 统计各类别总数
        count = dict(Counter(data))
        # 选择各类别最多的
        m = max(count.values())
        # 如果有多个类别总数相等且最多
        max_cat = [key for key in count if count[key] == m]
        cho = ra.choice(max_cat)
        return cho

    def _treeRecursion(self, data, min_gini, depth, max_depth):
        """构建决策树的递归函数"""
        gini = self._get_gini(data)
        # 如果数据中包含不同类别，GINI大于min_gini，进行划分
        if gini > min_gini and depth < max_depth:
            feature, criteria = self._split_feature(data)
            # 可能出现有不同类别但无法划分的情况
            if feature != 'none' and criteria != 'none':
                # 确实可以划分，则记录划分信息，并分左右子树递归
                info = (feature, criteria)
                tree = {'Info': info}
                tree['Left'] = self._treeRecursion(
                    self._split(data, info, True), min_gini, depth + 1, max_depth)
                tree['Right'] = self._treeRecursion(
                    self._split(data, info, False), min_gini, depth + 1, max_depth)
                return tree
            else:
                # 确实无法划分，则返回类别结果
                cat = self._classify(data[:, -1])
                return cat
        else:
            # 若已达到设定分类限制，返回当前类别结果
            cat = self._classify(data[:, -1])
            return cat

    def train(self, max_depth=0, min_gini=0):
        """
        对所给数据构建决策树
        参数：
            max_depth: 树结构的最大层树，达到最大值后停止构建子树，默认为无限制
            mini_gini：损失函数的最小值，达到最小值后停止构建子树，默认为0
        """
        if max_depth>0:
            # 当给出最大层数
            input_max_d=max_depth
        else:
            # 当不传入最大层数，默认不设限制
            input_max_d=2*self.rows_num
        self.tree = self._treeRecursion(self.data, min_gini, 0, input_max_d)

    def _search(self, tree, data):
        """
        按给定tree搜寻给定data的对应路径，返回路径终点（叶节点）对应类别
        """
        feature, criteria = tree['Info']
        # 如果小于边界值，进入左子树
        if data[feature] < criteria:
            sub_tree = tree['Left']
        else:
            # 否则进入右子树
            sub_tree = tree['Right']
        # 对子树迭代，重复上述过程，直到达到叶节点
        if type(sub_tree).__name__ == "dict":
            result = self._search(sub_tree, data)
        else:
            result = sub_tree
        return result

    def predict(self, data):
        """预测给定data对应类别"""
        if self.tree != None:
            # 对于输入data为向量的情况
            if data.ndim == 1:
                result = self._search(self.tree, data)
            # 对于输入data为矩阵的情况
            else:
                f = lambda x: self._search(self.tree, x)
                result = list(map(f, data))
            return result

    def _compare(self,true_cat, pred_cat):
        """比较真实值与预测值，返回矩阵"""
        k = len(self.categories)
        mat = np.zeros((k, k))
        # 矩阵ij位置表示真实值为i，预测值为j的个数
        for h in range(len(true_cat)):
            i = int(true_cat[h])
            j = int(pred_cat[h])
            mat[i, j] += 1
        mat = pd.DataFrame(mat, columns=self.categories, index=self.categories)
        return mat

    def test(self, *test_data):
        """对所给模型做检验"""
        if test_data == ():
            # 在不输入新的检验数据的情况下，用原数据进行检验
            self.test_data = self.data
        else:
            if type(test_data)==pd.core.frame.DataFrame:
                # 对输入的新数据做与原数据一样的数据处理
                self.test_data = PreProcessing(test_data[0], self._cat_name).data
            else:
                self.test_data=test_data[0]
        # 预测测试数据类别
        result = self.predict(self.test_data)
        # 记录混淆矩阵
        self.confusion_matrix = self._compare(self.test_data[:, -1],result)
        error=1-np.trace(self.confusion_matrix)/len(self.test_data)
        return error
