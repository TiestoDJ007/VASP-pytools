from pymatgen.io.vasp.outputs import Vasprun
from pymatgen.io.vasp.outputs import Elfcar
import matplotlib.pyplot as plt

# 设定切片位置
slice_position = 2.333
path_vasprunXML = "/mnt/d/ExperimentData/Nitriding_Layer_Simualtion/Summary/Structure_1/Data_Mo/ELF_Calculation/vasprun.xml"
path_ELFCAR = "/mnt/d/ExperimentData/Nitriding_Layer_Simualtion/Summary/Structure_1/Data_Mo/ELF_Calculation/ELFCAR"
vasprun_result = Vasprun(path_vasprunXML, parse_potcar_file=False)
cal_structure = vasprun_result.structures[0]
elfcar_result = Elfcar.from_file(path_ELFCAR)
elfcar_data = elfcar_result.data['total']

# 匹配最佳slice面
# xpoint 是W的结构，W Mo计算结构不一样
# size_direction = elfcar_result.xpoints
size_direction = elfcar_result.ypoints
# lenght_direction = cal_structure.lattice.a
lenght_direction = cal_structure.lattice.b
slice_point = int(slice_position / (lenght_direction / len(size_direction)))

# 取slice数据
# plot_data = elfcar_data[slice_point, :, 20:]
plot_data = elfcar_data[:, slice_point, :274]

# 绘制ELF面
cm = 1 / 2.54
plt.rcParams['figure.dpi'] = 600
plt.figure(figsize=(6 * cm, 3.5 * cm))
plt.subplots_adjust(left=0.02, right=0.9, top=0.99, bottom=0.15)
# 显示数据，并设置颜色映射和插值方法
im = plt.imshow(plot_data, cmap='jet', interpolation='bilinear', vmin=0, vmax=1)
# 添加颜色条，并设置其位置和大小
cbar = plt.colorbar(im, fraction=0.064, orientation='vertical', pad=0.02, aspect=7.8, format=("%.1f"))
cbar.ax.tick_params(labelsize=6)
# cbar.ax.set_ylabel(rotation=-90, va='bottom')
plt.xticks([])
plt.yticks([])
plt.savefig('ELFCAR.png')
plt.show()
