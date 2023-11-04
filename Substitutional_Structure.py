import os
import shutil
from copy import deepcopy

import numpy as np
from pymatgen.io.vasp import Poscar

if __name__ == "__main__":
#    Module_Number = int(5)
    Situation_Number = int(3)
    Diffusion_Positions = [
        ['a', 16],
        ['b', 84],
        ['i', 40]
    ]
    Diffusion_Atoms = ['W']
    bottom_limit = 3.0
    upper_limit = 13.0

    Structure_Poscar = Poscar.from_file(
        "/mnt/c/Users/jackx/OneDrive/Calculation_Data/TC17_TI80/Optimistic_Structures/POSCAR_SO_M{0}_S{1}".format(
            Module_Number, Situation_Number))

    for Diffusion_Atom in Diffusion_Atoms:
        for Diffusion_Position in Diffusion_Positions:
            Substitutional_Number = Diffusion_Position[1] - 1
            Substitutional_structure = deepcopy(Structure_Poscar.structure)
            Substitutional_Coord = deepcopy(Substitutional_structure[Substitutional_Number].coords)
            Substitutional_structure.remove_sites(range(Substitutional_Number, Substitutional_Number + 1))
            Substitutional_structure.append(Diffusion_Atom, Substitutional_Coord, coords_are_cartesian=True)

            sd_init = np.ones((Substitutional_structure.num_sites, 3))
            for number_atom in range(0,Substitutional_structure.num_sites):
                atom_position_z = Substitutional_structure[number_atom].z
                if atom_position_z<bottom_limit or atom_position_z >upper_limit:
                    sd_init[number_atom]=np.zeros((1,3))
            sd_atoms = sd_init

            Neb_Path = '/mnt/c/Users/jackx/OneDrive/Calculation_Data/TC17_TI80/NEB_Files/M{0}_S{1}/Substitutional/{2}/Optimistic/{3}'.format(
                Module_Number,
                Situation_Number,
                Diffusion_Atom,
                Diffusion_Position[
                    0])
            if os.path.exists(Neb_Path):
                shutil.rmtree(Neb_Path)
            os.makedirs(Neb_Path)
            Poscar_write = Poscar(Substitutional_structure)
            Poscar_write.selective_dynamics = sd_atoms
            Poscar_write.write_file('{}/POSCAR'.format(Neb_Path))
            Poscar_write.structure.to(filename='{}/POSCAR.cif'.format(Neb_Path))
