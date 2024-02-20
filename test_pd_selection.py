import unittest
import pd_selection
import pd_org

class TestSelection(unittest.TestCase):
    def setUp(self):
        pd_org.MAX_BITS_OF_MEMORY = 4
        
        pd_selection.TOURNAMENT_SIZE = 3
        self.organism_a = pd_org.PDOrg(pd_org.MemoryPDGenotype(1,[True, False], [False]))
        self.organism_b = pd_org.PDOrg(pd_org.MemoryPDGenotype(2,[True, False, False, True], [False, True]))
        self.organisms = [self.organism_a, self.organism_b]
        self.organism_a.average_payout = 0
        self.organism_b.average_payout = 9.8

    def test_get_best_half(self):
        result = pd_selection.get_best_half(self.organisms)
        expected = [self.organism_b]
        self.assertNotEqual(len(self.organisms), len(result))

    def test_get_number_of_tournaments(self):
        len1 = [1]
        len3 = [1] * 3
        len4 = [1] * 4
        len10 = [1] * 10
        pd_selection.TOURNAMENT_SIZE = 3
        expecteds = [1, 1, 2, 4]
        lens = [len1, len3, len4, len10]
        for expected, orgs in zip(expecteds, lens):
            result = pd_selection.get_number_of_tournaments(orgs)
            self.assertEqual(expected, result)


    def test_get_contender_generator(self):
        orgs = [ x for x in range(10)]
        orgs_copy = orgs[:]
        gen = pd_selection.get_contender_generator(orgs)
        expected_size = [3, 3, 3, 1]
        
        orgs_returned = []
        for i in range(len(expected_size)):
            clump = next(gen)
            orgs_returned.extend(clump)
            self.assertEqual(expected_size[i], len(clump))
        self.assertEqual(len(set(orgs_returned)), len(orgs_copy))
        
        clump = next(gen)
        self.assertEqual(3, len(clump))
        
    def test_get_next_generation_by_selection(self):
        result = pd_selection.get_next_generation_by_selection(self.organisms)
        self.assertEqual(len(self.organisms),len(result))
     
    def test_get_next_generation_by_static_payout(self):
        organism_a = pd_org.PDOrg(pd_org.MemoryPDGenotype(0,[True], []))
        organism_b = pd_org.PDOrg(pd_org.MemoryPDGenotype(0,[False], []))
        organisms = [organism_a, organism_b]
        static_competitors = [organism_a, organism_b]
        
        contender_generator = pd_selection.get_contender_generator(organisms)
        pd_selection.get_next_generation_by_selection(organisms)        
        results = pd_selection._get_next_generation(organisms, contender_generator)
        
       
        expected = [organism_a, organism_b]
        self.assertEqual(expected, expected)

if __name__ == "__main__":
    unittest.main()
