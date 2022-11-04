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
            Test get /home route
        -OK: Status code 200
        """
        r = self.app.get('/home')
        self.assertEqual(r.status_code, 200)

    def test_get_results_endpoint(self):
        """
            Test get /results route
        -OK: Status code 200
        """
        r = self.app.get('/results')
        self.assertEqual(r.status_code, 200)

    def test_get_doc_main_endpoint(self):
        """
            Test get documentation main route
        -OK: Status code 200
        """
        r = self.app.get('/doc/')
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()
