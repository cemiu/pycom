from typing import Optional

import pandas as pd

from pycom.interface import PyCom

import pycom.interface._find_helper as fh
from pycom.interface.data_loader import PyComDataLoader
from pycom.selector import MatrixFormat
from pycom.interface.query_helper import query_database
from pycom.util.format_util import user_path

# supress SettingWithCopyWarning from pandas
pd.options.mode.chained_assignment = None  # default='warn'


class PyComLocal(PyCom):
    """
    PyCom is a class that functions as the main interface for querying the PyCom database.

    db_path is required for all queries, and is the only required parameter for the PyCom class.

    mat_path is an optional parameter, and is only required for loading the coevolution matrices and
    alignments into memory.

    The files can be downloaded from https://pycom.brunel.ac.uk/downloads/ (db_path = pycom.db, mat_path = pycom.mat )

    Usage:
                >>> from pycom import PyCom
            For local use:
                >>> pycom = PyCom(db_path='/path/on/disk/pycom.db', mat_path='/path/on/disk/pycom.mat')
            Or for remote use:
                >>> pycom_remote = PyCom(remote=True)
            Find all proteins associated with cancer:
                >>> df = pycom.find(disease='cancer')
            Get the first page of results, 100 results per page:
                >>> page = pycom.paginate(df, page=1)
            Load the coevolution matrices for the first page of results:
                >>> pycom.load_matrices(page)
                >>> print(page.iloc[0].matrix)
            Get a list of all cofactors / diseases / organism in the database
                >>> cofactors = pycom.get_cofactor_list()
                >>> diseases = pycom.get_disease_list()
                >>> organisms = pycom.get_organism_list()

    Parameters:
        :param db_path: Path to the PyCom database (pycom.db)
        :param mat_path: Path to the coevolution matrix file (pycom.mat)
    """

    def __init__(
            self,
            db_path: str,
            mat_path: Optional[str] = None
    ):
        self.db_path = user_path(db_path)
        assert self.db_path is not None, 'db_path has to be set. `pycom.db` can be downloaded from ' \
                                         'https://pycom.brunel.ac.uk/downloads/'

        self.mat_path = user_path(mat_path)

    def find(
            self,
            constraint_dict: dict = None,
            /,
            *_,
            **kwargs
    ) -> pd.DataFrame:
        """
        Find proteins in the database that match the given criteria.

        This function searches the database for proteins that match the given criteria. The criteria can be specified using
        any combination of the parameters listed below.

        Use either constraint_dict or the individual parameters, not both.

        Usage:
            >>> from pycom import PyCom, ProteinParams
            >>> pyc = PyCom(db_path='/path/on/disk/pycom.db')
            >>>
            >>> pyc = pyc.find(disease='cancer')
            >>> # or
            >>> pyc = pyc.find({ProteinParams.DISEASE: 'cancer'})

        :param constraint_dict: A dictionary of constraints to apply to the search {ProteinParams: value}.
        :param uniprot_id: The UniProt ID of the protein.
        :param sequence: The amino acid sequence of protein to search for. (full match)
        :param min_length: Minimum number of residues.
        :param max_length: Maximum number of residues.
        :param min_helix: Min percentage of helical structure in the protein.
        :param max_helix: Max percentage of helical structure in the protein.
        :param min_turn: Min percentage of turn structure in the protein.
        :param max_turn: Max percentage of turn structure in the protein.
        :param min_strand: Min percentage of beta strand structure in the protein.
        :param max_strand: Max percentage of beta strand structure in the protein.
        :param organism_id: NCBI Taxonomy ID of the genus / species of the protein. (get_organism_list())
        :param organism: Taxonomic name of the genus / species of the protein. (case-insensitive, get_organism_list())
        :param cath: CATH classification of the protein ( '3.40.50.360' or '3.40.*.*' or '3.*' ).
        :param enzyme: Enzyme Commission number of the protein. ( '3.40.50.360' or '3.40.*.*' or '3.*' ).
        :param has_substrate: Whether the protein has a known substrate. (True/False)
        :param has_ptm: Whether the protein has a known post-translational modification. (True/False)
        :param has_pdb: Whether the protein has a known PDB structure. (True/False)
        :param disease: The disease associated with the protein. (name of disease, case-insensitive [e.g 'cancer'])
        :param disease_id: The ID of the disease associated with the protein. ('DI-00001', get_disease_list()
        :param has_disease: Whether the protein is associated with a disease. (True/False)
        :param cofactor: The cofactor associated with the protein. (name of cofactor, case-insensitive [e.g 'Zn(2+)'])
        :param cofactor_id: The ID of the cofactor associated with the protein. ('CHEBI:00001', get_cofactor_list())
        :return: A pandas DataFrame containing the proteins that match the given criteria.
        """
        # validate the parameters
        constraints = fh.get_valid_find_params(remote=False, constraint_dict=constraint_dict, **kwargs)

        # build the query
        query, params = fh.build_query_from_constraints(**constraints)

        query_result: pd.DataFrame = fh.query_db(db_path=self.db_path, query=query, params=params)
        query_result['matrix'] = pd.Series([None] * len(query_result), dtype='object')

        return query_result

    def load_matrices(
            self,
            df: pd.DataFrame,
            max_load: int = 1000,
            mat_format: MatrixFormat = MatrixFormat.NUMPY
    ) -> pd.DataFrame:
        """
        Load the coevolution matrices into memory

        Takes a DataFrame from PyCom.find() or PyCom.paginate() and loads the coevolution matrices into memory,
        into the 'matrix' column.

        Requires the coevolution matrix file (pycom.mat) to be downloaded from https://pycom.brunel.ac.uk/downloads/

        By default, this function will only load the first 1000 matrices. This can be changed by setting max_load.
        """
        assert self.mat_path is not None, 'mat_path has to be set. `pycom.mat` can be downloaded from ' \
                                          'https://pycom.brunel.ac.uk/downloads/'

        assert len(df) <= max_load, f'Attempting to load {len(df)} matrices, max_load is {max_load}. ' \
                                    f'Consider using PyCom.paginate(), or increasing max_load parameter'

        cml = fh.CoevolutionMatrixLoader(self.mat_path, mat_format=mat_format)

        df['matrix'] = df['sequence'].apply(lambda x: cml.load_coevolution_matrix(x))

        return df

    @staticmethod
    def paginate(df: pd.DataFrame, page: int, per_page: int = 100) -> pd.DataFrame:
        """
        Paginate a DataFrame that is generated by PyCom.find().
        This is useful for using PyCom.load_matrices() on a large DataFrame.

        First page is 1.
        By default, 100 results are returned per page; this can be changed by setting per_page.

        :param df: The DataFrame to paginate
        :param page: The page number to return
        :param per_page: The number of results to return per page
        """

        if 1 > page:
            raise ValueError(f'Pagination starts at 1, not {page}')
        return df.iloc[(page - 1) * per_page:page * per_page]

    def get_disease_list(self) -> pd.DataFrame:
        """
        Retrieves the list of all diseases in the database.

        Returns:
            List[str]: A list of diseases.
        """
        query = "SELECT diseaseId, diseaseName FROM disease"
        return query_database(query, self.db_path)

    def get_cofactor_list(self) -> pd.DataFrame:
        """
        Retrieves the list of all cofactors in the database.

        Returns:
            List[str]: A list of cofactors.
        """
        query = "SELECT cofactorId, cofactorName FROM cofactor"
        return query_database(query, self.db_path)

    def get_organism_list(self):
        """
        Retrieves the list of all organisms in the database.

        Returns:
            List[str]: A list of organisms.
        """
        query = "SELECT organismId, nameScientific, nameCommon, taxonomy FROM organism"
        return query_database(query, self.db_path)

    def get_data_loader(self) -> PyComDataLoader:
        """
        Returns the PyComDataLoader object that is used to load additional data into the dataframe.

        :return: PyComDataLoader
        """
        return PyComDataLoader(self.db_path)