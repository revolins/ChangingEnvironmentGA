"""
This module takes two PD orgs and determines 
their score in an iterated Prisoner's Dilemma.
"""

import pd_org
import itertools

# Parameters are set through set_global_variables() in main.py

# Individuals play 1 game (64 rounds) against each competitor in a tournament
NUMBER_OF_ROUNDS = 64

TEMPTATION = 5
REWARD = 3
PUNISHMENT = 1
SUCKER = 0

# Impose cost to memory
PROPORTION_COST_PER_MEMORY_BIT = .01

# Memory of previous moves from both the organism and its competitor
TOGGLE_SELF_MEMORY_ON = False

def pd_payout(a_cooperates, b_cooperates):
    """
    Determines reward given by the state of self and other in 1 round
    
    Another way to implement below code:
    if self_is_cooperator:
        if other_is_cooperator:
            return reward
        return sucker
    if other_is_cooperator:
        return temptation
    return punishment
    """
    # a_cooperates and b_cooperates are determined by PDOrg's will_cooperate
    if a_cooperates and b_cooperates:
        return REWARD, REWARD
    elif a_cooperates and not b_cooperates:
        return SUCKER, TEMPTATION
    elif not a_cooperates and b_cooperates:
        return TEMPTATION, SUCKER
    elif not a_cooperates and not b_cooperates:
        return PUNISHMENT, PUNISHMENT
    raise AssertionError("Impossible To Get Here")


def run_game(organism_a, organism_b):
    """
    Runs a game of NUMBER OF ROUNDS long
    Returns total payout for both organisms
    """
    organism_a.initialize_memory()
    organism_b.initialize_memory()
    
    total_payout_a = 0
    total_payout_b = 0
    
    for _ in range(NUMBER_OF_ROUNDS):
        # Decisions from a and b
        a_cooperates = organism_a.will_cooperate()
        b_cooperates = organism_b.will_cooperate()

        # Resulting payout from these decisions
        payout_a, payout_b = pd_payout(a_cooperates, b_cooperates)
        
        # Organisms retain memory of their own moves and those of their opponents.
        if TOGGLE_SELF_MEMORY_ON:
            organism_a.store_bit_of_memory(a_cooperates) # Memory is not in genotype
            organism_a.store_bit_of_memory(b_cooperates)
            organism_b.store_bit_of_memory(b_cooperates)
            organism_b.store_bit_of_memory(a_cooperates)
        # Opponent moves only
        else:
            organism_a.store_bit_of_memory(b_cooperates)
            organism_b.store_bit_of_memory(a_cooperates)

        total_payout_a += payout_a
        total_payout_b += payout_b

    # Stored moves are changed back to initial memory (taken from genotype)
    # Necessary to start new game, because organisms are shuffled
    organism_a.initialize_memory()
    organism_b.initialize_memory()
    
    return total_payout_a, total_payout_b
    
def adjusted_payout(organism_a, organism_b):
    """
    Returns adjusted payout reward (applied cost) for both organisms
    """
    def proportion_cost(org):
        """Total cost of memory; cost * specific memory length"""
        # TODO: we need to add in the summary memory length
        return PROPORTION_COST_PER_MEMORY_BIT * org.genotype.number_of_bits_of_memory
    
    def get_adjusted_payout(payout, proportion_cost):
        """Apply cost to payout; fitness function"""
        return payout * (1 - proportion_cost)
    
    # Total payout for both organisms in a game (64 rounds)
    payout_a, payout_b = run_game(organism_a, organism_b)

    a_proportion_cost = proportion_cost(organism_a)
    b_proportion_cost = proportion_cost(organism_b)
    
    adj_payout_a = get_adjusted_payout(payout_a, a_proportion_cost)
    adj_payout_b = get_adjusted_payout(payout_b, b_proportion_cost)
   
    return adj_payout_a, adj_payout_b
    
def get_average_payouts(organisms):
    """    
    COEVOLUTIONARY MODE
    Calculates the average payouts of all organisms in the list 
    (most likely contenders in a tournament).
    """
    # Total payouts for each organism in the list
    total_payouts = [0.0 for _ in organisms]

    # Generate all possible pairs of organisms
    # Ensures that each pair of organisms interact exactly once
    all_pairs = itertools.combinations(range(len(organisms)), 2)
    for i, j in all_pairs:
        org_a = organisms[i]
        org_b = organisms[j]
        payout_a, payout_b = adjusted_payout(org_a, org_b)
        total_payouts[i] += payout_a
        total_payouts[j] += payout_b

    # Number of opponents each organism competes with, or number of games it participates in
    number_of_games_per_org = len(organisms) - 1
    # Averaging payout for each organism
    average_payouts = [payout / number_of_games_per_org for payout in total_payouts] 
    
    # Update each organism's average_payout attribute
    for i in range(len(organisms)):
        organisms[i].average_payout = average_payouts[i]

def get_static_payouts(organisms, static_competitors):
    """
    STATIC MODE 
    Get average payouts for a list of organisms.
    """
    for org in organisms:
        # Update attribute directly
        org.average_payout = get_static_fitness(org, static_competitors)

def get_static_fitness(org, static_competitors):
    """
    STATIC MODE
    Gets fitness for a single organism against a group of fixed opponents
    """
    # Adjusted payouts for each game between the org and each opponent
    payouts = [adjusted_payout(org, comp)[0] for comp in static_competitors]
    # Return organism's average payout per opponent
    # TODO: Minor but why len(payouts) * 1.0 
    return sum(payouts) / (len(payouts) * 1.0)
