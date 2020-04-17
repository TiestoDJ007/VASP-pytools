#!/usr/bin/env bash

WORK_PATH=$(dirname $(readlink -f $0))
echo $WORK_PATH
for DIFFUSION_DIR in 102-04/ 102-10/ 102-13 ; do
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
    mpirun -np 16 vasp_std | tee ini.log;
    cd $WORK_PATH/$FIN_DIR
    mpirun -np 16 vasp_std | tee fin.log;
    cd $WORK_PATH/$DIFFUSION_DIR
    Delta_Distance=$(dist.pl ini/CONTCAR fin/CONTCAR)
    echo $Delta_Distance
    nebmake.pl ini/CONTCAR fin/CONTCAR 3
	cp ini/OUTCAR 00/
	cp fin/OUTCAR 04/
    cp $WORK_PATH/INCAR_CI $WORK_PATH/$DIFFUSION_DIR"INCAR"
    cp $WORK_PATH/{KPOINTS,POTCAR} $WORK_PATH/$DIFFUSION_DIR
    mpirun -np 15 vasp_std | tee NEB.log;
    cd $WORK_PATH
done

    