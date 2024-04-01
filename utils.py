"""
This module contains methods to evolve IPD strategies. 
"""

#!/usr/bin/python

from __future__ import division
import random
import csv
import os
import datetime
import pd_selection
import pd_analysis
import pd_org
import pd_make_detail_file

def create_initial_population(args):
    """
    Create a starting population by forming a list of randomly generated organisms.
    """
    org_type_map = {"pd": pd_org.PDOrg(args=args), "hybrid_pd": pd_org.PDOrg(args=args)} 
    if args.org_type in org_type_map:
        return [org_type_map[args.org_type] for _ in range(args.number_of_organisms)]
    
def get_mutated_population(args, population):
    """
    Return a new population with a percentage of organisms mutated based on the mutation rate.
    """
    new_population = []
    for org in population:
        if random.random() < args.mutation_rate:
            new_org = org.get_mutant(args)
            new_population.append(new_org)
        else:
            new_population.append(org)
    return new_population

def print_status(generation, population, environment):
    """Outputs information to console. Only used if VERBOSE is true"""
    average_fitness = get_average_fitness(population, environment)
    print("Gen = {}  Pop = {}  Fit = {}".format(generation, population, average_fitness))

def pd_evolve_population(args):
    """
    Evolution loop for PD org representation
    Returns data for "bits_of_memory_overtime.csv"
    """
    # A dictionary containing all past strategies evolved along the way
    past_organisms = {}

    # Create initial population
    organisms = create_initial_population(args)

    # Prepare header for output data
    output = []
    headers = []
    for i in range(args.max_bits_of_memory + 1):
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
    pd_make_detail_file.make_file_detail(organisms, past_organisms, 0, args.output_folder[0])
    
    for i in range(args.number_of_generations):
        # Static Mode       
        if args.selection_by_static_competitor: 
            organisms = pd_selection.get_next_generation_by_static_payout(args, organisms)
        # Coevolutionary Mode
        else: 
            organisms = pd_selection.get_next_generation_by_selection(args, organisms)
        # Mutate populataion
        organisms = get_mutated_population(args, organisms)

        # Calculates, for each generation, the count of organisms with memory lengths 
        # spanning from 0 to MAX_BITS_OF_MEMORY + 1. 
        output.append(pd_analysis.get_tally_of_number_of_bits_of_memory(args, organisms))

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
        if ( (i + 1) % args.output_frequency == 0):
            pd_make_detail_file.make_file_detail(organisms, past_organisms, i + 1, args.output_folder[0])

    return output

def get_average_fitness(pop, environment):
    """Gets average fitness of a population"""
    total = 0
    for org in pop:
        total += org.fitness(environment)
    return total / len(pop)

def save_table_to_file(table, filename):
    """Write a table to a file"""
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerows(table)

def save_string_to_file(string, filename):
    """Write a string to a file"""
    with open(filename, "w") as f:
        f.write(string)

def join_path(args, filename):
        return os.path.join(args.output_folder[0], filename)

def generate_data(args):
    """The main function; generates all the data"""
    # Create output folder for storing every component of the experiment
    if os.path.exists(args.output_folder[0]):
        raise IOError("output_folder: {} already exists".format(args.output_folder[0]))
    os.makedirs(args.output_folder[0])
    
    if args.org_type == "pd" or args.org_type == "hybrid_pd":
        output = pd_evolve_population(args)
        output_filename = join_path(args, "bits_of_memory_overtime.csv")
        save_table_to_file(output, output_filename)
