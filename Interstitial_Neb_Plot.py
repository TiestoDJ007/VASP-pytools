#!/home/universe/local_env/anaconda3/envs/abinit/bin/python
import os

import matplotlib.pyplot as plt
import numpy as np
from pymatgen.analysis.transition_state import NEBAnalysis
from scipy.interpolate import interp1d

if __name__ == "__main__":
    Work_Dir = '/mnt/c/Users/jackx/OneDrive/Calculation_Data/TC17_TI80'
    Module_Number = int(5)
    Situation_Number = int(3)
    # Diffusion_elements = ['Al', 'Cr', 'Mo', 'Nb', 'Sn', 'Ti', 'Zr']
    Diffusion_elements = ['Al', 'Nb', 'Sn', 'Ti', 'Zr']
    # Transition_Paths = ['01-19', '37-59', '59-01']
    # 'Path_2_Oct_alpha-To-Oct_inter_alpha/'
    # 'Path_2_Oct_inter_alpha-To-Oct_beta/'
    # 'Path_2_Oct_inter_beta-To-Oct_beta/“
    # 'Path_2_Oct_alpha-To-Oct_inter_beta/'
    # 'Path_2_Oct_inter_alpha-To-Oct_inter_beta/'
    # 'Path_1_Oct_alpha-2-Oct_inter_beta/', 'Path_1_Oct_inter_beta-2-Oct_beta/'
    # 'Path_1_C_a-To-Oct_inter_beta/', 'Path_1_Oct_alpha-To-C_a/'
    Transition_Paths = ['Path_1_Oct_inter_beta-To-Oct_beta/']
    Diffusion_structure = '/M{}_S{}'.format(Module_Number, Situation_Number)
    Diffusion_Method = 'Interstitial'
    Fig_Dir = '{}/NEB_Figures/{}'.format(Work_Dir, Diffusion_structure)
    # Neb_Dir = '{}{}{}/NEB_DATA'.format(Work_Dir, Diffusion_structure, Diffusion_elements)
    # OUTCAR_root = '/mnt/c/Users/jackx/OneDrive/Calculation_Data/TC17_TI80/M{0}_S{1}_single'.format(Module_Number,
    #                                                                                               Situation_Number)
    # figure_path = '/mnt/c/Users/jackx/OneDrive/Calculation_Data/TC17_TI80/figure/M{0}_S{1}_single'.format(Module_Number,
    #                                                                                                      Situation_Number)
    if not os.path.exists(Fig_Dir):
        os.makedirs(Fig_Dir)

    for Transition_Path in Transition_Paths:
        fig, ax = plt.subplots(figsize=(8, 6))
        for Diffusion_element in Diffusion_elements:
            Neb_Dir = '{}/NEB_Results{}/{}/{}/{}'.format(Work_Dir, Diffusion_structure, Diffusion_Method,
                                                         Diffusion_element,
                                                         Transition_Path)
            # OUTCAR_DIR = "{0}/{1}/{2}".format(Neb_Dir, Diffusion_element, Transition_Path)
            Neb_data = NEBAnalysis.from_dir(Neb_Dir)
            x = Neb_data.r / Neb_data.r[-1]
            y = Neb_data.energies - Neb_data.energies[0]
            f = interp1d(x, y, kind='cubic')
            xx = np.linspace(x.min(), x.max(), 100)
            ax.scatter(x, y * 1000, s=70)
            ax.plot(xx, f(xx) * 1000, label=Diffusion_element, linewidth=3)
            ax.legend()
        plt.xlim(0, 1)
        plt.xlabel('Reaction Coordinate', fontsize=25)
        plt.ylabel('Energy(meV)', fontsize=25)
        plt.tick_params(labelsize=18)
        axis = plt.gca()
        bwith = 2
        plt.rcParams['xtick.direction'] = 'in'
        plt.rcParams['ytick.direction'] = 'in'
        plt.tick_params(which='major', width=2, length=6)
        axis.spines['bottom'].set_linewidth(bwith)
        axis.spines['left'].set_linewidth(bwith)
        axis.spines['top'].set_linewidth(bwith)
        axis.spines['right'].set_linewidth(bwith)
        plt.legend(fontsize=15, edgecolor='none', loc='lower left', facecolor='none')
        plt.title('{}'.format(Transition_Path[:-1]), fontsize=25)
        plt.hlines(0, 0, 1.0, colors='gray', linestyles="dashed", lw=2)
        plt.tight_layout()
        plt.savefig('{0}/{1}'.format(Fig_Dir, Transition_Path[:-1]))
        plt.show()
        plt.close()
