import unittest

from TDD import TDD


class TestDataSource(unittest.TestCase):
    def setUp(self):
        self.TDD = TDD()

    def test_valid_state(self):
        state = 'Alabama'
        self.assertTrue(self.TDD.checkValidState(state))

    def test_invalid_state(self):
        state = 'Canada'
        self.assertFalse(self.TDD.checkValidState(state))

    def test_valid_case_type(self):
        covid_type = 'Confirmed'
        self.assertTrue(self.TDD.checkValidType(covid_type))

    def test_invalid_case_type(self):
        covid_type = 'Back from the dead'
        self.assertFalse(self.TDD.checkValidType(covid_type))
        

    def test_valid_date(self):
        date = "07-04-1200"
        self.assertTrue(self.TDD.checkIsDate(date))

    def test_invalid_date(self):
        date = "abc-d145"
        self.assertFalse(self.TDD.checkIsDate(date))

if __name__ == '__main__':
    unittest.main()