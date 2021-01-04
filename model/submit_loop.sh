for i in $(seq 0 99)
do
	sbatch --export=ii=${i} submit_exec004.sbat
	sleep 0.2
done

for i in $(seq 0 99)
do
	sbatch --export=ii=${i} submit_exec003.sbat
	sleep 0.2
done

for i in $(seq 0 99)
do
	sbatch --export=ii=${i} submit_exec002.sbat
	sleep 0.2
done

for i in $(seq 0 99)
do
	sbatch --export=ii=${i} submit_exec001.sbat
	sleep 0.2
done