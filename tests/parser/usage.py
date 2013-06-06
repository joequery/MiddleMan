# Tests that demonstrate direct usage of the parser and the reference grammar
# for substituting JSON values
import unittest
from tests.testhelpers import testfile
import parser

class ReferenceUsage(unittest.TestCase):
    def test_extract_references_simple(self):
        scheme = testfile("simple_scheme_1.txt")
        references = parser.extract_references(scheme)
        expected = ['${{mykey1}}$', '${{timezone}}$']
        self.assertListEqual(expected, references)

    def test_apply_scheme_to_json_simple(self):
        scheme = testfile("simple_scheme_1.txt")
        rawJSON = testfile("simple_json_1.txt")

        jsonAfterApplication = parser.apply_scheme_to_json(scheme, rawJSON)
        expected = {
            "key1": "myvalue1", 
            "key2": "some hardcoded value", 
            "time": "US/Central"
        }

        self.assertDictEqual(expected, jsonAfterApplication)

    def test_extract_simple_key_value_pair(self):
        rawJSON = testfile("simple_json_1.txt")
        reference = '${{mykey1}}$'
        expected = "myvalue1"
        extracted = parser.extract_reference_value_from_json(reference, rawJSON)
        self.assertEqual(expected, extracted)

