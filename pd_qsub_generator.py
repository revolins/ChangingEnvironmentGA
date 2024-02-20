import sys
import itertools
from subprocess import call
import datetime

array_size = 10
walltime = "03:59:00"
today = "{0:%Y}_{0:%B}_{0:%d}".format(datetime.datetime.now())
num_runs_per_job = 2
output_dir_base = "pdoutput" + today + "selection_by_static_competitor_5_Bits"
pop_costs = [-0.5, 0.0, 0.01, 0.05, 0.075, 0.1, 0.2, 0.3]
#mutation_bits = [0.1, 0.2, 0.3, 0.4, 0.5]
#mutation_initials = [0.1, 0.2, 0.3, 0.4, 0.5]
common = """
#!/bin/bash -login

#PBS -l walltime={1}
#PBS -l nodes=1:ppn=1
#PBS -l mem=1gb
#PBS -N changing_environment_{2}
#PBS -t 1-{0}

module load NumPy
module load SciPy

cd ~/ChangingEnvironmentGA
""".format(array_size, walltime, today)


config_common = """
[DEFAULT]
number_of_generations = 500
number_of_organisms = 500
org_type = pd
verbose = False
tournament_size = 10
number_of_rounds = 64
temptation = 5
reward = 3
punishment = 1
sucker = 0
proportion_cost_per_memory_bit = {0}
max_bits_of_memory = 5
mutation_likelihood_of_bits_of_memory = 0.1
mutation_likelihood_of_initial_memory_state = 0.1
toggle_self_memory_on = True
mutation_rate = 0.3
output_frequency = 10
selection_by_static_competitor = True
"""

def convert_config_file_name_to_job_string(file_name, output_dir_base):
    common_name = "python changing_environment_ga.py -c {0} -o {1}/{0}_arr${{PBS_ARRAYID}}".format(
        file_name, output_dir_base)
    result = [common_name + "_run{0}".format(run_number) for run_number in range(num_runs_per_job)]
    return "\n".join(result)

def write_to_file(filename, contents):
    with open(filename, "w") as file_handle:
        file_handle.write(contents)


def start_runs(jobs, submit_jobs=True, print_jobs=True):
    for job in jobs:
        contents = common + "\n" + job + "\n"
        write_to_file("tmp.sub", contents)
        if print_jobs:
            print("----------Submitting----------")
            print(contents)
        if submit_jobs:
            call(["qsub", 'tmp.sub'])
            call(["rm", 'tmp.sub']) 
    
def create_config_files():
    config_files = []
    #for pop_cost in itertools.product(pop_costs):
    for pop_cost in pop_costs:
        config_filename = "{1}_pd-{0}_gen.ini".format(pop_cost, "selection_by_static_competitor_5_Bits")
        contents = config_common.format(pop_cost)
        write_to_file(config_filename, contents)
        config_files.append(config_filename)
    return config_files

if __name__ == "__main__":
    config_files = create_config_files()
    jobs = [convert_config_file_name_to_job_string(name, output_dir_base) for name in config_files]
    start_runs(jobs, submit_jobs=True, print_jobs=True)
