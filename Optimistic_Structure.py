#!/home/universe/local_env/anaconda3/envs/abinit/bin/python
from copy import deepcopy

import numpy as np
from pymatgen.core import Lattice
from pymatgen.io.vasp import Poscar

# 界面中间预估位置
interface_position = 7.5
# Selective Dynamic 范围设定,区间内的原子位置可移动
# 界面上半层原子Z方向截止
top_layer_limit = 11.13
# 界面下半层原子Z方向截止
bottem_layer_limit = 2.1
# 上下层UBER最佳间距
interface_distance = 1.86
# 读取文件位置
POSCAR_PATH = "Data_file/POSCAR"
# 保存路径和文件名
POSCAR_SAVE = "Data_file/POSCAR_PreOpt"

# 上半层不动原子暂存list
list_top_layer = []
# 下半层不动原子暂存list
list_bottem_layer = []

# 读取原始原子位置
Poscar_Original = Poscar.from_file(POSCAR_PATH)
for number_atom in range(0, Poscar_Original.structure.num_sites):
    if Poscar_Original.structure[number_atom].z > interface_position:
        list_top_layer.append(number_atom)
    else:
        list_bottem_layer.append(number_atom)

# 上层动原子Z最小值
ZMin_top_layer_Dynamic = 100
for number_top in list_top_layer:
    if Poscar_Original.structure[number_top].z < ZMin_top_layer_Dynamic:
        ZMin_top_layer_Dynamic = Poscar_Original.structure[number_top].z
# 下层动原子Z最大值
ZMax_bottem_layer_Dynamic = 0
for number_bottem in list_bottem_layer:
    if Poscar_Original.structure[number_bottem].z > ZMax_bottem_layer_Dynamic:
        ZMax_bottem_layer_Dynamic = Poscar_Original.structure[number_bottem].z

# SelectiveDynamic矩阵初始化
SelectiveDynamic_array = np.zeros((Poscar_Original.structure.num_sites, 3))
# 更改上层结构优化原子SelectiveDynamic值
for number_SelectiveDynamic_top in list_top_layer:
    if Poscar_Original.structure[number_SelectiveDynamic_top].z < top_layer_limit:
        SelectiveDynamic_array[number_SelectiveDynamic_top] = np.ones(3)
# 更改上下层结构优化原子SelectiveDynamic值
for number_SelectiveDynamic_bottem in list_bottem_layer:
    if Poscar_Original.structure[number_SelectiveDynamic_bottem].z > bottem_layer_limit:
        SelectiveDynamic_array[number_SelectiveDynamic_bottem] = np.ones(3)

# 结构优化区的Z值间隔
gap_top_bottem = ZMin_top_layer_Dynamic - ZMax_bottem_layer_Dynamic

# 开始计算整体结构
total_structure = deepcopy(Poscar_Original)
total_structure.structure.lattice = Lattice.from_parameters(a=total_structure.structure.lattice.a,
                                                            b=total_structure.structure.lattice.b,
                                                            c=total_structure.structure.lattice.c - (
                                                                    gap_top_bottem - interface_distance) * 2,
                                                            alpha=total_structure.structure.lattice.alpha,
                                                            beta=total_structure.structure.lattice.beta,
                                                            gamma=total_structure.structure.lattice.gamma)
for number_top_layer in list_top_layer:
    total_structure.structure.sites[number_top_layer].x = Poscar_Original.structure.sites[number_top_layer].x
    total_structure.structure.sites[number_top_layer].y = Poscar_Original.structure.sites[number_top_layer].y
    total_structure.structure.sites[number_top_layer].z = Poscar_Original.structure.sites[
                                                              number_top_layer].z - gap_top_bottem + interface_distance
for number_bottem_layer in list_bottem_layer:
    total_structure.structure.sites[number_bottem_layer].x = Poscar_Original.structure.sites[number_bottem_layer].x
    total_structure.structure.sites[number_bottem_layer].y = Poscar_Original.structure.sites[number_bottem_layer].y
    total_structure.structure.sites[number_bottem_layer].z = Poscar_Original.structure.sites[number_bottem_layer].z

total_structure.comment = "Optimistic_Structure"
total_structure.selective_dynamics = SelectiveDynamic_array

total_structure.write_file(POSCAR_SAVE)
