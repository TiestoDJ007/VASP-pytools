from pymatgen.io.cif import CifParser
from pymatgen.io.cif import CifWriter
from pymatgen.io.vasp import Poscar
import numpy as np

parser = CifParser("Data_file/Layer_first.cif")
structure = parser.get_structures()[0]

upper_position = -14.0
bottom_position = -24.0
atomic_tot_number = len(structure.sites)
select_dynamics_list = []

number_atom = 0
for number_atom in range(0,atomic_tot_number):
    c_position = structure.cart_coords[number_atom][2]
    if bottom_position <c_position < upper_position:
        select_dynamics_list.append([1 ,1,1])
    else:
        select_dynamics_list.append([0,0,0])

select_dynamics_array = np.array(select_dynamics_list)

Poscar_Writer = Poscar(structure,selective_dynamics=select_dynamics_array)
# Poscar_Writer_Cart = Poscar_Writer.get_str(direct=False)

CIF_Writer = CifWriter(structure)

Poscar_Writer.write_file(filename="Data_file/POSCAR")
CIF_Writer.write_file(filename="Data_file/Layer_first_modified.cif")

