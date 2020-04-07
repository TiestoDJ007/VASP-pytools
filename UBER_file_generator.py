#!/home/universe/local_env/anaconda3/envs/abinit/bin/python
import os
from copy import deepcopy

from pymatgen import Lattice
from pymatgen.io.vasp import Poscar

Module_Number = int(5)
Situation_Number = int(1)
interface_position = 8.0
gap_distance = 0.05
max_distance = 2.95
initial_c = 2.0
up_c = 0.0

original_poscar = Poscar.from_file("Initial_Structure/POSCAR_M{}_S{}".format(Module_Number, Situation_Number))
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

for number_step in range(1, int((max_distance - initial_c) / gap_distance) + 1):

    path_name = "Calculation_Files/UBER/M{0}_S{1}_Uber_{2}A_{3}A_{4}A/{5}".format(Module_Number, Situation_Number,
                                                                             gap_distance + initial_c, gap_distance,
                                                                             max_distance, number_step)
    os.makedirs(path_name)

    total_structure = deepcopy(original_poscar)
    total_structure.structure.lattice = Lattice.from_parameters(a=total_structure.structure.lattice.a,
                                                                b=total_structure.structure.lattice.b,
                                                                c=total_structure.structure.lattice.c - (
                                                                        gap_alpha_beta - number_step * gap_distance - initial_c) * 2,
                                                                alpha=total_structure.structure.lattice.alpha,
                                                                beta=total_structure.structure.lattice.beta,
                                                                gamma=total_structure.structure.lattice.gamma)
    for number_alpha_Ti in alpha_Ti_list:
        total_structure.structure.sites[number_alpha_Ti].x = original_poscar.structure.sites[number_alpha_Ti].x
        total_structure.structure.sites[number_alpha_Ti].y = original_poscar.structure.sites[number_alpha_Ti].y
        total_structure.structure.sites[number_alpha_Ti].z = original_poscar.structure.sites[number_alpha_Ti].z + up_c
    for number_beta_Ti in beta_Ti_list:
        total_structure.structure.sites[number_beta_Ti].x = original_poscar.structure.sites[number_beta_Ti].x
        total_structure.structure.sites[number_beta_Ti].y = original_poscar.structure.sites[number_beta_Ti].y
        total_structure.structure.sites[number_beta_Ti].z = original_poscar.structure.sites[
                                                                number_beta_Ti].z - gap_alpha_beta + number_step * gap_distance + initial_c + up_c

    alpha_structure = deepcopy(total_structure)
    alpha_structure.structure.remove_sites(beta_Ti_list)
    alpha_structure.comment = "alpha_Ti"
    beta_structure = deepcopy(total_structure)
    beta_structure.structure.remove_sites(alpha_Ti_list)
    beta_structure.comment = "beta_Ti"
    total_structure.comment = "total_Ti"

    alpha_structure.write_file("{0}/POSCAR_alpha.vasp".format(path_name))
    beta_structure.write_file("{0}/POSCAR_beta.vasp".format(path_name))
    total_structure.write_file("{0}/POSCAR_total.vasp".format(path_name))
