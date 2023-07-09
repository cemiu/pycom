import sqlite3
from typing import List

import pandas as pd

import pycom.interface._find_helper as fh
from pycom.interface.query_helper import query_database
from pycom.util.format_util import user_path


# supress SettingWithCopyWarning from pandas
pd.options.mode.chained_assignment = None  # default='warn'


class PyCom:
    def __init__(
            self,
            db_path: str,
            mat_path: str = None,
            aln_path: str = None
    ):
        self.db_path = user_path(db_path)
        self.mat_path = user_path(mat_path)
        self.aln_path = user_path(aln_path)

    def find(
            self,
            constraint_dict: dict = None,
            uniprot_id: str = None,
            sequence: str = None,
            min_length: int = None,
            max_length: int = None,
            min_helix: float = None,
            max_helix: float = None,
            min_turn: float = None,
            max_turn: float = None,
            min_strand: float = None,
            max_strand: float = None,
            organism: str = None,
            cath: str = None,
            enzyme: str = None,
            has_substrate: bool = None,
            has_ptm: bool = None,
            has_pbd: bool = None,
            disease: str = None,
            disease_id: str = None,
            has_disease: bool = None,
            cofactor: str = None,
            cofactor_id: str = None,
    ) -> pd.DataFrame:
        raise NotImplementedError('Implementation at bottom of file')

    def load_matrices(
            self,
            df: pd.DataFrame,
            max_load: int = 1000
    ) -> pd.DataFrame:
        """
        Load the coevolution matrices into memory
        """
        assert self.mat_path is not None, 'No coevolution matrix file specified'

        assert len(df) <= max_load, f'Attempting to load {len(df)} matrices, max_load is {max_load}. ' \
                                    f'Consider using PyCom.paginate(), or increasing max_load parameter'

        cml = fh.CoevolutionMatrixLoader(self.mat_path)

        df['matrix'] = df['sequence'].apply(lambda x: cml.load_coevolution_matrix(x))

        return df

    @staticmethod
    def paginate(df: pd.DataFrame, page: int, per_page: int = 100) -> pd.DataFrame:
        if 1 > page:
            raise ValueError(f'Pagination starts at 1, not {page}')
        return df.iloc[(page - 1) * per_page:page * per_page]

    def get_disease_list(self) -> pd.DataFrame:
        query = "SELECT diseaseId, diseaseName FROM disease"
        return query_database(query, self.db_path)

    def get_cofactor_list(self) -> pd.DataFrame:
        query = "SELECT cofactorId, cofactorName FROM cofactor"
        return query_database(query, self.db_path)


def _pycom_find(
        self: PyCom,
        constraint_dict: dict = None,
        **kwargs
) -> pd.DataFrame:
    """
    Implementation of PyCom.find(), for capturing kwargs
    """
    # validate the parameters
    constraints = fh.get_valid_find_params(constraint_dict, **kwargs)

    # build the query
    query, params = fh.build_query_from_constraints(**constraints)

    query_result: pd.DataFrame = fh.query_db(db_path=self.db_path, query=query, params=params)

    query_result['matrix'] = pd.Series([None] * len(query_result), dtype='object')

    return query_result


PyCom.find = _pycom_find

if __name__ == '__main__':
    pyc = PyCom(
        db_path='/Users/phil/docs/prot_mat.db',
        mat_path='/Users/phil/docs/mat.h5'
    )

    res = pyc.find(
        min_length=100,
        max_length=200,
        enzyme='1.*'
    )

    # print(len(res))

    # pyc.load_coevolution_matrices(res)

    import time

    start = time.process_time()

    pyc.load_matrices(res)

    # print(time.process_time() - start)

    # print(res.iloc[0]['coevolution_matrix'])

    # print(res)
