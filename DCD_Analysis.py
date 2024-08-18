from pymatgen.io.vasp.outputs import Vasprun
from pymatgen.io.vasp.outputs import Chgcar
import matplotlib.pyplot as plt
import numpy as np

# 设定切片位置
slice_position = 2.17253
# Vasprun和3个CHGCAR路径
path_vasprunXML = "/mnt/e/ExperimentData/Nitriding_Layer_Simualtion/Summary/Structure_1/Data_W/DCD_Calculation/Total/vasprun.xml"
path_CHGCAR_total = "/mnt/e/ExperimentData/Nitriding_Layer_Simualtion/Summary/Structure_1/Data_W/DCD_Calculation/Total/CHGCAR"
path_CHGCAR_main = "/mnt/e/ExperimentData/Nitriding_Layer_Simualtion/Summary/Structure_1/Data_W/DCD_Calculation/CrN_Fe/CHGCAR"
path_CHGCAR_mono = "/mnt/e/ExperimentData/Nitriding_Layer_Simualtion/Summary/Structure_1/Data_W/DCD_Calculation/W/CHGCAR"
# 导入数据
vasprun_result = Vasprun(path_vasprunXML, parse_potcar_file=False)
cal_structure = vasprun_result.structures[0]
# 计算倒空间体积
Chgcar_dim = Chgcar.from_file(path_CHGCAR_total).dim
Vol_grid = Chgcar_dim[0] * Chgcar_dim[1] * Chgcar_dim[2]
Vol_structure = cal_structure.volume
volume_FFT = Vol_grid * Vol_structure
# 电荷数据
data_charge_total = Chgcar.from_file(path_CHGCAR_total).data['total']
data_charge_main = Chgcar.from_file(path_CHGCAR_main).data['total']
data_charge_mono = Chgcar.from_file(path_CHGCAR_mono).data['total']
# 计算DCD数据
data_DCD = (data_charge_main + data_charge_mono - data_charge_total)/Vol_structure
# data_DCD = data_charge_main+data_charge_mono
# 匹配最佳slice面
lenght_direction = cal_structure.lattice.a
slice_point = int(slice_position / (lenght_direction / data_charge_main.shape[1]))
# 画图用数据
data_plot = np.flip(data_DCD[:, slice_point, :])[:, 20:]

# 绘制CHGCAR面
cm = 1 / 2.54
plt.rcParams['figure.dpi'] = 600
plt.figure(figsize=(6 * cm, 2.8 * cm))
plt.subplots_adjust(left=0.01, right=0.88, top=0.98, bottom=0.02)
# 显示数据，并设置颜色映射和插值方法
# im = plt.imshow(data_plot, cmap='jet', interpolation='bilinear', vmin=-400, vmax=400)
im = plt.imshow(data_plot, cmap='jet', interpolation='bilinear')
# 添加颜色条，并设置其位置和大小
cbar = plt.colorbar(im, fraction=0.05, orientation='vertical', pad=0.02, aspect=9.6, format=("%.1f"))
cbar.ax.tick_params(labelsize=6)
# cbar.ax.set_ylabel(rotation=-90, va='bottom')
plt.xticks([])
plt.yticks([])
plt.savefig('CHGCAR.png')
plt.show()
