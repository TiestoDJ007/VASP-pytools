#!/usr/bin/env bash

source /PARA/app/scripts/cn-module.sh
source /PARA/app/other/vasp.5.4.4/vasp-module.sh
module load vasp/5.4.4-mpi3-O3-scalapack-vtst

for DIIFUSION_ATOM in ` ls -d */ ` ; do
	cp {INCAR_SO,KPOINTS} $DIIFUSION_ATOM
	cd $DIIFUSION_ATOM
	WORK_PATH=$(dirname $(readlink -f $0))
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
		srun -N 2 -n 48 -p paratera -J dilute-Ti vasp_std | tee ini.log
		cd $WORK_PATH/$FIN_DIR
		srun -N 2 -n 48 -p paratera -J dilute-Ti vasp_std | tee fin.log;
		cd $WORK_PATH/$DIFFUSION_DIR
		Delta_Distance=$(dist.pl ini/CONTCAR fin/CONTCAR)
		echo $Delta_Distance
		cd $WORK_PATH
	done
	cd ..
done
