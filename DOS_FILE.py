import os
import shutil

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
            PATH_DOS = "/mnt/c/Users/jackx/OneDrive/Calculation_Data/TC17_TI80/DOS/M{0}_S{1}/{2}/{3}/".format(
                Module_Number, Situation_Number, Diffusion_Atom, Diffusion_Position)
            if os.path.exists(PATH_DOS):
                shutil.rmtree(PATH_DOS)
            os.makedirs(PATH_DOS)
            CONTCAR_structure.to(filename='{}POSCAR'.format(PATH_DOS))
            CONTCAR_structure.to(filename='{}POSCAR.cif'.format(PATH_DOS))
            

