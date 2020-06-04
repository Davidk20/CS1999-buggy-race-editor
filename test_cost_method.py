import unittest
from cost_method import cost_method

class costTest(unittest.TestCase):

    def setUp(self):
        #buggy using default values
        self.test_buggy1 = cost_method([4, 'petrol', 1, 'none', 0, 0, 'white', 'plain', 'black', 'knobbly', 4, 'none', 'none', 0, 'false', 'false','false', 'false', 'steady'])
        #buggy where all categories are used with varying values
        self.test_buggy2 = cost_method([8, 'fusion', 1, 'hamster', 8, 5, 'white', 'dstripe', 'black', 'reactive', 10, 'aluminium', 'charge', 5, 'true', 'true','true', 'true', 'titfortat'])
        #buggy where all categories are used with default values
        self.test_buggy3 = cost_method([4, 'fusion', 1, 'solar', 1, 0, 'white', 'dstripe', 'black', 'maglev', 4, 'wood', 'biohazard', 1, 'true', 'true','true', 'true', 'titfortat'])
        #buggy with random values
        self.test_buggy4 = cost_method([8, 'electric', 3, 'wind', 1, 0, '#0400ff', 'hstripe', '#bbff00', 'steelband', 10, 'thinsteel', 'flame', 7, 'true', 'false','false', 'true', 'defensive'])


    def test_cost(self):
        self.assertEqual(self.test_buggy1.buggy_cost(), (64,82))
        self.assertEqual(self.test_buggy2.buggy_cost(), (1571,503))
        self.assertEqual(self.test_buggy3.buggy_cost(), (1012,360))
        self.assertEqual(self.test_buggy4.buggy_cost(), (672,734))


if __name__ == '__main__':
    unittest.main()