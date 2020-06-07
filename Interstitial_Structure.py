import os
import shutil
from copy import deepcopy

import numpy as np
from pymatgen.io.vasp import Poscar

if __name__ == "__main__":
    Module_Number = int(6)
    Situation_Number = int(1)
    Diffusion_Positions = [
        ['Oct_a', 13, 5, 29, 21, 26, 2],
        ['C_a', 13, 2],
        ['BC_b', 82, 10, 13],
        ['Oct_b', 66, 13]
    ]
    Diffusion_Atoms = ['Al', 'Cr', 'Mo', 'Nb', 'Sn', 'Ti', 'Zr']
    bottom_limit = 5.0
    upper_limit = 13.0

    Structure_Poscar = Poscar.from_file(
        "/mnt/c/Users/jackx/OneDrive/Calculation_Data/TC17_TI80/Optimistic_Structures/POSCAR_SO_M{0}_S{1}".format(
            Module_Number, Situation_Number))

    sd_init = np.ones((Structure_Poscar.natoms[0], 3))
    for number_atom in range(0, Structure_Poscar.natoms[0]):
        atom_position_z = Structure_Poscar.structure[number_atom].z
        if atom_position_z < bottom_limit or atom_position_z > upper_limit:
            sd_init[number_atom] = np.zeros((1, 3))
    sd_atoms = np.row_stack((sd_init, np.ones((1, 3))))

    for Diffusion_Atom in Diffusion_Atoms:
        for Diffusion_Position in Diffusion_Positions:
            interstitial_postion = np.zeros(3)
            for Atom_Number in Diffusion_Position[1:]:
                interstitial_postion = interstitial_postion + Structure_Poscar.structure[Atom_Number - 1].coords
            interstitial_postion = interstitial_postion / (len(Diffusion_Position) - 1)
            interstitial_structure = deepcopy(Structure_Poscar.structure)
            interstitial_structure.append(Diffusion_Atom, interstitial_postion, coords_are_cartesian=True)
            Neb_Path = '/mnt/c/Users/jackx/OneDrive/Calculation_Data/TC17_TI80/Optimistic_Files/M{0}_S{1}/Interstitial/{2}/{3}'.format(
                Module_Number,
                Situation_Number,
                Diffusion_Atom,
                Diffusion_Position[
                    0])
            if os.path.exists(Neb_Path):
                shutil.rmtree(Neb_Path)
            os.makedirs(Neb_Path)
            Poscar_write = Poscar(interstitial_structure)
            Poscar_write.selective_dynamics = sd_atoms
            Poscar_write.write_file('{}/POSCAR'.format(Neb_Path))
            Poscar_write.structure.to(filename='{}/POSCAR.cif'.format(Neb_Path))

# from math import sqrt

# tm = np.array([[(sqrt(3) + sqrt(2)), -(sqrt(3) - sqrt(2)), -2 * sqrt(2), 3 * sqrt(2)],
#               [-(sqrt(3) + sqrt(2)), (sqrt(3) - sqrt(2)), 2 * sqrt(2), 3 * sqrt(2)],
#               [2 * sqrt(3) - sqrt(2), -2 * sqrt(3) + sqrt(2), 2 * sqrt(2), 0]])
