from pymatgen.io.vasp.outputs import Vasprun
from pymatgen.electronic_structure.core import OrbitalType

#vasprun.xml文件位置设定
path_vasprunXML = "/mnt/e/Experiment Data/Nitriding_Layer_Simualtion/Vasp_Data/Layer_Add_Mo_DOS/DOS/vasprun.xml"
# 界面上半层原子Z方向截止
top_layer_limit = 11.13
# 界面下半层原子Z方向截止
bottem_layer_limit = 2.1

#读取vasprun.xml文件
result = Vasprun(path_vasprunXML,parse_potcar_file=False)
#读取dos数据
Complete_DOS = result.complete_dos
#读取site数据
atom_sites_total=Complete_DOS.structure.sites
#初始化所需统计的原子编号
atom_sites = []
#开始统计原子编号
for num_atom in range(0, atom_sites_total.count()):