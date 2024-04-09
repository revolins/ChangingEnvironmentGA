import configparser
import argparse
from utils import set_global_variables, generate_data
import time 
import random

def parse_everything(command_line_args=None):
    """Parse command line arguments"""
    arg_parser = argparse.ArgumentParser(
        description='The changing environments program.')
    
    # Expects 1 argument: output folder
    arg_parser.add_argument("-o", "--output_folder", nargs=1)
    arg_parser.add_argument("--seed", "--s", type=str, default=str(random.randint(0, int(time.time()))))
    arg_parser.add_argument("--number_of_generations", "--ng",  type=str, default="500")
    arg_parser.add_argument("--number_of_organisms", "--no",  type=str, default="10")
    arg_parser.add_argument("--org_type", type=str, default="pd")
    arg_parser.add_argument("--tournament_size", "--ts",  type=str, default="8")
    arg_parser.add_argument("--verbose", action='store_true', default=False)
    arg_parser.add_argument("--number_of_rounds", "--nr",  type=str, default="64")
    arg_parser.add_argument("--temptation", type=str, default="5")
    arg_parser.add_argument("--reward", type=str, default="3")
    arg_parser.add_argument("--punishment", type=str, default="1")
    arg_parser.add_argument("--sucker", type=str, default="0")
    arg_parser.add_argument("--proportion_cost_per_memory_bit", "--m_c", type=str, default="0.0")
    arg_parser.add_argument("--max_bits_of_memory", "--max_m", type=str, default="4")
    arg_parser.add_argument("--max_bits_of_summary", "--max_s", type=str, default="4")
    arg_parser.add_argument("--mutation_likelihood_of_bits_of_memory", "--ml_mem",  type=str, default="0.1")
    arg_parser.add_argument("--mutation_likelihood_of_initial_memory_state", "--ml_dec", type=str, default="0.1")
    arg_parser.add_argument("--toggle_self_memory_on", action='store_true', default=False)
    arg_parser.add_argument("--mutation_rate", "--mr",  type=str, default="0.00")
    arg_parser.add_argument("--output_frequency", type=str, default="10")
    arg_parser.add_argument("--selection_by_static_competitor", "--static", action="store_true", default=False)
    arg_parser.add_argument("--randomized_rounds", action="store_true", default=False)
    arg_parser.add_argument("--noise", type=str, default="0.0")
    
    args = arg_parser.parse_args(args=command_line_args)    

    output_folder = args.output_folder[0]
    verbose = str(args.verbose)
    toggle_self_memory_on = str(args.toggle_self_memory_on)
    selection_by_static_competitor = str(args.selection_by_static_competitor)
    randomized_rounds = str(args.randomized_rounds)

    # Set configuration based on argument setting
    config = configparser.ConfigParser() 
    # Set paths to config file and output folder as additional settings 
    config.set("DEFAULT", "output_folder", output_folder)
    config.set("DEFAULT", "seed", args.seed)
    config.set("DEFAULT", "number_of_generations", args.number_of_generations)
    config.set("DEFAULT", "number_of_organisms", args.number_of_organisms)
    config.set("DEFAULT", "org_type", args.org_type)
    config.set("DEFAULT", "tournament_size", args.tournament_size)
    config.set("DEFAULT", "verbose", verbose)
    config.set("DEFAULT", "number_of_rounds", args.number_of_rounds)
    config.set("DEFAULT", "temptation", args.temptation)
    config.set("DEFAULT", "reward", args.reward)
    config.set("DEFAULT", "punishment", args.punishment)
    config.set("DEFAULT", "sucker", args.sucker)
    config.set("DEFAULT", "proportion_cost_per_memory_bit", args.proportion_cost_per_memory_bit)
    config.set("DEFAULT", "max_bits_of_memory", args.max_bits_of_memory)
    config.set("DEFAULT", "max_bits_of_summary", args.max_bits_of_summary)
    config.set("DEFAULT", "mutation_likelihood_of_bits_of_memory", args.mutation_likelihood_of_bits_of_memory)
    config.set("DEFAULT", "mutation_likelihood_of_initial_memory_state", args.mutation_likelihood_of_initial_memory_state)
    config.set("DEFAULT", "toggle_self_memory_on", toggle_self_memory_on)
    config.set("DEFAULT", "mutation_rate", args.mutation_rate)
    config.set("DEFAULT", "output_frequency", args.output_frequency)
    config.set("DEFAULT", "selection_by_static_competitor", selection_by_static_competitor)
    config.set("DEFAULT", "randomized_rounds", randomized_rounds)
    config.set("DEFAULT", "noise", args.noise)
    
    config.set("DEFAULT", "start_time", str(time.time()))
    return config

def main(command_line_args=None):
    if command_line_args is not None:
        command_line_args = command_line_args.split()
    config = parse_everything(command_line_args)
    set_global_variables(config)
    generate_data()

if __name__ == "__main__":
    main()
