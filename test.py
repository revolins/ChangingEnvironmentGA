import subprocess
from tqdm import tqdm
import argparse
import datetime
import sys

def det_output(args):
    folder_str = 'pd'
    if args.hybrid:
        folder_str = folder_str + "hybrid"
    if args.static:
        args.mut_rat = 0.0
        folder_str = folder_str + "static"
    else:
        folder_str = folder_str + "coev"

    if args.noise > 0.0:
        folder_str = folder_str + "noise" + str(args.noise)
    if args.remove_mem_limit:
        folder_str = folder_str + "maxmem"
    
    if args.mut_rat > 0.09:
        folder_str = folder_str + "highmut_"
    elif args.mut_rat <= 0.09 and args.mut_rat > 0.0:
        folder_str = folder_str + "lowmut_"
    else:
        folder_str = folder_str + "nomut_"

    now = datetime.datetime.now()
    current_time = now.strftime('%m%d%y%H%M%S')
    output_folder = folder_str + current_time

    return output_folder, folder_str

def format_cmd(args):
    temp_cmd = []
    if args.static:
        temp_cmd.append("--static")
    if args.mut_rat > 0.0 and not args.static:
        temp_cmd.extend(["--mr", str(args.mut_rat)])
    if args.noise > 0.0:
        temp_cmd.extend(["--noise", str(args.noise)])
    if args.hybrid:
        temp_cmd.extend(["--org_type", "hybrid_pd"])
    if args.remove_mem_limit:
        temp_cmd.extend(["--max_bits_of_memory", str(16)])

    return temp_cmd

def build_plt_cmd(args):
    temp_cmd = []
    if args.output_frequency != 10:
        temp_cmd.extend(["--output_frequency", str(args.output_frequency)])
    if args.number_of_generations != 500:
        temp_cmd.extend(["--number_of_generations", str(args.number_of_generations)])

    return temp_cmd

def run_test(args):
    output_folder, test_type = det_output(args)
    temp_cmd = format_cmd(args)
    temp_str = build_plt_cmd(args)

    mem_cost = ['0.0', '0.01', '0.05', '0.075', '0.2']
    if args.ignore_matching: print("Initiating Unseeded Run")
    else: print("Initiating Seeded Run")
    for i in tqdm(range(1, args.num_test + 1)):
        for cost in mem_cost:
            default_cmd = ["python", "changing_environment_ga.py", "--m_c", cost, "-o", f"{output_folder}/pd_{test_type}test{i}_{cost}_cost"]
            if not args.ignore_matching: default_cmd.extend(["--seed", f"{i}"])
            if len(temp_cmd) > 0: default_cmd.extend(temp_cmd)
            if len(temp_str) > 0: default_cmd.extend(temp_str)

            subprocess.run(default_cmd)

    subprocess.run(["python", "compile_csv.py", "-o", output_folder])
    plot_str = ["python", "plot_csv.py", "-o", output_folder]
    if len(temp_str) > 0: plot_str.extend(temp_str)
    subprocess.run(plot_str)

    print(f"Experiment Concluded, results stored in {output_folder}")

def main():
    arg_parser = argparse.ArgumentParser(
        description='Testing Script for PD Experiments.')
    
    arg_parser.add_argument("--num_test", "--nt", type=int, default=100, help="(int), (DEFAULT=100), Specify number of unique seeded runs")
    arg_parser.add_argument("--static", "--s", action='store_true', default=False, help="(bool) (DEFAULT=False) Specify whether to test in static environment with no mutation rate")
    arg_parser.add_argument("--mut_rat", "--mr", type=float, default=0.0, help="(float) (DEFAULT=0.0) Set the rate at which the system will mutate memory and decision list")
    arg_parser.add_argument("--noise", "--n", type=float, default=0.0, help="(float) (DEFAULT = 0.0) Percent Likelihood the one of the opposing organisms moves is misread")
    arg_parser.add_argument("--hybrid", "--h", action='store_true', default=False, help="(bool) (DEFAULT = False) original memory model (FALSE), hybrid memory model (TRUE)")
    arg_parser.add_argument("--number_of_generations", "--ng", type=int, default=500, help="(int) (DEFAULT = 500) number of generations selected upon after a tournament")
    arg_parser.add_argument("--output_frequency", "--of", type=int, default=10, help="(int) (DEFAULT = 10) Determines the organisms output to the detail-*.csv, where * is the generation number")
    arg_parser.add_argument("--ignore_matching", "--ms", action='store_true', default=False, help="(bool) (DEFAULT = False) If the experiment will match seeds to the runs")
    arg_parser.add_argument("--remove_mem_limit", "--ml", action='store_true', default=False, help="(bool) (DEFAULT = False) If experiment will run without memory limit on number of bits of summary and memory")
    args = arg_parser.parse_args()  
    
    run_test(args)
    
if __name__ == "__main__":
    main()