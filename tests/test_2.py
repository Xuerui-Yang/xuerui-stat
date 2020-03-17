import pytest
from xuerui_stat.datatool.data_manager import DataManager
import pandas as pd
import os
from sklearn.datasets import load_iris

# get current directory
cur_dir=os.path.dirname(__file__)
__data_path__=os.path.join(cur_dir,'iris.csv')
__dir_path__=os.path.join(cur_dir,'Data')

if os.path.isfile(__data_path__):
    os.remove(__data_path__)
if os.path.isdir(__dir_path__):
    for file in os.listdir(__dir_path__):
        os.remove(os.path.join(__dir_path__,file))
    os.rmdir(__dir_path__)

def filenotfound_error_assert(func,*args):
    """
    if raises error, return True
    """
    try:
        func(*args)
    except FileNotFoundError:
        return True
    except:
        return False
    else:
        return False

def get_test_data():
    iris = load_iris()
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    # save data
    df.to_csv(__data_path__,index=0)
    return df

def test_iris():
    """
    test if the data file is writen successfully
    """
    assert not os.path.isfile(__data_path__)
    iris=get_test_data()
    assert os.path.isfile(__data_path__)
    df=pd.read_csv(__data_path__)
    pd.testing.assert_frame_equal(df,iris)

def test_import():
    """
    test if the data can be imported
    """
    iris=get_test_data()
    
    dm=DataManager(enable=True)
    dm.set_dir(__dir_path__)
    assert filenotfound_error_assert(dm.addto_dir,'wrong_data_path')
    dm.addto_dir(__data_path__)
    data_name=dm.rename_data(__data_path__)
    assert os.path.isfile(data_name)
    assert not os.path.isfile(__data_path__)
    
    df=dm.import_data(__data_path__)
    pd.testing.assert_frame_equal(df,iris)

if os.path.isfile(__data_path__):
    os.remove(__data_path__)
if os.path.isdir(__dir_path__):
    for file in os.listdir(__dir_path__):
        os.remove(os.path.join(__dir_path__,file))
    os.rmdir(__dir_path__)