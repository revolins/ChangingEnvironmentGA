"""
This module defines the genome representation or memory model of PD organisms in the population.
Two types of representations are available: MemoryPDGenotype and HybridPDGenotype.
"""

import random
    
class HybridPDGenotype(object):
    """
    Hybrid Memory Model Genotype for inheriting in the PDOrg Class
    temp file location for implementation
    """

    def __init__(self, number_of_bits_of_memory, number_of_bits_of_summary, decision_list, initial_memory, initial_summary, args):
        assert 0 <= number_of_bits_of_memory <= args.max_bits_of_memory
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

    def get_mutant_of_self(self, args):
        """
        Determines when and how each type of mutation occurs.
        Returns new (mutated) genotype.
        """
        random_value = random.random()

        # Size mutation
        if random_value < args.mutation_likelihood_of_bits_of_memory:
            return self._get_bits_of_memory_mutant()
        # Initial (specific) memory mutation
        # TODO: should we add another mutation likelihood parameter for summary memory?
        if random_value < args.mutation_likelihood_of_bits_of_memory + args.mutation_likelihood_of_initial_memory_state:
            return self._initial_memory_mutant()
        # Decision mutation
        return self._decision_list_mutant()

    def _get_bits_of_memory_mutant(self, args):
        """
        Increase or decrease length of initial (specific) and summary memory by 1 bit each.
        Affects length of decision list as well. 
        """
        should_increase_memory = random.choice([True, False])

        # If organism has no memory, don't decrease memory
        if (self.number_of_bits_of_memory == 0 or self.number_of_bits_of_summary == 0) and not should_increase_memory:
            return self
        
        # If organism has maximum memory length, don't increase memory
        if (self.number_of_bits_of_memory == args.max_bits_of_memory or self.number_of_bits_of_summary == args.max_bits_of_summary) and should_increase_memory:
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
            for i in range(length_of_new_decision_list - len(new_decision_list)):
                new_decision_list.append(random.choice([True, False]))

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
      
def _create_random_genotype():
    """
    Creates random memory PD genotype
    
    Used by PDOrg as default returned genotype
    """
    number_of_bits_of_memory = random.randrange(args.max_bits_of_memory + 1)
    number_of_bits_of_summary = random.randrange(args.max_bits_of_summary + 1)
    length = 2 ** number_of_bits_of_memory * (number_of_bits_of_summary + 1)
    decision_list = [random.choice([True, False]) for _ in range(length)]
    initial_memory = [random.choice([True, False]) for _ in range(number_of_bits_of_memory)]
    initial_summary = [random.choice([True, False]) for _ in range(number_of_bits_of_summary)]
    return HybridPDGenotype(number_of_bits_of_memory, number_of_bits_of_summary, decision_list, initial_memory, initial_summary)

