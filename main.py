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

# OBSOLETE
# def get_selected_population(population, environment):
#     """
#     Select a number of organisms based on tournament size, pick the best one, and append it to
#     a new population. Do this until the population is full.
#     """
#     new_population = []
#     for _ in range(NUMBER_OF_ORGANISMS):
#         orgs = [random.choice(population) for _ in range(TOURNAMENT_SIZE)]
#         new_population.append(get_best_organism(orgs, environment))
#     return new_population

# OBSOLETE
# def get_crowded_population(mutated_population, old_population, environment):
#     """
#     Crowding selection to preserve diversity and prevent premature convergence.
#     Compare each organism in the mutated population against another similar organism
#     from the old population and decide which of the two will survive. 
#     Returns a new population.
#     """
#     new_population = []
#     for org in mutated_population:
#         # Tournament-sized sample of random organisms from the old population
#         sample = [random.choice(old_population) for _ in range(TOURNAMENT_SIZE)] 
#         new_population.append(get_best_crowded_organism(org, sample, environment))
#     return new_population

# OBSOLETE
# def get_best_organism(pop, environment):
#     """Gets the best org in a given population"""
#     best_org = pop[0]
#     for org in pop:
#         if org.is_better_than(best_org, environment):
#             best_org = org
#     return best_org

# OBSOLETE
# def get_best_crowded_organism(new_org, sample, environment):
#     """Find the organism most similar to new_org in a given sample, return the better organism"""
#     most_similar = sample[0]
#     min_distance = float("inf")
#     for org in sample:
#         curr_dist = org.distance(new_org, environment)
#         if curr_dist < min_distance:
#             most_similar = org
#             min_distance = curr_dist
#     if new_org.is_better_than(most_similar, environment): 
#         return new_org
#     return most_similar

# OBSOLETE
# def get_next_generation(population, environment):
#     """Get a mutated population, then get a selected population from it"""
#     new_population = get_mutated_population(population)
#     if CROWDING: # Crowding selection
#         new_new_population = get_crowded_population(new_population, population, environment)
#     else: # Tournament selection
#         new_new_population = get_selected_population(new_population, environment)
#     return new_new_population

def print_status(generation, population, environment):
    """Outputs information to console. Only used if VERBOSE is true"""
    average_fitness = get_average_fitness(population, environment)
    print("Gen = {}  Pop = {}  Fit = {}".format(generation, population, average_fitness))

def pd_evolve_population():
    """Evolution loop for PD org representation"""
    past_organisms = {}
    
    organisms = create_initial_population()
    output = []
    headers = []
    for i in range(pd_org.MAX_BITS_OF_MEMORY + 1):
        headers.append("Organisms With " + str(i) + " Bits of Memory")
    output.append(headers)
    for org in organisms:
    #adding into the dictionary
        if org in past_organisms:
            past_organisms[org].append(org)
        else:
            past_organisms[org] = [org]
        
    pd_make_detail_file.make_file_detail(organisms, past_organisms, 0, OUTPUT_FOLDER)
    
    for i in range(NUMBER_OF_GENERATIONS):       
        if SELECTION_BY_STATIC_COMPETITOR: # Static Mode
            organisms = pd_selection.get_next_generation_by_static_payout(organisms)
        else: # Coevolutionary Mode
            organisms = pd_selection.get_next_generation_by_selection(organisms)
        organisms = get_mutated_population(organisms)
        output.append(pd_analysis.get_tally_of_number_of_bits_of_memory(organisms))

        for org in organisms:
        #adding into the dictionary
            if org in past_organisms:
                past_organisms[org].append(org)
            else:
                past_organisms[org] = [org]
        if ( (i + 1) % OUTPUT_FREQUENCY == 0):
            pd_make_detail_file.make_file_detail(organisms, past_organisms, i + 1, OUTPUT_FOLDER)

    return output

# OBSOLETE
# def evolve_population(reference_environment, alternative_environment):
#     """Evolution loop for other types of genome representation"""
#     #Set up the output lists
#     current_fitness_list = [("Generation", "Average_Fitness", 
#                     "Standard_Deviation")]
#     current_fitness_best = [("Generation", "Best_Fitness", "Best_Org")]

#     reference_fitness_list = [("Generation", "Ref_Average_Fitness", 
#                     "Ref_Standard_Deviation")]
#     reference_fitness_best = [("Generation", "Ref_Best_Fitness", "Ref_Best_Org")]

#     #Set up the other variables
#     current_environment = reference_environment
#     start_of_trimester_2 = int(floor(NUMBER_OF_GENERATIONS/3.0))
#     start_of_trimester_3 = int(floor(NUMBER_OF_GENERATIONS*2.0/3.0))

#     population = create_initial_population()
#     #In each generation...
#     for gen in range(NUMBER_OF_GENERATIONS):
#         #Check if the environment needs changed
#         if gen == start_of_trimester_2:
#             current_environment = alternative_environment
#         elif gen == start_of_trimester_3:
#             current_environment = reference_environment
#         #Get the next generation
#         population = get_next_generation(population, current_environment)

#         #Append the stats to the output lists
#         average_fitness, stdev, best_org, best_fitness = get_generation_stats(
#             population, current_environment)
#         current_fitness_list.append((gen, average_fitness, stdev))
#         current_fitness_best.append((gen, best_fitness, best_org))
        
#         average_fitness, stdev, best_org, best_fitness = get_generation_stats(
#             population, reference_environment)
#         reference_fitness_list.append((gen, average_fitness, stdev))
#         reference_fitness_best.append((gen, best_fitness, best_org))

#         if VERBOSE:
#             print_status(gen, population, current_environment)
    
#     #Return the output lists
#     result =  (current_fitness_list, current_fitness_best, 
#                reference_fitness_list, reference_fitness_best)
#     return result

def get_generation_stats(population, environment):
    """Gets the stats for the given population"""
    average_fitness = get_average_fitness(population, environment)
    best_org = get_best_organism(population, environment)
    best_fitness = best_org.fitness(environment)
    stdev = stats.tstd([org.fitness(environment) 
                        for org in population])
    return average_fitness, stdev, best_org, best_fitness
    

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
    global CONFIG_FILE
    CONFIG_FILE = config.get("DEFAULT", "config_file")
    global START_TIME
    START_TIME = config.getfloat("DEFAULT", "start_time")

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

    # if ORG_TYPE != "pd": # OBSOLETE
    #     global TOURNAMENT_SIZE
    #     TOURNAMENT_SIZE = config.getint("DEFAULT", "tournament_size")    
    # if ORG_TYPE == "string": # OBSOLETE
    #     string_org.TARGET_STRING = config.get("DEFAULT", "target_string")
    #     string_org.LETTERS = config.get("DEFAULT", "letters")
    # elif ORG_TYPE == "vector": # OBSOLETE
    #     fitness_function_type_str = config.get("DEFAULT", "fitness_function_type")
    #     global FITNESS_FUNCTION_TYPE
    #     if fitness_function_type_str == "flat":
    #         FITNESS_FUNCTION_TYPE = ff.flat_function
    #     elif fitness_function_type_str == "sphere":
    #         FITNESS_FUNCTION_TYPE = ff.sphere_function
    #     elif fitness_function_type_str == "rosenbrock":
    #         FITNESS_FUNCTION_TYPE = ff.rosenbrock_function
    #     elif fitness_function_type_str == "rana":
    #         FITNESS_FUNCTION_TYPE = ff.rana_function
    #     elif fitness_function_type_str == "deceptive":
    #         FITNESS_FUNCTION_TYPE = ff.deceptive
    #     elif fitness_function_type_str == "schafferf7":
    #         FITNESS_FUNCTION_TYPE = ff.schafferF7
    #     else:
    #         raise AssertionError("Unknown (but needed) function type (i.e. sphere)")
    #     real_value_vector_org.LENGTH = config.getint("DEFAULT", "length")
    #     range_minimum = config.getfloat("DEFAULT", "range_minimum")
    #     real_value_vector_org.RANGE_MIN = range_minimum
    #     range_maximum = config.getfloat("DEFAULT", "range_maximum")
    #     real_value_vector_org.RANGE_MAX = range_maximum
    #     mut_effect_size = config.getfloat("DEFAULT", "mutation_effect_size")
    #     ff.MUTATION_EFFECT_SIZE = mut_effect_size
    #     real_value_vector_org.MUTATION_EFFECT_SIZE = mut_effect_size
    #     global ALTERNATE_ENVIRONMENT_CORR
    #     ALTERNATE_ENVIRONMENT_CORR = config.getfloat(
    #         "DEFAULT", "alternate_environment_corr")
    #     global CROWDING
    #     CROWDING = eval(config.get("DEFAULT", "crowding"))

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
    # Create output folder, place copy of config file inside
    if os.path.exists(OUTPUT_FOLDER):
        raise IOError("output_folder: {} already exists".format(OUTPUT_FOLDER))
    os.makedirs(OUTPUT_FOLDER)
    config_filename = os.path.basename(CONFIG_FILE)

    def join_path(filename):
        return os.path.join(OUTPUT_FOLDER, filename)

    config_dest = os.path.join(OUTPUT_FOLDER, config_filename)
    shutil.copyfile(CONFIG_FILE, config_dest)

    # if ORG_TYPE == "vector": # OBSOLETE
    #     fitness_function = ff.Fitness_Function(FITNESS_FUNCTION_TYPE, real_value_vector_org.LENGTH)
    #     fitness_function.create_fitness2(ALTERNATE_ENVIRONMENT_CORR)
    #     reference_environment = fitness_function.fitness1_fitness
    #     alternative_environment = fitness_function.fitness2_fitness
    # elif ORG_TYPE == "string": # OBSOLETE
    #     reference_environment = string_org.default_environment
    #     alternative_environment = string_org.hash_environment
    # if ORG_TYPE != "pd": # OBSOLETE
    #     experienced_fits, experienced_bests, reference_fits, reference_bests = evolve_population(
    #     reference_environment, alternative_environment)

    if ORG_TYPE == "pd":
        output = pd_evolve_population()
        output_filename = join_path("bits_of_memory_overtime.csv")
        save_table_to_file(output, output_filename)

    # What's going on here??
    # else:
    #     experienced_filename = join_path("experienced_fitnesses.csv")
    #     reference_filename = join_path("reference_fitnesses.csv")
    #     experienced_best_filename = join_path("experienced_best_fitnesses.csv")
    #     reference_best_filename = join_path("reference_best_fitnesses.csv")
    #     corr_filename = join_path("correlation.dat")
   

    #     save_table_to_file(experienced_fits, experienced_filename)
    #     save_table_to_file(experienced_bests, experienced_best_filename)
    #     save_table_to_file(reference_fits, reference_filename)
    #     save_table_to_file(reference_bests, reference_best_filename)
    #     if ORG_TYPE == "vector":
    #         save_string_to_file(str(fitness_function.correlation()), corr_filename)
        
    time_filename = join_path("time.dat")     
    start_time = datetime.datetime.fromtimestamp(START_TIME)
    end_time = datetime.datetime.now()
    time_str = "Start_time {}\nEnd_time {}\nDuration {}\n".format(start_time, end_time, end_time - start_time)
    save_string_to_file(time_str, time_filename)
    
