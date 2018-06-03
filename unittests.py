import unittest
import os
from Iterate import checkout
import requests
import understand

class TestOurCodeALittle(unittest.TestCase):
    """
    Our basic test class
    """

    def test_checkout(self):
        """
        The actual test.
        Any method which starts with ``test_`` will considered as a test case.
        """
        result = checkout(os.getcwd() + '/new/java', 'b2e28785163e6614cc64e0f08fe723807d27fd0f')
        self.assertIsNone(result)

    def test_check_github(self):
    	r = requests.get('https://api.github.com/repos/structurizr/java/pulls', auth=('', ''))
    	self.assertTrue(r.ok)

    def test_udb(self):
        os.system('und create -db new1.udb -languages java') # create understand database for newer version
        os.system('und create -db old1.udb -languages java') # create understand database for older version

        os.system('und -db new1.udb add ' + os.getcwd() + '/new/java')   # add/update newer version
        os.system('und -db old1.udb add ' + os.getcwd() + '/old/java')   # add/update older version

        try:
            os.system('und -quiet analyze new1.udb') #analyze udb to add files into the udb object.
            os.system('und -quiet analyze old1.udb')
        except Exception as e:
            print("Cannot analyze data!")
			

        old1db = understand.open(os.getcwd() + '/old1.udb') #open the udb object.
        new1db = understand.open(os.getcwd() + '/new1.udb')

        self.assertIsNotNone(new1db)

if __name__ == '__main__':
    	unittest.main()

