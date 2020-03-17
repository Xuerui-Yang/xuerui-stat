name = "xuerui-stat"

# Let users know if they're missing any of our hard dependencies
hard_dependencies = ("sys", "os", "shutil", "pandas", "numpy", "random", "collections", "matplotlib", "seaborn")
missing_dependencies = []

for dependency in hard_dependencies:
    try:
        __import__(dependency)
    except ImportError as e:
        missing_dependencies.append("{0}: {1}".format(dependency, str(e)))

if missing_dependencies:
    raise ImportError(
        "Unable to import required dependencies:\n" +
        "\n".join(missing_dependencies)
    )
del hard_dependencies, dependency, missing_dependencies

from .datatool.data_manager import DataManager
from .analysis.random_forest import *
from .analysis.factor_analysis import FactorAnalysis

__all__=['DataManager', 'FactorAnalysis', 'DecisionTree', 'PlotTree', 'RandomForest']
