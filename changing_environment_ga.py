import configparser
import argparse
from main import set_global_variables, generate_data
from string import ascii_uppercase
import time 

def parse_everything(command_line_args=None):
    """Parse command line arguments"""
    conf_parser = argparse.ArgumentParser(
        description='The changing environments program.')
    
    # Expects 2 arguments: config file & output folder
    # s or 'seed' (int, OPTIONAL)
    conf_parser.add_argument("-c", "--config_file", nargs=1)
    conf_parser.add_argument("-o", "--output_folder", nargs=1)
    conf_parser.add_argument("--seed", type=str, default=str(time.time()))
    
    args = conf_parser.parse_args(args=command_line_args)    

    output_folder = args.output_folder[0]
    config_file = args.config_file[0]

    # Read contents of config file
    config = configparser.ConfigParser()
    config.read([config_file]) 
    # Set paths to config file and output folder as additional settings
    config.set("DEFAULT", "config_file", config_file) 
    config.set("DEFAULT", "output_folder", output_folder)
    config.set("DEFAULT", "seed", args.seed)
    
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
