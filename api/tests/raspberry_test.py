import unittest
from raspberrypi import Raspberry


class RaspberryTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(RaspberryTest, self).__init__(*args, **kwargs)
        self.raspberry = Raspberry()

    def test_get_uuid(self):
        """
            Test the Raspberry Pi object has an uuid attribute (partition key in DynamoDB)
        -OK: uuid exists
        """
        self.assertTrue(self.raspberry.uuid)

    def test_get_device(self):
        """
            Test the device name of the Raspberry object (sort key in DynamoDB)
        -OK: Device name 'raspberry'
        """
        self.assertTrue(self.raspberry.device == 'raspberry')

    def test_get_throttled(self):
        """
            Test the Raspberry Pi object has a throttled attribute
        -OK: throttled exists
        """
        self.assertTrue(self.raspberry.throttled)


if __name__ == '__main__':
    unittest.main()
