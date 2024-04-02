"""
This module defines the genome representation or memory model of HybridPD organisms in the population.
Two types of representations are available: MemoryPDGenotype and HybridPDGenotype.
"""

import random
from collections import deque

# Parameters are set through set_global_variables() in utils.py 
MAX_BITS_OF_MEMORY = None
MAX_BITS_OF_SUMMARY = None
MUTATION_LIKELIHOOD_OF_BITS_OF_MEMORY = None
MUTATION_LIKELIHOOD_OF_INITIAL_MEMORY_STATE = None
    
class HybridPDGenotype(object):
    """
    Hybrid Memory Model Genotype for inheriting in the HybridPDOrg Class
    temp file location for implementation
    """

    def __init__(self, number_of_bits_of_memory, number_of_bits_of_summary, decision_list, initial_memory, initial_summary):
        assert 0 <= number_of_bits_of_memory <= MAX_BITS_OF_MEMORY
        assert len(decision_list) == 2 ** number_of_bits_of_memory * (number_of_bits_of_summary + 1)
        assert len(initial_memory) == number_of_bits_of_memory
        assert len(initial_summary) == number_of_bits_of_summary
        self.number_of_bits_of_memory = number_of_bits_of_memory
        self.number_of_bits_of_summary = number_of_bits_of_summary
        self.decision_list = decision_list
        self.initial_memory = initial_memory
        self.initial_summary = initial_summary
    
    
    def __eq__(self, other):
        """Overload equality operator"""
        return (self.number_of_bits_of_memory == other.number_of_bits_of_memory and
                self.number_of_bits_of_summary == other.number_of_bits_of_summary and
                self.decision_list == other.decision_list and
                self.initial_memory == other.initial_memory and
                self.initial_summary == other.initial_summary)
    
    def __ne__(self, other):
        """Overload not equal operator"""
        return not self == other
    
    def __str__(self):
        """String representation"""
        return "HybridPDGenotype({}, {}, {}, {}, {})".format(self.number_of_bits_of_memory,
                                                     self.number_of_bits_of_summary,
                                                     self.decision_list,
                                                     self.initial_memory,
                                                     self.initial_summary)
    
    def __repr__(self):
        """In this case, same as __str__"""
        return str(self)
        
    def __hash__(self):
        """Overload hash operator, necessary for dictionaries and such"""
        hashable_tuple = (self.number_of_bits_of_memory, 
            self.number_of_bits_of_summary,
            tuple(self.decision_list), 
            tuple(self.initial_memory),
            tuple(self.initial_summary))
        return hash(hashable_tuple) # We don't consider IDs and parents, only strategy
    
    def __type__(self):
        """Return type as string for easy checking"""
        return 'hybrid'

    def get_mutant_of_self(self):
        """
        Determines when and how each type of mutation occurs.
        Returns new (mutated) genotype.
        """
        random_value = random.random()

        # Size mutation
        if random_value < MUTATION_LIKELIHOOD_OF_BITS_OF_MEMORY:
            return self._get_bits_of_memory_mutant()
        # Initial (specific) memory mutation
        # TODO: should we add another mutation likelihood parameter for summary memory?
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
        if (self.number_of_bits_of_memory == 0 or self.number_of_bits_of_summary == 0) and not should_increase_memory:
            return self
        
        # If organism has maximum memory length, don't increase memory
        if (self.number_of_bits_of_memory == MAX_BITS_OF_MEMORY or self.number_of_bits_of_summary == MAX_BITS_OF_SUMMARY) and should_increase_memory:
            #Return full normal memory but hybrid relies on 2*k * (j+1)
            return self
        
        # If we increase memory length
        if should_increase_memory:
            new_number_of_bits_of_memory = self.number_of_bits_of_memory + 1 # (k) 
            new_number_of_bits_of_summary = self.number_of_bits_of_summary + 1 # (j)
            # Length of new decision list 2^k(j+1)
            length_of_new_decision_list = 2 ** new_number_of_bits_of_memory * (new_number_of_bits_of_summary + 1)
            
            # Double list, duplicate decisions
            # Retain as much of the original pattern as possible, not sure if matters
            # Also try to mimic original mutation method as closely as possible
            new_decision_list = 2 * self.decision_list
            
            # Fill the rest of the new list with random decisions
            # for i in range(length_of_new_decision_list - len(new_decision_list)):
            #     new_decision_list.append(random.choice([True, False]))

            # Add 1 extra bit to initial memory
            new_initial_memory = self.initial_memory[:]
            new_initial_memory.append(random.choice([True,False]))

            # Add 1 extra bit to summary memory
            new_initial_summary = self.initial_summary[:]
            new_initial_summary.append(random.choice([True, False]))

            return HybridPDGenotype(new_number_of_bits_of_memory, new_number_of_bits_of_summary, new_decision_list, new_initial_memory, new_initial_summary)

        # If we decrease memory length
        new_number_of_bits_of_memory = self.number_of_bits_of_memory - 1 # (k)
        new_number_of_bits_of_summary = self.number_of_bits_of_summary - 1 # (j)
        #length_of_new_decision_list = len(self.decision_list) // 2
        length_of_new_decision_list = 2 ** new_number_of_bits_of_memory * (new_number_of_bits_of_summary + 1) # (2^k(j+1))
        
        # Update size of memory and decision lists, most distant past memory bits removed
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

        # Mutate in summary memory
        mutation_location = random.randrange(len(self.initial_summary))
        new_initial_summary = self.initial_summary[:]
        new_initial_summary[mutation_location] = not new_initial_summary[mutation_location]

        return HybridPDGenotype(self.number_of_bits_of_memory, self.number_of_bits_of_summary, self.decision_list, new_initial_memory, new_initial_summary)

class HybridPDOrg(object):
    """
    This class creates a HyrbidPD organism.
    A HybridPD organism consists of a genotype, ID, parent, and average payout. 
    """
    
    next_org_id = 0
    
    def __init__(self, genotype=None, parent=None):
        if genotype is None:
            genotype = _create_random_genotype()
        self.genotype = genotype
        self.memory = None
        self.initialize_memory()
        self.id = HybridPDOrg.next_org_id
        HybridPDOrg.next_org_id += 1
        self.parent = parent
        self.average_payout = None
        
        
    def get_mutant(self):
        """Get mutated version of self"""
        return HybridPDOrg(self.genotype.get_mutant_of_self(), self.id)
    
    def __eq__(self, other):
        """Overload equality operator based on genotype"""
        return self.genotype == other.genotype
    
    def __ne__(self, other):
        """Overload not equal operator"""
        return not self == other
    
    def __str__(self):
        """String representation"""
        return "HybridPDOrg({})".format(self.genotype)
    
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
        print("************* self.memory ***************", self.memory, flush=True)
        print("************* binary string index ***************", binary_string_index, flush=True)
        print("************* length: genotype decision list ****************: ", len(self.genotype.decision_list), flush=True)
        print("************* genotype decision list ****************: ", self.genotype.decision_list, flush=True)
        print("************* decision list index ****************: ", decision_list_index, flush=True)
        return self.genotype.decision_list[decision_list_index]
       
    def store_bit_of_memory(self, did_cooperate):
        """
        Stores opponent's last move in memory at the right end of memory and
        deletes oldest move (on left)
        """
        self.memory.append(did_cooperate)
        self.memory.popleft()   
        
    def initialize_memory(self):
        """Get double-ended queue memory"""
        self.memory = deque(self.genotype.initial_memory + self.genotype.initial_summary) # makes a copy
    
    def fitness(self, environment):
        raise NotImplementedError()
   
            
def _create_random_genotype():
    """
    Creates random memory PD genotype
    
    Used by HybridPDOrg as default returned genotype
    """
    number_of_bits_of_memory = random.randrange(MAX_BITS_OF_MEMORY + 1)
    number_of_bits_of_summary = random.randrange(MAX_BITS_OF_SUMMARY + 1)
    length = 2 ** number_of_bits_of_memory * (number_of_bits_of_summary + 1)
    decision_list = [random.choice([True, False]) for _ in range(length)]
    initial_memory = [random.choice([True, False]) for _ in range(number_of_bits_of_memory)]
    initial_summary = [random.choice([True, False]) for _ in range(number_of_bits_of_summary)]
    return HybridPDGenotype(number_of_bits_of_memory, number_of_bits_of_summary, decision_list, initial_memory, initial_summary)