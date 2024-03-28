"""
This module contains methods to evolve IPD strategies. 
"""

#!/usr/bin/python

from __future__ import division
import random
from string import ascii_uppercase
import csv
import OLD.string_org as string_org
import OLD.real_value_vector_org as real_value_vector_org
import scipy.stats as stats
import OLD.old_fitness_function as ff
from math import floor
import os
import shutil
import datetime
import pd_selection
import pd_analysis
import pd_tournament
import pd_org
import pd_make_detail_file

FITNESS_FUNCTION_TYPE = None
NUMBER_OF_ORGANISMS = None
MUTATION_RATE = None
NUMBER_OF_GENERATIONS = None
OUTPUT_FILE = None
ORG_TYPE = None
TOURNAMENT_SIZE = None
VERBOSE = False
ALTERNATE_ENVIRONMENT_CORR = None
START_TIME = None
CROWDING = False # True to activate Crowding Selection
OUTPUT_FREQUENCY = None
SELECTION_BY_STATIC_COMPETITOR = False # True to activate static environment

def create_initial_population():
    """
    Create a starting population by forming a list of randomly generated organisms.
    """
    org_type_map = {"string": string_org.StringOrg, "vector": real_value_vector_org.RealValueVectorOrg, "pd": pd_org.PDOrg}
    if ORG_TYPE in org_type_map:
        return [org_type_map[ORG_TYPE]() for _ in range(NUMBER_OF_ORGANISMS)]
    
def get_mutated_population(population):
    """
    Return a new population with a percentage of organisms mutated based on the mutation rate.
    """
    new_population = []
    for org in population:
        if random.random() < MUTATION_RATE:
            new_org = org.get_mutant()
            new_population.append(new_org)
        else:
            new_population.append(org)
    return new_population

def print_status(generation, population, environment):
    """Outputs information to console. Only used if VERBOSE is true"""
    average_fitness = get_average_fitness(population, environment)
    print("Gen = {}  Pop = {}  Fit = {}".format(generation, population, average_fitness))

def pd_evolve_population():
    """
    Evolution loop for PD org representation
    Returns data for "bits_of_memory_overtime.csv"
    """
    # A dictionary containing all past strategies evolved along the way
    past_organisms = {}

    # Create initial population
    organisms = create_initial_population()

    # Prepare header for output data
    output = []
    headers = []
    for i in range(pd_org.MAX_BITS_OF_MEMORY + 1):
        headers.append("Organisms With " + str(i) + " Bits of Memory")
    output.append(headers)

    # Adding each organism's strategy as keys
    # Each key holds a list of occurrences for the same strategy
    # IDs and parents are not considered due to PD org's __hash__ method;
    # organisms appended to the same list will have same strategy, but not IDs or parents. 
    for org in organisms:
        # If the strategy is encountered multiple times, its occurrence is appended to a list
        if org in past_organisms:
            past_organisms[org].append(org)
        # Otherwise, a new list containing the strategy is created
        else:
            past_organisms[org] = [org]

    # Create detail file for first generation
    # There should be no parent data at this point
    pd_make_detail_file.make_file_detail(organisms, past_organisms, 0, OUTPUT_FOLDER)
    
    for i in range(NUMBER_OF_GENERATIONS):
        # Static Mode       
        if SELECTION_BY_STATIC_COMPETITOR: 
            organisms = pd_selection.get_next_generation_by_static_payout(organisms)
        # Coevolutionary Mode
        else: 
            organisms = pd_selection.get_next_generation_by_selection(organisms)
        # Mutate populataion
        organisms = get_mutated_population(organisms)

        # Calculates, for each generation, the count of organisms with memory lengths 
        # spanning from 0 to MAX_BITS_OF_MEMORY + 1. 
        output.append(pd_analysis.get_tally_of_number_of_bits_of_memory(organisms))

        # Adding more into existing dictionary
        # TODO: Why does this work? Why does the dictionary length remain unchanged? 
            # We're testing with 0.0 mutation rate
            # Will probably change with higher mutation rate
        # You would expect past_organisms to grow over time as newer strategies are discovered.
        for org in organisms:
            if org in past_organisms:
                past_organisms[org].append(org)
            else:
                past_organisms[org] = [org]

        # Make detail file every OUTPUT_FREQUENCY generations
        if ( (i + 1) % OUTPUT_FREQUENCY == 0):
            pd_make_detail_file.make_file_detail(organisms, past_organisms, i + 1, OUTPUT_FOLDER)

    return output

def get_average_fitness(pop, environment):
    """Gets average fitness of a population"""
    total = 0
    for org in pop:
        total += org.fitness(environment)
    return total / len(pop)


def set_global_variables(config):
    """Sets all the global variables based on a config file"""
    # Added to config file from command line
    global OUTPUT_FOLDER
    OUTPUT_FOLDER = config.get("DEFAULT", "output_folder")
    # global CONFIG_FILE
    # CONFIG_FILE = config.get("DEFAULT", "config_file")
    global START_TIME
    START_TIME = config.getfloat("DEFAULT", "start_time")
    global SEED
    SEED = config.getint("DEFAULT", "seed")
    random.seed(SEED)

    # Pre-specified in config file
    global VERBOSE
    VERBOSE = config.getboolean("DEFAULT", "verbose")
    global NUMBER_OF_ORGANISMS
    NUMBER_OF_ORGANISMS = config.getint("DEFAULT", "number_of_organisms")
    global NUMBER_OF_GENERATIONS
    NUMBER_OF_GENERATIONS = config.getint("DEFAULT", "number_of_generations")
    global ORG_TYPE
    ORG_TYPE = config.get("DEFAULT", "org_type")
    global MUTATION_RATE
    MUTATION_RATE = config.getfloat("DEFAULT", "mutation_rate")
    global OUTPUT_FREQUENCY
    OUTPUT_FREQUENCY = config.getint("DEFAULT", "output_frequency")

    if ORG_TYPE == "pd":
        global SELECTION_BY_STATIC_COMPETITOR
        SELECTION_BY_STATIC_COMPETITOR = config.getboolean("DEFAULT", "selection_by_static_competitor")
        pd_tournament.NUMBER_OF_ROUNDS = config.getint("DEFAULT", "number_of_rounds")
        pd_tournament.TEMPTATION = config.getint("DEFAULT", "temptation")
        pd_tournament.REWARD = config.getint("DEFAULT", "reward")
        pd_tournament.PUNISHMENT = config.getint("DEFAULT", "punishment")
        pd_tournament.SUCKER = config.getint("DEFAULT", "sucker")
        pd_tournament.PROPORTION_COST_PER_MEMORY_BIT = config.getfloat("DEFAULT", "proportion_cost_per_memory_bit")
        pd_tournament.TOGGLE_SELF_MEMORY_ON = config.getboolean("DEFAULT", "toggle_self_memory_on")
        pd_selection.TOURNAMENT_SIZE = config.getint("DEFAULT", "tournament_size")
        pd_org.MAX_BITS_OF_MEMORY = config.getint("DEFAULT", "max_bits_of_memory")
        pd_org.MUTATION_LIKELIHOOD_OF_BITS_OF_MEMORY = config.getfloat("DEFAULT", "mutation_likelihood_of_bits_of_memory")
        pd_org.MUTATION_LIKELIHOOD_OF_INITIAL_MEMORY_STATE = config.getfloat("DEFAULT", "mutation_likelihood_of_initial_memory_state")

def save_table_to_file(table, filename):
    """Write a table to a file"""
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerows(table)

def save_string_to_file(string, filename):
    """Write a string to a file"""
    with open(filename, "w") as f:
        f.write(string)

def generate_data():
    """The main function; generates all the data"""
    # Create output folder for storing every component of the experiment
    if os.path.exists(OUTPUT_FOLDER):
        raise IOError("output_folder: {} already exists".format(OUTPUT_FOLDER))
    os.makedirs(OUTPUT_FOLDER)

    #TODO: merge join path with other functions
    def join_path(filename):
        return os.path.join(OUTPUT_FOLDER, filename)

    if ORG_TYPE == "pd":
        output = pd_evolve_population()
        output_filename = join_path("bits_of_memory_overtime.csv")
        save_table_to_file(output, output_filename)
        
    time_filename = join_path("time.dat")     
    start_time = datetime.datetime.fromtimestamp(START_TIME)
    end_time = datetime.datetime.now()
    time_str = "Start_time {}\nEnd_time {}\nDuration {}\n".format(start_time, end_time, end_time - start_time)
    save_string_to_file(time_str, time_filename)
    
