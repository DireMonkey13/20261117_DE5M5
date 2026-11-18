# Import unittest and app functions
# from X import *

#Write your unit tests, create test data, assert and evaluate

import unittest
import pandas as pd
from pipeline import missing_values, remove_quotes, date_difference

class TestOperations(unittest.TestCase):

    def setUp(self):
        #ARRANGE

        # NOTE: Setup tests here at the top of the code to make changes easier

        ### TEST: date_difference()
        # Test dataframe for date differences 
        self.df = pd.DataFrame({
            "Book checkout": ["01/11/2026","05/11/2026","10/11/2026"],
            "Book Returned": ["10/11/2026","05/11/2026","01/11/2026"]
        })

        ### TEST: remove_quotes()
        # Test quotes are removed
        self.quote_value = '"""02/04/2024"""'

        ### TEST: missing_values()
        # Test missing values reported correctly
        self.row_with_null = pd.Series(["Book A", None, 123])
        self.row_without_null = pd.Series(["Book A", "01/11/2026", 123])



    def test_missing_values_true(self):

        # Test missing value correctly detected

        # ARRANGE
        #row = pd.Series(["Book A", None, 123])

        # ACT
        result = missing_values(self.row_with_null)

        #ASSERT
        self.assertTrue( result, "Missing value was not detected")

    def test_missing_values_false(self):

        # Test no missing values detected when row fully populated

        # ARRANGE
        #row = pd.Series(["Book A", "01/11/2026", 123])

        # ACT
        result = missing_values(self.row_without_null)

        #ASSERT
        self.assertFalse( result, "Missing value incorrectly detected")

    def test_remove_quotes(self):

        # Test quotes have been removed from test string

        # ARRANGE
        #value = '"""02/04/2024"""'

        # ACT
        result = remove_quotes(self.quote_value)

        #ASSERT
        self.assertEqual( result, "02/04/2024","Quotes not removed correctly")

    def test_date_difference(self):

        # ACT
        result = date_difference( self.df, "Book checkout","Book Returned","Days Borrowed")

        #ASSERT
        # Note: The test was failing so I added the print statement to find out what it was returning
        #       Turns out the function was using american date format so the function has been amended
        #       to force uk dates
        print( "Returned Days Borrowed:", result["Days Borrowed"].iloc[0])
        self.assertEqual( result["Days Borrowed"].iloc[0], 9, "Date difference is incorrect")
        
        
    def test_same_date_difference(self):

        # ACT
        result = date_difference( self.df, "Book checkout","Book Returned","Days Borrowed")

        #ASSERT
        print( "Returned Days Borrowed:", result["Days Borrowed"].iloc[1])
        self.assertEqual( result["Days Borrowed"].iloc[1], 0, "Date difference is incorrect")

    def test_negative_date_difference(self):

        # ACT
        result = date_difference( self.df, "Book checkout","Book Returned","Days Borrowed")

        #ASSERT
        print( "Returned Days Borrowed:", result["Days Borrowed"].iloc[2])
        self.assertEqual( result["Days Borrowed"].iloc[2], -9, "Date difference is incorrect")

    def tearDown(self):
        # Remove assets no longer needed
        pass


if __name__ == "__main__":
    unittest.main()