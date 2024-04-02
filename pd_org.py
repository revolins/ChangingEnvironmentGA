"""
This module defines the genome representation or memory model of the original PD organisms in the population.
Two types of representations are available: MemoryPDGenotype and HybridPDGenotype.
"""

import random
from collections import deque

# Parameters are set through set_global_variables() in utils.py 
MAX_BITS_OF_MEMORY = None
MUTATION_LIKELIHOOD_OF_BITS_OF_MEMORY = None
MUTATION_LIKELIHOOD_OF_INITIAL_MEMORY_STATE = None

class StochasticPDGenotype(object):
    """Genotype for static COIN FLIP/random type opponents in static environment"""
    def __init__(self, probability=.5, number_of_bits_of_memory=0):
        self.probability = probability
        self.number_of_bits_of_memory = number_of_bits_of_memory

    def __type__(self):
        return 'stochastic'

class MemoryPDGenotype(object):
    """
    Original Memory Model Genotype for inheriting in the PDOrg Class
    """

    def __init__(self, number_of_bits_of_memory, decision_list, initial_memory):
        assert 0 <= number_of_bits_of_memory <= MAX_BITS_OF_MEMORY
        assert len(decision_list) == 2 ** number_of_bits_of_memory
        assert len(initial_memory) == number_of_bits_of_memory
        self.number_of_bits_of_memory = number_of_bits_of_memory
        self.decision_list = decision_list
        self.initial_memory = initial_memory
    
    
    def __eq__(self, other):
        """Overload equality operator"""
        return (self.number_of_bits_of_memory == other.number_of_bits_of_memory and
                self.decision_list == other.decision_list and
                self.initial_memory == other.initial_memory)
    
    def __ne__(self, other):
        """Overload not equal operator"""
        return not self == other
    
    def __str__(self):
        """String representation"""
        return "MemoryPDGenotype({}, {}, {})".format(self.number_of_bits_of_memory,
                                                     self.decision_list,
                                                     self.initial_memory)
    
    def __repr__(self):
        """In this case, same as __str__"""
        return str(self)
        
    def __hash__(self):
        """Overload hash operator, necessary for dictionaries and such"""
        hashable_tuple = (self.number_of_bits_of_memory, 
            tuple(self.decision_list), 
            tuple(self.initial_memory))
        return hash(hashable_tuple)
    
    def __type__(self):
        """Return type as string for easy checking"""
        return 'memory'

    def get_mutant_of_self(self):
        """
        Determines when and how each type of mutation occurs.
        Returns new (mutated) genotype.
        """
        
        # Size mutation
        random_value = random.random()
        if random_value < MUTATION_LIKELIHOOD_OF_BITS_OF_MEMORY:
            return self._get_bits_of_memory_mutant()
        # Initial (specific) memory mutation
        if random_value < MUTATION_LIKELIHOOD_OF_BITS_OF_MEMORY + MUTATION_LIKELIHOOD_OF_INITIAL_MEMORY_STATE:
            return self._initial_memory_mutant()
        # Decision mutation
        return self._decision_list_mutant()


    def _get_bits_of_memory_mutant(self):
        """
        Increase or decrease length of initial (specific) and summary memory by 1 bit each.
        Affects length of decision list as well. 
        """
        should_increase_memory = random.choice([True, False])

         # If organism has no memory, don't decrease memory
        if self.number_of_bits_of_memory == 0 and not should_increase_memory:
            return self
        
        # If organism has maximum memory length, don't increase memory
        if self.number_of_bits_of_memory == MAX_BITS_OF_MEMORY and should_increase_memory:
            #Return full normal memory but hybrid relies on 2*k * (j+1)
            return self
        
        # If we increase memory length
        if should_increase_memory:
            new_number_of_bits_of_memory = self.number_of_bits_of_memory + 1 # (k)

            # Double list, duplicate decisions
            # Retain as much of the original pattern as possible, not sure if matters
            # Also try to mimic original mutation method as closely as possible
            new_decision_list = self.decision_list * 2

            # Add 1 extra bit to initial memory
            new_initial_memory = self.initial_memory[:]
            new_initial_memory.append(random.choice([True,False]))

            return MemoryPDGenotype(new_number_of_bits_of_memory, new_decision_list, new_initial_memory)
        
        # If we decrease memory length
        new_number_of_bits_of_memory = self.number_of_bits_of_memory - 1
        length_of_new_decision_list = len(self.decision_list) // 2

        # Update size of memory and decision lists, most distant past memory bits removed
        new_decision_list = self.decision_list[:length_of_new_decision_list]
        new_initial_memory = self.initial_memory[:-1]
        return MemoryPDGenotype(new_number_of_bits_of_memory, new_decision_list, new_initial_memory) 
        
    def _decision_list_mutant(self):
        """Randomly flip a single bit in decision list"""
        mutation_location = random.randrange(len(self.decision_list))
        new_decision_list = self.decision_list[:]
        new_decision_list[mutation_location] = not new_decision_list[mutation_location]
        return MemoryPDGenotype(self.number_of_bits_of_memory, new_decision_list, self.initial_memory)
        
    def _initial_memory_mutant(self):
        """
        Randomly flip a single bit in both initial specified and summary memory.
        This affects the state of memory the organism starts with.  
        """
        # If there is no memory, no change is made.
        if self.number_of_bits_of_memory == 0:
            return self
        
        # Mutate in specified memory
        mutation_location = random.randrange(len(self.initial_memory))
        new_initial_memory = self.initial_memory[:]
        new_initial_memory[mutation_location] = not new_initial_memory[mutation_location]
        return MemoryPDGenotype(self.number_of_bits_of_memory, self.decision_list, new_initial_memory)

class PDOrg(object):
    """
    This class creates a PD organism.
    A PD organism consists of a genotype, ID, parent, and average payout.
    """
    
    next_org_id = 0
    
    def __init__(self, genotype=None, parent=None):
        if genotype is None:
            genotype = _create_random_genotype()
        self.genotype = genotype
        self.initialize_memory()
        self.id = PDOrg.next_org_id
        PDOrg.next_org_id += 1
        self.parent = parent
        self.average_payout = None
        
        
    def get_mutant(self):
        """Get mutated version of self"""
        return PDOrg(self.genotype.get_mutant_of_self(), self.id)
    
    def __eq__(self, other):
        """Overload equality operator based on genotype"""
        return self.genotype == other.genotype
    
    def __ne__(self, other):
        """Overload not equal operator"""
        return not self == other
    
    def __str__(self):
        """String representation"""
        return "PDOrg({})".format(self.genotype)
    
    def __repr__(self):
        """In this case, the same as __str__"""
        return str(self)
        
    def __hash__(self):
        """Overload hash operator with that of genotype"""
        return hash(self.genotype)
        
    def will_cooperate(self):
        """
        Returns True if organism will cooperate, else False for defection
        
        First convert self.memory to a binary string ("101")
        Then, convert binary string to integer (5)
        Return value of decision list at index
        """
        if not self.memory:
            decision_list_index = 0
        else:
            binary_string_index = "".join("1" if i else "0" for i in self.memory)
            decision_list_index = int(binary_string_index, 2)
        return self.genotype.decision_list[decision_list_index]
       
    def store_bit_of_memory(self, did_cooperate):
        """
        Stores opponent's last move in memory at the right end of memory and
        deletes oldest move (on left)
        """
        self.memory.append(did_cooperate)
        self.memory.popleft()   
        
    def initialize_memory(self):
        self.memory = deque(self.genotype.initial_memory)

    def fitness(self, environment):
        raise NotImplementedError()
        
class PDStochasticOrg(PDOrg):
    """
    This class creates a PDStochastic organism.
    A PD organism consists of a genotype, ID, parent, and average payout. 
    Reliant on PDOrg and will pass through most member functions
    """
    next_org_id = 0

    def __init__(self, genotype=None, parent=None):
        if genotype is None:
            genotype = StochasticPDGenotype()
        self.genotype = genotype
        self.id = PDStochasticOrg.next_org_id
        PDStochasticOrg.next_org_id += 1
        self.parent = parent
        self.average_payout = None
    
    def get_mutant(self):
        new_genotype = random.random()
        return PDStochasticOrg(new_genotype, self.id)
    
    def _str_(self):
        return "PDStochasticOrg({})".format(self.genotype)

    def will_cooperate(self):
        return self.genotype.probability > random.random()

    def store_bit_of_memory(self, did_cooperate):
        pass
    
    def initialize_memory(self):
        pass

    def fitness(self, environment):
        raise NotImplementedError()
   
            
def _create_random_genotype():
    """
    Creates random memory PD genotype
    
    Used by PDOrg as default returned genotype
    """
    number_of_bits_of_memory = random.randrange(MAX_BITS_OF_MEMORY + 1)
    length = 2 ** number_of_bits_of_memory
    decision_list = [random.choice([True, False]) for _ in range(length)]
    initial_memory = [random.choice([True, False]) for _ in range(number_of_bits_of_memory)]
    return MemoryPDGenotype(number_of_bits_of_memory, decision_list, initial_memory)

# Hard-coded static competitors for baseline testing
MAX_BITS_OF_MEMORY = 1
ALL_DEFECT = PDOrg(MemoryPDGenotype(0, [False], []))
TIT_FOR_TAT = PDOrg(MemoryPDGenotype(1, [False, True], [True]))
COIN_FLIP = PDStochasticOrg()
STATIC_COMPETITORS = [ALL_DEFECT, TIT_FOR_TAT, COIN_FLIP]