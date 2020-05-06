from copy import deepcopy

import numpy as np
from pymatgen.io.vasp import Poscar

if __name__ == "__main__":
    Module_Number = int(6)
    Situation_Number = int(1)
    Diffusion_Positions = [['Oct_alpha', 15, 7, 31, 23, 28, 4],
                           ['Oct_inter', 13, 15, 87, 84, 7, 4],
                           ['Oct_beta', 67, 15]]
    Diffusion_Atoms = ['Al']
    Structure_Poscar = Poscar.from_file(
        "Calculation_Files/Optimistic_Structure/POSCAR_SO_M{0}_S{1}".format(Module_Number, Situation_Number))
    for Diffusion_Position in Diffusion_Positions:
        interstitial_postion = np.zeros(3)
        for Atom_Number in Diffusion_Position[1:]:
            interstitial_postion = interstitial_postion + Structure_Poscar.structure[Atom_Number - 1].coords
        interstitial_postion = interstitial_postion / (len(Diffusion_Position) - 1)
        for Diffusion_Atom in Diffusion_Atoms:
            interstitial_structure = deepcopy(Structure_Poscar.structure)
            interstitial_structure.append(Diffusion_Atom, interstitial_postion, coords_are_cartesian=True)
            Neb_Path = 'Calculation_Files/CI-NEB/Interstitial/M{0}_S{1}/{2}'.format(Module_Number, Situation_Number,
                                                                                    Diffusion_Atom)
            # if os.path.exists(Neb_Path):
            #    shutil.rmtree(Neb_Path)
            # os.makedirs(Neb_Path)
            Poscar(interstitial_structure).write_file('{}/POSCAR_{}'.format(Neb_Path, Diffusion_Position[0]))
