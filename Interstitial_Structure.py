import os
import shutil
from copy import deepcopy

import numpy as np
from pymatgen.io.vasp import Poscar

if __name__ == "__main__":
    Module_Number = int(5)
    Situation_Number = int(3)
    Diffusion_Positions = [
        ['1_Oct_alpha', 40, 16, 44, 8, 28, 4],
        ['1_Tet_inter', 84, 40, 4, 88],
        ['1_Oct_inter_beta', 80, 76, 84, 88, 40, 4],
        ['1_Oct_beta', 80, 76],
        ['1_Tet_beta', 80, 84, 88, 76],
        # ['1_BO_alpha', 4, 40, 28],
        ['2_Oct_alpha', 28, 19, 32, 15, 43, 8],
        ['2_Oct_inter_alpha', 88, 83, 39, 15, 28, 4],
        ['2_Oct_inter_beta', 88, 76, 79, 83, 39, 4],
        ['2_Oct_beta', 76, 79],
        ['2_Tet_beta', 79, 76, 88, 83]
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
            Neb_Path = 'Calculation_Files/CI-NEB/M{0}_S{1}/Interstitial/{2}/{3}'.format(Module_Number, Situation_Number,
                                                                                        Diffusion_Atom,
                                                                                        Diffusion_Position[0])
            if os.path.exists(Neb_Path):
                shutil.rmtree(Neb_Path)
            os.makedirs(Neb_Path)
            Poscar_write = Poscar(interstitial_structure)
            Poscar_write.selective_dynamics = sd_atoms
            Poscar_write.write_file('{}/POSCAR'.format(Neb_Path))
