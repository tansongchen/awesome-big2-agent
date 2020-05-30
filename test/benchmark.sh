#PBS -q mix       
#PBS -V
#PBS -S /bin/bash
#PBS -j oe
#PBS -o /disk/tansongchen/tmp/test/${PBS_JOBID%.*}
#PBS -l nodes=1:ppn=1
#PBS -l walltime=240:00:00

cd $PBS_O_WORKDIR

for index in {0..129}
do
    python3 src/big2.py -a test -d test2 -g ${index}
done

for index in {0..129}
do
    python3 src/big2.py -a test2 -d test -g ${index}
done
