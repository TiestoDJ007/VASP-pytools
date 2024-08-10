import pandas as pd
import numpy as np
from pymatgen.io.vasp.outputs import Vasprun
from pymatgen.electronic_structure.core import OrbitalType

# LDOS文件暂时不需要，本态密度处理针对PDOS和TDOS，得出的数据用csv格式存储
# 需要手动输入所处理的原子轨道，原子名称
# vasprun.xml文件位置设定
path_vasprunXML = "Data_file/vasprun.xml"
# 小于该z方向数值的原子
top_layer_limit = 13.1
# 大于该z方向数值的原子
bottem_layer_limit = 6.3
# 读取vasprun.xml文件
result = Vasprun(path_vasprunXML, parse_potcar_file=False)
# 获得能量格点
Energy_Label = result.complete_dos.energies
# 读取原子位置信息
element_site = result.complete_dos.structure.sites
# 读取原子数量
element_amount = result.complete_dos.structure.num_sites
# 初始化数据
Fe_s = Fe_p = Fe_d = Cr_s = Cr_p = Cr_d = N_s = N_p = N_d = W_s = W_p = W_d = np.zeros([1, 2001])
# 判断原子是否在选取内，并填充数据
for atomic_site in range(0, element_amount - 1, 1):
    z_position = element_site[atomic_site].z
    if bottem_layer_limit < z_position < top_layer_limit:
        atomic_name = element_site[atomic_site].label
        if atomic_name == "Cr":
            Cr_s = Cr_s + result.complete_dos.get_site_spd_dos(element_site[atomic_site])[OrbitalType.s].get_densities()
            Cr_p = Cr_p + result.complete_dos.get_site_spd_dos(element_site[atomic_site])[OrbitalType.p].get_densities()
            Cr_d = Cr_d + result.complete_dos.get_site_spd_dos(element_site[atomic_site])[OrbitalType.d].get_densities()
        elif atomic_name == "Fe":
            Fe_s = Fe_s + result.complete_dos.get_site_spd_dos(element_site[atomic_site])[OrbitalType.s].get_densities()
            Fe_p = Fe_p + result.complete_dos.get_site_spd_dos(element_site[atomic_site])[OrbitalType.p].get_densities()
            Fe_d = Fe_d + result.complete_dos.get_site_spd_dos(element_site[atomic_site])[OrbitalType.d].get_densities()
        elif atomic_name == "N":
            N_s = N_s + result.complete_dos.get_site_spd_dos(element_site[atomic_site])[OrbitalType.s].get_densities()
            N_p = N_p + result.complete_dos.get_site_spd_dos(element_site[atomic_site])[OrbitalType.p].get_densities()
            N_d = N_d + result.complete_dos.get_site_spd_dos(element_site[atomic_site])[OrbitalType.d].get_densities()
        else:
            W_s = W_s + result.complete_dos.get_site_spd_dos(element_site[atomic_site])[OrbitalType.s].get_densities()
            W_p = W_p + result.complete_dos.get_site_spd_dos(element_site[atomic_site])[OrbitalType.p].get_densities()
            W_d = W_d + result.complete_dos.get_site_spd_dos(element_site[atomic_site])[OrbitalType.d].get_densities()
# 获取费米能级
E_Fermi = result.efermi
print("E_Fermi = {} eV".format(E_Fermi))
# 输出数据文件
DOS_DATA = np.row_stack([Energy_Label,
                         Fe_s, Fe_p, Fe_d,
                         N_s, N_p, N_d,
                         Cr_s, Cr_p, Cr_d,
                         W_s, W_p, W_d, ]).T
DOS_DATA_df = pd.DataFrame(DOS_DATA)
DOS_DATA_df.columns = ['Energy_Label',
                       'Fe_s', 'Fe_p', 'Fe_d',
                       'N_s', 'N_p', 'N_d',
                       'Cr_s', 'Cr_p', 'Cr_d',
                       'W_s', 'W_p', 'W_d']

DOS_Writer = pd.ExcelWriter('pdos.xlsx')
DOS_DATA_df.to_excel(DOS_Writer, 'page_1', float_format='%.4f')
DOS_Writer.close()
