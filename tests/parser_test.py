import unittest
from tests.testhelpers import testfile

import parser

class ReferenceBNFExtraction(unittest.TestCase):
    def test_single_dict_key_single_quotes(self):
        reference = "['mykey1']"
        expected = [["[", "mykey1", "]"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted)

    def test_single_dict_key_double_quotes(self):
        reference = '["mykey1"]'
        expected = [["[", "mykey1", "]"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted)

    def test_multiple_dict_keys_single_quotes(self):
        reference = "['mykey1']['myinnerkey2']"
        expected = [["[", "mykey1", "]"], ["[", "myinnerkey2", "]"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted)

    def test_multiple_dict_keys_double_quotes(self):
        reference = '["mykey1"]["myinnerkey2"]'
        expected = [["[", "mykey1", "]"], ["[", "myinnerkey2", "]"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted)

    def test_many_dict_keys(self):
        reference = "['mykey1']['myinnerkey2']['evendeeper3']"
        expected = [["[", "mykey1", "]"], ["[", "myinnerkey2", "]"], 
                ["[", "evendeeper3", "]"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted)

class ReferenceValueExtraction(unittest.TestCase):
    def test_extract_simple_key_value_pair(self):
        rawJSON = testfile("simple_json_1.txt")
        reference = '${{mykey1}}$'
        expected = "myvalue1"
        extracted = parser.extract_reference_value_from_json(reference, rawJSON)
        self.assertEqual(expected, extracted)

class JSONParserTest(unittest.TestCase):
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


