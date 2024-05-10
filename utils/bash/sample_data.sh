#!/bin/bash

#SBATCH -n 128
#SBATCH -p lyu_docking
#SBATCH -w node240

python ../sample_data.py \
--file_path /lustre/fs6/lyu_lab/scratch/jlyu/work/VMAT2/prot_docking/sph_scanning/combo_directories/es_1.2_ld_0.1/LSD_cations/check_unfinished/round1.overlap.csv \
--output_path /lustre/fs6/lyu_lab/scratch/yliu03/Active-Learning-for-Docking/vmat2/exp_400k_2.csv \
--num_samples 400000 \
# --sampling_cutoff 1000 \
--score_field dockscore \