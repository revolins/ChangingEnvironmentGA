import subprocess
from tqdm import tqdm
import argparse
import datetime

def format_command(args):
    if args.static:
        args.mut_rat = 0.0
        folder_str = "static"
    else:
        folder_str = "coev"
    
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

def run_test(args):
    output_folder, test_type = format_command(args)

    mem_cost = ['0.0', '0.01', '0.05', '0.075', '0.2']
    print("Initiating Seeded Run")
    for i in tqdm(range(1, args.num_test + 1)):
        for cost in mem_cost:
            temp_cmd = []
            if args.static:
                temp_cmd.append("--static")
            if args.mut_rat > 0.0 and not args.static:
                temp_cmd.extend(["--mr", str(args.mut_rat)])
            default_cmd = ["python", "changing_environment_ga.py", "--seed", f"{i}", "--m_c", cost, "-o", f"{output_folder}/pd_{test_type}test{i}_{cost}_cost"]
            if len(temp_cmd) > 0: default_cmd.extend(temp_cmd)

            subprocess.run(default_cmd)

    subprocess.run(["python", "compile_csv.py", "-o", output_folder])
    subprocess.run(["python", "plot_csv.py", "-o", output_folder])

    print(f"Experiment Concluded, results stored in {output_folder}")

def main():
    arg_parser = argparse.ArgumentParser(
        description='Testing Script for PD Experiments.')
    
    arg_parser.add_argument("--num_test", "--nt", type=int, default=100, help="(int), (DEFAULT=100), Specify number of unique seeded runs")
    arg_parser.add_argument("--static", "--s", action='store_true', default=False, help="(bool) (DEFAULT=False) Specify whether to test in static environment with no mutation rate")
    arg_parser.add_argument("--mut_rat", "--mr", type=float, default=0.0, help="(float) (DEFAULT=0.0) Set the rate at which the system will mutate memory and decision list")
    args = arg_parser.parse_args()  
    
    run_test(args)
    
if __name__ == "__main__":
    main()