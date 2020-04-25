#!/home/universe/local_env/anaconda3/envs/abinit/bin/python
import os

import matplotlib.pyplot as plt
from pymatgen.analysis.transition_state import NEBAnalysis

if __name__ == "__main__":
    Module_Number = int(3)
    Situation_Number = int(1)
    # Diffusion_elements = ['Al', 'Cr', 'Mo', 'Nb', 'Sn', 'Ti', 'Zr']
    Diffusion_elements = ['Zr']
    Transition_Paths = ['41-01', '41-07', '57-07', '57-19']
    # Transition_Paths = ['57-19']
    OUTCAR_root = '/mnt/c/Users/jackx/OneDrive/Calculation_Data/TC17_TI80/M{}_S{}_single'.format(Module_Number,
                                                                                                 Situation_Number)
    figure_path = '/mnt/c/Users/jackx/OneDrive/Calculation_Data/TC17_TI80/figure/M{0}_S{1}_single'.format(Module_Number,
                                                                                                          Situation_Number)
    if not os.path.exists(figure_path):
        os.makedirs(figure_path)

    for Transition_Path in Transition_Paths:
        for Diffusion_element in Diffusion_elements:
            OUTCAR_DIR = "{0}/{1}/{2}".format(OUTCAR_root, Diffusion_element, Transition_Path)
            Neb_data = NEBAnalysis.from_dir(OUTCAR_DIR)
            plot = Neb_data.get_plot()
            plot.rcParams['figure.figsize'] = (8.0, 6.0)
            plot.title('{}_{}'.format(Diffusion_element, Transition_Path), fontsize=30)
            plt.tight_layout()
            plot.savefig('{0}/{1}_{2}.png'.format(figure_path, Diffusion_element, Transition_Path))
            plot.show()
            plot.close()
