import unittest
import app as tested_app


class RestAPITest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(RestAPITest, self).__init__(*args, **kwargs)

    def setUp(self):
        """
            Test initial setup of the flask app
        -OK: Set up is fine
        """
        tested_app.app.config['TESTING'] = True
        self.app = tested_app.app.test_client()

    def test_get_homepage(self):
        """
            Test get / route
        -OK: Status code 200
        """
        r = self.app.get('/')
        self.assertEqual(r.status_code, 200)

    def test_get_pc1(self):
        """
            Test get /devices/pc1 route
        -OK: Status code 200
        """
        r = self.app.get('/devices/pc1')
        self.assertEqual(r.status_code, 200)

    # TODO: Uncomment when data available in DynamoDb
    # def test_get_pc1_status(self):
    #     """
    #         Test get /devices/pc1/status route
    #     -OK: Status code 200
    #     """
    #     r = self.app.get('/devices/pc1/status')
    #     self.assertEqual(r.status_code, 200)

    def test_get_pc2(self):
        """
            Test get /devices/pc2 route
        -OK: Status code 200
        """
        r = self.app.get('/devices/pc2')
        self.assertEqual(r.status_code, 200)

    # TODO: Uncomment when data available in DynamoDb
    # def test_get_pc2_status(self):
    #     """
    #         Test get /devices/pc2/status route
    #     -OK: Status code 200
    #     """
    #     r = self.app.get('/devices/pc2/status')
    #     self.assertEqual(r.status_code, 200)

    def test_get_raspberry(self):
        """
            Test get /devices/raspberry route
        -OK: Status code 200
        """
        r = self.app.get('/devices/raspberry')
        self.assertEqual(r.status_code, 200)

    def test_get_raspberry_status(self):
        """
            Test get /devices/raspberry/status route
        -OK: Status code 200
        """
        r = self.app.get('/devices/raspberry/status')
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()
