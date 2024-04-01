import argparse
from utils import generate_data
import time

def parse_everything(command_line_args=None):
    """Parse command line arguments"""
    arg_parser = argparse.ArgumentParser(
        description='The changing environments program.')
    
    # Expects 1 argument: output folder
    arg_parser.add_argument("-o", "--output_folder", nargs=1)
    arg_parser.add_argument("--seed", "--s", type=int, default=int(time.time()))
    arg_parser.add_argument("--number_of_generations", "--ng",  type=int, default=500)
    arg_parser.add_argument("--number_of_organisms", "--no",  type=int, default=10)
    arg_parser.add_argument("--org_type", type=str, default="pd")
    arg_parser.add_argument("--tournament_size", "--ts",  type=int, default=8)
    arg_parser.add_argument("--verbose", action='store_true', default=False)
    arg_parser.add_argument("--number_of_rounds", "--nr",  type=int, default=64)
    arg_parser.add_argument("--temptation", type=int, default=5)
    arg_parser.add_argument("--reward", type=int, default=3)
    arg_parser.add_argument("--punishment", type=int, default=1)
    arg_parser.add_argument("--sucker", type=int, default=0)
    arg_parser.add_argument("--proportion_cost_per_memory_bit", "--m_c", type=float, default=0.0)
    arg_parser.add_argument("--max_bits_of_memory", "--max_m", type=int, default=4)
    arg_parser.add_argument("--max_bits_of_summary", "--max_s", type=int, default=4)
    arg_parser.add_argument("--mutation_likelihood_of_bits_of_memory", "--ml_mem",  type=float, default=1.0)
    arg_parser.add_argument("--mutation_likelihood_of_initial_memory_state", "--ml_dec", type=float, default=1.0)
    arg_parser.add_argument("--toggle_self_memory_on", action='store_true', default=False)
    arg_parser.add_argument("--mutation_rate", "--mr",  type=float, default=0.00)
    arg_parser.add_argument("--output_frequency", type=int, default=10)
    arg_parser.add_argument("--selection_by_static_competitor", "--static", action="store_true", default=False)
    arg_parser.add_argument("--randomized_rounds", action="store_true", default=False)
    arg_parser.add_argument("--noise", type=float, default=0.0)
    
    args = arg_parser.parse_args(args=command_line_args)    
    return args

def main(command_line_args=None):
    if command_line_args is not None:
        command_line_args = command_line_args.split()
    args = parse_everything(command_line_args)
    generate_data(args)

if __name__ == "__main__":
    main()
