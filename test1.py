from objects import CFR
import unittest

class TestCFR(unittest.TestCase):
    def test_setRate(self):
        car = CFR()
        car.setRate(days=7, rate=120)
        self.assertEqual(car.rate7, 120)

if __name__ == '__main__':
    unittest.main()