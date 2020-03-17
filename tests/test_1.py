import pytest
from xuerui_stat.datatool.data_manager import DataManager
import pandas as pd
import os

# get current directory
cur_dir=os.path.dirname(__file__)
__dir_path__=os.path.join(cur_dir,'Data')
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

def test_mkd():
    """
    test if the data directory can be set correctly
    """
    dm=DataManager(enable=False)
    dm.initialise()
    assert dm.get_dir()==''
    # test if errors can be found
    assert filenotfound_error_assert(dm.set_dir,'')
    assert filenotfound_error_assert(dm.set_dir,'/wrong_path/htap_gnorw/')

    # test if a new directory can be set
    assert not os.path.isdir(__dir_path__)
    dm.set_dir(__dir_path__)
    assert os.path.isdir(__dir_path__)
    assert dm.get_dir()==__dir_path__
    dm.initialise()


