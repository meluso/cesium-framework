for i in $(seq 0 273)
do
	sbatch --export=ii=${i} submit_exec009.sbat
	sleep 0.1
done