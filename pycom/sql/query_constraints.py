from functools import partial

from pycom.selector.selector_params import ProteinParams
from pycom.sql.constraints_utils import organism_constraint, class_constraint, class_param, to_int, to_float, to_bool

"""This class defines the constraints for the query builder

It both defines the constraint to query mapping and validation
of the parameters.
"""

_constraints_simple = {
    ProteinParams.ID: {  # uniprot id
        'constraint': lambda _: 'entry.entryId = ?',
        'param': lambda x: str(x),
        # 'validate': lambda x: bool(re.match(r'^[\d\w]{6,10}$', x))
    },
    ProteinParams.SEQUENCE: {  # sequence
        'constraint': lambda _: 'entry.sequence = ?',
        'param': lambda x: str(x).upper(),
        # 'validate': lambda x: bool(re.match(r'^[A-Z]+$', x))
    },
    ProteinParams.MIN_LENGTH: {  # minimum sequence length
        'constraint': lambda _: 'entry.sequenceLength >= ?',
        'param': partial(to_int, entry=ProteinParams.MIN_LENGTH),
    },
    ProteinParams.MAX_LENGTH: {  # maximum sequence length
        'constraint': lambda _: 'entry.sequenceLength <= ?',
        'param': partial(to_int, entry=ProteinParams.MAX_LENGTH),
    },
}

_constraints_struct = {
    ProteinParams.MIN_HELIX: {  # minimum fraction of protein in helix
        'constraint': lambda _: 'entry.structhelix >= ?',
        'param': partial(to_float, entry=ProteinParams.MIN_HELIX),
    },
    ProteinParams.MAX_HELIX: {  # maximum fraction of protein in helix
        'constraint': lambda _: 'entry.structhelix <= ?',
        'param': partial(to_float, entry=ProteinParams.MAX_HELIX),
    },
    ProteinParams.MIN_TURN: {  # minimum fraction of protein in turn
        'constraint': lambda _: 'entry.structturn >= ?',
        'param': partial(to_float, entry=ProteinParams.MIN_TURN),
    },
    ProteinParams.MAX_TURN: {  # maximum fraction of protein in turn
        'constraint': lambda _: 'entry.structturn <= ?',
        'param': partial(to_float, entry=ProteinParams.MAX_TURN),
    },
    ProteinParams.MIN_STRAND: {  # minimum fraction of protein in strand
        'constraint': lambda _: 'entry.structstrand >= ?',
        'param': partial(to_float, entry=ProteinParams.MIN_STRAND),
    },
    ProteinParams.MAX_STRAND: {  # maximum fraction of protein in strand
        'constraint': lambda _: 'entry.structstrand <= ?',
        'param': partial(to_float, entry=ProteinParams.MAX_STRAND),
    },
    ProteinParams.HAS_PTM: {  # has post-translational modification
        'constraint': lambda _: 'entry.hasPTM = ?',
        'param': partial(to_bool, entry=ProteinParams.HAS_PTM)
    },
    ProteinParams.HAS_SUBSTRATE: {  # has substrate
        'constraint': lambda _: 'entry.hasSubstrate = ?',
        'param': partial(to_bool, entry=ProteinParams.HAS_SUBSTRATE)
    },
    ProteinParams.HAS_PDB: {  # has PDB structure
        'constraint': lambda _: 'entry.hasPDB = ?',
        'param': partial(to_bool, entry=ProteinParams.HAS_PDB)
    },
}

_constraints_special = {
    ProteinParams.ORGANISM: {  # organism
        'constraint': organism_constraint,
        'param': lambda x: f'%:{x}:%',  # add wildcards
    },
    ProteinParams.CATH: {  # CATH class
        'constraint': partial(class_constraint, entry_type='cath'),
        'param': lambda x: class_param(x),
    },
    ProteinParams.ENZYME: {  # Enzyme class
        'constraint': partial(class_constraint, entry_type='enzyme'),
        'param': lambda x: class_param(x),
    },
}

# merge all constraints into the final list
constraints_template = {**_constraints_simple, **_constraints_struct, **_constraints_special}

# check that all constraints are implemented
assert set(constraints_template.keys()) == set(ProteinParams), 'Not all query constraints are implemented'
