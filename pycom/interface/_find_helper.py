import sqlite3
from typing import Optional

import h5py
import pandas as pd

from pycom.selector import ProteinParams, MatrixFormat
from pycom.sql.query_builder import PyComSQLQueryBuilder
from pycom.util.format_util import md5_hash


def get_valid_find_params(
        constraint_dict: dict = None,
        **kwargs
):
    """
    Validate that the parameters passed to find() are valid and return a dictionary of the parameters
    """
    # if no arguments are passed, return all proteins
    assert not (constraint_dict is not None and kwargs != {}), 'Use either a dictionary or keywords, not both'

    if constraint_dict is None:  # no dictionary passed, use kwargs
        constraint_dict = kwargs

    if constraint_dict == {}:
        import warnings
        warnings.warn('Calling PyCom.find() without constraints returns all proteins, this may be slow')

    valid_keys = set(ProteinParams)
    for key in constraint_dict:  # check that all keys are valid
        assert key in valid_keys, f'"{key}" is not a defined constraint'

    return constraint_dict


def build_query_from_constraints(**constraint_dict):
    """
    Build a query from a dictionary of constraints
    """
    builder = PyComSQLQueryBuilder()
    for key, value in constraint_dict.items():
        builder.add_constraint(key, value)
    return builder.build()


def query_db(db_path, query, params):
    """
    Takes in a query generated by PyComSQLQueryBuilder and returns a pandas DataFrame

    It is possible to wrap this function in a memoize decorator to cache the results of queries

    e.g. when using flask-caching:
        query_db = cache.memoize(timeout=360, cache_none=True)(query_db)
    """
    conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
    c = conn.cursor()
    c.execute(query, params)

    result: list = c.fetchall()
    result: pd.DataFrame = pd.DataFrame(result, columns=PyComSQLQueryBuilder.columns)

    conn.close()

    return result


class CoevolutionMatrixLoader:
    """
    A class that loads coevolution matrices from an HDF5 file
    """
    def __init__(
            self,
            matrix_path,
            mat_format: MatrixFormat = MatrixFormat.NUMPY
    ):
        self.matrix_path = matrix_path
        self.mat_db: h5py.File = h5py.File(matrix_path, 'r')
        self.mat_formatter = mat_format

    def load_coevolution_matrix(self, sequence: str) -> Optional[pd.DataFrame]:
        """
        Load a coevolution matrix from an HDF5 file
        """
        md5 = md5_hash(sequence)

        try:
            return self.mat_formatter(self.mat_db[md5][:])
        except KeyError:
            return None
