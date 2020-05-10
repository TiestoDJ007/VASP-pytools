#!/usr/bin/env bash

WORK_PATH=$(dirname $(readlink -f $0))

for DIFFUSION_ATOM in Al/ Cr/ Mo/ Nb/ Sn/ Ti/ Zr/ ; do
    echo "DIFFUSION ATOM is" $DIFFUSION_ATOM
    for DIFFUSION_STRUCTURE in 1_Oct_alpha/ 1_Tet_inter/ 2_Oct_inter_beta/ 1_Oct_beta/ 2_Oct_alpha/ 2_Tet_beta/1_Oct_inter_beta/ 2_Oct_beta/ 1_Tet_beta/ 2_Oct_inter_alpha/ ; do
        CONTCAR_COPY_PATH=$WORK_PATH/CONTCAR_COPY/$DIFFUSION_ATOM$DIFFUSION_STRUCTURE
        CONTCAR_FILE=$WORK_PATH/$DIFFUSION_ATOM$DIFFUSION_STRUCTURE"CONTCAR"
        mkdir -p $CONTCAR_COPY_PATH
        cp $CONTCAR_FILE $CONTCAR_COPY_PATH
    done
    echo $DIFFUSION_STRUCTURE "Done!"
done
