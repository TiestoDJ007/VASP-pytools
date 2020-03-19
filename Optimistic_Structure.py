#!/home/universe/local_env/anaconda3/envs/abinit/bin/python
from copy import deepcopy

from pymatgen import Lattice
from pymatgen.io.vasp import Poscar

interface_position = 8.0
interface_distance = 1.9557073022475353
Module_Number = int(3)
Situation_Number = int(1)

original_poscar = Poscar.from_file("Initial_Structure/POSCAR_M{0}_S{1}".format(Module_Number, Situation_Number))
alpha_Ti_list = []
beta_Ti_list = []
for number_atom in range(0, original_poscar.structure.num_sites):
    if original_poscar.structure[number_atom].z > interface_position:
        beta_Ti_list.append(number_atom)
    else:
        alpha_Ti_list.append(number_atom)

alpha_Ti_max = 0
for number_alpha in alpha_Ti_list:
    if original_poscar.structure[number_alpha].z > alpha_Ti_max:
        alpha_Ti_max = original_poscar.structure[number_alpha].z

beta_Ti_min = 100
for number_beta in beta_Ti_list:
    if original_poscar.structure[number_beta].z < beta_Ti_min:
        beta_Ti_min = original_poscar.structure[number_beta].z

gap_alpha_beta = beta_Ti_min - alpha_Ti_max

path_name = "Calculation_Files/Optimistic_Structure"

total_structure = deepcopy(original_poscar)
total_structure.structure.lattice = Lattice.from_parameters(a=total_structure.structure.lattice.a,
                                                            b=total_structure.structure.lattice.b,
                                                            c=total_structure.structure.lattice.c - (
                                                                    gap_alpha_beta - interface_distance) * 2,
                                                            alpha=total_structure.structure.lattice.alpha,
                                                            beta=total_structure.structure.lattice.beta,
                                                            gamma=total_structure.structure.lattice.gamma)
for number_alpha_Ti in alpha_Ti_list:
    total_structure.structure.sites[number_alpha_Ti].x = original_poscar.structure.sites[number_alpha_Ti].x
    total_structure.structure.sites[number_alpha_Ti].y = original_poscar.structure.sites[number_alpha_Ti].y
    total_structure.structure.sites[number_alpha_Ti].z = original_poscar.structure.sites[number_alpha_Ti].z
for number_beta_Ti in beta_Ti_list:
    total_structure.structure.sites[number_beta_Ti].x = original_poscar.structure.sites[number_beta_Ti].x
    total_structure.structure.sites[number_beta_Ti].y = original_poscar.structure.sites[number_beta_Ti].y
    total_structure.structure.sites[number_beta_Ti].z = original_poscar.structure.sites[
                                                            number_beta_Ti].z - gap_alpha_beta + interface_distance

total_structure.comment = "Optimistic_Structure"

total_structure.write_file(
    "Calculation_Files/Optimistic_Structure/POSCAR_SO_M{0}_S{1}".format(Module_Number, Situation_Number))
