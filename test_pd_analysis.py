import unittest
import pd_analysis
import pd_org

class TestSelection(unittest.TestCase):
    def test_get_tally_of_number_of_bits_of_memory(self):
        """
        Returns a list of length MAX_BITS_OF_MEMORY + 1 where each position represents the number
        of organisms with that many number of bits of memory
        """
        pd_org.MAX_BITS_OF_MEMORY = 4
        
        organism_a = pd_org.PDOrg(pd_org.MemoryPDGenotype(1,[True, False], [False]))
        organism_b = pd_org.PDOrg(pd_org.MemoryPDGenotype(2,[True, False, False, True], [False, True]))
        organisms = [organism_a, organism_b, organism_a, organism_a]
        
        tally = pd_analysis.get_tally_of_number_of_bits_of_memory(organisms)
        expected = [0, 3, 1, 0, 0]
        self.assertEqual(tally, expected)

        
if __name__ == "__main__":
    unittest.main()