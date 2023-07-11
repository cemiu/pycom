
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

    ORGANISM_ID = 'organism_id'
    ORGANISM = 'organism'

    CATH = 'cath'
    ENZYME = 'enzyme'

    HAS_SUBSTRATE = 'has_substrate'
    HAS_PTM = 'has_ptm'

    HAS_PDB = 'has_pdb'

    DISEASE = 'disease'
    DISEASE_ID = 'disease_id'
    HAS_DISEASE = 'has_disease'

    COFACTOR = 'cofactor'
    COFACTOR_ID = 'cofactor_id'

    def description(self):
        return descriptions[self]

    # cofactors

    # keywords?
    # substrates / rheaIDs?


descriptions = {
    ProteinParams.ID: 'The UniProt ID of the protein.',
    ProteinParams.SEQUENCE: 'The amino acid sequence of protein to search for. (full match)',
    ProteinParams.MIN_LENGTH: 'Minimum number of residues.',
    ProteinParams.MAX_LENGTH: 'Maximum number of residues.',
    ProteinParams.MIN_HELIX: 'Min percentage of helical structure in the protein.',
    ProteinParams.MAX_HELIX: 'Max percentage of helical structure in the protein.',
    ProteinParams.MIN_TURN: 'Min percentage of turn structure in the protein.',
    ProteinParams.MAX_TURN: 'Max percentage of turn structure in the protein.',
    ProteinParams.MIN_STRAND: 'Min percentage of beta strand structure in the protein.',
    ProteinParams.MAX_STRAND: 'Max percentage of beta strand structure in the protein.',
    ProteinParams.ORGANISM_ID: 'NCBI Taxonomy ID of the genus / species of the protein. (get_organism_list())',
    ProteinParams.ORGANISM: 'Name of the genus / species of the protein. (case insensitive [e.g. \'proteobacteria\'])',
    ProteinParams.CATH: 'CATH classification of the protein ( \'3.40.50.360\' or \'3.40.*.*\' or \'3.*\' ).',
    ProteinParams.ENZYME: 'Enzyme Commission number of the protein. ( \'3.40.50.360\' or \'3.40.*.*\' or \'3.*\' ).',
    ProteinParams.HAS_SUBSTRATE: 'Whether the protein has a known substrate. (True/False)',
    ProteinParams.HAS_PTM: 'Whether the protein has a known post-translational modification. (True/False)',
    ProteinParams.HAS_PDB: 'Whether the protein has a known PDB structure. (True/False)',
    ProteinParams.DISEASE: 'The disease associated with the protein. (name of disease, case insensitive '
                           '[e.g \'cancer\'])',
    ProteinParams.DISEASE_ID: 'The ID of the disease associated with the protein. (\'DI-00001\', get_disease_list()',
    ProteinParams.HAS_DISEASE: 'Whether the protein is associated with a disease. (True/False)',
    ProteinParams.COFACTOR: 'The cofactor associated with the protein. (name of cofactor, case insensitive '
                            '[e.g \'Zn(2+)\'])',
    ProteinParams.COFACTOR_ID: 'The ID of the cofactor associated with the protein. '
                               '(\'CHEBI:00001\', get_cofactor_list()',
}

assert set(descriptions.keys()) == set(ProteinParams), 'Descriptions missing for some ProteinParams'
