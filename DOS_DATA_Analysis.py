import pandas as pd
import numpy as np
from pymatgen.io.vasp.outputs import Vasprun
from pymatgen.electronic_structure.core import OrbitalType

# LDOS文件暂时不需要，本态密度处理针对PDOS和TDOS，得出的数据用csv格式存储
# 需要手动输入所处理的原子轨道，原子名称
# vasprun.xml文件位置设定
path_vasprunXML = "Data_file/vasprun.xml"
# 界面上半层原子Z方向截止
top_layer_limit = 11.13
# 界面下半层原子Z方向截止
bottem_layer_limit = 2.1

# 读取vasprun.xml文件
result = Vasprun(path_vasprunXML, parse_potcar_file=False)
# 读取dos数据
Complete_DOS = result.complete_dos
# 读取对应轨道，对应元素的PDOS数据
PDOS_Fe = Complete_DOS.get_element_spd_dos("Fe")
PDOS_Cr = Complete_DOS.get_element_spd_dos("Cr")
PDOS_N = Complete_DOS.get_element_spd_dos("N")
PDOS_W = Complete_DOS.get_element_spd_dos("W")
# 读取TDOS数据
TDOS = result.tdos.get_densities()

# 进行轨道分解，获得对应轨道数据
PDOS_Fe_s = PDOS_Fe[OrbitalType.s].get_densities()
PDOS_Fe_p = PDOS_Fe[OrbitalType.p].get_densities()
PDOS_Fe_d = PDOS_Fe[OrbitalType.d].get_densities()
PDOS_N_s = PDOS_N[OrbitalType.s].get_densities()
PDOS_N_p = PDOS_N[OrbitalType.p].get_densities()
PDOS_N_d = PDOS_N[OrbitalType.d].get_densities()
PDOS_Cr_s = PDOS_Cr[OrbitalType.s].get_densities()
PDOS_Cr_p = PDOS_Cr[OrbitalType.p].get_densities()
PDOS_Cr_d = PDOS_Cr[OrbitalType.d].get_densities()
PDOS_W_s = PDOS_W[OrbitalType.s].get_densities()
PDOS_W_p = PDOS_W[OrbitalType.p].get_densities()
PDOS_W_d = PDOS_W[OrbitalType.d].get_densities()

# 获得能量格点
Energy_Label = Complete_DOS.energies

#获取费米能级
E_Fermi = result.efermi
print("E_Fermi = {} eV".format(E_Fermi))

# 输出csv文件
DOS_DATA = np.array([Energy_Label,
                     PDOS_Fe_s, PDOS_Fe_p, PDOS_Fe_d,
                     PDOS_N_s, PDOS_N_p, PDOS_N_d,
                     PDOS_Cr_s, PDOS_Cr_p, PDOS_Cr_d,
                     PDOS_W_s, PDOS_W_p, PDOS_W_d,
                     TDOS]).T
DOS_DATA_df = pd.DataFrame(DOS_DATA)
DOS_DATA_df.columns = ['Energy_Label',
                       'PDOS_Fe_s', 'PDOS_Fe_p', 'PDOS_Fe_d',
                       'PDOS_N_s', 'PDOS_N_p', 'PDOS_N_d',
                       'PDOS_Cr_s', 'PDOS_Cr_p', 'PDOS_Cr_d',
                       'PDOS_W_s', 'PDOS_W_p', 'PDOS_W_d',
                       'TDOS']

DOS_Writer = pd.ExcelWriter('pdos.xlsx')
DOS_DATA_df.to_excel(DOS_Writer,'page_1',float_format='%.4f')
DOS_Writer.close()
