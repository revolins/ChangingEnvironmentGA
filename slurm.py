import subprocess
import argparse
import os

from test import det_output

def calc_slurm_time(total_seconds):
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def build_slurm_cmd(start_cmd, args):
    if args.num_test != 100:
        start_cmd = start_cmd + f' --num_test {args.num_test}'

    if args.static and args.mut_rat == 0.0: start_cmd = start_cmd + ' --static'
    if args.output_frequency != 10 and args.output_frequency > 0: start_cmd = start_cmd + f' --of {args.output_frequency}'
    if args.noise > 0.0: start_cmd = start_cmd + f' --noise {args.noise}'
    if args.number_of_generations != 500 and args.number_of_generations > 0: start_cmd = start_cmd + f' --ng {args.number_of_generations}'
    if args.mut_rat > 0.0: start_cmd = start_cmd + f' --mr {args.mut_rat}'
    if args.random_nr: start_cmd = start_cmd + ' --random_nr'
    if args.hybrid: start_cmd = start_cmd + ' --hybrid'
    if args.ignore_matching: start_cmd = start_cmd + ' --ignore_matching'

    run_seconds = args.num_test * args.test_time # approximately X seconds per a given test
    run_time = calc_slurm_time(run_seconds)

    return start_cmd, run_time

def run_slurm(args):
    output_folder, _ = det_output(args)
    start_cmd = 'srun python test.py'
    full_cmd, slurm_time = build_slurm_cmd(start_cmd, args)
    with open('run_exp.sb', 'w+') as f:
        f.seek(0)
        f.write('#!/bin/bash --login\n')

        f.write(f'#SBATCH --job-name={output_folder}\n')
        f.write('#SBATCH --nodes=1\n')
        f.write('#SBATCH --cpus-per-task=16\n')
        f.write('#SBATCH --mem-per-cpu=1G\n')
        f.write(f'#SBATCH --{slurm_time}\n')
        if args.username != None:
            f.write('#SBATCH --mail-type=BEGIN,END\n')
            f.write(f'#SBATCH --mail-user={args.username}@msu.edu\n')
        f.write('#SBATCH --output=%x-%j.SLURMout\n')

        f.write('module load Conda/3\n')
        f.write('conda activate heart_env\n')

        f.write(full_cmd + '\n')

        f.write('scontrol show job $SLURM_JOB_ID\n')
        f.write('js -j $SLURM_JOB_ID\n')
    f.close()
    if args.run:
        subprocess.run(['sbatch', 'run_exp.sb'])
    else:
        assert args.run, "type 'sbatch run_exp.sb' to execute current experiment. \n\
        WARNING: run_exp.sb will be overwritten if slurm.py is executed again.\n\
        WARNING: double check experiment settings in run_exp.sb"

def main():
    arg_parser = argparse.ArgumentParser(
        description='Interface Script for PD Experiments in HPCC. WARNING: #SBATCH variables are hard-coded and will need to be updated manually')
    
    arg_parser.add_argument("--num_test", "--nt", type=int, default=100, help="(int), (DEFAULT=100), Specify number of unique seeded runs")
    arg_parser.add_argument("--static", "--s", action='store_true', default=False, help="(bool) (DEFAULT=False) Specify whether to test in static environment with no mutation rate")
    arg_parser.add_argument("--mut_rat", "--mr", type=float, default=0.0, help="(float) (DEFAULT=0.0) Set the rate at which the system will mutate memory and decision list")
    arg_parser.add_argument("--noise", "--n", type=float, default=0.0, help="(float) (DEFAULT = 0.0) Percent Likelihood the one of the opposing organisms moves is misread")
    arg_parser.add_argument("--random_nr", "--rnr", action='store_true', default=False, help="(bool) (DEFAULT=False) Specify if number of tournament rounds are randomized in a single game")
    arg_parser.add_argument("--hybrid", '--h', action='store_true', default=False, help="(bool) (DEFAULT = False) original memory model (FALSE), hybrid memory model (TRUE)")
    arg_parser.add_argument("--number_of_generations", "--ng", type=int, default=500, help="(int) (DEFAULT = 500) number of generations selected upon after a tournament")
    arg_parser.add_argument("--output_frequency", "--of", type=int, default=10, help="(int) (DEFAULT = 10) Determines the organisms output to the detail-*.csv, where * is the generation number")
    arg_parser.add_argument("--ignore_matching", "--ms", action='store_true', default=False, help="(bool) (DEFAULT = False) If the experiment will match seeds to the runs")
    arg_parser.add_argument("--username", "--un", type=str, default=None, help='(str) Set to your username to determine email you when test starts and finishes')
    arg_parser.add_argument("--test_time", "--tt", type=int, default=10, help="(int) (DEFAULT=10) Set number of seconds given for each test SLURM will allow")
    arg_parser.add_argument("--run", "--r", action='store_true', default=False, help="(bool) (DEFAULT=False) Set to automatically submit SLURM job")
    args = arg_parser.parse_args()  
    
    run_slurm(args)
    
if __name__ == "__main__":
    main()