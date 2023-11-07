#!/home/universe/local_env/anaconda3/envs/abinit/bin/python
import numpy as np
from copy import deepcopy
from pymatgen.io.vasp import Poscar
from pymatgen.core import Lattice

# 界面中间预估位置
interface_position = 8.0
# 界面上半层原子固定起始位置
top_layer_limit = 2.0
# 界面下半层原子固定起始位置
bottem_layer_limit = 15.0
# 上下层UBER最佳间距
interface_distance = 2.5662262085598324
# 读取文件位置
POSCAR_PATH = "Data_file/POSCAR"
# 保存路径和文件名
POSCAR_SAVE = "Calculation_Files/Optimistic_Structure"

# 上半层原子暂存list
list_top_layer = []
# 下半层原子暂存list
list_bottem_layer = []

Poscar_Original = Poscar.from_file(POSCAR_PATH)
for number_atom in range(0, Poscar_Original.structure.num_sites):
    if Poscar_Original.structure[number_atom].z > interface_position:
        list_top_layer.append(number_atom)
    else:
        list_bottem_layer.append(number_atom)
    # 计入top_layer_limit之下, bottem_layer_limit之上的原子序号
    if Poscar_Original.structure[number_atom].z < top_layer_limit:
        list_top_layer.append(number_atom)
    if Poscar_Original.structure[number_atom].z > bottem_layer_limit:
        list_bottem_layer.append(number_atom)

# 上层动原子Z最大值
ZMax_top_layer_Dynamic = 0
for number_top in list_top_layer:
    if Poscar_Original.structure[number_top].z > ZMax_top_layer_Dynamic:
        ZMax_top_layer_Dynamic = Poscar_Original.structure[number_top].z
# 下层动原子Z最大值
ZMax_bottem_layer_Dynamic = 100
for number_bottem in list_bottem_layer:
    if Poscar_Original.structure[number_bottem].z < ZMax_bottem_layer_Dynamic:
        ZMax_bottem_layer_Dynamic = Poscar_Original.structure[number_bottem].z

# SelectiveDynamic矩阵初始化
SelectiveDynamic_array = np.ones((Poscar_Original.natoms[0], 3))
# 更改上层结构优化原子SelectiveDynamic值
for number_SelectiveDynamic_top in list_top_layer:
    SelectiveDynamic_array[number_SelectiveDynamic_top] = np.zeros(3)
# 更改上下层结构优化原子SelectiveDynamic值
for number_SelectiveDynamic_bottem in list_bottem_layer:
    SelectiveDynamic_array[number_SelectiveDynamic_bottem] = np.zeros(3)

# 结构优化区的Z值间隔
gap_alpha_beta = ZMax_top_layer_Dynamic - ZMax_bottem_layer_Dynamic

# 开始计算整体结构
total_structure = deepcopy(Poscar_Original)
total_structure.structure.lattice = Lattice.from_parameters(a=total_structure.structure.lattice.a,
                                                            b=total_structure.structure.lattice.b,
                                                            c=total_structure.structure.lattice.c - (
                                                                    gap_alpha_beta - interface_distance) * 2,
                                                            alpha=total_structure.structure.lattice.alpha,
                                                            beta=total_structure.structure.lattice.beta,
                                                            gamma=total_structure.structure.lattice.gamma)
for number_alpha_Ti in alpha_Ti_list:
    total_structure.structure.sites[number_alpha_Ti].x = original_poscar.structure.sites[number_alpha_Ti].x
    total_structure.structure.sites[number_alpha_Ti].y = original_poscar.structure.sites[number_alpha_Ti].y
    total_structure.structure.sites[number_alpha_Ti].z = original_poscar.structure.sites[number_alpha_Ti].z
for number_beta_Ti in beta_Ti_list:
    total_structure.structure.sites[number_beta_Ti].x = original_poscar.structure.sites[number_beta_Ti].x
    total_structure.structure.sites[number_beta_Ti].y = original_poscar.structure.sites[number_beta_Ti].y
    total_structure.structure.sites[number_beta_Ti].z = original_poscar.structure.sites[
                                                            number_beta_Ti].z - gap_alpha_beta + interface_distance

total_structure.comment = "Optimistic_Structure"
total_structure.selective_dynamics = sd_array

total_structure.write_file(
    "Calculation_Files/Optimistic_Structure/POSCAR_SO_M{0}_S{1}".format(Module_Number, Situation_Number))
