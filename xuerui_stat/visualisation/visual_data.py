from .settings import Settings
import matplotlib.pyplot as plt
import seaborn as sns

settings = Settings()

def show_fig(activate=True):
    """
    Show Figures When True
    Save Figures into a specified files when False
    """
    if activate:
        plt.show()
    else:
        plt.savefig()
        print('To display the figures, please set "True" in <show_fig()>.')

def plot_eigenvalues(mtx):
    """
    Barplot of sorted eigenvalues
    
    Parameters:
     - mtx: A squared matrix; numpy array
    """
    values = np.linalg.eigvals(mtx)
    sorted_indices = np.argsort(values)[::-1]
    values = values[sorted_indices]
    k = len(values)

    labels = ["%.2f %%" % (values / sum(values) * 100)[i]
                for i in range(k)]
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(range(len(values)), values, color=settings.main_color)
    ax.set_facecolor(settings.bg_color)
    ax.set_xticks(range(k))
    ax.set_xticklabels([i for i in range(1, k + 1)])
    rects = ax.patches
    for rect, label in zip(rects, labels):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, label,
                ha='center', va='bottom', color='white')
    plt.tight_layout()

def plot_correlations(df):
    """
    Compute the correlation matrix for data and plot a heatmap

    Parameters:
     - df: A pandas DataFrame
    """
    m_cor = df.corr()
    fig, ax = plt.subplots(figsize=(11, 9))
    # Add diverging colormap from red to blue
    cmap = sns.diverging_palette(10, 180, center='dark', as_cmap=True)
    sns.heatmap(m_cor,
        xticklabels=m_cor.columns, yticklabels=m_cor.columns,
        vmin=-1, vmax=1, cmap=cmap, square=True, cbar_kws={"shrink": .5}, ax=ax)
    plt.tight_layout()
