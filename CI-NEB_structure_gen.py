#!/home/universe/local_env/anaconda3/envs/abinit/bin/python
import os

import numpy as np
from pymatgen.io.vasp import Poscar
from pymatgen_diffusion.neb.pathfinder import IDPPSolver


def D2_list_to_nparray(D2_list):
    array_list = []
    for list in D2_list:
        array_list.append(np.array(list).astype(int))
    return np.array(array_list)


if __name__ == "__main__":

    Work_Dir = '/mnt/d/PycharmProjects/TI80/Calculation_Files/CI-NEB'
    Diffusion_structure = '/M3_S1'
    Diffusion_element = '/Sn'
    Transition_Paths = ['/41-01', '/41-07', '/57-07', '/57-19']
    image_value = 3
    init_Contcar_Paths = []
    final_Contcar_Paths = []

    for Transition_Path in Transition_Paths:
        init_Contcar_Paths.append(
            '{}'.format(Work_Dir + Diffusion_structure + Diffusion_element + Transition_Path + '/ini/CONTCAR'))
        final_Contcar_Paths.append(
            '{}'.format(Work_Dir + Diffusion_structure + Diffusion_element + Transition_Path + '/fin/CONTCAR'))
    for number_path in range(len(init_Contcar_Paths)):
        init_Poscar = Poscar.from_file(init_Contcar_Paths[number_path], False)
        final_Poscar = Poscar.from_file(final_Contcar_Paths[number_path], False)

        init_structure = init_Poscar.structure
        final_structure = final_Poscar.structure

        tst_obj = IDPPSolver.from_endpoints(endpoints=[init_structure, final_structure], nimages=int(image_value),
                                            sort_tol=6.0)
        neb_point = tst_obj.run(maxiter=1000, tol=1e-05, gtol=1e-3, step_size=0.1, max_disp=5.0, spring_const=5.0)

        sd = D2_list_to_nparray(init_Poscar.selective_dynamics)
        for neb_number in range(len(neb_point)):
            image_number = '/' + '{:0>2d}'.format(neb_number)
            image_path = Work_Dir + Diffusion_structure + Diffusion_element + Transition_Paths[
                number_path] + image_number
            os.makedirs(image_path)
            POSCAR_path = image_path + '/POSCAR'
            neb_point[neb_number].to(fmt="poscar", filename=POSCAR_path)
