#!/home/universe/local_env/anaconda3/envs/abinit/bin/python
import os
import shutil
from copy import deepcopy

import numpy as np
from pymatgen.io.vasp import Poscar

if __name__ == "__main__":
    bottom_limit = 3.0
    upper_limit = 13.0
    Module_Number = int(5)
    Situation_Number = int(3)
    Vacancies_Sites = [16, 40, 84, 80]  # 一定要按照空位扩散顺序写
    Diffusion_Atoms = ['Al', 'Cr', 'Mo', 'Nb', 'Sn', 'Ti', 'Zr']
    Original_POSCAR = Poscar.from_file(
        "/mnt/c/Users/jackx/OneDrive/Calculation_Data/TC17_TI80/Optimistic_Structures/POSCAR_SO_M{0}_S{1}".format(
            Module_Number, Situation_Number))

    Vacancy_Number = 0
    while Vacancy_Number + 1 < len(Vacancies_Sites):
        Ini_Atom_Number = Vacancies_Sites[Vacancy_Number]
        Fin_Atom_Number = Vacancies_Sites[Vacancy_Number + 1]
        for Diffusion_Atom in Diffusion_Atoms:
            Ini_Structure = deepcopy(Original_POSCAR)
            Fin_Structure = deepcopy(Original_POSCAR)
            Ini_x = Original_POSCAR.structure[Ini_Atom_Number - 1].x
            Ini_y = Original_POSCAR.structure[Ini_Atom_Number - 1].y
            Ini_z = Original_POSCAR.structure[Ini_Atom_Number - 1].z
            Fin_x = Original_POSCAR.structure[Fin_Atom_Number - 1].x
            Fin_y = Original_POSCAR.structure[Fin_Atom_Number - 1].y
            Fin_z = Original_POSCAR.structure[Fin_Atom_Number - 1].z
            Ini_Structure.structure.remove_sites([Ini_Atom_Number - 1, Fin_Atom_Number - 1])
            Fin_Structure.structure.remove_sites([Ini_Atom_Number - 1, Fin_Atom_Number - 1])

            sd_init = np.ones((Ini_Structure.natoms[0], 3))
            for number_atom in range(0, Ini_Structure.natoms[0]):
                atom_position_z = Ini_Structure.structure[number_atom].z
                if atom_position_z < bottom_limit or atom_position_z > upper_limit:
                    sd_init[number_atom] = np.zeros((1, 3))
            sd_atoms = np.row_stack((sd_init, np.ones((1, 3))))

            Ini_Structure.structure.append(Diffusion_Atom, (Ini_x, Ini_y, Ini_z), coords_are_cartesian=True)
            Ini_Structure.selective_dynamics = sd_atoms

            Fin_Structure.structure.append(Diffusion_Atom, (Fin_x, Fin_y, Fin_z), coords_are_cartesian=True)
            Fin_Structure.selective_dynamics = sd_atoms

            structure_path = "/mnt/c/Users/jackx/OneDrive/Calculation_Data/TC17_TI80/NEB_Files/M{0}_S{1}/Vacancy/{2}".format(
                Module_Number, Situation_Number,
                Diffusion_Atom)
            cineb_path = structure_path + "/{0:0>2d}-{1:0>2d}".format(Ini_Atom_Number, Fin_Atom_Number)
            if os.path.exists(cineb_path):
                shutil.rmtree(cineb_path)
            os.makedirs(cineb_path)
            Ini_Structure.write_file(cineb_path + "/POSCAR_Ini")
            Fin_Structure.write_file(cineb_path + "/POSCAR_Fin")
        Vacancy_Number = Vacancy_Number + 1
