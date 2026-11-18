import unittest
from calculator import Calculator

class TestOperations(unittest.TestCase):

    def setUp(self):
        #ARRANGE
        self.calc = Calculator(8,2)
        self.calc = Calculator(9,0)

    def test_sum(self):
        self.assertEqual(self.calc.get_sum(),10,"The Sum is wrong")

    def test_division(self):
        self.assertEqual(self.calc.get_division(),0,"The Sum is wrong")

    def tearDown(self):
        # Optional - Destroy/remove assests no longer needed (e.g. database tables)
        pass

if __name__ == "__main__":
    unittest.main()

#Testing change