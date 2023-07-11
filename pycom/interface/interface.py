from typing import Optional

import pandas as pd

import pycom.interface._find_helper as fh
from pycom.selector import MatrixFormat
from pycom.interface.query_helper import query_database
from pycom.util.format_util import user_path

# supress SettingWithCopyWarning from pandas
pd.options.mode.chained_assignment = None  # default='warn'


class PyCom:
    """
    PyCom is a class that functions as the main interface for querying the PyCom database.

    db_path is required for all queries, and is the only required parameter for the PyCom class.

    mat_path and aln_path are optional parameters, and are only required for loading the coevolution matrices and
    alignments into memory.

    The files can be downloaded from https://pycom.brunel.ac.uk/downloads/ (db_path = pycom.db, mat_path = pycom.mat )

    Usage:
        >>> from pycom import PyCom
        >>> pycom = PyCom(db_path='/path/on/disk/pycom.db', mat_path='/path/on/disk/pycom.mat')
        >>>
        >>> df = pycom.find(disease='cancer')  # Find all proteins associated with cancer
        >>> page = pycom.paginate(df, page=1)  # get the first page of results, 100 results per page
        >>>
        >>> pycom.load_matrices(page)  # load the coevolution matrices for the first page of results
        >>> print(page.iloc[0].matrix)  # print the coevolution matrix for the first result
        >>>
        >>> print(pycom.get_cofactor_list())  # get a list of all cofactors in the database
        >>> print(pycom.get_disease_list())  # get a list of all diseases in the database

    Parameters:
        :param db_path: Path to the PyCom database (pycom.db)
        :param mat_path: Path to the coevolution matrix file (pycom.mat)
        :param aln_path: Path to the alignment file, currently unused

    """

    def __init__(
            self,
            db_path: str,
            mat_path: Optional[str] = None,
            aln_path: Optional[str] = None
    ):
        self.db_path = user_path(db_path)
        assert self.db_path is not None, 'db_path has to be set. `pycom.db` can be downloaded from ' \
                                         'https://pycom.brunel.ac.uk/downloads/'

        self.mat_path = user_path(mat_path)
        self.aln_path = user_path(aln_path)

    def find(
            self,
            constraint_dict: Optional[dict] = None,
            uniprot_id: Optional[str] = None,
            sequence: Optional[str] = None,
            min_length: Optional[int] = None,
            max_length: Optional[int] = None,
            min_helix: Optional[float] = None,
            max_helix: Optional[float] = None,
            min_turn: Optional[float] = None,
            max_turn: Optional[float] = None,
            min_strand: Optional[float] = None,
            max_strand: Optional[float] = None,
            organism_id: Optional[str] = None,
            organism: Optional[str] = None,
            cath: Optional[str] = None,
            enzyme: Optional[str] = None,
            has_substrate: Optional[bool] = None,
            has_ptm: Optional[bool] = None,
            has_pbd: Optional[bool] = None,
            disease: Optional[str] = None,
            disease_id: Optional[str] = None,
            has_disease: Optional[bool] = None,
            cofactor: Optional[str] = None,
            cofactor_id: Optional[str] = None,
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
            >>> dfa = pyc.find(disease='cancer')
            >>> # or
            >>> dfb = pyc.find({ProteinParams.DISEASE: 'cancer'})

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
        :param has_pbd: Whether the protein has a known PDB structure. (True/False)
        :param disease: The disease associated with the protein. (name of disease, case-insensitive [e.g 'cancer'])
        :param disease_id: The ID of the disease associated with the protein. ('DI-00001', get_disease_list()
        :param has_disease: Whether the protein is associated with a disease. (True/False)
        :param cofactor: The cofactor associated with the protein. (name of cofactor, case-insensitive [e.g 'Zn(2+)'])
        :param cofactor_id: The ID of the cofactor associated with the protein. ('CHEBI:00001', get_cofactor_list())
        :return: A pandas DataFrame containing the proteins that match the given criteria.
        """
        raise NotImplementedError('Implementation at bottom of file')

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
