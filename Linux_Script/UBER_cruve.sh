#!/usr/bin/env bash
#source /PARA/app/scripts/cn-module.sh
#source /PARA/app/other/vasp.5.4.4/vasp-module.sh
#module load vasp/5.4.4-mpi3-O3-scalapack-vtst
echo >structure_energy
for Number_dir in $(seq 1 1 20); do
  DISTANCE=$(printf "%.1f" $(echo "scale=2;${Number_dir}*(0.5)" | bc))
  echo "Distance=$DISTANCE"
  cp {INCAR,KPOINTS,POTCAR-bottem,POTCAR-top,POTCAR-total} POSCAR_Uber_${DISTANCE}A/
  cd POSCAR_Uber_${DISTANCE}A || return
  cp POSCAR_top.vasp POSCAR
  cp POTCAR-top POTCAR
  mpirun -np 128 vasp_std
  E_top=$(grep "TOTEN" OUTCAR | tail -1 | awk '{printf"%12.6f \n",$5}')
  cp POSCAR_bottem.vasp POSCAR
  cp POTCAR-bottem POTCAR
  mpirun -np 128 vasp_std
  E_bottem=$(grep "TOTEN" OUTCAR | tail -1 | awk '{printf"%12.6f \n",$5}')
  cp POSCAR_total.vasp POSCAR
  cp POTCAR-total POTCAR
  mpirun -np 128 vasp_std
  E_total=$(grep "TOTEN" OUTCAR | tail -1 | awk '{printf"%12.6f \n",$5}')
  W_seq=$(printf "%.6f" $(echo "scale=2;$E_total-$E_top-$E_bottem" | bc))
  cd ..
  echo -e "DISTANCE=$DISTANCE\nE_top=$E_top E_bottem=$E_bottem E_total=$E_total\nW_seq=$W_seq\n" >>structure_energy
done
cat structure_energy
