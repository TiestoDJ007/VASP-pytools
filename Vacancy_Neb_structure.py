#!/home/universe/local_env/anaconda3/envs/abinit/bin/python
import os
import shutil
from copy import deepcopy

import numpy as np
from pymatgen.io.vasp import Poscar

Module_Number = int(4)
Situation_Number = int(1)
First_Atom = [1]
Second_Atom = [19]
Diffusion_Atoms = ['Al', 'Cr', 'Mo', 'Nb', 'Sn', 'Ti', 'Zr']
Original_POSCAR = Poscar.from_file(
    "Calculation_Files/Optimistic_Structure/POSCAR_SO_M{0}_S{1}".format(Module_Number, Situation_Number))

for atom_first in First_Atom:
    for atom_second in Second_Atom:
        for Diffusion_Atom in Diffusion_Atoms:
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

            # sd_bool = Ini_Structure.selective_dynamics
            # sd_int = []
            # for bool_list in sd_bool:
            #    int_list = np.array(bool_list).astype(int)
            #    sd_int.append(int_list)
            # sd_int.append(np.array((1, 1, 1)))
            # sd_int = np.array(sd_int)

            sd_int = np.zeros((np.sum(Ini_Structure.natoms), 3))
            sd_int = np.row_stack((sd_int, [1, 1, 1]))

            Ini_Structure.structure.append(Diffusion_Atom, (Ini_x, Ini_y, Ini_z), coords_are_cartesian=True)
            Ini_Structure.selective_dynamics = sd_int

            Fin_Structure.structure.append(Diffusion_Atom, (Fin_x, Fin_y, Fin_z), coords_are_cartesian=True)
            Fin_Structure.selective_dynamics = sd_int

            structure_path = "Calculation_Files/CI-NEB/M{0}_S{1}_single/{2}".format(Module_Number, Situation_Number,
                                                                                    Diffusion_Atom)
            cineb_path = structure_path + "/{0:0>2d}-{1:0>2d}".format(atom_first, atom_second)
            if os.path.exists(cineb_path):
                shutil.rmtree(cineb_path)
            os.makedirs(cineb_path)
            Ini_Structure.write_file(cineb_path + "/POSCAR_Ini")
            Fin_Structure.write_file(cineb_path + "/POSCAR_Fin")

        # pot_file = Potcar(symbols=Fin_Structure.site_symbols, functional='PBE')
        # pot_file.write_file(structure_path + "/POTCAR")