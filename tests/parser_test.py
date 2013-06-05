import unittest
from tests.testhelpers import testfile

import parser

class ReferenceBNFExtractionSimple(unittest.TestCase):
    """
    Test simple dictionary references
    """
    def test_single_dict_key_single_quotes(self):
        reference = "['mykey1']"
        expected = [["mykey1"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("dict", e.getName())

    def test_single_dict_key_double_quotes(self):
        reference = '["mykey1"]'
        expected = [["mykey1"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("dict", e.getName())

    def test_multiple_dict_keys_single_quotes(self):
        reference = "['mykey1']['myinnerkey2']"
        expected = [["mykey1"], ["myinnerkey2"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("dict", e.getName())

    def test_multiple_dict_keys_double_quotes(self):
        reference = '["mykey1"]["myinnerkey2"]'
        expected = [["mykey1"], ["myinnerkey2"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("dict", e.getName())

    def test_many_dict_keys(self):
        reference = "['mykey1']['myinnerkey2']['evendeeper3']"
        expected = [["mykey1"],["myinnerkey2"],["evendeeper3"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("dict", e.getName())

    """
    Test simple index references
    """
    def test_single_index(self):
        reference = "[10]"
        expected = [["10"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("index", e.getName())

    def test_multiple_indexes(self):
        reference = "[10][20]"
        expected = [["10"], ["20"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("index", e.getName())

    """
    Test simple subrange references
    """
    def test_single_subrange_with_both_numbers(self):
        reference = "[10:20]"
        expected = [["10", ":", "20"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("subrange", e.getName())

    def test_single_subrange_with_negative_second_number(self):
        reference = "[10:-20]"
        expected = [["10", ":", "-20"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("subrange", e.getName())

    def test_single_subrange_with_blank_first_number(self):
        reference = "[:10]"
        expected = [[":", "10"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("subrange", e.getName())

    def test_single_subrange_with_blank_first_number_negative_second_number(self):
        reference = "[:-10]"
        expected = [[":", "-10"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("subrange", e.getName())

    def test_single_subrange_with_blank_second_number(self):
        reference = "[10:]"
        expected = [["10", ":"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("subrange", e.getName())

    def test_single_subrange_with_no_numbers(self):
        reference = "[:]"
        expected = [[":"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("subrange", e.getName())

    """
    Test simple subdict references
    """
    def test_subdict_with_one_key(self):
        reference = "{'mykey1'}"
        expected = [["mykey1"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("subdict", e.getName())

    def test_subdict_with_one_key_with_dbl_quotes(self):
        reference = '{"mykey1"}'
        expected = [["mykey1"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("subdict", e.getName())

    def test_subdict_with_two_keys_no_spaces(self):
        reference = "{'mykey1','mykey2'}"
        expected = [["mykey1", "mykey2"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("subdict", e.getName())

    def test_subdict_with_two_keys_with_spaces(self):
        reference = "{'mykey1', 'mykey2'}"
        expected = [["mykey1", "mykey2"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("subdict", e.getName())

class ReferenceBNFExtractionIntegration(unittest.TestCase):
    """
    Test complex combinations of references
    """
    def test_index_after_simple_dict(self):
        reference = "['mykey1'][5]"
        expected = [["mykey1"], ["5"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())

        expectedTypes = ["dict", "index"]
        
        for i,e in enumerate(extracted):
            self.assertEqual(expectedTypes[i], e.getName())


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


