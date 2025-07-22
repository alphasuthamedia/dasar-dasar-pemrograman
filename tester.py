import unittest
import tkinter as tk
from unittest.mock import patch
import C_KM_AlphaSuthaMedia_2306275935_TP04 as fileCode

class TestMainApp(unittest.TestCase):
    def setUp(self):
        self.app = fileCode
    
    # test if output of checkSumCalculation() is correct
    def test_calculate_checksum(self):
        self.assertEqual(self.app.checkSumCalculation("123456789012"), 8)
        self.assertEqual(self.app.checkSumCalculation("230627505203"), 3)

    # test if input is valid
    def test_input_valid(self):
        self.assertEqual(self.app.inputChecker("123456789012"), True)
        self.assertEqual(self.app.inputChecker("230627505203"), True)
    
    # test if input is not valid and rejected
    def test_input_not_valid(self):
        self.assertEqual(self.app.inputChecker("somealphabetic"), False)
        self.assertEqual(self.app.inputChecker("somealphanumeric01"), False)


if __name__ == '__main__':
    unittest.main()
