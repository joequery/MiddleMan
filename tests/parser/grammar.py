# Tests that demonstrate proper references.
import unittest
from tests.testhelpers import testfile
from mmlib.jsonparser import extract_reference_parts
from mmlib.jsonparser.mm_parsererrors import has_balanced_tokens

class ParserHelperTests(unittest.TestCase):
    def test_has_balanced_tokens(self):
        test_str = "()"
        self.assertTrue(has_balanced_tokens("(", ")", test_str))

        test_str = "[]"
        self.assertTrue(has_balanced_tokens("[", "]", test_str))

        test_str = "[[]"
        self.assertFalse(has_balanced_tokens("[", "]", test_str))

        test_str = "[[]]"
        self.assertTrue(has_balanced_tokens("[", "]", test_str))

        test_str = "['[']]"
        self.assertFalse(has_balanced_tokens("[", "]", test_str))

        test_str = "{'key1', 'key2',}"
        self.assertTrue(has_balanced_tokens("{", "}", test_str))

        test_str = "['hello']]"
        self.assertFalse(has_balanced_tokens("[", "]", test_str))

class ReferenceBNFExtractionSimple(unittest.TestCase):
    """
    Test simple key references
    """
    def test_single_key_single_quotes(self):
        reference = "['mykey1']"
        expected = [["mykey1"]]
        extracted = extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("key", e.getName())

    def test_single_key_double_quotes(self):
        reference = '["mykey1"]'
        expected = [["mykey1"]]
        extracted = extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("key", e.getName())

    def test_key_with_underscores(self):
        reference = "['my_key1']"
        expected = [["my_key1"]]
        extracted = extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("key", e.getName())

    def test_multiple_keys_single_quotes(self):
        reference = "['mykey1']['myinnerkey2']"
        expected = [["mykey1"], ["myinnerkey2"]]
        extracted = extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("key", e.getName())

    def test_multiple_keys_double_quotes(self):
        reference = '["mykey1"]["myinnerkey2"]'
        expected = [["mykey1"], ["myinnerkey2"]]
        extracted = extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("key", e.getName())

    def test_many_keys(self):
        reference = "['mykey1']['myinnerkey2']['evendeeper3']"
        expected = [["mykey1"],["myinnerkey2"],["evendeeper3"]]
        extracted = extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("key", e.getName())

    def test_single_key_with_filter(self):
        reference = "['mykey1']|bool"
        expected = [["mykey1", "bool"]]
        extracted = extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("key", e.getName())

    def test_multiple_keys_with_filter(self):
        reference = "['mykey1']['myinnerkey2']|bool"
        expected = [["mykey1"],["myinnerkey2", "bool"]]
        extracted = extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("key", e.getName())

    """
    Test simple index references
    """
    def test_single_index(self):
        reference = "[10]"
        expected = [["10"]]
        extracted = extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("index", e.getName())

    def test_multiple_indexes(self):
        reference = "[10][20]"
        expected = [["10"], ["20"]]
        extracted = extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("index", e.getName())

    """
    Test simple sublist references
    """
    def test_single_sublist_with_both_numbers(self):
        reference = "[10:20]"
        expected = [["10", ":", "20"]]
        extracted = extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("sublist", e.getName())

    def test_single_sublist_with_negative_second_number(self):
        reference = "[10:-20]"
        expected = [["10", ":", "-20"]]
        extracted = extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("sublist", e.getName())

    def test_single_sublist_with_blank_first_number(self):
        reference = "[:10]"
        expected = [[":", "10"]]
        extracted = extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("sublist", e.getName())

    def test_single_sublist_with_blank_first_number_negative_second_number(self):
        reference = "[:-10]"
        expected = [[":", "-10"]]
        extracted = extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("sublist", e.getName())

    def test_single_sublist_with_blank_second_number(self):
        reference = "[10:]"
        expected = [["10", ":"]]
        extracted = extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("sublist", e.getName())

    def test_single_sublist_with_no_numbers(self):
        reference = "[:]"
        expected = [[":"]]
        extracted = extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("sublist", e.getName())

    """
    Test simple subdict references
    """
    def test_subdict_with_one_key(self):
        reference = "{'mykey1'}"
        expected = [["mykey1"]]
        extracted = extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("subdict", e.getName())

    def test_subdict_with_one_key_with_dbl_quotes(self):
        reference = '{"mykey1"}'
        expected = [["mykey1"]]
        extracted = extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("subdict", e.getName())

    def test_subdict_with_two_keys_no_spaces(self):
        reference = "{'mykey1','mykey2'}"
        expected = [["mykey1", "mykey2"]]
        extracted = extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("subdict", e.getName())

    def test_subdict_with_two_keys_with_spaces(self):
        reference = "{'mykey1', 'mykey2'}"
        expected = [["mykey1", "mykey2"]]
        extracted = extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())
        for e in extracted:
            self.assertEqual("subdict", e.getName())

class ReferenceBNFExtractionComplex(unittest.TestCase):
    """
    Test complex combinations of references
    """
    def test_index_after_simple_key(self):
        reference = "['mykey1'][5]"
        expected = [["mykey1"], ["5"]]
        extracted = extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())

        expectedTypes = ["key", "index"]

        for i,e in enumerate(extracted):
            self.assertEqual(expectedTypes[i], e.getName())

    def test_simple_key_after_index(self):
        reference = "[5]['mykey1']"
        expected = [["5"], ["mykey1"]]
        extracted = extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())

        expectedTypes = ["index", "key"]

        for i,e in enumerate(extracted):
            self.assertEqual(expectedTypes[i], e.getName())

    def test_subdict_after_key(self):
        reference = "['mykey1']{'innerkey1', 'innerkey2'}"
        expected = [["mykey1"], ["innerkey1", "innerkey2"]]
        extracted = extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())

        expectedTypes = ["key", "subdict"]

        for i,e in enumerate(extracted):
            self.assertEqual(expectedTypes[i], e.getName())

    def test_subdict_after_sublist(self):
        reference = "[1:5]{'innerkey1', 'innerkey2'}"
        expected = [["1", ":", "5"], ["innerkey1", "innerkey2"]]
        extracted = extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())

        expectedTypes = ["sublist", "subdict"]

        for i,e in enumerate(extracted):
            self.assertEqual(expectedTypes[i], e.getName())

    def test_sublist_after_subdict(self):
        reference = "{'innerkey1', 'innerkey2'}[1:5]"
        expected = [["innerkey1", "innerkey2"], ["1", ":", "5"]]
        extracted = extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())

        expectedTypes = ["subdict", "sublist"]

        for i,e in enumerate(extracted):
            self.assertEqual(expectedTypes[i], e.getName())

    def test_key_sublist_key_index(self):
        reference = "['mykey1'][4:]['myinnerkey'][-1]"
        expected = [["mykey1"], ["4", ":"], ["myinnerkey"], ["-1"]]
        extracted = extract_reference_parts(reference)
        self.assertEqual(expected, extracted.asList())

        expectedTypes = ["key", "sublist", "key", "index"]

        for i,e in enumerate(extracted):
            self.assertEqual(expectedTypes[i], e.getName())


