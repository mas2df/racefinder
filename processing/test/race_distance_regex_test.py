import unittest
from processing.utils import getDistanceAndType, getDistanceUnitAndType

data = [
["5K run", "5", "K", "run"],
["10K run", "10", "K", "run"],
["8K run", "8", "K", "run"],
["5K novelty run", "5", "K", "novelty run"],
["5K walk", "5", "K", "walk"],
["1M fun run", "1", "M", "fun run"],
["1M walk", "1", "M", "walk"],
["13.1M run", "13.1", "M", "run"],
["27.2M trail run", "27.2", "M", "trail run"],
["fun run", "", "", "fun run"],
["triathlon", "", "", "triathlon"],
["kid's run", "", "", "kid's run"],
["track meet", "", "", "track meet"],
["track-meet", "", "", "track-meet"],
]

class MyTest(unittest.TestCase):
    def test_getDistanceUnitAndType(self):
        for test_data in data:
            print "Testing: " + test_data[0]

            result = getDistanceUnitAndType(test_data[0])

            self.assertEqual(test_data[1], result[0])
            self.assertEqual(test_data[2], result[1])
            self.assertEqual(test_data[3], result[2])

    def test_getDistanceAndType(self):
        for test_data in data:
            print "Testing: " + test_data[0]

            result = getDistanceAndType(test_data[0])

            if test_data[1] and test_data[2]:
                self.assertEqual((test_data[1] + " " + test_data[2]), result[0])
            else:
                self.assertEqual("", result[0])
            self.assertEqual(test_data[3], result[1])