import main
import unittest

class TestMainModule(unittest.TestCase):
    
    def test_get_fitness_perfect(self):
        fitness = main.get_fitness(main.TARGET_STRING)
        self.assertEqual(fitness, len(main.TARGET_STRING))

    def test_get_fitness_worst(self):
        terrible_org = "0" * len(main.TARGET_STRING)
        fitness = main.get_fitness(terrible_org)
        self.assertEqual(fitness, 0)

    def test_get_fitness_one_off(self):
        one_off = main.TARGET_STRING[:-1] + "0"
        fitness = main.get_fitness(one_off)
        self.assertEqual(fitness, len(main.TARGET_STRING) - 1)


if __name__ == "__main__":
    unittest.main()
