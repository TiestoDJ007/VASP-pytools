#!/usr/bin/env bash

source /PARA/app/scripts/cn-module.sh
source /PARA/app/other/vasp.5.4.4/vasp-module.sh
module load vasp/5.4.4-mpi3-O3-scalapack-vtst

WORK_PATH=$(dirname $(readlink -f $0))
echo $WORK_PATH
for DIFFUSION_DIR in ` ls -d */ ` ; do
    INI_DIR=$DIFFUSION_DIR"ini"
    FIN_DIR=$DIFFUSION_DIR"fin"
    mkdir $INI_DIR $FIN_DIR
    cp {INCAR_SO,KPOINTS,POTCAR} $INI_DIR/
    mv $INI_DIR/INCAR_SO $INI_DIR/INCAR
    cp {INCAR_SO,KPOINTS,POTCAR} $FIN_DIR/
    mv $FIN_DIR/INCAR_SO $FIN_DIR/INCAR
    cp $DIFFUSION_DIR"POSCAR_Ini" $INI_DIR
	mv $WORK_PATH/$INI_DIR/POSCAR_Ini $WORK_PATH/$INI_DIR/POSCAR
    cp $DIFFUSION_DIR"POSCAR_Fin" $FIN_DIR
	mv $WORK_PATH/$FIN_DIR/POSCAR_Fin $WORK_PATH/$FIN_DIR/POSCAR
    cd $WORK_PATH/$INI_DIR
    srun -N 1 -n 24 -p paratera -J dilute-Ti vasp_std | tee ini.log;
    cd $WORK_PATH/$FIN_DIR
    srun -N 1 -n 24 -p paratera -J dilute-Ti vasp_std | tee fin.log;
    cd $WORK_PATH/$DIFFUSION_DIR
    Delta_Distance=$(dist.pl ini/CONTCAR fin/CONTCAR)
    echo $Delta_Distance
    nebmake.pl ini/CONTCAR fin/CONTCAR 3
    cp $WORK_PATH/INCAR_CI $WORK_PATH/$DIFFUSION_DIR"INCAR"
    cp $WORK_PATH/{KPOINTS,POTCAR} $WORK_PATH/$DIFFUSION_DIR
    srun -N 1 -n 24 -p paratera -J dilute-Ti vasp_std | tee NEB.log;
    cd $WORK_PATH
done

    