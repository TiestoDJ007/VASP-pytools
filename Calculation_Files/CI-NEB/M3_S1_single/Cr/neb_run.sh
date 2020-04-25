#!/usr/bin/env bash

WORK_PATH=$(dirname $(readlink -f $0))
echo $WORK_PATH
for DIFFUSION_DIR in ` ls -d */ ` ; do
    cd $WORK_PATH/$DIFFUSION_DIR
    Delta_Distance=$(dist.pl ini/CONTCAR fin/CONTCAR)
    echo $Delta_Distance
	cp ini/OUTCAR 00/
	cp fin/OUTCAR 04/
    cp $WORK_PATH/INCAR_CI $WORK_PATH/$DIFFUSION_DIR"INCAR"
    cp $WORK_PATH/{KPOINTS,POTCAR} $WORK_PATH/$DIFFUSION_DIR
    mpirun -np 15 vasp_std | tee NEB.log;
    cd $WORK_PATH
done
