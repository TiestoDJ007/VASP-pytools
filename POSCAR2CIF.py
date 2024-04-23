from pymatgen.io.cif import CifWriter
from pymatgen.io.vasp import Poscar

poscar_data = Poscar.from_file("Data_file/POSCAR")
structure = poscar_data.structure
cif_writer = CifWriter(struct=structure)
cif_writer.write_file("Data_file/layer_opt.cif")
#poscar_data.write_file("POSCAR_lattice_opt")