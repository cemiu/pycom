import os
import sqlite3

db_path = '/Users/philipp/Documents/prot.db'


'''
id: entry.entryId = id
sequence: entry.sequence = sequence
minlength: entry.sequenceLength >= minlength
maxlength: entry.sequenceLength <= maxlength
organism: organism.taxonomy LIKE '%organism%' => organism.organismId => entry.organismId
structhelix: entry.structhelix <= structhelix
structturn: entry.structturn <= structturn
structstrand: entry.structstrand <= structstrand
cathclass (A.B.C.D): cath_class.cath_1 = A, cath_class.cath_2 = B, cath_class.cath_3 = C, cath_class.cath_4 = D => cath_class.entryId => entry.entryId
enzymeclass (A.B.C.D): enzyme_class.enzyme_1 = A, enzyme_class.enzyme_2 = B, enzyme_class.enzyme_3 = C, enzyme_class.enzyme_4 = D => enzyme_class.entryId => entry.entryId
'''

def test():
    conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
    c = conn.cursor()

    # Define the constraints
    id, sequence, minlength, maxlength, organism, structhelix, structturn, structstrand, cathclass, enzymeclass = None, None, None, None, None, None, None, None, None, None

    # id = 123
    sequence = 'MPHYVVVKSPMRRRRSPRRRSPRVCYSPRRVACSPRRRSPRRRSPRRRSPRRSIVVY'
    # minlength = 10
    # maxlength = 100
    # organism = 'Aizoaceae'
    # structhelix = 5
    # structturn = 3
    # structstrand = 2
    # cathclass = '1.2.3.4'
    # enzymeclass = '5.6.7.8'

    # Define the query template
    query = '''
    SELECT entry.entryId
    FROM entry
    JOIN organism ON organism.organismId = entry.organismId
    JOIN cath_class ON cath_class.entryId = entry.entryId
    /* JOIN enzyme_class ON enzyme_class.entryId = entry.entryId */
    WHERE ({0})
    '''

    # Define the query conditions based on the constraints
    conditions = []
    params = []
    if id is not None:
        conditions.append('entry.entryId = ?')
        params.append(id)
    if sequence is not None:
        conditions.append('entry.sequence = ?')
        params.append(sequence)
    if minlength is not None:
        conditions.append('entry.sequenceLength >= ?')
        params.append(minlength)
        params.append(maxlength)
    if maxlength is not None:
        conditions.append('entry.sequenceLength <= ?')
        params.append(maxlength)
    if organism is not None:
        conditions.append('organism.taxonomy LIKE ? AND organism.organismId = entry.organismId')
        params.append(f'%{organism}%')
    if structhelix is not None:
        conditions.append('entry.structhelix <= ?')
        params.append(structhelix)
    if structturn is not None:
        conditions.append('entry.structturn <= ?')
        params.append(structturn)
    if structstrand is not None:
        conditions.append('entry.structstrand <= ?')
        params.append(structstrand)
    if cathclass is not None:
        conditions.append('cath_class.cath_1 = ? AND cath_class.cath_2 = ? AND cath_class.cath_3 = ? AND cath_class.cath_4 = ? AND cath_class.entryId = entry.entryId')
        params.extend(cathclass.split('.'))
    if enzymeclass is not None:
        conditions.append('enzyme_class.enzyme_1 = ? AND enzyme_class.enzyme_2 = ? AND enzyme_class.enzyme_3 = ? AND enzyme_class.enzyme_4 = ? AND enzyme_class.entryId = entry.entryId')
        params.extend(enzymeclass.split('.'))

    # Build the final query
    print(conditions)
    conditions.append('1=1')
    conditions_formatted = ' AND '.join(map('{0}'.format, conditions))
    query = query.format(conditions_formatted)

    # Execute the query
    # params = [p for p in params if p is not None]

    print(query)
    print(params)
    c.execute(query, params)
    result = c.fetchall()

    # Print the result
    print(result)

test()
