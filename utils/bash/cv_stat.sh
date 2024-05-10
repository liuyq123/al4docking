#!/bin/bash

#SBATCH -n 1
#SBATCH -p hpc_a10
#SBATCH --array=1-200

python ../cv_stat.py -i ${SLURM_ARRAY_TASK_ID} \
--preds_dir /lustre/fs6/lyu_lab/scratch/yliu03/Active-Learning-for-Docking/atp/leading/results/round2 \
--output_dir /lustre/fs6/lyu_lab/scratch/yliu03/Active-Learning-for-Docking/atp/leading/results/round2/all \
--folds v1 v2 v3 v4 v5 \