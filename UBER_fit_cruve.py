#!/home/universe/local_env/anaconda3/envs/abinit/bin/python

from math import sin, pi
import matplotlib.pyplot as plt
import numpy as np
from pymatgen.io.vasp import Poscar
from scipy.optimize import curve_fit, fminbound

def UBER_FUNC(d, E_0, l, d_0):
    return -E_0 * (1 + (d - d_0) / l) * np.exp(-(d - d_0) / l)

if __name__ == '__main__':

    eV2J = 16.0217662
    d, E = [], []
    start_number = 2
    finish_number = 6
    UBER_file = open(
        "Data_file/structure_energy", 'r')
    original_poscar = Poscar.from_file(
        "Data_file/POSCAR")
    lines = UBER_file.readlines()
    for number_data in range(0, lines.__len__() - 4, 4):
        d.append(float(lines[number_data + 1].strip("DISTANCE=")))
        E.append(float(lines[number_data + 3].strip("W_seq=")))
    E = np.array(E)
    d = np.array(d)

    Area_Value = original_poscar.structure.lattice.a * original_poscar.structure.lattice.b * sin(
        original_poscar.structure.lattice.alpha * pi / 180)

    parameter, func = curve_fit(lambda d, E_0, l, d_0: UBER_FUNC(d, E_0, l, d_0), d[start_number:finish_number],
                                E[start_number:finish_number])
    plt.figure()
    d_fit = np.arange(0.1, 10, 0.01)
    E_fit = lambda x: UBER_FUNC(x, parameter[0], parameter[1], parameter[2])
    Interface_Distance = fminbound(E_fit, 0, 3)
    print("Interface Distance = {}".format(Interface_Distance))
    print("W_Seq = {}".format(E_fit(Interface_Distance) / Area_Value * eV2J))
    plt.plot(d, E / Area_Value * eV2J, 'ko', label="Original Data")
    plt.plot(d_fit, E_fit(d_fit) / Area_Value * eV2J, 'r-', label="Fitting Curve")
    plt.xlim(0.0, 8)
    plt.ylim(-10, 10)
    plt.legend()
    plt.show()
