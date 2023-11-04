import os
import shutil
from copy import deepcopy

import numpy as np
from pymatgen.io.vasp import Poscar

if __name__ == "__main__":
    # 替换原子的位置
    Substitute_Positions = [1, 2, 9, 10]
    Substitute_Numbers = []
    # 替换原子的名称
    Substitute_Atoms = ['W']
    Structure = Poscar.from_file("Data_file/POSCAR").structure
    # 替换原子初始坐标矩阵
    Substitute_Coords = np.zeros((len(Substitute_Positions), 3))
    Substitute_index = 0
    # 建立替换矩阵
    for Substitute_Position in Substitute_Positions:
        Substitute_Number = Substitute_Position - 1
        Substitute_Coord = deepcopy(Structure[Substitute_Number].coords)
        Substitute_Coords[Substitute_index] = Substitute_Coord
        Substitute_Numbers.append(Substitute_Number)
        Substitute_index = Substitute_index + 1
    # 删除带替换原子
    Structure.remove_sites(Substitute_Numbers)
    # 添加替换原子到最后
    index = 0
    while index < len(Substitute_Positions):
        Structure.append(Substitute_Atoms[0], Substitute_Coords[index], coords_are_cartesian=True)
        index = index + 1
    # 重置Selected Dynamics
    Substitute_SelectedDynamics = np.zeros((Structure.num_sites, 3))
    Substitute_Poscar = Poscar(Structure, selective_dynamics=Substitute_SelectedDynamics)
    # 输出替换后的POSCAR,selected_dynamic 在其他程序中执行
    Substitute_Poscar.write_file('Data_file/POSCAR_Substi')
    Substitute_Poscar.structure.to(filename='Data_file/POSCAR_Substi.cif')
