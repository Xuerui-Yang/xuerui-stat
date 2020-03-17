import numpy as np
import pandas as pd
import random as ra


class PreProcessing():
    """
    重置用于训练决策树的数据，使得类别特征置于末列，并转化为数字
    传入参数：
    - data 用于训练决策树的数据，类型为DataFrame
    - cat_name 类别特征名称
    可调用参数：
    - rows_num 数据行数
    - columns_num 数据列数
    - features 数据所有特征名
    - categories 数据所有类别名
    - data 重置后的数据，类型为np.array
    可调用函数：无
    """

    def __init__(self, data, cat_name):
        self._cat_name=cat_name
        (self.rows_num, self.columns_num) = data.shape
        self.data = self.__cats_to_last(data, cat_name)
        self.features = self.data.columns
        self.categories = self.__get_cat()
        self.data=self.data.values
        self.__cats_to_nums()


    def __cats_to_last(self, data, cat_name):
        """将类别特征置于末位"""
        # 获取类别特征所在列
        right = data.loc[:, cat_name]
        # 获取其他所有特征矩阵
        left = data.drop(cat_name, axis=1)
        # 合并左右列（用concat而非join因为join会重新按index排序）
        out = pd.concat([left,right],axis=1)
        return out

    def __get_cat(self):
        """获取所有类别名称"""
        # 提取类别特征对应向量
        cats=list(self.data[self._cat_name])
        # 删去重复项
        out=list(set(cats))
        # 按照原顺序排列（set会改变顺序，导致每次运行顺序不同）
        out.sort(key=cats.index)
        return out

    def __cats_to_nums(self):
        """将数据集中的划分类别转化为0，1，2……"""
        # 遍历数据集每行元素
        for i in range(self.rows_num):
            # 寻找与该行类别匹配的类
            for j in range(len(self.categories)):
                # 将匹配到的类别改为数字并退出循环
                if self.data[i, -1] == self.categories[j]:
                    self.data[i, -1] = j
                    break

