#!/home/universe/local_env/anaconda3/envs/abinit/bin/python
import os
from copy import deepcopy

import numpy as np
from pymatgen.io.vasp import Poscar, Potcar

Module_Number = int(1)
Situation_Number = int(1)
First_Atom = [61]
Second_Atom = [4, 13, 15, 17]
Original_POSCAR = Poscar.from_file(
    "Calculation_Files/Optimistic_Structure/POSCAR_SO_M{0}_S{1}".format(Module_Number, Situation_Number))

for atom_first in First_Atom:
    for atom_second in Second_Atom:
        Ini_Structure = deepcopy(Original_POSCAR)
        Fin_Structure = deepcopy(Original_POSCAR)
        Ini_x = Original_POSCAR.structure[atom_first - 1].x
        Ini_y = Original_POSCAR.structure[atom_first - 1].y
        Ini_z = Original_POSCAR.structure[atom_first - 1].z
        Fin_x = Original_POSCAR.structure[atom_second - 1].x
        Fin_y = Original_POSCAR.structure[atom_second - 1].y
        Fin_z = Original_POSCAR.structure[atom_second - 1].z
        Ini_Structure.structure.remove_sites([atom_first - 1, atom_second - 1])
        Fin_Structure.structure.remove_sites([atom_first - 1, atom_second - 1])

        sd_bool = Ini_Structure.selective_dynamics
        sd_int = []
        for bool_list in sd_bool:
            int_list = np.array(bool_list).astype(int)
            sd_int.append(int_list)
        sd_int.append(np.array((1, 1, 1)))
        sd_int = np.array(sd_int)

        Ini_Structure.structure.append('Al', (Ini_x, Ini_y, Ini_z), coords_are_cartesian=True)
        Ini_Structure.selective_dynamics = sd_int

        Fin_Structure.structure.append('Al', (Fin_x, Fin_y, Fin_z), coords_are_cartesian=True)
        Fin_Structure.selective_dynamics = sd_int

        os.makedirs(
            "Calculation_Files/CI-NEB/{2}/{0}-{1}/".format(atom_first, atom_second, Fin_Structure.site_symbols[1]))

        Ini_Structure.write_file(
            "Calculation_Files/CI-NEB/{2}/{0}-{1}/POSCAR_Ini".format(atom_first, atom_second,
                                                                     Fin_Structure.site_symbols[1]))
        Fin_Structure.write_file(
            "Calculation_Files/CI-NEB/{2}/{0}-{1}/POSCAR_Fin".format(atom_first, atom_second,
                                                                     Fin_Structure.site_symbols[1]))

        pot_file = Potcar(symbols=Fin_Structure.site_symbols, functional='PBE')
        pot_file.write_file("Calculation_Files/CI-NEB/{1}/POTCAR".format(Fin_Structure.site_symbols[0],
                                                                         Fin_Structure.site_symbols[1]))
