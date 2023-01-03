#!/bin/bash
#SBATCH -p gpuq
#SBATCH -q gpu
#SBATCH --job-name=Gorani-Persian
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --mem=32GB
#SBATCH --gres=gpu:A100.80gb:1
#SBATCH --export=ALL
#SBATCH -t 5-0:0:0
#SBATCH --array=1,20,40,60,80,100
#SBATCH --output=/scratch/sahmad46/training/Gorani-Persian-%a-%j.txt
#SBATCH --mail-type=ALL
#SBATCH --mail-user=sahmad46@gmu.edu

ml gnu10; ml cuda; ml cudnn; ml nvidia-hpc-sdk; ml python;

echo "Start process"
echo "SLURM_JOBID: " $SLURM_JOBID
echo "SLURM_ARRAY_TASK_ID: " $SLURM_ARRAY_TASK_ID
echo "SLURM_ARRAY_JOB_ID: " $SLURM_ARRAY_JOB_ID

RUNPATH=/scratch/sahmad46
cd $RUNPATH

echo "Starting Venv"
source $RUNPATH/venvs/joeynmt_torch1/bin/activate

echo "Running the script"
python3 -m joeynmt train training/configs/Gorani-Persian_$SLURM_ARRAY_TASK_ID.yaml

deactivate
echo "End process"