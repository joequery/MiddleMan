import unittest
from tests.testhelpers import testfile

import parser

class JSONParserTest(unittest.TestCase):
    def test_trim_json_whitespace(self):
        ipJSON = testfile("httpbinIP.txt")
        expected = '{"origin": "74.192.112.168"}'
        trimmedJSON = parser.trim_json_whitespace(ipJSON)
        self.assertEqual(expected, trimmedJSON)
