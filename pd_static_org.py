"""
Static Genotype for restricting strategies to classic strategies
"""

import random
from collections import deque

class StaticPDGenotype(object):
    """
    This class creates a genotype.
    """

    def __init__(self, number_of_bits_of_memory, decision_list, initial_memory):
        assert 0 <= number_of_bits_of_memory <= 4
        assert len(decision_list) == 2 ** number_of_bits_of_memory
        assert len(initial_memory) == number_of_bits_of_memory
        self.number_of_bits_of_memory = number_of_bits_of_memory
        self.decision_list = decision_list
        self.initial_memory = initial_memory
    
    
    def __eq__(self, other):
        return (self.number_of_bits_of_memory == other.number_of_bits_of_memory and
                self.decision_list == other.decision_list and
                self.initial_memory == other.initial_memory)
    
    def __ne__(self, other):
        return not self == other
    
    def __str__(self):
        return "StaticPDGenotype({}, {}, {})".format(self.number_of_bits_of_memory,
                                                     self.decision_list,
                                                     self.initial_memory)
    
    def __repr__(self):
        return str(self)
        
    def __hash__(self):
        hashable_tuple = (self.number_of_bits_of_memory, 
            tuple(self.decision_list), 
            tuple(self.initial_memory))
        return hash(hashable_tuple)

    def get_mutant_of_self(self):
        """
        Determines when and how each type of mutation occurs.
        Returns new (mutated) genotype.
        """
        
        random_value = random.random()
        if random_value < 0.0:
            return self._get_bits_of_memory_mutant()
        if random_value < 0.0:
            return self._initial_memory_mutant()
        return self._decision_list_mutant()


    def _get_bits_of_memory_mutant(self):
        should_increase_memory = random.choice([True, False])
        if self.number_of_bits_of_memory == 0 and not should_increase_memory:
            return self
        if self.number_of_bits_of_memory == 1 and should_increase_memory:
            return self
        if should_increase_memory:
            new_number_of_bits_of_memory = self.number_of_bits_of_memory + 1
            new_decision_list = self.decision_list * 2
            new_initial_memory = self.initial_memory[:]
            new_initial_memory.append(random.choice([True,False]))
            return StaticPDGenotype(new_number_of_bits_of_memory, new_decision_list, new_initial_memory)
        # should decrease memory
        new_number_of_bits_of_memory = self.number_of_bits_of_memory - 1
        length_of_new_decision_list = len(self.decision_list) // 2
        new_decision_list = self.decision_list[:length_of_new_decision_list]
        new_initial_memory = self.initial_memory[:-1]
        return StaticPDGenotype(new_number_of_bits_of_memory, new_decision_list, new_initial_memory) 
        
    def _decision_list_mutant(self):
        mutation_location = random.randrange(len(self.decision_list))
        new_decision_list = self.decision_list[:]
        new_decision_list[mutation_location] = not new_decision_list[mutation_location]
        return StaticPDGenotype(self.number_of_bits_of_memory, new_decision_list, self.initial_memory)
        
    def _initial_memory_mutant(self):
        """
        Normally, a single of bit of initial memory is flipped,
        but if there is no memory, no change is made
        """
        if self.number_of_bits_of_memory == 0:
            return self
        mutation_location = random.randrange(len(self.initial_memory))
        new_initial_memory = self.initial_memory[:]
        new_initial_memory[mutation_location] = not new_initial_memory[mutation_location]
        return StaticPDGenotype(self.number_of_bits_of_memory, self.decision_list, new_initial_memory)

class StaticOrg(object):
    """
    This class creates a PD organism.
    """
    
    next_org_id = 0
    
    def __init__(self, genotype=None, parent=None):
        if genotype is None:
            genotype = _create_random_genotype()
        self.genotype = genotype
        self.initialize_memory()
        self.id = StaticOrg.next_org_id
        StaticOrg.next_org_id += 1
        self.parent = parent
        self.average_payout = None
        
        
    def get_mutant(self):
        return StaticOrg(self.genotype.get_mutant_of_self(), self.id)
    
    def __eq__(self, other):
        return self.genotype == other.genotype
    
    def __ne__(self, other):
        return not self == other
    
    def __str__(self):
        return "StaticOrg({})".format(self.genotype)
    
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
   
            
def _create_random_genotype():
    """
    Creates random memory PD genotype
    
    Used by StaticOrg as default returned genotype
    """
    number_of_bits_of_memory = random.randrange(5)
    length = 2 ** number_of_bits_of_memory
    decision_list = [random.choice([True, False]) for _ in range(length)]
    initial_memory = [random.choice([True, False]) for _ in range(number_of_bits_of_memory)]
    return StaticPDGenotype(number_of_bits_of_memory, decision_list, initial_memory)