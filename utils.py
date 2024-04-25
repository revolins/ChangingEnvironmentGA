"""
This module contains methods to evolve IPD strategies. 
"""

#!/usr/bin/python

from __future__ import division
import random
import csv
import os
import numpy as np
import datetime
import pd_selection
import pd_analysis
import pd_tournament
import pd_org
import hybrid_pd_org
import pd_make_detail_file
import compile_csv

FITNESS_FUNCTION_TYPE = None
NUMBER_OF_ORGANISMS = None
MUTATION_RATE = None
NUMBER_OF_GENERATIONS = None
ORG_TYPE = None
TOURNAMENT_SIZE = None
VERBOSE = False
ALTERNATE_ENVIRONMENT_CORR = None
START_TIME = None
CROWDING = False # True to activate Crowding Selection
OUTPUT_FOLDER = None
OUTPUT_FREQUENCY = None
SELECTION_BY_STATIC_COMPETITOR = False # True to activate static environment
RANDOMIZED_ROUNDS = False
#PROB_ORG = False

def create_initial_population():
    """
    Create a starting population by forming a list of randomly generated organisms.
    """
    org_type_map = {"pd": pd_org.PDOrg, "hybrid_pd": hybrid_pd_org.HybridPDOrg}#,\
                     #"friend_pd": hybrid_pd_org.HybridPDOrg(genotype='coop'), "hostile_pd": hybrid_pd_org.HybridPDOrg(genotype='hostile')}
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
    mem_output = []
    sum_output = []
    declen_output = []
    mem_headers = []
    sum_headers = []
    dec_headers = []
    for i in range(pd_org.MAX_BITS_OF_MEMORY + 1):
        mem_headers.append("Organisms With " + str(i) + " Bits of Memory")
        sum_headers.append("Organisms With " + str(i) + " Bits of Summary")
    for i in range(NUMBER_OF_ORGANISMS):
        dec_headers.append(f"Organism #{i}")
    mem_output.append(mem_headers)
    sum_output.append(sum_headers)
    declen_output.append(dec_headers)

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
        mem_output.append(pd_analysis.get_tally_of_number_of_bits_of_memory(organisms))
        if organisms[-1].genotype.type() == 'hybrid':
            sum_output.append(pd_analysis.get_tally_of_number_of_bits_summary(organisms))
        declen_output.append([len(org.genotype.decision_list) for org in organisms])

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

    return mem_output, sum_output, declen_output

def get_average_fitness(pop, environment):
    """Gets average fitness of a population"""
    total = 0
    for org in pop:
        total += org.fitness(environment)
    return total / len(pop)


def set_global_variables(config):
    """Sets all the global variables based on a config file"""
    # Added to config from command line
    global OUTPUT_FOLDER
    OUTPUT_FOLDER = config.get("DEFAULT", "output_folder")
    global START_TIME
    START_TIME = config.getfloat("DEFAULT", "start_time")

    # Default Values
    global SEED
    SEED = config.getint("DEFAULT", "seed")
    random.seed(SEED)
    np.random.seed(SEED)
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
    # global PROB_ORG
    # PROB_ORG = config.getboolean("DEFAULT", "prob_org")

    if ORG_TYPE == "pd" or ORG_TYPE == "hybrid_pd":
        pd_org.MAX_BITS_OF_MEMORY = config.getint("DEFAULT", "max_bits_of_memory")
        pd_org.MUTATION_LIKELIHOOD_OF_BITS_OF_MEMORY = config.getfloat("DEFAULT", "mutation_likelihood_of_bits_of_memory")
        pd_org.MUTATION_LIKELIHOOD_OF_INITIAL_MEMORY_STATE = config.getfloat("DEFAULT", "mutation_likelihood_of_initial_memory_state")
        hybrid_pd_org.MAX_BITS_OF_MEMORY = config.getint("DEFAULT", "max_bits_of_memory")
        hybrid_pd_org.MUTATION_LIKELIHOOD_OF_BITS_OF_MEMORY = config.getfloat("DEFAULT", "mutation_likelihood_of_bits_of_memory")
        hybrid_pd_org.MUTATION_LIKELIHOOD_OF_INITIAL_MEMORY_STATE = config.getfloat("DEFAULT", "mutation_likelihood_of_initial_memory_state")
        global SELECTION_BY_STATIC_COMPETITOR
        SELECTION_BY_STATIC_COMPETITOR = config.getboolean("DEFAULT", "selection_by_static_competitor")
        pd_tournament.NUMBER_OF_ROUNDS = config.getint("DEFAULT", "number_of_rounds")
        pd_tournament.RANDOMIZED_ROUNDS = config.getboolean("DEFAULT", "randomized_rounds")
        pd_tournament.SEED = config.getint("DEFAULT", "seed")
        pd_tournament.NOISE = config.getfloat("DEFAULT", "noise")
        pd_tournament.TEMPTATION = config.getint("DEFAULT", "temptation")
        pd_tournament.REWARD = config.getint("DEFAULT", "reward")
        pd_tournament.PUNISHMENT = config.getint("DEFAULT", "punishment")
        pd_tournament.SUCKER = config.getint("DEFAULT", "sucker")
        pd_tournament.PROPORTION_COST_PER_MEMORY_BIT = config.getfloat("DEFAULT", "proportion_cost_per_memory_bit")
        pd_tournament.TOGGLE_SELF_MEMORY_ON = config.getboolean("DEFAULT", "toggle_self_memory_on")
        #pd_tournament.PROB_ORG = config.getboolean("DEFAULT", "prob_org")
        pd_selection.TOURNAMENT_SIZE = config.getint("DEFAULT", "tournament_size")

def save_table_to_file(table, filename):
    """Write a table to a file"""
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerows(table)

def save_string_to_file(string, filename):
    """Write a string to a file"""
    with open(filename, "w") as f:
        f.write(string)

def join_path(filename):
        return os.path.join(OUTPUT_FOLDER, filename)

def generate_data():
    """The main function; generates all the data"""
    # Create output folder for storing every component of the experiment
    if os.path.exists(OUTPUT_FOLDER):
        raise IOError("output_folder: {} already exists".format(OUTPUT_FOLDER))
    os.makedirs(OUTPUT_FOLDER)
    
    if ORG_TYPE == "pd" or ORG_TYPE == "hybrid_pd":
        mem_output, sum_output, declen_output = pd_evolve_population()
        save_table_to_file(mem_output, join_path("bits_of_memory_overtime.csv"))
        save_table_to_file(declen_output, join_path("decision_list_length_aggregate.csv"))
    if ORG_TYPE == "hybrid_pd":
        save_table_to_file(sum_output, join_path("bits_of_summary_overtime.csv"))
        
    time_filename = join_path("time.dat")     
    start_time = datetime.datetime.fromtimestamp(START_TIME)
    end_time = datetime.datetime.now()
    time_str = "Start_time {}\nEnd_time {}\nDuration {}\n".format(start_time, end_time, end_time - start_time)
    save_string_to_file(time_str, time_filename)
