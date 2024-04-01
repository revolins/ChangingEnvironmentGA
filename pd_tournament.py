"""
This module takes two PD orgs and determines 
their score in an iterated Prisoner's Dilemma
"""

import itertools
import numpy as np
import random

def pd_payout(args, a_cooperates, b_cooperates):
    """
    Function my_reward determines reward given by the state of self and other
        
    Another way to implement below code:
    if self_is_cooperator:
        if other_is_cooperator:
            return reward
        return sucker
    if other_is_cooperator:
        return temptation
    return punishment
    """
            
    if a_cooperates and b_cooperates:
        return args.reward, args.reward
    elif a_cooperates and not b_cooperates:
        return args.sucker, args.temptation
    elif not a_cooperates and b_cooperates:
        return args.temptation, args.sucker
    elif not a_cooperates and not b_cooperates:
        return args.punishment, args.punishment
    raise AssertionError("Impossible To Reach End of PD Payout")


def run_game(args, organism_a, organism_b):
    """
    Run a game of NUMBER OF ROUNDS long
    Return payout for both organisms
    """
    organism_a.initialize_memory()
    organism_b.initialize_memory()
    
    total_payout_a = 0
    total_payout_b = 0
    if args.randomized_rounds:
        # Size 500 to match NUMBER_OF_GENERATIONS, scale=3 for full scope of std. dev., mean set to NUMBER_OF_ROUNDS
        curr_num_rounds = np.random.choice(list(np.random.default_rng(seed=args.seed).normal(loc=args.number_of_rounds, scale=3, size=args.number_of_generations).astype(int)))
        if curr_num_rounds <= 0:
            raise AssertionError(f"Number of Randomized Rounds - {curr_num_rounds} is too low, scale or loc requires adjustment")
    else:
        curr_num_rounds = args.number_of_rounds
    
    for _ in range(curr_num_rounds):
        a_cooperates = organism_a.will_cooperate()
        b_cooperates = organism_b.will_cooperate()

        if random.random() < args.noise:
            noisy_decision = np.random.choice([0, 1])

            if noisy_decision == 0: a_cooperates = not a_cooperates
            else: b_cooperates = not b_cooperates

        payout_a, payout_b = pd_payout(args, a_cooperates, b_cooperates)
        
        if args.toggle_self_memory_on:
            organism_a.store_bit_of_memory(a_cooperates)
            organism_a.store_bit_of_memory(b_cooperates)
            organism_b.store_bit_of_memory(b_cooperates)
            organism_b.store_bit_of_memory(a_cooperates)
        else:
            organism_a.store_bit_of_memory(b_cooperates)
            organism_b.store_bit_of_memory(a_cooperates)

        total_payout_a += payout_a
        total_payout_b += payout_b
    
    organism_a.initialize_memory()
    organism_b.initialize_memory()
    
    return total_payout_a, total_payout_b
    
def adjusted_payout(args, organism_a, organism_b):
    """
    Returns adjusted payout reward for each organism
    """
    def proportion_cost(args, org):
        if args.org_type == "hybrid_pd":
            return args.proportion_cost_per_memory_bit * (org.genotype.number_of_bits_of_memory + org.genotype.number_of_bits_summary)
        else:
            return args.proportion_cost_per_memory_bit * org.genotype.number_of_bits_of_memory
    
    def get_adjusted_payout(payout, proportion_cost):
        return payout * (1 - proportion_cost)
        
    payout_a, payout_b = run_game(args, organism_a, organism_b)

    a_proportion_cost = proportion_cost(args, organism_a)
    b_proportion_cost = proportion_cost(args, organism_b)
    
    adj_payout_a = get_adjusted_payout(payout_a, a_proportion_cost)
    adj_payout_b = get_adjusted_payout(payout_b, b_proportion_cost)
   
    return adj_payout_a, adj_payout_b
    
def get_average_payouts(args, organisms):
    """    
    Lists all possible pairs of organisms, calls adj_payout
    Averages all together
    Updates organisms.average_payout for every org in organisms list
    """
    total_payouts = [0.0 for _ in organisms]
    all_pairs = itertools.combinations(range(len(organisms)), 2)
    for i, j in all_pairs:
        org_a = organisms[i]
        org_b = organisms[j]
        payout_a, payout_b = adjusted_payout(args, org_a, org_b)
        total_payouts[i] += payout_a
        total_payouts[j] += payout_b
            
    number_of_games_per_org = len(organisms) - 1
    average_payouts = [payout / number_of_games_per_org for payout in total_payouts] 
    
    for i in range(len(organisms)):
        organisms[i].average_payout = average_payouts[i]

def get_static_payouts(args, organisms, static_competitors):
    """
    Get average payouts for orgs in static competitions
    """

    for org in organisms:
        org.average_payout = get_static_fitness(args, org, static_competitors)

def get_static_fitness(args, org, static_competitors):
    """
    Gets fitness for orgs in static competitions
    """
    
    payouts = [adjusted_payout(args, org, comp)[0] for comp in static_competitors]

    return sum(payouts) / float(len(payouts))