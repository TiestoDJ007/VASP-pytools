#!/usr/bin/bash

initial_interface_distance=$(printf "%.2f" -0.2)
interface_delta=$(printf "%.2f" 0.5)
loop_number=$(printf "%d" 16)
echo >structure_energy
echo
for Number_dir in $(seq 1 1 ${loop_number}); do
  DISTANCE=$(printf "%.2f" $(echo "scale=2;${Number_dir}*${interface_delta}+${initial_interface_distance}" | bc))
  echo "Distance=$DISTANCE"
  cp {INCAR,KPOINTS,POTCAR_bottem,POTCAR_top,POTCAR_total} POSCAR_Uber_${DISTANCE}A/
  cd POSCAR_Uber_${DISTANCE}A || return
  cp POSCAR_top.vasp POSCAR
  cp POTCAR_top POTCAR
  mpirun -np 128 vasp_std
  E_top=$(grep "TOTEN" OUTCAR | tail -1 | awk '{printf"%12.6f \n",$5}')
  cp POSCAR_bottem.vasp POSCAR
  cp POTCAR_bottem POTCAR
  mpirun -np 128 vasp_std
  E_bottem=$(grep "TOTEN" OUTCAR | tail -1 | awk '{printf"%12.6f \n",$5}')
  cp POSCAR_total.vasp POSCAR
  cp POTCAR_total POTCAR
  mpirun -np 128 vasp_std
  E_total=$(grep "TOTEN" OUTCAR | tail -1 | awk '{printf"%12.6f \n",$5}')
  W_seq=$(printf "%.6f" $(echo "scale=2;$E_total-$E_top-$E_bottem" | bc))
  cd ..
  echo -e "DISTANCE=$DISTANCE\nE_top=$E_top E_bottem=$E_bottem E_total=$E_total\nW_seq=$W_seq\n" >>structure_energy
done
cat structure_energy
