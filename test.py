from build import CELL
unit=CELL("α-Ti_SO.vasp")

slab=unit.makeslab([1,2,0],layer=1)
slab.print_poscar("α-Ti_(120).vasp")