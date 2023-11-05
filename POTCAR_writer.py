from pymatgen.io.vasp import Potcar

potcar_symbols = ["Cr", "Fe", "N", "W"]
potcar = Potcar(potcar_symbols)
potcar.write_file("Data_file/POTCAR-total")
