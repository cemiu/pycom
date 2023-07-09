# from pycom.interface import PyCom
from pycom.interface import PyCom
from pycom.selector.selector_params import ProteinParams

# example of planned workflow

pycom = PyCom(db_path='~/docs/prot_mat.db', mat_path='~/docs/mat.h5')

# mode 1
entries1 = pycom.find({
    ProteinParams.MIN_HELIX: 0.1046,
    ProteinParams.MAX_HELIX: 0.2,
})  # returns a list of entries

print(f'Found {len(entries1)} entries')

# mode 2
entries2 = pycom.find(
    min_helix=0.1046,
    max_helix=0.2,
)  # returns a list of entries

print(f'Found {len(entries2)} entries')

entries_paged = pycom.paginate(entries1, page=23, per_page=2)  # returns a paginated list of entries

print(f'Page 1 has {len(entries_paged)} entries')

print(entries_paged.iloc[0])

pycom.load_matrices(entries_paged)  # loads the matrices into the entries

print(entries_paged.iloc[0])

# print(entries_paged[0].coevolution_matrix)  # returns the coevolution matrix

# pycom.lo
