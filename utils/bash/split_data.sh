#!/bin/bash

#SBATCH -n 64
#SBATCH -p bigmem
#SBATCH -w node062

python /lustre/fs6/lyu_lab/scratch/yliu03/Active-Learning-for-Docking/data_processing/split_data.py \
--file_path /lustre/fs6/lyu_lab/scratch/yliu03/Active-Learning-for-Docking/data/dock3/ampc/raw/unsplited/random1.csv \
--num_splits 5 \
--output_dir /lustre/fs6/lyu_lab/scratch/yliu03/Active-Learning-for-Docking/data/dock3/ampc/raw/random1 \
