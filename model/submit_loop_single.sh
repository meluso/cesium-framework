for i in $(seq 0 20275)
do
	sbatch --export=ii=${i} submit_exec005.sbat
	sleep 0.1
done