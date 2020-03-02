#!/bin/bash

#SBATCH --job-name=test
#SBATCH --output=test.out
#SBATCH --error=test.err
#SBATCH --time=02:00:00
#SBATCH --nodes=1
#SBATCH --partition=gpu2
#SBATCH --ntasks=4 
#SBATCH --gres=gpu:1

# to run file:
# sbatch ./run.sbatch

module load cuda/10.0

# conda activate hiv-dip

./rnn_batch.py $1
