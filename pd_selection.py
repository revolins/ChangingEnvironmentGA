import pd_tournament
import random

TOURNAMENT_SIZE = None

def get_best_half(organisms):
    """
    This will run a tournament with the given organisms and
    return a list of the top half of the organisms in terms of payout
    """
    sorted_orgs = sorted(organisms, key=lambda org: org.average_payout, reverse=True)
    best_half_orgs = sorted_orgs[:len(organisms) // 2]
    return best_half_orgs[:]

def get_number_of_tournaments(organisms):
    number_of_tournaments = len(organisms) // TOURNAMENT_SIZE
    if not len(organisms) % TOURNAMENT_SIZE:
        number_of_tournaments += 1
    return number_of_tournaments


def get_contender_generator(organisms, number_of_tournaments):
        
    def generate_contenders(organisms):
        while True:
            random.shuffle(organisms)
            for i in range(number_of_tournaments):
                yield organisms[TOURNAMENT_SIZE * i: TOURNAMENT_SIZE * (i + 1)]         
    return generate_contenders(organisms)
    
def get_next_generation_by_selection(organisms):
    """
    Get next generation by selection is a function that takes a list of organisms
    Shuffle the organisms and group them into TOURNAMENT_SIZEd clumps
    For a given tournament size, it runs a tournament
    selects the best half
    Adds them to a population that becomes the next generation
    If more tournaments more need to be run after all the clumps are used, we shuffle the
    population and make more clumps
    It repeats more tournaments until the next generation reaches the population size
    """
    number_of_tournaments = get_number_of_tournaments(organisms)
    contender_generator = get_contender_generator(organisms, number_of_tournaments)
    
    #pick organisms for tournament
    #gets organisms average payout

    for _ in range(number_of_tournaments):
        contenders = next(contender_generator)
        pd_tournament.get_average_payouts(contenders)
    
    return  _get_next_generation(organisms, contender_generator)


def _get_next_generation(organisms, contender_generator):

    next_generation = []
   
    while len(next_generation) < len(organisms):
        #pick organisms for the tournament
        contenders = next(contender_generator)
        #gets winners of contenders
        winners = get_best_half(contenders)
        #add winners to the next generation
        next_generation += winners
    #make next_generation same length as organisms
    return next_generation[:len(organisms)]
    
