# xuerui-stat
[![Build Status](https://www.travis-ci.org/Xuerui-Yang/xuerui-stat.svg?branch=master
)](https://www.travis-ci.org/Xuerui-Yang/xuerui-stat)

An open-source Python package for using statistical tools and methods.

## Source code
https://github.com/Xuerui-Yang/xuerui-stat

## Installation
```
pip install xuerui-stat
```

## Tools and methods

### DataManager
+ Description

It is a tool to manage data files. Once a data file is imported, the tool would move it to a specified data directory automatically. And when importing data, the tool can search files in the data directory.

+ Example
```python
from xuerui_stat import DataManager
dm = DataManager(enable=True)
```
This command defines a class to name the tool. For the first use, users should use the command 'set_dir(yourpath)' with your prefered path to set your data directory, for example,
```python
dm.set_dir('/home/xuerui/Documents/Data/')
```
Once it is done, the directory path is printed like this:

>Data directory: '/home/xuerui/Documents/Data/'

The parameter 'enable' for the class can be set as True or False. When it is True, the data file imported by the command below would be moved to the data directory automatically. 
```python
df=dm.import_data('/home/xuerui/Documents/PythonProjects/FactorAnalysis/example.csv')
```
Otherwise users can manually move the files using the such command:
```python
dm.addto_dir('/home/xuerui/Documents/example.csv')
```
The moved data files are renamed by adding the script names, in order to identify them. For example, 'example.csv' is imported in 'my_example.py' using the above command. So it would be moved to the data directory and renamed as 'MyExample_example.csv'. 

Users can also check the contents under the data directory using
```python
dm.list_dir()
```

### DecisionTree, PlotTree, RandomForest
+ Description

These commands give users tools for data mining by using tree relevant methods.

+ Example

As above, the following commands import the data which is to be analyse.
```python
from xuerui_stat import *
dm = DataManager(enable=False)
data=dm.import_data("/home/xuerui/Documents/PythonProjects/test.csv")
```

The decision tree method can be applied to the data by specifying the name of category.
```python
dt=DecisionTree(data,'Cat')
dt.train()
t=dt.tree
print(t)

pt=PlotTree(dt)
pt.tree_structure_plot()

dt.test()
pt.confusion_matrix_plot()
```

The tree and confusion matrix can be plotted via the 'PlotTree' module.

Furthermore, the random forest can also be used as follows:
```python
rf=RandomForest(data,'Cat')
rf.train(num_tree=300,max_depth=0,min_gini=0)
print(rf.oob_error)
dt.test()
print(dt.confusion_matrix)
```
