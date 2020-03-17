import matplotlib.pyplot as plt
import seaborn as sns



class PlotTree():
    def __init__(self,tree_class):
        self._tree_class=tree_class
        self._decision_node = dict(boxstyle="sawtooth", fc="0.8")
        self._leaf_node = dict(boxstyle="round4", fc="0.8")
        self._arrow_args = dict(arrowstyle="<-")

    def __get_tree_depth(self,tree):
        """获取树的深度"""
        depth = 0
        # 定义的dict中首位储存的是节点信息，不计入计数
        for key in ('Left', 'Right'):
            # 记录各子节点的深度
            sub_tree = tree[key]
            if type(sub_tree).__name__ == "dict":
                # 如果该节点有分支，迭代计算该节点的深度
                thisdepth = self.__get_tree_depth(sub_tree)
            else:
                # 否则深度为一
                thisdepth = 1
            # 比较各分支深度，保留最深记录
            if thisdepth > depth:
                depth = thisdepth
        # 分支深度加一即为当前节点深度
        return depth + 1


    def __plot_node(self,node_txt, cntr_pt, prnt_pt, node_type):
        self._ax1.annotate(node_txt, xy=prnt_pt, xycoords='axes fraction',
                                xytext=cntr_pt, textcoords='axes fraction',
                                va="center", ha="center", bbox=node_type, arrowprops=self._arrow_args)


    def __plot_mid_text(self,cntr_pt, prnt_pt, txt_string):
        xMid = (prnt_pt[0] - cntr_pt[0]) / 2.0 + cntr_pt[0]
        yMid = (prnt_pt[1] - cntr_pt[1]) / 2.0 + cntr_pt[1]
        self._ax1.text(xMid, yMid, txt_string, va="center",
                            ha="center", rotation=30)

    def __plot_tree(self,tree, prnt_pt, node_txt, branch=None):
        self._layer += 1
        diff = 1 / 2**(self._layer)
        keys = list(tree.keys())
        text = tree[keys[0]]
        if branch == 'Left':
            self._xOff -= diff
        elif branch == 'Right':
            self._xOff += diff
        else:
            pass
        cntr_pt = (self._xOff, self._yOff)
        self.__plot_mid_text(cntr_pt, prnt_pt, node_txt)
        self.__plot_node(text, cntr_pt, prnt_pt, self._decision_node)
        self._yOff = self._yOff - 1.0 / self._totalD
        for key in keys[1:]:
            sub_tree = tree[key]
            if type(sub_tree).__name__ == 'dict':
                self.__plot_tree(sub_tree, cntr_pt, str(key), key)
            else:
                if key == 'Left':
                    x = self._xOff - diff / 2
                elif key == 'Right':
                    x = self._xOff + diff / 2
                else:
                    pass
                self.__plot_node(sub_tree, (x, self._yOff), cntr_pt, self._leaf_node)
                self.__plot_mid_text((x, self._yOff), cntr_pt, str(key))
        if branch == 'Left':
            self._xOff += diff
        elif branch == 'Right':
            self._xOff -= diff
        else:
            pass
        self._layer -= 1
        self._yOff = self._yOff + 1.0 / self._totalD

    def tree_structure_plot(self):
        fig = plt.figure(1, facecolor='white')
        fig.clf()
        axprops = dict(xticks=[], yticks=[])
        self._ax1 = plt.subplot(111, frameon=False, **axprops)
        self._totalD = float(self.__get_tree_depth(self._tree_class.tree))
        self._xOff = 0.5
        self._yOff = 1.0
        self._layer = 0
        self.__plot_tree(self._tree_class.tree, (0.5, 1.0), '')
        plt.show()

    def confusion_matrix_plot(self):
        mat=self._tree_class.confusion_matrix
        if mat is None:
            print("The confusion matrix is not computed. Please use 'test()' in 'DecisionTree' class to get it.")
        else:
            fig, ax = plt.subplots(figsize=(6, 6))
            sns.heatmap(mat,xticklabels=mat.columns,yticklabels=mat.index,
                cbar_kws={"shrink": .5}, ax=ax)
            plt.tight_layout()
            plt.show()
