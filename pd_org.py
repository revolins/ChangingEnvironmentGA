"""
This module defines the genome representation of organisms in the population.
Two types of representations are available: MemoryPDGenotype and HybridPDGenotype.
"""

import random
import pd_tournament
from collections import deque

# Parameters are set through set_global_variables() in main.py 
MAX_BITS_OF_MEMORY = None
MUTATION_LIKELIHOOD_OF_BITS_OF_MEMORY = None
MUTATION_LIKELIHOOD_OF_INITIAL_MEMORY_STATE = None

class StochasticPDGenotype(object):
    """What is this for"""
    def __init__(self, probability=.5, number_of_bits_of_memory=0):
        self.probability = probability
        self.number_of_bits_of_memory = number_of_bits_of_memory

class MemoryPDGenotype(object):
    """
    Original genotype representation from Cruz et al. 2016 
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
        """In this case, the same as __str__"""
        return str(self)
        
    def __hash__(self):
        """Overload hash operator, necessary for dictionaries and such"""
        # Convert decision list and initial (specific) memory into immutable tuples
        hashable_tuple = (self.number_of_bits_of_memory, 
            tuple(self.decision_list), 
            tuple(self.initial_memory)) # We don't consider IDs
        return hash(hashable_tuple) 

    def get_mutant_of_self(self):
        """
        Determines when and how each type of mutation occurs.
        Returns new (mutated) genotype.
        """
        
        random_value = random.random()
        if random_value < MUTATION_LIKELIHOOD_OF_BITS_OF_MEMORY:
            return self._get_bits_of_memory_mutant()
        if random_value < MUTATION_LIKELIHOOD_OF_BITS_OF_MEMORY + MUTATION_LIKELIHOOD_OF_INITIAL_MEMORY_STATE:
            return self._initial_memory_mutant()
        return self._decision_list_mutant()


    def _get_bits_of_memory_mutant(self):
        """
        Increase or decrease initial (specific) memory length by 1 bit.
        Affects length of decision list as well. 
        """
        should_increase_memory = random.choice([True, False])
        if self.number_of_bits_of_memory == 0 and not should_increase_memory:
            return self
        if self.number_of_bits_of_memory == MAX_BITS_OF_MEMORY and should_increase_memory:
            return self
        if should_increase_memory:
            new_number_of_bits_of_memory = self.number_of_bits_of_memory + 1
            new_decision_list = self.decision_list * 2
            new_initial_memory = self.initial_memory[:]
            new_initial_memory.append(random.choice([True,False]))
            return MemoryPDGenotype(new_number_of_bits_of_memory, new_decision_list, new_initial_memory)
        # should decrease memory
        # Should there be an else statement here?
        new_number_of_bits_of_memory = self.number_of_bits_of_memory - 1
        length_of_new_decision_list = len(self.decision_list) // 2
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
        Flip a single bit of initial (specified) memory.
        If there is no memory, no change is made.
        """
        if self.number_of_bits_of_memory == 0:
            return self
        mutation_location = random.randrange(len(self.initial_memory))
        new_initial_memory = self.initial_memory[:]
        new_initial_memory[mutation_location] = not new_initial_memory[mutation_location]
        return MemoryPDGenotype(self.number_of_bits_of_memory, self.decision_list, new_initial_memory)
    
class HybridPDGenotype(object):
    """
    Hybrid Memory Model Genotype for inheriting in the PDOrg Class
    temp file location for implementation
    """

    def __init__(self, number_of_bits_of_memory, number_of_bits_of_summary, decision_list, initial_memory, initial_summary):
        # print("CURRENT NUMBER OF BITS OF MEMORY")
        # print(number_of_bits_of_memory)
        assert 0 <= number_of_bits_of_memory <= MAX_BITS_OF_MEMORY
        # print("Decision List Sanity Check")
        # print(len(decision_list))
        # print(2 ** number_of_bits_of_memory * (number_of_bits_of_summary + 1))
        assert len(decision_list) == 2 ** number_of_bits_of_memory * (number_of_bits_of_summary + 1)
        assert len(initial_memory) == number_of_bits_of_memory
        self.number_of_bits_of_memory = number_of_bits_of_memory
        self.number_of_bits_of_summary = number_of_bits_of_summary
        self.decision_list = decision_list
        self.initial_memory = initial_memory
        self.initial_summary = initial_summary
    
    
    def __eq__(self, other):
        return (self.number_of_bits_of_memory == other.number_of_bits_of_memory and
                self.number_of_bits_of_summary == other.number_of_bits_of_summary and
                self.decision_list == other.decision_list and
                self.initial_memory == other.initial_memory and
                self.initial_summary == other.initial_summary)
    
    def __ne__(self, other):
        return not self == other
    
    def __str__(self):
        return "HybridPDGenotype({}, {}, {}, {}, {})".format(self.number_of_bits_of_memory,
                                                     self.number_of_bits_of_summary,
                                                     self.decision_list,
                                                     self.initial_memory,
                                                     self.initial_summary)
    
    def __repr__(self):
        return str(self)
        
    def __hash__(self):
        hashable_tuple = (self.number_of_bits_of_memory, 
            self.number_of_bits_of_summary,
            tuple(self.decision_list), 
            tuple(self.initial_memory),
            tuple(self.initial_summary))
        return hash(hashable_tuple)

    def get_mutant_of_self(self):
        """
        Determines when and how each type of mutation occurs.
        Returns new (mutated) genotype.
        """

        #Mutant of Summary as well as Memory? Currently a mutant of just memory
        
        random_value = random.random()

        # Size mutation
        if random_value < MUTATION_LIKELIHOOD_OF_BITS_OF_MEMORY:
            return self._get_bits_of_memory_mutant()
        # Initial (specific) memory mutation
        if random_value < MUTATION_LIKELIHOOD_OF_BITS_OF_MEMORY + MUTATION_LIKELIHOOD_OF_INITIAL_MEMORY_STATE:
            return self._initial_memory_mutant()
        # Decision mutation
        return self._decision_list_mutant()


    def _get_bits_of_memory_mutant(self):
        """
        Increase or decrease initial (specific) memory length by 1 bit.
        Affects length of decision list as well. 
        """
        should_increase_memory = random.choice([True, False])
        if self.number_of_bits_of_memory == 0 and self.number_of_bits_of_summary == 0 and not should_increase_memory:
            return self
        if self.number_of_bits_of_memory == MAX_BITS_OF_MEMORY and self.number_of_bits_of_summary == MAX_BITS_OF_SUMMARY and should_increase_memory:
            #Return full normal memory but hybrid relies on 2*k * (j+1)
            return self
        if should_increase_memory:
            new_number_of_bits_of_memory = self.number_of_bits_of_memory + 1
            new_number_of_bits_of_summary = self.number_of_bits_of_summary + 1
            new_decision_list = 2 ** self.decision_list * (len(self.decision_list) + 1)
            new_initial_memory = self.initial_memory[:]
            new_initial_memory.append(random.choice([True,False]))
            new_initial_summary = self.initial_summary[:]
            new_initial_summary.append(random.choice([True, False]))
            return HybridPDGenotype(new_number_of_bits_of_memory, new_number_of_bits_of_summary, new_decision_list, new_initial_memory, new_initial_summary)
        # should decrease memory
        # Current bug, decreasing memory out of order? Unlikely
        # length of decision list causes cascading issues after generations? More likely
        # Slicing necessary for summary and memory? Unlikely
        # Should there be an else statement here?
        new_number_of_bits_of_memory = self.number_of_bits_of_memory - 1
        new_number_of_bits_of_summary = self.number_of_bits_of_summary - 1
        length_of_new_decision_list = (2 // len(self.decision_list)) // (len(self.decision_list) + 1)
        new_decision_list = self.decision_list[:length_of_new_decision_list]
        new_initial_memory = self.initial_memory[:-1]
        new_initial_summary = self.initial_summary[:-1]
        return HybridPDGenotype(new_number_of_bits_of_memory, new_number_of_bits_of_summary, new_decision_list, new_initial_memory, new_initial_summary) 
        
    def _decision_list_mutant(self):
        """Randomly flip a single bit in decision list"""
        mutation_location = random.randrange(len(self.decision_list))
        new_decision_list = self.decision_list[:]
        new_decision_list[mutation_location] = not new_decision_list[mutation_location]
        return HybridPDGenotype(self.number_of_bits_of_memory, self.number_of_bits_of_summary, new_decision_list, self.initial_memory, self.initial_summary)
        
    def _initial_memory_mutant(self):
        """
        Flip a single bit of initial (specified) memory.
        If there is no memory, no change is made.
        """
        if self.number_of_bits_of_memory == 0:
            return self
        mutation_location = random.randrange(len(self.initial_memory))
        new_initial_memory = self.initial_memory[:]
        new_initial_memory[mutation_location] = not new_initial_memory[mutation_location]
        new_initial_summary = self.initial_summary[:]
        return HybridPDGenotype(self.number_of_bits_of_memory, self.number_of_bits_of_summary, self.decision_list, new_initial_memory, new_initial_summary)

class PDOrg(object):
    """
    This class creates a PD organism.
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
        return PDOrg(self.genotype.get_mutant_of_self(), self.id)
    
    def __eq__(self, other):
        return self.genotype == other.genotype
    
    def __ne__(self, other):
        return not self == other
    
    def __str__(self):
        return "PDOrg({})".format(self.genotype)
    
    def __repr__(self):
        return str(self)
        
    def __hash__(self):
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
    
    def is_better_than(self, other, environment):
        raise NotImplementedError()
        
class PDStochasticOrg(PDOrg):
    """
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
    
    def is_better_than(self, other, environment):
        raise NotImplementedError()
   
            
def _create_random_genotype():
    """
    Creates random memory PD genotype
    
    Used by PDOrg as default returned genotype
    """
    number_of_bits_of_memory = random.randrange(MAX_BITS_OF_MEMORY + 1)
    number_of_bits_of_summary = random.randrange(MAX_BITS_OF_SUMMARY + 1)
    length = 2 ** number_of_bits_of_memory * (number_of_bits_of_summary + 1)
    decision_list = [random.choice([True, False]) for _ in range(length)]
    initial_memory = [random.choice([True, False]) for _ in range(number_of_bits_of_memory)]
    initial_summary = [random.choice([True, False]) for _ in range(number_of_bits_of_summary)]
    return HybridPDGenotype(number_of_bits_of_memory, number_of_bits_of_summary, decision_list, initial_memory, initial_summary)


MAX_BITS_OF_MEMORY = 1
MAX_BITS_OF_SUMMARY = 1

# Define fixed opponent strategies for Static Mode
ALL_DEFECT = PDOrg(MemoryPDGenotype(0, [False], []))
TIT_FOR_TAT = PDOrg(MemoryPDGenotype(1, [False, True], [True]))
COIN_FLIP = PDStochasticOrg() # Random strategy
STATIC_COMPETITORS = [ALL_DEFECT, TIT_FOR_TAT, COIN_FLIP]

