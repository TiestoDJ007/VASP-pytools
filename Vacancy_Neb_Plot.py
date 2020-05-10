#!/home/universe/local_env/anaconda3/envs/abinit/bin/python
import os

import matplotlib.pyplot as plt
import numpy as np
from pymatgen.analysis.transition_state import NEBAnalysis
from scipy.interpolate import interp1d

if __name__ == "__main__":
    Module_Number = int(4)
    Situation_Number = int(1)
    Diffusion_elements = ['Al', 'Cr', 'Mo', 'Nb', 'Sn', 'Ti', 'Zr']
    # Diffusion_elements = ['Zr']
    # Transition_Paths = ['01-19', '37-59', '59-01']
    Transition_Paths = ['37-59']
    OUTCAR_root = '/mnt/c/Users/jackx/OneDrive/Calculation_Data/TC17_TI80/M{0}_S{1}_single'.format(Module_Number,
                                                                                                   Situation_Number)
    figure_path = '/mnt/c/Users/jackx/OneDrive/Calculation_Data/TC17_TI80/figure/M{0}_S{1}_single'.format(Module_Number,
                                                                                                          Situation_Number)
    if not os.path.exists(figure_path):
        os.makedirs(figure_path)

    for Transition_Path in Transition_Paths:
        fig, ax = plt.subplots(figsize=(8, 6))
        for Diffusion_element in Diffusion_elements:
            OUTCAR_DIR = "{0}/{1}/{2}".format(OUTCAR_root, Diffusion_element, Transition_Path)
            Neb_data = NEBAnalysis.from_dir(OUTCAR_DIR)
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
        plt.legend(fontsize=15, edgecolor='none', loc='upper left', facecolor='none')
        plt.title('{} Path'.format(Transition_Path), fontsize=25)
        plt.hlines(0, 0, 1.0, colors='gray', linestyles="dashed", lw=2)
        plt.savefig('{0}/{1}.png'.format(figure_path, Transition_Path))
        plt.show()
        plt.close()
