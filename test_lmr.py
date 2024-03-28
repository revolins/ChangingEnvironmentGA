import subprocess
from tqdm import tqdm
import argparse

def run_test(args):
    # TODO: Update folder naming schemes with a utils.py in order for different files to work between tests
    print("Initiating Seeded Run")
    for i in tqdm(range(1, args.num_test + 1)):
        subprocess.run(["python", "changing_environment_ga.py", "--seed", f"{i}", "--m_c", "0.0", "--mr", "0.01", "-o", f"pd_check/pd_static_test{i}_0.0_cost"])
        subprocess.run(["python", "changing_environment_ga.py", "--seed", f"{i}", "--m_c", "0.01", "--mr", "0.01", "-o", f"pd_check/pd_static_test{i}_0.01_cost"])
        subprocess.run(["python", "changing_environment_ga.py", "--seed", f"{i}", "--m_c", "0.05", "--mr", "0.01", "-o", f"pd_check/pd_static_test{i}_0.05_cost"])
        subprocess.run(["python", "changing_environment_ga.py", "--seed", f"{i}", "--m_c", "0.075", "--mr", "0.01", "-o", f"pd_check/pd_static_test{i}_0.075_cost"])
        subprocess.run(["python", "changing_environment_ga.py", "--seed", f"{i}", "--m_c", "0.2", "--mr", "0.01", "-o", f"pd_check/pd_static_test{i}_0.2_cost"])

    subprocess.run(["python", "build_csv.py"])
    subprocess.run(["python", "build_plot.py"])

    print("Experiment Concluded, results stored in pd_check")

def main():
    arg_parser = argparse.ArgumentParser(
        description='Testing Script for Co-Evolutionary, Low Mutation Rate PD.')
    
    arg_parser.add_argument("--num_test", "--nt", type=int, default=100, help="(int), (DEFAULT=100), Specify number of unique seeded runs")
    args = arg_parser.parse_args()  
    
    run_test(args)
    
if __name__ == "__main__":
    main()