import unittest
from calculator import Calculator

class TestOperations(unittest.TestCase):
    
    # ARRANGE, ACT and ASSERT <- General template

    def test_sum(self):
        #ARRANGE
        testCal = Calculator(8,2)
        #ACT & ASSERT
        self.assertEqual(testCal.get_sum(), 10, "The sum is wrong")

    def test_difference(self):
        #ARRANGE
        testCal = Calculator(8,2)
        #ACT & ASSERT
        self.assertEqual(testCal.get_difference(), 6, "The difference is wrong")

    def test_product(self):
        #ARRANGE
        testCal = Calculator(8,2)
        #ACT & ASSERT
        self.assertEqual(testCal.get_product(), 16, "The product is wrong")

    def test_division(self):
        #ARRANGE
        testCal = Calculator(8,2)
        #ACT & ASSERT
        self.assertEqual(testCal.get_division(), 4, "The division is wrong")

if __name__ == "__main__":
    unittest.main()
