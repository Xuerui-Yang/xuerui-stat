import sys
import os
import shutil
import pandas as pd


class DataDirectory():
    """
    Read data, save data， show informations
    """

    def __init__(self):
        """
        Initialise with the working directory and data directory
        """
        # search for the data directory under the script directory
        script_dir = os.path.split(os.path.realpath(__file__))[0]
        self.__path_file = os.path.join(script_dir, 'data_dir.txt')
        self.__data_dir = self.__get_old_dir()

    def initialise(self):
        """
        Delete the path file so that no data directory is recorded
        """
        if os.path.isfile(self.__path_file):
            self.__data_dir = ''
            os.remove(self.__path_file)

    def get_dir(self, print_info=False):
        """
        Get the current directory, data directory, and other informations
        """
        if print_info:
            print("Current working directory: '%s'" % os.getcwd())

            if self.__data_dir != '':
                print("Data directory: '%s'" % self.__data_dir)
            else:
                print(
                    "Fail to get the data directory. Use 'set_dir(your_path)' to make it.")

        return self.__data_dir

    def __get_old_dir(self):
        """
        Get the path from the path file
        """
        if os.path.isfile(self.__path_file):
            # get the data directory from the txt file
            with open(self.__path_file, 'r') as f:
                data_dir = f.read()
            if not os.path.isdir(data_dir):
                # if the data directory is invalid
                data_dir = ''
        else:
            # if the path file is not found
            data_dir = ''
        return data_dir

    def __move_dir(self, old_path, new_path):
        """
        Move files from one directory to tanother one
        """
        if os.path.isdir(old_path) and os.path.isdir(new_path):
            file_list = os.listdir(old_path)
            for file in file_list:
                old_file = os.path.join(old_path, file)
                new_file = os.path.join(new_path, file)
                shutil.move(old_file, new_file)
            # remove the old directory
            os.rmdir(old_path)

    def __make_dir(self, data_dir):
        """
        Check if the directory exists
        Make a new directory for if not exists
        """
        # delete the whitespaces
        dirc = data_dir.strip()
        # delete the '/'
        data_dir = dirc.rstrip('/')

        # check if exists
        if os.path.isdir(data_dir):
            return True
        else:
            # make the directory
            try:
                os.mkdir(data_dir)
            except FileNotFoundError:
                return False
            except:
                raise ValueError("Undefined error occurs.")
            else:
                return True

    def set_dir(self, new_path):
        """
        Make a new data directory and move the files from the old directory
        """
        old_path = self.__get_old_dir()
        if (old_path == new_path) and (old_path != ''):
            pass
        else:
            # if the new and the old differ
            # try to make a new directory
            res = self.__make_dir(new_path)
            if res:
                # if succeed, move the old directory to the new one
                self.__move_dir(old_path, new_path)
                # write the new path into the path file
                with open(self.__path_file, 'w') as f:
                    f.write(new_path)
                self.__data_dir = new_path
                print("The new data directory is made successfully.")
                print("Data directory: '%s'" % self.__data_dir)
            else:
                raise FileNotFoundError("Fail to make the data directory.")

    def list_dir(self):
        """
        Get the file names in the data directory
        """
        if self.__data_dir != '':
            print(os.listdir(self.__data_dir))
        else:
            raise FileNotFoundError("Data directory does not exist.")

    def search_dir(self, data_path):
        """
        Search the file in the data directory
        """
        if self.__data_dir != '':
            new_path = self.rename_data(data_path)
            if os.path.isfile(new_path):
                return new_path
            else:
                return None
        else:
            raise FileNotFoundError("Data directory does not exist.")

    def rename_data(self, data_path):
        """
        Rename the data file in the data directory with the format such as 'ScriptName_dataname.txt'
        """
        # get the data name and suffix
        split_path = os.path.basename(data_path).split('.')
        # change the data name to uppercase
        data_name = split_path[0]+'.'+split_path[1]
        # get the script name and change its format
        script_name = self.get_script_name().title().replace('_', '')
        # join the script name and data name
        data_name = '_'.join([script_name, data_name])
        new_path = os.path.join(self.__data_dir, data_name)
        return new_path

    @staticmethod
    def get_script_name():
        """
        Get the name of script
        """
        current_path = sys.argv[0]
        bn_path = os.path.basename(current_path)
        l = os.path.splitext(bn_path)
        name = l[0]
        return name

    def addto_dir(self, data_path):
        """
        Move data to the data directory manually
        """
        if self.__data_dir != '':
            if os.path.isfile(data_path):
                new_path = self.rename_data(data_path)
                shutil.move(data_path, new_path)
            else:
                raise FileNotFoundError("'%s' does not exist." % data_path)
        else:
            print("Data directory does not exist.")
