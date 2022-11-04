import unittest
from api.raspberrypi import Raspberry


class RaspberryTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(RaspberryTest, self).__init__(*args, **kwargs)
        self.raspberry = Raspberry()

    def test_singleton(self):
        """
            Test the singleton pattern of the class Raspberry
        -OK: Every Raspberry instance created is the same, only one unique instance can be created
        """
        r1 = Raspberry()
        r2 = Raspberry()
        self.assertTrue(r1 == r2)

    def test_get_device(self):
        """
            Test the device name of the Raspberry object
        -OK: Device name 'raspberry'
        """
        self.assertTrue(self.raspberry.device == 'raspberry')


if __name__ == '__main__':
    unittest.main()
