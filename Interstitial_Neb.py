#!/home/universe/local_env/anaconda3/envs/abinit/bin/python
import os
import shutil

from pymatgen.io.vasp import Poscar
from pymatgen_diffusion.neb.pathfinder import IDPPSolver

if __name__ == "__main__":
    Opt_Dir = '/mnt/c/Users/jackx/OneDrive/Calculation_Data/TC17_TI80'
    Work_Dir = '/mnt/d/PycharmProjects/TI80/Calculation_Files/CI-NEB'
    Diffusion_structure = '/M5_S3'
    Diffusion_Method = '/Interstitial'
    Diffusion_Atom = '/Zr'
    Paths_list = [["1_Oct_alpha/", "1_Oct_inter_beta/"],
                  ["1_Oct_inter_beta/", "1_Oct_beta/"],
                  ["2_Oct_alpha/", "2_Oct_inter_alpha/"],
                  ["2_Oct_inter_alpha/", "2_Oct_inter_beta/"],
                  ["2_Oct_inter_beta/", "2_Oct_beta/"],
                  ["2_Oct_alpha/", "2_Oct_inter_beta/"],
                  ["2_Oct_inter_alpha/", "2_Oct_beta/"]
                  ]
    image_value = 3
    for Path_list in Paths_list:
        ini_CONTCAR = '{}{}{}/OPT_DATA/{}/{}CONTCAR'.format(Opt_Dir, Diffusion_structure, Diffusion_Method,
                                                            Diffusion_Atom,
                                                            Path_list[0])
        fin_CONTCAR = '{}{}{}/OPT_DATA/{}/{}CONTCAR'.format(Opt_Dir, Diffusion_structure, Diffusion_Method,
                                                            Diffusion_Atom,
                                                            Path_list[1])
        ini_OUTCAR = '{}{}{}/OPT_DATA{}/{}OUTCAR'.format(Opt_Dir, Diffusion_structure, Diffusion_Method,
                                                         Diffusion_Atom,
                                                         Path_list[0])
        fin_OUTCAR = '{}{}{}/OPT_DATA{}/{}OUTCAR'.format(Opt_Dir, Diffusion_structure, Diffusion_Method,
                                                         Diffusion_Atom,
                                                         Path_list[1])
        ini_structure = Poscar.from_file(ini_CONTCAR).structure
        fin_structure = Poscar.from_file(fin_CONTCAR).structure

        tst_obj = IDPPSolver.from_endpoints(endpoints=[ini_structure, fin_structure], nimages=int(image_value),
                                            sort_tol=10.0)
        neb_point = tst_obj.run(maxiter=10000, tol=1e-05, gtol=1e-3, step_size=0.1, max_disp=8.0, spring_const=5.0)

        for neb_number in range(len(neb_point)):
            image_number = '/' + '{:0>2d}'.format(neb_number)
            image_Pathname = '/Path_{}-To-{}'.format(Path_list[0][:-1], Path_list[1][2:-1])
            image_Path = '{}{}{}{}/NEB/{}{}'.format(Work_Dir, Diffusion_structure, Diffusion_Method,
                                                    Diffusion_Atom,
                                                    image_Pathname, image_number)
            if os.path.exists(image_Path):
                shutil.rmtree(image_Path)
            os.makedirs(image_Path)
            POSCAR_path = image_Path + '/POSCAR'
            Cif_path = image_Path + '/POSCAR.cif'
            Poscar(neb_point[neb_number]).write_file('{}'.format(POSCAR_path))
            Poscar(neb_point[neb_number]).structure.to(filename=Cif_path)
            if neb_number == 0:
                shutil.copy(ini_OUTCAR, image_Path)
            elif neb_number == image_value + 1:
                shutil.copy(fin_OUTCAR, image_Path)
