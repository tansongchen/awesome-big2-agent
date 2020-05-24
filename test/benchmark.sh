#PBS -q mix       
#PBS -V
#PBS -S /bin/bash
#PBS -j oe
#PBS -o /disk/tansongchen/tmp/test/${PBS_JOBID%.*}
#PBS -l nodes=1:ppn=1
#PBS -l walltime=240:00:00

cd $PBS_O_WORKDIR

for index in {0..1299}
do
    python3 big2.py -a awesome -d smart -g ${index}
done

for index in {0..1299}
do
    python3 big2.py -a smart -d awesome -g ${index}
done
