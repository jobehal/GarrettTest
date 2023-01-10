from main import PhoneBill
import unittest   # The test framework

class Test_TestIncrementDecrement(unittest.TestCase):
    def test_increment(self):
        self.assertEqual(PhoneBill.calculate(r"E:\Projekty\Garrett_Test\moje\generated_sample_2.csv"), 659.2)

if __name__ == '__main__':
    unittest.main()
