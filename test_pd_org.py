import unittest
import pd_org
from pd_org import MemoryPDGenotype as Geno

class TestMemoryPDGenotype(unittest.TestCase):

    def setUp(self):
        pd_org.MAX_BITS_OF_MEMORY = 5
        self.num_bits = 2
        self.decision_list = [True, False, False, True]
        self.initial_mem = [True, False]
        self.geno = Geno(self.num_bits, self.decision_list, self.initial_mem)
        
        
    def test_init(self):
        self.assertEqual(self.num_bits, self.geno.number_of_bits_of_memory)
        self.assertEqual(self.decision_list, self.geno.decision_list)
        self.assertEqual(self.initial_mem, self.geno.initial_memory)
        

    def test_init_bad(self):
        with self.assertRaises(AssertionError):
            Geno(2, [True]*4, [False])

        with self.assertRaises(AssertionError):
            Geno(2, [True]*3, [False]*2)
        
        with self.assertRaises(AssertionError):
            Geno(6, [True]*(2**6), [False]*6)
            
        with self.assertRaises(AssertionError):
            Geno(-1, [], [])

    def test_eq(self):
        geno2 = Geno(self.num_bits, self.decision_list, self.initial_mem)
        self.assertEqual(self.geno, geno2)
        
        geno3 =  Geno(1, [False, True], [False])
        self.assertNotEqual(self.geno, geno3)
        
        geno4 = Geno(self.num_bits, [True, True, False, True], self.initial_mem)
        self.assertNotEqual(self.geno, geno4)
        
        geno5 = Geno(self.num_bits, self.decision_list, [False, True])
        self.assertNotEqual(self.geno, geno5)
        
    def test_str(self):
        expected = "MemoryPDGenotype(2, [True, False, False, True], [True, False])"
        result = str(self.geno)
        self.assertEqual(expected, result)
        
        result_repr = repr(self.geno)
        self.assertEqual(expected, result_repr)
    
    def test_decision_list_mutant(self):
        mutant = self.geno._decision_list_mutant()
        self.assertNotEqual(mutant, self.geno)
        self.assertEqual(mutant.number_of_bits_of_memory,
            self.geno.number_of_bits_of_memory)
        self.assertNotEqual(mutant.decision_list, self.geno.decision_list)
        self.assertEqual(mutant.initial_memory, self.geno.initial_memory)
        
    def test_initial_memory_mutant(self):
        mutant = self.geno._initial_memory_mutant()
        self.assertNotEqual(mutant, self.geno)
        self.assertEqual(mutant.number_of_bits_of_memory,
            self.geno.number_of_bits_of_memory)
        self.assertEqual(mutant.decision_list, self.geno.decision_list)
        self.assertNotEqual(mutant.initial_memory, self.geno.initial_memory)
    
    def test_initial_memory_mutant_no_memory(self):
        no_memory = Geno(0, [True], [])
        mutant = no_memory._initial_memory_mutant()
        self.assertEqual(mutant, no_memory)
    
    def test_bits_of_memory_mutant(self):
        for _ in range(100):
            mutant = self.geno._get_bits_of_memory_mutant()
            if mutant.number_of_bits_of_memory == 1:
                self.assertEqual(mutant.decision_list, self.geno.decision_list[:2])
                self.assertEqual(mutant.initial_memory, self.geno.initial_memory[:1])
            elif mutant.number_of_bits_of_memory == 3:
                self.assertEqual(mutant.decision_list, self.geno.decision_list * 2)
                self.assertEqual(mutant.initial_memory[:-1], self.geno.initial_memory)
                self.assertIn(mutant.initial_memory[-1], [True, False])
            else:
                self.fail("number of bits MUST change")
                
        
    

if __name__ == "__main__":
    unittest.main()
