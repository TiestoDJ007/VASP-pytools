#!/home/universe/local_env/anaconda3/envs/abinit/bin/python
from pymatgen.entries.compatibility import MaterialsProjectCompatibility

compat = MaterialsProjectCompatibility()
processed_entries=compat.process_entries(unprocessed_entr)