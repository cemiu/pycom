
# from enum import StrEnum  # only available in Python 3.11+
from enum import Enum


class ProteinParams(str, Enum):
    """Selector parameters for proteins"""
    ID = 'uniprot_id'
    SEQUENCE = 'sequence'

    MIN_LENGTH = 'min_length'
    MAX_LENGTH = 'max_length'

    MIN_HELIX = 'min_helix'
    MAX_HELIX = 'max_helix'
    MIN_TURN = 'min_turn'
    MAX_TURN = 'max_turn'
    MIN_STRAND = 'min_strand'
    MAX_STRAND = 'max_strand'

    ORGANISM = 'organism'
    CATH = 'cath'
    ENZYME = 'enzyme'

    HAS_SUBSTRATE = 'has_substrate'
    HAS_PTM = 'has_ptm'

    HAS_PDB = 'has_pdb'

    # cofactors
    # disease
    # has_pbd

    # keywords?
    # substrates / rheaIDs?
