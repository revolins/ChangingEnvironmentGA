import subprocess
from tqdm import tqdm
import argparse
import datetime

def run_test(args):
    now = datetime.datetime.now()
    current_time = now.strftime('%m%d%y%H%M%S')
    output_folder = "coevhighmut_" + current_time
    print("Initiating Seeded Run")
    for i in tqdm(range(1, args.num_test + 1)):
        subprocess.run(["python", "changing_environment_ga.py", "--seed", f"{i}", "--m_c", "0.0", "--mr", "0.1", "-o", f"{output_folder}/pd_coevhimut_test{i}_0.0_cost"])
        subprocess.run(["python", "changing_environment_ga.py", "--seed", f"{i}", "--m_c", "0.01", "--mr", "0.1", "-o", f"{output_folder}/pd_coevhimut_test{i}_0.01_cost"])
        subprocess.run(["python", "changing_environment_ga.py", "--seed", f"{i}", "--m_c", "0.05", "--mr", "0.1", "-o", f"{output_folder}/pd_coevhimut_test{i}_0.05_cost"])
        subprocess.run(["python", "changing_environment_ga.py", "--seed", f"{i}", "--m_c", "0.075", "--mr", "0.1", "-o", f"{output_folder}/pd_coevhimut_test{i}_0.075_cost"])
        subprocess.run(["python", "changing_environment_ga.py", "--seed", f"{i}", "--m_c", "0.2", "--mr", "0.1", "-o", f"{output_folder}/pd_coevhimut_test{i}_0.2_cost"])

    subprocess.run(["python", "compile_csv.py", "-o", output_folder])
    subprocess.run(["python", "plot_csv.py", "-o", output_folder])

    print(f"Experiment Concluded, results stored in {output_folder}")

def main():
    arg_parser = argparse.ArgumentParser(
        description='Testing Script for Co-Evolutionary, Low Mutation Rate PD.')
    
    arg_parser.add_argument("--num_test", "--nt", type=int, default=100, help="(int), (DEFAULT=100), Specify number of unique seeded runs")
    args = arg_parser.parse_args()  
    
    run_test(args)
    
if __name__ == "__main__":
    main()