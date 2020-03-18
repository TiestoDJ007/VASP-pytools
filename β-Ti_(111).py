from pymatgen.core.surface import SlabGenerator
from pymatgen.ext.matproj import MPRester
from pymatgen.io.vasp.inputs import Poscar
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

mpr = MPRester('nfXxe0aDBRPSy4sI')

mp_id = "mp-46"
struct = mpr.get_structure_by_material_id(mp_id)
struct = SpacegroupAnalyzer(struct).get_conventional_standard_structure()
slab = SlabGenerator(struct, miller_index=[2, 1, 0], min_slab_size=20.0, min_vacuum_size=15.0, center_slab=True)

for n, slabs in enumerate(slab.get_slabs()):
    slabs_bak = slabs.copy()
    slabs.make_supercell([[1, 0, 0],
                          [0, 1, 0],
                          [0, 0, 1]])
#    fig = plt.figure()
#    ax = fig.add_subplot(111)
#    plot_slab(slabs, ax, adsorption_sites=True)
#    plt.savefig(str(n) + '_β-Ti_001.png', img_format='png')
    open('POSCAR_' + mp_id + '-' + str(n), 'w').write(str(Poscar(slabs)))
test = SpacegroupAnalyzer(slabs).get_conventional_standard_structure()
open('test', 'w').write(str(Poscar(test)))