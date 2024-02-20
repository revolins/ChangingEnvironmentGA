import unittest
import pd_org
import pd_tournament
from pd_tournament import pd_payout

class TestPDPayout(unittest.TestCase):
    def test_pd_payout(self):
        def alt_pd_payout(self_is_cooperator, other_is_cooperator):
            if self_is_cooperator:
                if other_is_cooperator:
                    return pd_tournament.REWARD
                return pd_tournament.SUCKER
            if other_is_cooperator:
                return pd_tournament.TEMPTATION
            return pd_tournament.PUNISHMENT
        
        for a_cooperates in [True, False]:
            for b_cooperates in [True, False]:
                payout_a, payout_b = pd_payout(a_cooperates, b_cooperates)
                expected_payout_a = alt_pd_payout(a_cooperates, b_cooperates)
                expected_payout_b = alt_pd_payout(b_cooperates, a_cooperates)
                
                self.assertEqual(expected_payout_a, payout_a)
                self.assertEqual(expected_payout_b, payout_b)
                
                
class TestFunctionsSelfMemoryOn(unittest.TestCase):
    def setUp(self):
        pd_org.MAX_BITS_OF_MEMORY = 4
        pd_tournament.NUMBER_OF_ROUNDS = 2
        pd_tournament.TOGGLE_SELF_MEMORY_ON = True
        self.organism_a = pd_org.PDOrg(pd_org.MemoryPDGenotype(1,[True, False], [False]))
        self.organism_b = pd_org.PDOrg(pd_org.MemoryPDGenotype(2,[True, False, False, True], [False, True]))
        
        
    
    def test_run_game(self):
        total_payout_a, total_payout_b = pd_tournament.run_game(self.organism_a, self.organism_b)
        expected_total_payout_a = 0
        expected_total_payout_b = 10
        self.assertEqual(expected_total_payout_a, total_payout_a)
        self.assertEqual(expected_total_payout_b, total_payout_b)
        
    def test_adj_payout(self):
        adj_payout_a, adj_payout_b = pd_tournament.adjusted_payout(self.organism_a, self.organism_b)
        expected_adj_payout_a = 0
        expected_adj_payout_b = 9.8
        self.assertAlmostEqual(expected_adj_payout_a, adj_payout_a, 2)
        self.assertAlmostEqual(expected_adj_payout_b, adj_payout_b, 2)
                
    def test_get_average_payouts(self):
        organisms = [self.organism_a, self.organism_b]
        pd_tournament.get_average_payouts(organisms)
        actual_payout_a = self.organism_a.average_payout
        actual_payout_b = self.organism_b.average_payout
        expected_payout_a = 0
        expected_payout_b = 9.8
        self.assertEqual(expected_payout_a, actual_payout_a)
        self.assertEqual(expected_payout_b, actual_payout_b)
       
        organisms = [self.organism_a, self.organism_b, self.organism_a]
        pd_tournament.get_average_payouts(organisms)
        actual_payout_a = self.organism_a.average_payout
        actual_payout_b = self.organism_b.average_payout
        expected_payout_a = 1.98
        expected_payout_b = 9.8
        self.assertEqual(expected_payout_a, actual_payout_a)
        self.assertEqual(expected_payout_b, actual_payout_b)

class TestFunctionsSelfMemoryOff(unittest.TestCase):
    def setUp(self):
        pd_org.MAX_BITS_OF_MEMORY = 4
        pd_tournament.NUMBER_OF_ROUNDS = 2
        pd_tournament.TOGGLE_SELF_MEMORY_ON = False
        self.organism_a = pd_org.PDOrg(pd_org.MemoryPDGenotype(1,[True, False], [False]))
        self.organism_b = pd_org.PDOrg(pd_org.MemoryPDGenotype(2, [True, False, False, True], [False, True]))
        
    def test_run_game(self):
        total_payout_a, total_payout_b = pd_tournament.run_game(self.organism_a, self.organism_b)
        expected_total_payout_a = 3
        expected_total_payout_b = 8
        self.assertEqual(expected_total_payout_a, total_payout_a)
        self.assertEqual(expected_total_payout_b, total_payout_b)
    
    def test_adj_payout(self):
        adj_payout_a, adj_payout_b = pd_tournament.adjusted_payout(self.organism_a, self.organism_b)
        expected_adj_payout_a = 2.97
        expected_adj_payout_b = 7.84
        self.assertAlmostEqual(expected_adj_payout_a, adj_payout_a, 2)
        self.assertAlmostEqual(expected_adj_payout_b, adj_payout_b, 2)
      
    def test_get_average_payouts(self):
        organisms = [self.organism_a, self.organism_b]
        pd_tournament.get_average_payouts(organisms)
        actual_payout_a = self.organism_a.average_payout
        actual_payout_b = self.organism_b.average_payout
        expected_payout_a = 2.97
        expected_payout_b = 7.84
        self.assertAlmostEqual(expected_payout_a, actual_payout_a, 2)
        self.assertEqual(expected_payout_b, actual_payout_b)
       
        organisms = [self.organism_a, self.organism_b, self.organism_a]
        pd_tournament.get_average_payouts(organisms)
        actual_payout_a = self.organism_a.average_payout
        actual_payout_b = self.organism_b.average_payout
        expected_payout_a = 3.46
        expected_payout_b = 7.84
        self.assertAlmostEqual(expected_payout_a, actual_payout_a, 2)
        self.assertEqual(expected_payout_b, actual_payout_b)
    
    def test_get_static_payouts(self):
        org_a = pd_org.PDOrg(pd_org.MemoryPDGenotype(0, [True], []))
        org_b = pd_org.PDOrg(pd_org.MemoryPDGenotype(0, [False], []))
        static_competitors = [org_a, org_b]
        organisms = [org_a, org_b]
        
        pd_tournament.get_static_payouts(organisms, static_competitors)
        org_a_expected = 3.0
        org_b_expected = 6.0

        self.assertAlmostEqual(org_a_expected, org_a.average_payout, 2)
        self.assertAlmostEqual(org_b_expected, org_b.average_payout, 2)

    def test_get_static_fitness(self):

        org_a = pd_org.PDOrg(pd_org.MemoryPDGenotype(0, [True], []))
        org_b = pd_org.PDOrg(pd_org.MemoryPDGenotype(0, [False], []))
        org_c = pd_org.PDOrg(pd_org.MemoryPDGenotype(0, [True], []))
        org_d = pd_org.PDOrg(pd_org.MemoryPDGenotype(0, [False], []))
        static_competitors = [org_a, org_b]
        organisms = [org_c, org_d]

        org_a_expected = 3.0
        org_b_expected = 6.0

        org_a_result = pd_tournament.get_static_fitness(org_a, static_competitors)
        org_b_result = pd_tournament.get_static_fitness(org_b, static_competitors)

        self.assertAlmostEqual(org_a_expected, org_a_result, 2)
        self.assertAlmostEqual(org_b_expected, org_b_result, 2)

if __name__ == "__main__":
    unittest.main()
