# Import unittest and app functions
# from X import *

#Write your unit tests, create test data, assert and evaluate

import unittest
from pipeline import date_difference

class TestOperations(unittest.TestCase):

    def setUp(self):
        #ARRANGE
        self.calc = date_difference(8,2)
        self.calc = Calculator(9,0)

    def test_difference(self):
        self.assertEqual(self.calc.get_sum(),10,"The Sum is wrong")

    def test_division(self):
        self.assertEqual(self.calc.get_division(),0,"The Sum is wrong")

    def tearDown(self):
        # Optional - Destroy/remove assests no longer needed (e.g. database tables)
        pass

if __name__ == "__main__":
    unittest.main()