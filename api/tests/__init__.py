import unittest
import os
from dotenv import load_dotenv
load_dotenv()
# Only if using a Raspberry device, the tests are trigger (library conflicts)
if os.environ['DEVICE'] == 'RASPBERRY':
    from tests.raspberry_test import RaspberryTest
    from restapi_test import RestAPITest
else:
    from restapi_test import RestAPITest

if __name__ == '__main__':

    unittest.main()
