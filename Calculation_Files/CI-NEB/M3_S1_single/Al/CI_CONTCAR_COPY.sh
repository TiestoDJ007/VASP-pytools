#!/usr/bin/env bash

WORK_PATH=$(dirname $(readlink -f $0))
mkdir copy
for Element_DIR in Ti/ Zr/ ; do
for Transition_DIR in 41-01/  41-07/  57-07/  57-19/ ; do
copy_dir=$Element_DIR$Transition_DIR
mkdir -p copy/$copy_dir'fin'
cp $copy_dir/fin/CONTCAR copy/$copy_dir'fin/CONTCAR'
mkdir -p copy/$copy_dir'ini'
cp $copy_dir/ini/CONTCAR copy/$copy_dir'ini/CONTCAR'
done
done