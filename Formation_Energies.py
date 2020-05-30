import os
import shutil
from copy import deepcopy

from pymatgen.io.vasp import Poscar

if __name__ == "__main__":
    Module_Number = int(5)
    Situation_Number = int(3)
    Diffusion_Atoms = ['Al', 'Cr', 'Mo', 'Nb', 'Sn', 'Ti', 'Zr']
    Diffusion_Positions = ['1_Oct_alpha', '1_Oct_beta','1_Oct_inter_beta']
    for Diffusion_Atom in Diffusion_Atoms:
        for Diffusion_Position in Diffusion_Positions:
            PATH_CONTCAR = "/mnt/c/Users/jackx/OneDrive/Calculation_Data/TC17_TI80/Optimistic_Results/M{0}_S{1}/{2}/{3}/CONTCAR".format(
                Module_Number, Situation_Number, Diffusion_Atom, Diffusion_Position)
            CONTCAR_structure = Poscar.from_file(PATH_CONTCAR).structure
            Atoms_number = CONTCAR_structure.num_sites
            Solute = deepcopy(CONTCAR_structure)
            Solvent = deepcopy(CONTCAR_structure)
            Mixture = deepcopy(CONTCAR_structure)
            Solute.remove_sites(range(0, Atoms_number - 1))
            Solvent.remove_sites(range(Atoms_number - 1, Atoms_number))
            PATH_Formation = "/mnt/c/Users/jackx/OneDrive/Calculation_Data/TC17_TI80/Formatoin_Energy/M{0}_S{1}/{2}/{3}/".format(
                Module_Number, Situation_Number, Diffusion_Atom, Diffusion_Position)
            if os.path.exists(PATH_Formation):
                shutil.rmtree(PATH_Formation)
            os.makedirs(PATH_Formation)
            Solute.to(filename='{}POSCAR_Solute'.format(PATH_Formation))
            Solute.to(filename='{}POSCAR_Solute.cif'.format(PATH_Formation))
            Solvent.to(filename='{}POSCAR_Solvent'.format(PATH_Formation))
            Solvent.to(filename='{}POSCAR_Solvent.cif'.format(PATH_Formation))
            Mixture.to(filename='{}POSCAR_Mixture'.format(PATH_Formation))
            Mixture.to(filename='{}POSCAR_Mixture.cif'.format(PATH_Formation))
