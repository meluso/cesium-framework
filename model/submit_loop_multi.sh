for i in $(seq 0 99)
do
	sbatch --export=ii=${i} submit_exec008.sbat
	sleep 0.2
done

for i in $(seq 0 99)
do
	sbatch --export=ii=${i} submit_exec007.sbat
	sleep 0.2
done

for i in $(seq 0 99)
do
	sbatch --export=ii=${i} submit_exec006.sbat
	sleep 0.2
done