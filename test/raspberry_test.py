import unittest
from raspberrypi.raspberry_singleton import Raspberry


class RaspberryTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(RaspberryTest, self).__init__(*args, **kwargs)

    def test_singleton(self):
        """
            Test the singleton pattern of the class Raspberry
        -OK: Every Raspberry instance created is the same, only one unique instance can be created
        """
        r1 = Raspberry()
        r2 = Raspberry()
        self.assertTrue(r1 == r2)


if __name__ == '__main__':
    unittest.main()
