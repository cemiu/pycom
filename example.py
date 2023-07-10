from pycom import PyCom
from pycom.selector.selector_params import ProteinParams

pyc = PyCom(db_path='~/docs/pycom.db', mat_path='~/docs/pycom.mat')


# Query the database by passing a dictionary of conditions
entries_a = pyc.find({
    ProteinParams.ENZYME: '3.*.*.*',
    ProteinParams.DISEASE: 'cancer',  # string search, case-insensitive
})


# Alternatively, query the database by passing keyword arguments
entries_b = pyc.find(
    cofactor='FAD',  # string search, case-insensitive
    has_ptm=True,
    has_disease=True,
)


# Get the lists of available cofactors and diseases
cofactors = pyc.get_cofactor_list()
diseases = pyc.get_disease_list()

print('The cofactors are:')
print(cofactors)


# Make a large query, then paginate the results:
entries = pyc.find(min_length=5, max_length=20)
print(f'Found {len(entries)} entries with length <= 20')

page = pyc.paginate(entries, page=1)  # get first n entries (default 100)
print(f'Found {len(page)} entries on page 1')


# Load the coevolution matrices for the results:
pyc.load_matrices(page)

print('Coevolution matrix for the first entry:')
print(page.iloc[0].matrix)
