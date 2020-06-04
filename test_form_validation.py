import unittest
from form_validation import buggy_validation

class validationTest(unittest.TestCase):


    def setUp(self):
        # perfect buggy using default values should pass every test
        self.test_buggy1 = buggy_validation([4, 'petrol', 1, 'none', 0, 0, 'white', 'plain', 'black', 'knobbly', 4, 'none', 'none', 0, 'false', 'false','false', 'false', 'steady'])
        #Buggy valid to games rules with more customisation than default buggy
        self.test_buggy2 = buggy_validation([12, 'rocket', 4, 'wind', 1, 0, 'blue', 'dstripe', 'red', 'maglev', 18, 'titanium', 'flame', 2, 'false', 'true','false', 'true', 'titfortat'])
        #buggy testing when an odd number of wheels
        self.test_buggy3 = buggy_validation([5, 'petrol', 1, 'none', 0, 0, 'white', 'plain', 'black', 'knobbly', 4, 'none', 'none', 0, 'false', 'false','false', 'false', 'steady'])
        #Buggy with wheels less than 4 but still an even number
        self.test_buggy4 = buggy_validation([2, 'petrol', 1, 'none', 0, 0, 'white', 'plain', 'black', 'knobbly', 4, 'none', 'none', 0, 'false', 'false','false', 'false', 'steady'])
        #Buggy with two fuel identical fuel types
        self.test_buggy5 = buggy_validation([4, 'petrol', 1, 'petrol', 1, 0, 'white', 'plain', 'black', 'knobbly', 4, 'none', 'none', 0, 'false', 'false','false', 'false', 'steady'])
        #Buggy with a secondary fuel type but no quantity of fuel
        self.test_buggy6 = buggy_validation([4, 'petrol', 1, 'petrol', 0, 0, 'white', 'plain', 'black', 'knobbly', 4, 'none', 'none', 0, 'false', 'false','false', 'false', 'steady'])
        #A buggy with the primary and secondary colour the same and a flag type not plain
        self.test_buggy7 = buggy_validation([4, 'petrol', 1, 'none', 0, 0, 'white', 'dstripe', 'white', 'knobbly', 4, 'none', 'none', 0, 'false', 'false','false', 'false', 'steady'])
        #Buggy with less tyres than there are wheels
        self.test_buggy8 = buggy_validation([6, 'petrol', 1, 'none', 0, 0, 'white', 'plain', 'black', 'knobbly', 4, 'none', 'none', 0, 'false', 'false','false', 'false', 'steady'])
        #A buggy with non-consumable power types which have a quantity more than 1
        self.test_buggy9 = buggy_validation([4, 'wind', 4, 'none', 0, 0, 'white', 'plain', 'black', 'knobbly', 4, 'none', 'none', 0, 'false', 'false','false', 'false', 'steady'])
        #A buggy which should fail all of the possible tests
        self.test_buggy10 = buggy_validation([4, 'petrol', 1, 'none', 0, 0, 'white', 'plain', 'black', 'knobbly', 4, 'none', 'none', 0, 'false', 'false','false', 'false', 'steady'])


    def test_numerical(self):
        self.assertEqual(self.test_buggy1.numerical_test(),'success')
        self.assertEqual(self.test_buggy2.numerical_test(),'success')
        self.assertEqual(self.test_buggy3.numerical_test(),'fail')
        self.assertEqual(self.test_buggy4.numerical_test(),'fail')
        self.assertEqual(self.test_buggy5.numerical_test(),'success')
        self.assertEqual(self.test_buggy6.numerical_test(),'success')
        self.assertEqual(self.test_buggy7.numerical_test(),'success')
        self.assertEqual(self.test_buggy8.numerical_test(),'fail')
        self.assertEqual(self.test_buggy9.numerical_test(),'success')
    def test_comparison(self):
        self.assertEqual(self.test_buggy1.comparison_test(),'success')
        self.assertEqual(self.test_buggy2.comparison_test(),'success')
        self.assertEqual(self.test_buggy3.comparison_test(),'success')
        self.assertEqual(self.test_buggy4.comparison_test(),'success')
        self.assertEqual(self.test_buggy5.comparison_test(),'fail')
        self.assertEqual(self.test_buggy6.comparison_test(),'fail')
        self.assertEqual(self.test_buggy7.comparison_test(),'fail')
        self.assertEqual(self.test_buggy8.comparison_test(),'success')
        self.assertEqual(self.test_buggy9.comparison_test(),'success')
    def test_hamster(self):
        self.assertEqual(self.test_buggy1.hamster_test(),'success')
        self.assertEqual(self.test_buggy2.hamster_test(),'success')
        self.assertEqual(self.test_buggy3.hamster_test(),'success')
        self.assertEqual(self.test_buggy4.hamster_test(),'success')
        self.assertEqual(self.test_buggy5.hamster_test(),'success')
        self.assertEqual(self.test_buggy6.hamster_test(),'success')
        self.assertEqual(self.test_buggy7.hamster_test(),'success')
        self.assertEqual(self.test_buggy8.hamster_test(),'success')
        self.assertEqual(self.test_buggy9.hamster_test(),'success')
    def test_consumable(self):
        self.assertEqual(self.test_buggy1.consumable_test(),'success')
        self.assertEqual(self.test_buggy2.consumable_test(),'success')
        self.assertEqual(self.test_buggy3.consumable_test(),'success')
        self.assertEqual(self.test_buggy4.consumable_test(),'success')
        self.assertEqual(self.test_buggy5.consumable_test(),'success')
        self.assertEqual(self.test_buggy6.consumable_test(),'success')
        self.assertEqual(self.test_buggy7.consumable_test(),'success')
        self.assertEqual(self.test_buggy8.consumable_test(),'success')
        self.assertEqual(self.test_buggy9.consumable_test(),'fail')


if __name__ == '__main__':
    unittest.main()