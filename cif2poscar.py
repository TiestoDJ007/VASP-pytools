import numpy as np
from pymatgen.io.cif import CifParser
from pymatgen.io.cif import CifWriter
from pymatgen.io.vasp import Poscar

parser = CifParser("Data_file/Layer_first.cif")
structure = (parser.get_structures()[0]) * (-1)
#POSCAR_Data = Poscar.from_file('Data_file/POSCAR')
#structure = POSCAR_Data.structure

upper_position = 17.0
bottom_position = 7.0
atomic_tot_number = len(structure.sites)
select_dynamics_list = []

number_atom = 0
for number_atom in range(0, atomic_tot_number):
    c_position = structure.cart_coords[number_atom][2]
    if bottom_position < c_position < upper_position:
        select_dynamics_list.append([1, 1, 1])
    else:
        select_dynamics_list.append([0, 0, 0])

select_dynamics_array = np.array(select_dynamics_list)
# Poscar_Writer_Cart = Poscar_Writer.get_str(direct=False)

CIF_Writer = CifWriter(structure)
CIF_Writer.write_file(filename="Data_file/Layer_first_modified.cif")

Poscar_parser = CifParser(filename="Data_file/Layer_first_modified.cif")
Poscar_structure = Poscar_parser.get_structures()[0]
Poscar_writer = Poscar(Poscar_structure, selective_dynamics=select_dynamics_array)
#Poscar_writer = Poscar(structure, selective_dynamics=select_dynamics_array)
Poscar_writer.write_file(filename="Data_file/POSCAR")
