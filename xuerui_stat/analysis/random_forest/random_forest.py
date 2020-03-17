import numpy as np
import pandas as pd
import random as ra
from collections import Counter

from .preprocessing import PreProcessing
from .decision_tree import DecisionTree



class RandomForest(DecisionTree):
    """
    创建决策树，用于对连续型数据建立分类模型。
    采用CART算法，即最小化GINI值的二叉决策树方法
    输入：
    - data 用于训练决策树的数据，类型为DataFrame
    - cat_name 类别特征名称
    输出：无
    可调用参数：无
    可调用函数：
    - train(num_tree,max_depth,min_gini,subf_num)
        用于生成决策树
        输出：
        -1> 一个dict类型的决策树，记录在self.tree中，结构形如{'Info':info,'Left':left,'Right':right}
            其中Info包含两项：划分特征对应列标号以及划分的具体数值。
            Left和Right分别储存左右子树或最终划分结果
        -2> Out of Bag(OOB)误差，记录在self.oob_error中
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
        super().__init__(data,cat_name)


    def _split_feature(self, data):
        """重写该函数，在决策树基础上增加随机选择子特征的过程"""
        smallest = 1
        # 随机选择一些特征作为候选划分特征
        subfeatures=ra.sample(range(self.columns_num - 1),self.subf_num)
        for element in subfeatures:
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

    def train(self,num_tree,max_depth=0,min_gini=0,subf_num=0):
        """
        对所给数据构建随机森林
        参数：
            num_tree: 森林中包含决策树的棵数
            max_depth: 单棵树深度的最大值，达到最大值后停止构建子树，默认为无穷大，即不设置深度限制
            mini_gini：损失函数的最小值，达到最小值后停止构建子树，默认为0
            subf_num: Forest—RI中每次划分用的子特征数，默认为总特征数的根号取整
        """
        # 初始化数结构和参数
        self.tree={}
        oob_tests=[]
        if max_depth>0:
            input_max_d=max_depth
        else:
            input_max_d=2*self.rows_num
        self.num_tree=num_tree
        if subf_num>0 and isinstance(subf_num,int):
            self.subf_num=subf_num
        else:
            self.subf_num=int(round(np.sqrt(self.columns_num)))
        # 训练全部决策树
        for i in range(num_tree):
            # 从全部样本中有放回抽出样本个数个子样本
            boots=ra.choices(range(self.rows_num),k=self.rows_num)
            boot_data=self.data[boots]
            self.tree[i]=self._treeRecursion(boot_data,min_gini,0,input_max_d)
            # 收集OOB样本
            oob_tests.append(self._oob_test(self.tree[i],boots))
        # 计算总体OOB误差
        self.oob_error=np.mean(oob_tests)

    def _oob_test(self,tree,boots):
        """OOB测试预测能力"""
        # 取出全样本与bootstrap子样本的补集
        oob=list(set(range(self.rows_num))-set(boots))
        oob_data=self.data[oob]
        # 对于输入data为向量的情况
        if self.data.ndim == 1:
            result = self._search(tree, oob_data)
        # 对于输入data为矩阵的情况
        else:
            f = lambda x: self._search(tree, x)
            result = list(map(f, oob_data))
        mat=self._compare(oob_data[:,-1],result)
        error=1-np.trace(mat)/len(oob_data)
        return error

    def _vote(self,data):
        """将数据向量输入随机森林中每棵树得到多个结果，投票出选择最多的结果"""
        preds=[]
        for i in range(self.num_tree):
            # 遍历每棵树，将分类结果添加到preds中
            preds.append(self._search(self.tree[i],data))
        # 归票，选择投票最多的类别
        result=self._classify(preds)
        return result

    def predict(self,data):
        """预测给定data对应类别"""
        if self.tree!=None:
            #对于输入data为向量的情况
            if data.ndim==1:
                result=self._vote(data)
            # 对于输入data为矩阵的情况
            else:
                result=[]
                for element in data:
                    result.append(self._vote(element))
            return result

