import matplotlib as mpl
import seaborn as sns
import os
import sys


class Settings():
    """Class that saves all the settings"""

    def __init__(self):
        """Initalise settings"""
        # Figure settings
        self.figure_width = 12
        self.figure_height = 10
        self.bg_color = sns.xkcd_rgb['dark grey']
        self.main_color = sns.xkcd_rgb['dark aquamarine']
        self.cmap = mpl.colors.ListedColormap([self.bg_color, self.main_color])
        self.col_density = 'seismic'
        self.emphasize_color = 'red'
        self.figures_dir = os.path.join(sys.argv[0], 'Figures')
