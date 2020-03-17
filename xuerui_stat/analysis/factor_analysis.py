import numpy as np
import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt
from ..visualisation import visual_data as vd
from ..datatool import basic_func as bf

class FactorAnalysis():
    """
    Fit a FA model
    Rotate Loadings

    Note:
    1. Input data as a pandas DataFrame
    2. Use analyse(k,rotation) to get loadings
        - k: Number of factors
        - rotation: True/False
    """

    def __init__(self, data):
        self.data = data
        self.loadings = None
        self.rotation_matrix = None
        self.corr_matrix=bf.corr_mtx(data)
        vd.plot_eigenvalues(self.corr_matrix)

    @staticmethod
    def _fit_model(psi, corr_matrix, n_factors, return_error=True):
        """Calculate the sum squared residuals
        ---------
        Variables:
        - psi: Corvariance of epsilons, p*p diagonal matrix,
                length-p np.array
        - corr_matrix: Correlation matrix of features,
                p*p np.array
        - n_factors: Number of factors,
                int value
        - return_error: If True,return error, else return loadings
                bool TRUE(default) or FALSE
        ---------
        Returns:
        - error: float scalar
                residuals=corr_matrix-loadings*loadings^T
                sum squared residuals
        - loadings: p*n_factor np.array
                Loadings * Loadings^T = Corr-Psi
        """
        # Calculate Corr-Psi
        np.fill_diagonal(corr_matrix, 1 - psi)
        # Calculate the eigensystem
        values, vectors = np.linalg.eig(corr_matrix)
        # Sort the values from the largest
        # Keep n factors
        sorted_indices = np.argsort(values)[::-1][:n_factors]
        values = values[sorted_indices]
        vectors = vectors[:, sorted_indices]
        # Calculate Loadings
        loadings = np.dot(vectors, np.diag(np.sqrt(np.maximum(values, 0))))
        if return_error:
            # Calculate the error
            residuals = corr_matrix - np.dot(loadings, loadings.T)
            error = np.sum(residuals**2)
            return error
        else:
            return loadings

    def _compute_loadings(self,corr_matrix, n_factors):
        """Find the loadings that minimize the error
        ---------
        Variables:
        - data: matrix of the features
                n*p DataFrame
        - n_factors: Number of factors,
                int value
        ---------
        Returns:
        - loadings: p*n_factor DataFrame
        """
        p = len(corr_matrix)
        start = 1 - abs(corr_matrix - np.eye(p)).max(axis=0)
        bounds = [(0.0001, 1) for i in range(p)]
        objective = self._fit_model
        result = sp.optimize.minimize(objective, start,
                                      method='L-BFGS-B',
                                      bounds=bounds,
                                      options={'maxiter': 1000},
                                      args=(corr_matrix, n_factors))
        # get factor column names
        columns = ['Factor{}'.format(i) for i in range(1, n_factors + 1)]
        loadings = self._fit_model(
            result.x, corr_matrix, n_factors, return_error=False)
        loadings = pd.DataFrame(loadings,
                                index=self.data.columns.values,
                                columns=columns)
        return loadings

    @staticmethod
    def _rotation(loadings):
        """Rotate the loadings using varimax method
        ---------
        Variables:
        - loadings: Loadings obtained by _compute_loadings()
                p*n_factor DataFrame
        ---------
        Returns:
        - loadings: Loadings after rotation
                p*n_factor DataFrame
        - r: n_factor*n_factor np.array
                Rotation matrix
        """
        lds = loadings.values
        index_names = loadings.index.values
        columns_names = loadings.columns.values

        # p features and k factors
        p, k = lds.shape
        # Nprmalize the loadings before rotating
        normalize = np.sqrt((lds**2).sum(axis=1))
        lds = (lds.T / normalize).T
        # Initialize the rotation matrix
        # k*k orthogonal
        r = np.eye(k)

        # Iteration
        # maximal times:500
        j = 0
        for i in range(500):
            last_j = j
            # Roatate the loadings
            new_lds = np.dot(lds, r)
            # Centralize the squared loadings
            c = new_lds**2 - (new_lds**2).mean(axis=0)
            # Singular value decomposition
            u, s, v = np.linalg.svd(np.dot(lds.T, c * new_lds))
            # Get the new rotation matrix
            r = np.dot(u, v)
            # Use j to be the criterion
            j = np.sum(s)
            # Check convergence
            if last_j != 0 and j / last_j < 1 + 1e-5:
                break

        # Get the loadings after rotation
        lds = np.dot(lds, r)
        lds = (lds.T * normalize).T
        loadings = pd.DataFrame(lds,
                                index=index_names,
                                columns=columns_names)
        return loadings, r

    def analyse(self, n_factors, rotation=False):
        """Main function for factor analysis"""
        loadings = self._compute_loadings(self.corr_matrix,n_factors)
        if rotation:
            loadings, r = self._rotation(loadings)
            self.rotation_matrix = r

        self.loadings = loadings

    def get_communalities(self):
        """Calculate the communalities"""
        if self.loadings is not None:
            communalities = (self.loadings ** 2).sum(axis=1)
            communalities = pd.DataFrame(
                communalities, columns=['Communalities'])
            return communalities

    def get_uniqueness(self):
        """Calculate the specific variance"""
        if self.loadings is not None:
            communalities = self.get_communalities()
            uniqueness = (1 - communalities)
            uniqueness.columns = ['Uniqueness']
            return uniqueness

    def get_communalities_uniqueness(self):
        """Calculate the communalities"""
        if self.loadings is not None:
            communalities = (self.loadings ** 2).sum(axis=1)
            uniqueness = 1 - communalities
            ar = np.array([communalities, uniqueness]).T
            result = pd.DataFrame(ar, columns=['Communalities', 'Uniqueness'],
                                  index=self.data.columns)
            return result

    def get_score(self):
        """Calculate the scores using Bartlett scores"""
        if self.loadings is not None:
            x = bf.central_standard(self.data)
            lds = self.loadings.values
            uniqueness = self.get_uniqueness().values[:, 0]
            p = np.diag(1 / uniqueness)
            part_a = np.linalg.inv(np.dot(np.dot(lds.T, p), lds))
            part_b = np.dot(np.dot(lds.T, p), (x - np.mean(x, axis=0)).T)
            f = np.dot(part_a, part_b).T
            scores = pd.DataFrame(f, columns=self.loadings.columns)
            return scores
