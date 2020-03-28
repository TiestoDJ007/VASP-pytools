#!/usr/bin/env bash
source /PARA/app/scripts/cn-module.sh
source /PARA/app/other/vasp.5.4.4/vasp-module.sh
module load vasp/5.4.4-mpi3-O3-scalapack-vtst

echo > cpu_time
for n_KPAR in 1 2 3 4 6 8 ; do
    for n_NCORE in 1 2 3 4 6 8 ; do
        cp INCAR_ini INCAR
        echo -e " KPAR = $n_KPAR\n NCORE = $n_NCORE\n" >> INCAR
        srun -N 2 -n 48 -p paratera -J test_NCORE vasp_std
        TIME_USED=`grep "Total CPU time used" OUTCAR | awk '{printf"%12.6f \n",$6}'`
        echo KPAR = $n_KPAR NCORE = $n_NCORE TIME_USED = $TIME_USED >> cpu_time
    done

done
