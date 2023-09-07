from pymatgen.io.vasp import Potcar
potcar_symbols = ["Cr","Fe","N"]
potcar = Potcar(potcar_symbols)
potcar.write_file("POTCAR-total")