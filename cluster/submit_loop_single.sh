for i in $(seq 0 45)
do
	sbatch --export=ii=${i} submit_exec010.sbat
	sleep 0.1
done