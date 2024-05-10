#!/bin/bash

#SBATCH -n 64
#SBATCH -p bigmem
#SBATCH -w node062
#SBATCH --mail-type=ALL         
#SBATCH --mail-user=yliu03@rockefeller.edu

python /lustre/fs6/lyu_lab/scratch/yliu03/Active-Learning-for-Docking/data_processing/recall.py \
--data_path /lustre/fs6/lyu_lab/scratch/yliu03/Active-Learning-for-Docking/vmat2_exp/results/round2_exp2_smoothed \
--id_field zinc_id \
--score_field dockscore \
--preds_field preds \
--ground_truth_path /lustre/fs6/lyu_lab/scratch/jlyu/work/VMAT2/prot_docking/sph_scanning/combo_directories/es_1.2_ld_0.1/LSD_cations/check_unfinished/round1.overlap.csv \
--pct_list 0.02 0.03 0.04 0.05 0.1 \
--top_n 100000 \
--experiment_name round2_exp2_smoothed \
--output vmat2_100k.csv \
