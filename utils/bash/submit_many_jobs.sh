#!/bin/bash

TOTAL_JOB_NUM=100

INITIAL_SUBMIT_NUM=40
ADDITIONAL_SUBMIT_NUM=20
THRESHOLD=20

JOB_NAME=predict_ampc

N_CPU=1
PARTITION=lyu,hpc

VALIDATION_FOLD=v2
ROUND=round2_5

COUNT=0

initial_submit() {
    sbatch -n ${N_CPU} -p ${PARTITION} --array=1-${INITIAL_SUBMIT_NUM} --name ${JOB_NAME} CUDA_VISIBLE_DEVICES=$(($SLURM_ARRAY_TASK_ID%2)) python ../../prediction.py \
-d ../../../../data/dock3/ampc/featurized/ampc_scored/fold$(($SLURM_ARRAY_TASK_ID+$COUNT)) \
--output_dir  ../../predictions/ampc/$ROUND/$VALIDATION_FOLD/fold$(($SLURM_ARRAY_TASK_ID+$COUNT)) \
--graph_conv_layers 32 512 512 256 \
--predictor_hidden_feats 64 \
--model_dir ../../model_checkpoints/ampc/$ROUND/$VALIDATION_FOLD \
  
    COUNT=$(($COUNT+$INITIAL_SUBMIT_NUM))
}

additional_submit() {
    sbatch -n ${N_CPU} -p ${PARTITION} --array=1-${ADDITIONAL_SUBMIT_NUM} --name ${JOB_NAME} CUDA_VISIBLE_DEVICES=$(($SLURM_ARRAY_TASK_ID%2)) python ../../prediction.py \
-d /lustre/fs6/lyu_lab/scratch/yliu03/Active-Learning-for-Docking/prospective_data/featurized/all/file$(($SLURM_ARRAY_TASK_ID+$COUNT)) \
--output_dir  ../../predictions/prospective/$DATA_SET/$ROUND/v${VALIDATION_FOLD}/file$(($SLURM_ARRAY_TASK_ID+$COUNT)) \
--graph_conv_layers 64 2048 1024 \
--predictor_hidden_feats 256 \
--model_dir ../../model_checkpoints/prospective/$DATA_SET/$ROUND/v${VALIDATION_FOLD} \

    COUNT=$(($COUNT+$ADDITIONAL_SUBMIT_NUM))
}

check_current_job_num() {
    squeue --name="$JOB_NAME" --noheader --format=%T | wc -l
}

initial_submit

while true; do

    CUR_NUM=$(check_current_job_num)

    if [ ${CUR_NUM} -lt ${THRESHOLD} ]; then
        additional_submit
    fi

    sleep 60

    if [ ${COUNT} -ge ${TOTAL_JOB_NUM} ]; then
      exit 1
    fi

done