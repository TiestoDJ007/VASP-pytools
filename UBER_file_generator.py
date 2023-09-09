#!/home/universe/local_env/anaconda3/envs/abinit/bin/python
import os
from copy import deepcopy

from pymatgen.core import Lattice
from pymatgen.io.vasp import Poscar

# 输入文件名称路径
file_path_name = "Data_file/POSCAR"
# 输入原始界面中间值
interface_position = 7.15
# 界面步长
interface_step = 1.59
# 最大界面间距
max_interface_distance = 2.01
# 起始界面间距
initial_interface_distance = 0
up_c = 0.0

original_poscar = Poscar.from_file(file_path_name)
# 设置界面层A
substance_top = []
# 设置界面层B
substance_bottem = []
# 将界面层A和B的编号导入list中
for number_atom in range(0, original_poscar.structure.num_sites):
    if original_poscar.structure[number_atom].z < interface_position:
        substance_bottem.append(number_atom)
    else:
        substance_top.append(number_atom)

# 查找界面距离最近的原子
substance_top_cMax = int(100)
for number_top in substance_top:
    if original_poscar.structure[number_top].z < substance_top_cMax:
        substance_top_cMax = original_poscar.structure[number_top].z

substance_bottem_cMin = int(0)
for number_bottem in substance_bottem:
    if original_poscar.structure[number_bottem].z > substance_bottem_cMin:
        substance_bottem_cMin = original_poscar.structure[number_bottem].z

# 计算两界面之间间距
interface_width = abs(substance_bottem_cMin - substance_top_cMax)

# 建立不同间距的界面模型
for number_step in range(1, int((max_interface_distance-initial_interface_distance) / interface_step) + 1):
    print(number_step)
    # 间距设置
    step_distance = number_step * interface_step
    # 建立UBER原子模型存放路径
    # path_name = "Data_file/UBER_Files/POSCAR_Uber_{0}A".format(
    #     (step_distance + initial_interface_distance).__format__('.2f'))
    path_name = "/mnt/d/Experiment Data/Nitriding_Layer_Simualtion/Data/Layer_Uber/"
    # 生成模型
    # 生成总模型
    total_structure = deepcopy(original_poscar)
    total_structure.structure.lattice = Lattice.from_parameters(a=original_poscar.structure.lattice.a,
                                                                b=original_poscar.structure.lattice.b,
                                                                # 确保真空层厚度一致
                                                                c=original_poscar.structure.lattice.c - interface_width +
                                                                  step_distance + initial_interface_distance,
                                                                alpha=original_poscar.structure.lattice.alpha,
                                                                beta=original_poscar.structure.lattice.beta,
                                                                gamma=original_poscar.structure.lattice.gamma)
    # 生成上层模型，通过从总模型删除下层模型
    for number_substance_top in substance_top:
        total_structure.structure.sites[number_substance_top].x = original_poscar.structure.sites[
            number_substance_top].x
        total_structure.structure.sites[number_substance_top].y = original_poscar.structure.sites[
            number_substance_top].y
        total_structure.structure.sites[number_substance_top].z = original_poscar.structure.sites[
                                                                      number_substance_top].z - interface_width + up_c + step_distance + initial_interface_distance
        # 生成下层模型，通过从总模型删除上层模型
    for number_substance_bottem in substance_bottem:
        total_structure.structure.sites[number_substance_bottem].x = original_poscar.structure.sites[
            number_substance_bottem].x
        total_structure.structure.sites[number_substance_bottem].y = original_poscar.structure.sites[
            number_substance_bottem].y
        total_structure.structure.sites[number_substance_bottem].z = original_poscar.structure.sites[
                                                                         number_substance_bottem].z + up_c

    # 标记
    substance_top_structure = deepcopy(total_structure)
    substance_top_structure.structure.remove_sites(substance_bottem)
    substance_top_structure.comment = "substance_top"
    substance_bottem_structure = deepcopy(total_structure)
    substance_bottem_structure.structure.remove_sites(substance_top)
    substance_bottem_structure.comment = "substance_bottem"
    total_structure.comment = "total_structure"

    # 写模型文件
    #os.makedirs(path_name)
    #substance_top_structure.write_file("{0}/POSCAR_top.vasp".format(path_name))
    #substance_bottem_structure.write_file("{0}/POSCAR_bottem.vasp".format(path_name))
    total_structure.write_file("{0}/POSCAR_total.vasp".format(path_name))
