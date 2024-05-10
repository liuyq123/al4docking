#!/bin/bash

#SBATCH -n 2
#SBATCH -p lyu_docking

python /lustre/fs6/lyu_lab/scratch/yliu03/Active-Learning-for-Docking/utils/check_file_existence.py \
--preds_data_path /lustre/fs6/lyu_lab/scratch/yliu03/Active-Learning-for-Docking/src/gcn/predictions/ampc/random_002/v1 \
--total_file_num 101 \