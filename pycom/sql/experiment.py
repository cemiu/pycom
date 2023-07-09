import sqlite3

from pycom.selector.selector_params import ProteinParams
from query_builder import PyComSQLQueryBuilder


db_path = '/Users/philipp/DocumentsLocal/prot.db'

if __name__ == '__main__':
    builder = PyComSQLQueryBuilder()
    # builder.add_constraint('id', 'P0C9F7')
    # builder.add_constraint('sequence', 'MRIAKIGVIALFLFMALGGIGGVMLAGYTFILRAG')
    # builder.add_constraint('minlength', 300)
    # builder.add_constraint('maxlength', 400)
    builder.add_constraint(ProteinParams.MIN_HELIX, 0.1046)
    builder.add_constraint(ProteinParams.MAX_HELIX, 0.105)
    # builder.add_constraint('turnmin', 0.1046)
    # builder.add_constraint('turnmax', 0.105)
    # builder.add_constraint('strandmin', 0.1046)
    # builder.add_constraint('strandmax', 0.105)
    # builder.add_constraint('organism', 'Ochrophyta')
    # builder.add_constraint('cath', '1.20.*.*')
    # builder.add_constraint('enzyme', '1.*')

    # builder.add_constraint('helixmin', 'abc')

    query, params = builder.build()

    conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
    c = conn.cursor()

    c.execute(query, params)

    print(c.fetchall())
