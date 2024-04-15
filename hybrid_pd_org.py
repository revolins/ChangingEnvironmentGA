"""
This module defines the genome representation or memory model of HybridPD organisms in the population.
Two types of representations are available: MemoryPDGenotype and HybridPDGenotype.
"""

import random
from collections import deque

# Parameters are set through set_global_variables() in utils.py 
MAX_BITS_OF_MEMORY = None
MUTATION_LIKELIHOOD_OF_BITS_OF_MEMORY = None
MUTATION_LIKELIHOOD_OF_INITIAL_MEMORY_STATE = None
    
class HybridPDGenotype(object):
    """
    Hybrid Memory Model Genotype for inheriting in the HybridPDOrg Class
    """

    def __init__(self, number_of_bits_of_memory, number_of_bits_of_summary, decision_list, initial_memory, initial_summary):
        assert 0 <= number_of_bits_of_memory + number_of_bits_of_summary <= MAX_BITS_OF_MEMORY
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
    
    def type(self):
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
        Increase or decrease length of initial specific and summary memory by 1 bit each.
        Affects length of decision list as well. 
        """
        should_increase_memory = random.choice([True, False])

        # If organism has no memory, don't decrease anything
        if (self.number_of_bits_of_memory + self.number_of_bits_of_summary == 0) and not should_increase_memory:
            return self
        
        # If organism has maximum memory, don't increase anything
        if (self.number_of_bits_of_memory + self.number_of_bits_of_summary == MAX_BITS_OF_MEMORY) and should_increase_memory:
            return self
        
        # Changing both is risky under a single max memory threshold
        # If True, update SUMMARY memory
        # If False, update SPECIFIC memory
        summary_or_memory = random.choice([True, False]) 

        # If we increase memory length
        if should_increase_memory:
            # Specific memory (k)
            new_number_of_bits_of_memory = self.number_of_bits_of_memory
            new_initial_memory = self.initial_memory[:]
            # Increase specific memory
            if not summary_or_memory:
                # Update length
                new_number_of_bits_of_memory = self.number_of_bits_of_memory + 1 
                # Add 1 extra bit to initial memory
                new_initial_memory.append(random.choice([True,False]))

            # Summed memory (j)
            new_number_of_bits_of_summary = self.number_of_bits_of_summary
            new_initial_summary = self.initial_summary[:]
            # Increase summed memory
            if summary_or_memory:
                # Update length
                new_number_of_bits_of_summary = self.number_of_bits_of_summary + 1  
                # Add 1 extra bit to summary memory
                new_initial_summary.append(random.choice([True, False]))

            # Length of new decision list 2^k(j+1)
            length_of_new_decision_list = 2 ** new_number_of_bits_of_memory * (new_number_of_bits_of_summary + 1)
            
            # Double list, duplicate decisions
            # Retain as much of the original pattern as possible, not sure if matters
            # Also try to mimic original mutation method as closely as possible
            new_decision_list = 2 * self.decision_list
            
            # Fill the rest of the new list with random decisions
            for i in range(length_of_new_decision_list - len(new_decision_list)):
                new_decision_list.append(random.choice([True, False]))

            # SANITY CHECK
            assert len(new_decision_list) == length_of_new_decision_list, "DECISION LIST LENGTH DON'T MATCH (INCREASING)"

            return HybridPDGenotype(new_number_of_bits_of_memory, new_number_of_bits_of_summary, new_decision_list, new_initial_memory, new_initial_summary)

        # If we decrease memory length

        # Specific memory (k)
        new_number_of_bits_of_memory = self.number_of_bits_of_memory
        new_initial_memory = self.initial_memory[:]
        # Decrease specific memory
        if not summary_or_memory:
            new_number_of_bits_of_memory = self.number_of_bits_of_memory - 1 
            # Remove most distant memory bit
            new_initial_memory = self.initial_memory[:-1]

        # Summed memory (j)
        new_number_of_bits_of_summary = self.number_of_bits_of_summary
        new_initial_summary = self.initial_summary[:]
        # Decrease summed memory
        if summary_or_memory:
            new_number_of_bits_of_summary = self.number_of_bits_of_summary - 1
            # Remove most distant memory bit
            new_initial_summary = self.initial_summary[:-1]

        # Length of new decision list (2^k(j+1))
        length_of_new_decision_list = 2 ** new_number_of_bits_of_memory * (new_number_of_bits_of_summary + 1) 
        
        # Decrease decision list
        new_decision_list = self.decision_list[:length_of_new_decision_list]

        # SANITY CHECK
        assert len(new_decision_list) == length_of_new_decision_list, "DECISION LIST LENGTH DON'T MATCH (DECREASING)"

        # TODO: Currently, the decision list shrinks after subtracting from bits of summary and memory.
        # Wouldn't we expect the list to shrink inverse of it's original size? Like the following function?
        #length_of_new_decision_list = (len(self.decision_list) // 2) // (len(self.number_of_bits_of_summary) + 1)
        return HybridPDGenotype(new_number_of_bits_of_memory, new_number_of_bits_of_summary, new_decision_list, new_initial_memory, new_initial_summary) 
        
    def _decision_list_mutant(self):
        """Randomly flip a single bit in decision list"""
        mutation_location = random.randrange(len(self.decision_list))
        new_decision_list = self.decision_list[:]
        new_decision_list[mutation_location] = not new_decision_list[mutation_location]
        return HybridPDGenotype(self.number_of_bits_of_memory, self.number_of_bits_of_summary, new_decision_list, self.initial_memory, self.initial_summary)
        
    def _initial_memory_mutant(self):
        """
        Randomly flip a single bit in initial specific and summed memory.
        This affects the state of memory the organism starts with.  
        """
        # TODO: If organisms have the option to use specific, summary memory, or both,
        # mutations should be applied to both types of memory. 
        # Otherwise, organisms relying solely on summary memory might not mutate frequently enough
        # if mutations are only applied to specific memory.
        # Splitting this into two functions is possible, but this approach is simpler.

        # No changes if there is no memory
        if self.number_of_bits_of_memory + self.number_of_bits_of_summary == 0:
            return self
        
        new_initial_memory = self.initial_memory[:]
        # If there is specific memory
        if self.number_of_bits_of_memory > 0:
            # Mutate in specific memory
            mutation_location = random.randrange(len(self.initial_memory))
            new_initial_memory[mutation_location] = not new_initial_memory[mutation_location]

        new_initial_summary = self.initial_summary[:]
        # If there is summary memory
        if self.number_of_bits_of_summary > 0:
            # Mutate in summary memory
            mutation_location = random.randrange(len(self.initial_summary))
            new_initial_summary[mutation_location] = not new_initial_summary[mutation_location]

        # TODO: Fix Summary Memory mutation, does it need to be called separately?
        # TODO: Dont we expect to combine memory and summary at one point? Wouldnt that make only memory important instead of just summary? 
        # Is it necessary to mutate summary at all given this condition? Can we split summary from memory?
        #mutation_location = random.randrange(len(self.initial_summary))
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
        """
        # No specific or summary memory
        if not self.memory:
            decision_list_index = 0 # organism will have a decision list of size 1

        # At least specific or summary memory
        else:
            # Length of initial specific memory (k)
            len_memory = self.genotype.number_of_bits_of_memory
            assert len(self.genotype.initial_memory) == self.genotype.number_of_bits_of_memory

            # If specific memory exists
            if len_memory > 0:
                # print("k= ", len_memory)
                # Convert specific memory into binary string (True: 1, False: 0)
                binary_string = "".join("1" if i else "0" for i in list(self.memory)[:len_memory])
                # Convert binary string into integer
                binary_index = int(binary_string, 2)
                # print("binary string index= ", binary_index)

                # Count number of cooperate (True) moves in summed memory
                # summary_index is 0 if summed memory is empty
                summary_index = sum(1 for i in list(self.memory)[len_memory:] if i==True)
                # print("summary index= ", summary_index)

                # Which "block" does binary_index belong to?
                # If summary memory doesn't exist, works like PDOrg
                decision_list_index = binary_index + (2 ** len_memory) * summary_index

            # If specified memory doesn't exist, summary memory has to at least exist
            else:
                assert len(self.genotype.initial_summary) > 0

                # In this case, decision list has size (j+1)
                decision_list_index = sum(1 for i in self.memory if i==True)

                assert decision_list_index <= (self.genotype.number_of_bits_of_summary)


        # print("************************** NEW ORGANISM GENOTYPE ********************************", flush=True)
        # print("self.memory= ", self.memory)            
        # print("length: genotype decision list= ", len(self.genotype.decision_list))
        # print("genotype decision list= ", self.genotype.decision_list)
        # print("decision list index= ", decision_list_index, flush=True)

        return self.genotype.decision_list[decision_list_index]
       
    def store_bit_of_memory(self, did_cooperate):
        """
        Stores opponent's last move in memory at the left end of memory and
        deletes oldest move (on right)
        """
        # Newest goes to the front of the list
        self.memory.appendleft(did_cooperate) 
        self.memory.pop()   
        
    def initialize_memory(self):
        """Get double-ended queue memory"""
        self.memory = deque(self.genotype.initial_memory + self.genotype.initial_summary)

    def fitness(self, environment):
        raise NotImplementedError()
   
            
def _create_random_genotype():
    """
    Creates random memory PD genotype
    
    Used by HybridPDOrg as default returned genotype
    """
    # randrange generate number in range [0, MAX_BITS_OF_MEMORY] = total bits of mem
    # get random index to make a random split
    # one of the lists may or may not exist
    # This implies that organisms have the option to use specific, summary memory, or both
    total_bits_of_memory = random.randrange(MAX_BITS_OF_MEMORY + 1)
    number_of_bits_of_memory = random.randrange(total_bits_of_memory + 1)
    number_of_bits_of_summary = total_bits_of_memory - number_of_bits_of_memory
    assert number_of_bits_of_memory + number_of_bits_of_summary <= MAX_BITS_OF_MEMORY
    length = 2 ** number_of_bits_of_memory * (number_of_bits_of_summary + 1)
    decision_list = [random.choice([True, False]) for _ in range(length)]
    initial_memory = [random.choice([True, False]) for _ in range(number_of_bits_of_memory)]
    initial_summary = [random.choice([True, False]) for _ in range(number_of_bits_of_summary)]
    return HybridPDGenotype(number_of_bits_of_memory, number_of_bits_of_summary, decision_list, initial_memory, initial_summary)