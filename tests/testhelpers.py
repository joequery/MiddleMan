# Convenient functions for testing
import os
import unittest

import middleman

def testfile(path):
    txt = ""
    with open(os.path.join("tests", "testfiles", path)) as f:
        txt = f.read()
    return txt



class MMTestCase(unittest.TestCase):
    '''
    Default middleMan test case
    '''

    def setUp(self):
        self.client = middleman.app.test_client()
