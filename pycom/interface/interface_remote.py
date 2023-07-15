import numpy as np
import requests
import pandas as pd

from pycom.interface import PyCom
from pycom.selector import MatrixFormat
from typing import Dict

import pycom.interface._find_helper as fh


class PyComRemote(PyCom):
    """
    A Python wrapper for the PyCom API.

    This class provides a way to interact with the PyCom API in a Pythonic way, using
    standard Python data types and structures. It converts the JSON responses from the API into
    pandas DataFrame objects, which are easier to work with for data analysis.

    Example Usage:

        pyc = PyComRemote()
        results = pyc.find(
            {ProteinParams.DISEASE: "cancer", ProteinParams.MAX_LENGTH: 150}, page=1, per_page=5, matrix=True)
        disease_list = pyc.get_disease_list()
        cofactor_list = pyc.get_cofactor_list()
        organism_list = pyc.get_organism_list()

    """
    def __init__(self, remote: bool = True):
        self.base_url = 'https://pycom.brunel.ac.uk/api'

    def _get_url(self, endpoint: str) -> str:
        """
        Helper method that returns the URL for a given API endpoint.
        """
        return f'{self.base_url}/{endpoint}'

    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """
        Helper method that sends a GET request to the provided endpoint with optional parameters
        and returns the JSON response.
        """
        response = requests.get(self._get_url(endpoint), params=params)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:  # Bad request, forwards the error message from the API
                raise requests.exceptions.HTTPError(f'Error while making request to {endpoint}: '
                                                    f'{e.response.json()["message"]}')
            else:  # Other error, raises the original exception
                raise e
        return response.json()

    def find(  # noqa: Different order of named parameters
            self,
            constraint_dict: dict = None,
            /,
            *,
            page: int = None,
            per_page: int = 10,
            matrix: bool = False,
            mat_format: MatrixFormat = MatrixFormat.NUMPY,
            **kwargs
    ) -> pd.DataFrame:
        """
        Fetches protein data from the 'find' endpoint as a pandas DataFrame.

        Parameters:
            constraint_dict (dict): A dictionary of constraints for the protein data.
            page (int): The page number to request. Defaults to 1.
            per_page (int): The number of results per page. Defaults to 10.
            matrix (bool): Whether to include the matrices in the results. Defaults to False.
            mat_format (MatrixFormat): The format of the matrices. Defaults to MatrixFormat.NUMPY.

        Returns:
            pandas.DataFrame: DataFrame containing the protein data.

        """
        assert page is not None, 'page must be specified for remote queries (pycom.find(..., page=1))'
        assert per_page <= 100, 'per_page must be <= 100 for remote queries (pycom.find(..., per_page=100))'
        if matrix:
            assert per_page <= 10, \
                'per_page must be <= 10 for remote queries with matrices (pycom.find(..., per_page=10, matrix=True))'

        params = fh.get_valid_find_params(remote=True, constraint_dict=constraint_dict, **kwargs)
        params.update({'page': page, 'per_page': per_page, 'matrix': matrix})

        response = self._make_request('find', params)

        if 'results' not in response:
            return pd.DataFrame()  # Return empty DataFrame if there are no results.

        res = pd.DataFrame(response['results'])

        if res.empty:
            return res

        if matrix:
            res['matrix'] = res['matrix'].apply(np.array)  # MatrixFormat assumes numpy array
            res['matrix'] = res['matrix'].apply(mat_format)  # Convert to desired format

        return res

    def get_disease_list(self) -> pd.DataFrame:
        """
        Fetches disease data from the 'get-disease-list' endpoint as a pandas DataFrame.

        Returns:
            pandas.DataFrame: DataFrame containing the disease data.

        """
        response = self._make_request('get-disease-list')

        if len(response) == 0:
            return pd.DataFrame()  # Return empty DataFrame if there are no results.

        return pd.DataFrame(response)

    def get_cofactor_list(self) -> pd.DataFrame:
        """
        Fetches cofactor data from the 'get-cofactor-list' endpoint as a pandas DataFrame.

        Returns:
            pandas.DataFrame: DataFrame containing the cofactor data.

        """
        response = self._make_request('get-cofactor-list')

        if len(response) == 0:
            return pd.DataFrame()  # Return empty DataFrame if there are no results.

        return pd.DataFrame(response)

    def get_organism_list(self) -> pd.DataFrame:
        """
        Fetches organism data from the 'get-organism-list' endpoint as a pandas DataFrame.

        Returns:
            pandas.DataFrame: DataFrame containing the organism data.

        """
        response = self._make_request('get-organism-list')

        if len(response) == 0:
            return pd.DataFrame()  # Return empty DataFrame if there are no results.

        return pd.DataFrame(response)

    @staticmethod
    def paginate(*_, **__) -> pd.DataFrame:
        raise NotImplementedError('Pagination is not supported for the remote API, use the `page` and `per_page` '
                                  'parameters in the `find` method instead.')

    def load_matrices(*_, **__) -> pd.DataFrame:
        raise NotImplementedError('Loading matrices is not supported for the remote API, use the `matrix` parameter '
                                  'in the `find` method instead.')
