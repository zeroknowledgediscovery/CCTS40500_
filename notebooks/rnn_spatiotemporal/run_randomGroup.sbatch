#!/bin/bash

group=$1
SBC=./tmp${group}.sbc
echo "#!/bin/bash" > $SBC
echo "#SBATCH --job-name=randomGroup${group}" >> $SBC
echo "#SBATCH --output=randomGroup${group}.out" >> $SBC
echo "#SBATCH --error=randomGroup${group}.err" >> $SBC
echo "#SBATCH --time=06:00:00" >> $SBC
echo "#SBATCH --nodes=1" >> $SBC
echo "#SBATCH --partition=gpu2" >> $SBC
echo "#SBATCH --ntasks=4" >> $SBC 
echo "#SBATCH --gres=gpu:1" >> $SBC

echo "module load cuda/10.0" >> $SBC
echo "./rnn_randomGroup.py ${group}" >> $SBC

sbatch $SBC
