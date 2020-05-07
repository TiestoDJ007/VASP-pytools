#!/usr/bin/env bash

source /public1/soft/other/vasp/cn-module-vasp.5.4.1.sh
module load vasp/intel17/vasp541-O1

for DIIFUSION_ATOM in ` ls -d */ ` ; do
	cp {INCAR_SO,KPOINTS} $DIIFUSION_ATOM
	cd $DIIFUSION_ATOM
	WORK_PATH=$(dirname $(readlink -f $0))
	for DIFFUSION_DIR in ` ls -d */ ` ; do
		DIFFUSION_PATH=$WORK_PATH/$DIFFUSION_DIR
		cp {INCAR_SO,KPOINTS,POTCAR} $DIFFUSION_PATH/
		mv $DIFFUSION_PATH"INCAR_SO" $DIFFUSION_PATH"INCAR"
		cd $DIFFUSION_PATH
		srun -N 3 -n 72 -p vip_19 -J dilute-Ti vasp_std | tee ini.log
		cd $WORK_PATH
	done
	cd ..
done
