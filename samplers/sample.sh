#!/bin/bash

#SBATCH -n 64
#SBATCH -p bigmem
#SBATCH -w node062

python -u sample.py --config sample.yaml