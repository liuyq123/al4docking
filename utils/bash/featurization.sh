#!/bin/bash

#SBATCH -n 2
#SBATCH -p hpc
#SBATCH -x node242
#SBATCH --array=1-5

# TARGET=ampc
# ROUND=round3_5

# python ../featurization.py \
# -d ../../data/dock3/$TARGET/raw/$ROUND/fold${SLURM_ARRAY_TASK_ID}.csv \
# --data_dir ../../data/dock3/$TARGET/featurized/$ROUND/fold${SLURM_ARRAY_TASK_ID} \
# --tasks dockscore

python ../featurization.py \
--file_path /lustre/fs6/lyu_lab/scratch/yliu03/Active-Learning-for-Docking/data/dock3/ampc/raw/random1/fold${SLURM_ARRAY_TASK_ID}.csv \
--output_dir /lustre/fs6/lyu_lab/scratch/yliu03/Active-Learning-for-Docking/data/dock3/ampc/featurized/random1/fold${SLURM_ARRAY_TASK_ID} \
--id_field zincid \
--tasks dockscore \

# python ../featurization.py \
# --file_path /lustre/fs6/lyu_lab/scratch/yliu03/Active-Learning-for-Docking/vmat2/round1_exp2_f_smoothed_p4_score/fold${SLURM_ARRAY_TASK_ID}.csv \
# --output_dir /lustre/fs6/lyu_lab/scratch/yliu03/Active-Learning-for-Docking/vmat2/featurized/round1_exp2_f_smoothed_p4_score/fold${SLURM_ARRAY_TASK_ID} \
# --id_field zinc_id \
# --tasks dockscore \
# --use_edges \