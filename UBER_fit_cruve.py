#!/home/universe/local_env/anaconda3/envs/abinit/bin/python
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

if __name__ == '__main__':

    d, E = [], []
    UBER_file = open('data_UBER', 'r')
    lines = UBER_file.readlines()
    for number_data in range(0, 152, 4):
        d.append(float(lines[number_data + 1].strip("DISTANCE=")))
        E.append(float(lines[number_data + 3].strip("W_seq=")))

    parameter, func = curve_fit(lambda d, E_0, l, d_0: -E_0 * (1 + (d - d_0) / l) * np.exp(-(d - d_0) / l), d, E)
    plt.figure()
    d_fit = np.arange(0.1, 10, 0.1)
    E_0, l, d_0 = parameter
    E_fit = -E_0 * (1 + (d_fit - d_0) / l) * np.exp(-(d_fit - d_0) / l)
    plt.plot(d, E, 'ko', label="Original Data")
    plt.plot(d_fit, E_fit, 'r-', label="Fitting Curve")
    plt.xlim(0.5,8)
    plt.ylim(-30,10)
    plt.legend()
    plt.show()
