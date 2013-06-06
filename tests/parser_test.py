import unittest
from tests.testhelpers import testfile

from pyparsing import ParseException
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
    Test simple sublist references
    """
    def test_single_sublist_with_both_numbers(self):
        reference = "[10:20]"
        expected = [["10", ":", "20"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("sublist", e.getName())

    def test_single_sublist_with_negative_second_number(self):
        reference = "[10:-20]"
        expected = [["10", ":", "-20"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("sublist", e.getName())

    def test_single_sublist_with_blank_first_number(self):
        reference = "[:10]"
        expected = [[":", "10"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("sublist", e.getName())

    def test_single_sublist_with_blank_first_number_negative_second_number(self):
        reference = "[:-10]"
        expected = [[":", "-10"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("sublist", e.getName())

    def test_single_sublist_with_blank_second_number(self):
        reference = "[10:]"
        expected = [["10", ":"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("sublist", e.getName())

    def test_single_sublist_with_no_numbers(self):
        reference = "[:]"
        expected = [[":"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("sublist", e.getName())

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

    def test_simple_dict_after_index(self):
        reference = "[5]['mykey1']"
        expected = [["5"], ["mykey1"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())

        expectedTypes = ["index", "dict"]
        
        for i,e in enumerate(extracted):
            self.assertEqual(expectedTypes[i], e.getName())

    def test_subdict_after_dict(self):
        reference = "['mykey1']{'innerkey1', 'innerkey2'}"
        expected = [["mykey1"], ["innerkey1", "innerkey2"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())

        expectedTypes = ["dict", "subdict"]
        
        for i,e in enumerate(extracted):
            self.assertEqual(expectedTypes[i], e.getName())

    def test_subdict_after_sublist(self):
        reference = "[1:5]{'innerkey1', 'innerkey2'}"
        expected = [["1", ":", "5"], ["innerkey1", "innerkey2"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())

        expectedTypes = ["sublist", "subdict"]
        
        for i,e in enumerate(extracted):
            self.assertEqual(expectedTypes[i], e.getName())

    def test_sublist_after_subdict(self):
        reference = "{'innerkey1', 'innerkey2'}[1:5]"
        expected = [["innerkey1", "innerkey2"], ["1", ":", "5"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())

        expectedTypes = ["subdict", "sublist"]
        
        for i,e in enumerate(extracted):
            self.assertEqual(expectedTypes[i], e.getName())

    def test_dict_sublist_dict_index(self):
        reference = "['mykey1'][4:]['myinnerkey'][-1]"
        expected = [["mykey1"], ["4", ":"], ["myinnerkey"], ["-1"]]
        extracted = parser.extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())

        expectedTypes = ["dict", "sublist", "dict", "index"]
        
        for i,e in enumerate(extracted):
            self.assertEqual(expectedTypes[i], e.getName())


class ReferenceBNFExtractionErrors(unittest.TestCase):
    """
    Test errors with simple dicts
    """
    def test_dict_without_closing_bracket(self):
        with self.assertRaises(ParseException):
            reference = "['mykey1'"
            parser.extract_reference_parts(reference)

    def test_dict_without_opening_bracket(self):
        with self.assertRaises(ParseException):
            reference = "'mykey1']"
            parser.extract_reference_parts(reference)

    def test_dict_without_any_brackets(self):
        with self.assertRaises(ParseException):
            reference = "'mykey1'"
            parser.extract_reference_parts(reference)

    def test_dict_without_opening_quote(self):
        with self.assertRaises(ParseException):
            reference = "[mykey1']"
            parser.extract_reference_parts(reference)

    def test_dict_without_closing_quote(self):
        with self.assertRaises(ParseException):
            reference = "['mykey1]"
            parser.extract_reference_parts(reference)

    def test_dict_without_any_quotes(self):
        with self.assertRaises(ParseException):
            reference = "[mykey1]"
            parser.extract_reference_parts(reference)

    """
    Test errors with simple indexes
    """
    def test_index_without_opening_bracket(self):
        with self.assertRaises(ParseException):
            reference = "1]"
            parser.extract_reference_parts(reference)

    def test_index_without_closing_bracket(self):
        with self.assertRaises(ParseException):
            reference = "[1"
            parser.extract_reference_parts(reference)

    def test_index_without_any_brackets(self):
        with self.assertRaises(ParseException):
            reference = "1"
            parser.extract_reference_parts(reference)

    def test_index_letter_in_number(self):
        with self.assertRaises(ParseException):
            reference = "[1a1]"
            parser.extract_reference_parts(reference)

    def test_index_trailing_symbol(self):
        with self.assertRaises(ParseException):
            reference = "[11-]"
            parser.extract_reference_parts(reference)

    def test_index_too_many_negative_signs(self):
        with self.assertRaises(ParseException):
            reference = "[--11]"
            parser.extract_reference_parts(reference)

    """
    Test errors with simple sublists
    """
    def test_sublist_without_opening_bracket(self):
        with self.assertRaises(ParseException):
            reference = "1:2]"
            parser.extract_reference_parts(reference)

    def test_sublist_without_closing_bracket(self):
        with self.assertRaises(ParseException):
            reference = "[1:2"
            parser.extract_reference_parts(reference)

    def test_sublist_too_many_colons(self):
        with self.assertRaises(ParseException):
            reference = "[1::2]"
            parser.extract_reference_parts(reference)

    def test_sublist_trailing_colons(self):
        with self.assertRaises(ParseException):
            reference = "[1:2:]"
            parser.extract_reference_parts(reference)

    def test_sublist_non_numeric_symbols(self):
        with self.assertRaises(ParseException):
            reference = "[1:a]"
            parser.extract_reference_parts(reference)

    """
    Test errors with simple subdicts
    """
    def test_subdicts_without_opening_brace(self):
        with self.assertRaises(ParseException):
            reference = "'testing'}"
            parser.extract_reference_parts(reference)

    def test_subdicts_without_closing_brace(self):
        with self.assertRaises(ParseException):
            reference = "{'testing'"
            parser.extract_reference_parts(reference)

    def test_subdicts_with_trailing_comma(self):
        with self.assertRaises(ParseException):
            reference = "{'testing', 'test2', }"
            parser.extract_reference_parts(reference)

    def test_subdicts_without_opening_quote(self):
        with self.assertRaises(ParseException):
            reference = "{testing'}"
            parser.extract_reference_parts(reference)

    def test_subdicts_without_closing_quote(self):
        with self.assertRaises(ParseException):
            reference = "{'testing}"
            parser.extract_reference_parts(reference)

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


