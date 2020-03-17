import sys
import os
import shutil
import pandas as pd
from .data_directory import DataDirectory


class DataManager(DataDirectory):
    """
    Read data, save data， show informations
    """

    def __init__(self, enable=True):
        """
        Initialise with the working directory and data directory

        Parameters:
        - enable: True/False. If True, data files would be moved to the data directory automatically
        """
        super().__init__()
        self.__enable = enable
        self.__where_data = 0

    def import_data(self, data_path, **args):
        """
        Import data and add to the data directory
        """
        # read the data
        df = self.__read_data(data_path, **args)
        if df is None:
            raise ValueError("Data fails to be imported.")
        else:
            if self.__enable:
	        # print the path of data directory
                self.get_dir(True)
                # move the file to the data directory
                self.__auto_addto_dir(data_path)
            return df

    def __read_by_suffix(self, data_path, **args):
        """
        Identify the file type and read data
        """
        # get the file type
        tp = data_path.split('.')[-1]
        if tp == 'csv':
            with open(data_path) as f:
                df = pd.read_csv(f, **args)
        elif tp == 'txt':
            with open(data_path) as f:
                df = pd.read_table(f, **args)
        else:
            raise TypeError("Type '.%s' is not supported." % tp)
        return df

    def __read_data(self, data_path, **args):
        """
        Read data from the path provided or from the data directory
        """
        # check the validity of data path
        abs_path = os.path.abspath(data_path)
        if os.path.isfile(abs_path):
            # read data directly from the path provided
            df = self.__read_by_suffix(abs_path, **args)
            print("Data is imported from '%s'." % abs_path)
            self.__where_data = 1
        else:
            print("'%s' does not exist." % data_path)
            # check if the data is in the data directory
            print("Searching in the data directory...")
            new_path = self.search_dir(data_path)
            if new_path is not None:
                df = self.__read_by_suffix(new_path, **args)
                print("Data is imported from the data directory.")
                self.__where_data = 2
            else:
                print("Data is not found in the data directory.")
                # self.__where_data = 0
                df = None
        return df

    def __auto_addto_dir(self, data_path):
        """
        Move data to the data directory automatically
        """
        if self.__where_data==0:
            raise ValueError("Data fails to be imported.")
        elif self.__where_data == 1:
            # data is to be moved to data directory
            new_path = self.rename_data(data_path)
            shutil.move(data_path, new_path)
        elif self.__where_data == 2:
            # data is already in data directory
            pass
        else:
            raise ValueError('Undefined error occurs.')
