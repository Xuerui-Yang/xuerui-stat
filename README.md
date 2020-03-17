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
