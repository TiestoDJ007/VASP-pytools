#!/home/universe/local_env/anaconda3/envs/abinit/bin/python
import os
from copy import deepcopy

from pymatgen.core import Lattice
from pymatgen.io.vasp import Poscar

#输入文件名称路径
file_path_name="Data_file/POSCAR"
#输入原始界面中间值
interface_position = 10
#界面步长
interface_step = 0.01
#最大界面间距
max_interface_distance = 2
initial_c = 0.8913503859094439
up_c = 0.0

original_poscar = Poscar.from_file(file_path_name)
#设置界面层A
substance_top = []
#设置界面层B
substance_bottem = []
#将界面层A和B的编号导入list中
for number_atom in range(0, original_poscar.structure.num_sites):
    if original_poscar.structure[number_atom].z > interface_position:
        substance_bottem.append(number_atom)
    else:
        substance_top.append(number_atom)

#查找界面距离最近的原子
substance_top_cMax = int(0)
for number_top in substance_top:
    if original_poscar.structure[number_top].z > substance_top_cMax:
        substance_top_cMax = original_poscar.structure[number_top].z

substance_bottem_cMin = int(100)
for number_bottem in substance_bottem:
    if original_poscar.structure[number_bottem].z < substance_bottem_cMin:
        substance_bottem_cMin = original_poscar.structure[number_bottem].z

#计算两界面之间间距
interface_width = abs(substance_bottem_cMin - substance_top_cMax)

#建立不同间距的界面模型
for number_step in range(1, int((max_interface_distance - initial_c) / interface_step) + 1):
#间距设置
    step_distance = number_step*interface_step
#建立UBER原子模型存放路径
    path_name = "Data_file/UBER_Files/POSCAR_Uber_{0}A".format(step_distance)
    os.makedirs(path_name)
#生成模型
    total_structure = deepcopy(original_poscar)
    total_structure.structure.lattice = Lattice.from_parameters(a=total_structure.structure.lattice.a,
                                                                b=total_structure.structure.lattice.b,
                                                                #确保真空层厚度一致
                                                                c=total_structure.structure.lattice.c - abs(
                                                                        interface_width - number_step * interface_step  - initial_c) * 2,
                                                                alpha=total_structure.structure.lattice.alpha,
                                                                beta=total_structure.structure.lattice.beta,
                                                                gamma=total_structure.structure.lattice.gamma)
    for number_substance_top in substance_top:
        total_structure.structure.sites[number_substance_top].x = original_poscar.structure.sites[number_substance_top].x
        total_structure.structure.sites[number_substance_top].y = original_poscar.structure.sites[number_substance_top].y
        total_structure.structure.sites[number_substance_top].z = original_poscar.structure.sites[number_substance_top].z + up_c
    for number_substance_bottem in substance_bottem:
        total_structure.structure.sites[number_substance_bottem].x = original_poscar.structure.sites[number_substance_bottem].x
        total_structure.structure.sites[number_substance_bottem].y = original_poscar.structure.sites[number_substance_bottem].y
        total_structure.structure.sites[number_substance_bottem].z = original_poscar.structure.sites[
                                                                    number_substance_bottem].z - interface_width + number_step * interface_step + initial_c + up_c

    substance_top_structure = deepcopy(total_structure)
    substance_top_structure.structure.remove_sites(substance_bottem)
    substance_top_structure.comment = "substance_top"
    substance_bottem_structure = deepcopy(total_structure)
    substance_bottem_structure.structure.remove_sites(substance_top)
    substance_bottem_structure.comment = "substance_bottem"
    total_structure.comment = "total_structure"

    substance_top_structure.write_file("{0}/POSCAR_top.vasp".format(path_name))
    substance_bottem_structure.write_file("{0}/POSCAR_bottem.vasp".format(path_name))
    total_structure.write_file("{0}/POSCAR_total.vasp".format(path_name))
