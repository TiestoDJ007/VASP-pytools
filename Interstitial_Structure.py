import os
import shutil
from copy import deepcopy

import numpy as np
from pymatgen.io.vasp import Poscar

if __name__ == "__main__":
    Module_Number = int(6)
    Situation_Number = int(1)
    Diffusion_Positions = [
        ['1_Oct_alpha', 15, 7, 31, 23, 28, 4],
        ['1_Oct_inter', 13, 15, 87, 84, 7, 4],
        ['1_Oct_beta', 67, 15],
        ['1_Tet_beta', 87, 11, 67, 15],
        # ['1_BO_alpha', 4, 40, 28],
        ['2_Oct_alpha', 15, 7, 31, 23, 28, 4],
        ['2_Oct_beta', 67, 15],
        ['2_Tet_beta', 87, 11, 67, 15]
    ]
    Diffusion_Atoms = ['Al', 'Cr', 'Mo', 'Nb', 'Sn', 'Ti', 'Zr']
    bottom_limit = 3.0
    upper_limit = 13.0

    Structure_Poscar = Poscar.from_file(
        "Calculation_Files/Optimistic_Structure/POSCAR_SO_M{0}_S{1}".format(Module_Number, Situation_Number))

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
            Neb_Path = 'Calculation_Files/CI-NEB/M{0}_S{1}/Interstitial/{2}/Optimistic/{3}'.format(Module_Number,
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

from math import sqrt

tm = np.array([[(sqrt(3) + sqrt(2)), -(sqrt(3) - sqrt(2)), -2 * sqrt(2), 3 * sqrt(2)],
               [-(sqrt(3) + sqrt(2)), (sqrt(3) - sqrt(2)), 2 * sqrt(2), 3 * sqrt(2)],
               [2 * sqrt(3) - sqrt(2), -2 * sqrt(3) + sqrt(2), 2 * sqrt(2), 0]])