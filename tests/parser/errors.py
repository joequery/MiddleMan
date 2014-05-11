# Tests that demonstrate errors in reference syntax that should cause our parser
# to raise an exception.
import unittest
from tests.testhelpers import testfile

from pyparsing import ParseException
from mmlib.jsonparser import(
    extract_reference_parts, extract_reference_value_from_json
)

###################################
# Begin new, specific error tests
###################################
class MalformedKeyTests(unittest.TestCase):

    def test_nested_key(self):
        with self.assertRaises(ParseException) as e:
            ref = "[['hello']]"
            extract_reference_parts(ref)

        expected_err = "Error parsing [['hello']]: ' expected at index 1"
        self.assertEqual(str(e.exception.msg), expected_err)

    def test_unclosed_opening_key_no_keystr(self):
        with self.assertRaises(ParseException) as e:
            ref = "['hello']["
            extract_reference_parts(ref)

        expected_err = "Error parsing ['hello'][: unmatched [ at index 9"
        self.assertEqual(str(e.exception.msg), expected_err)

    def test_unclosed_opening_key_with_keystr(self):
        with self.assertRaises(ParseException) as e:
            ref = "['hello']['there'"
            extract_reference_parts(ref)

        expected_err = "Error parsing ['hello']['there': unmatched [ at index 9"
        self.assertEqual(str(e.exception.msg), expected_err)

    def test_unopened_closing_key_no_keystr(self):
        with self.assertRaises(ParseException) as e:
            ref = "['hello']]"
            extract_reference_parts(ref)

        expected_err = "Error parsing ['hello']]: unmatched ] at index 9"
        self.assertEqual(str(e.exception.msg), expected_err)

    def test_unopened_closing_key_with_keystr(self):
        with self.assertRaises(ParseException) as e:
            ref = "['hello']'there']"
            extract_reference_parts(ref)

        expected_err = "Error parsing ['hello']'there']: [ expected at index 9"
        self.assertEqual(str(e.exception.msg), expected_err)

    def test_unopened_closing_key_with_keystr_dblquote(self):
        with self.assertRaises(ParseException) as e:
            ref = "['hello']\"there\"]"
            extract_reference_parts(ref)

        expected_err = "Error parsing ['hello']\"there\"]: [ expected at index 9"
        self.assertEqual(str(e.exception.msg), expected_err)

    def test_empty_keystr(self):
        with self.assertRaises(ParseException) as e:
            ref = "[]"
            extract_reference_parts(ref)

        expected_err = "Error parsing []: Empty brackets are invalid - provide an index or key"
        self.assertEqual(str(e.exception.msg), expected_err)

class MalformedIndexTests(unittest.TestCase):
    def test_negative_after_num(self):
        with self.assertRaises(ParseException) as e:
            ref = "[1-]"
            extract_reference_parts(ref)

        expected_err = "Error parsing [1-]: ] expected at index 2"
        self.assertEqual(str(e.exception.msg), expected_err)

    def test_doublenegative(self):
        with self.assertRaises(ParseException) as e:
            ref = "[--1]"
            extract_reference_parts(ref)

        expected_err = "Error parsing [--1]: digit expected at index 2"
        self.assertEqual(str(e.exception.msg), expected_err)

    def test_nonnumeric(self):
        with self.assertRaises(ParseException) as e:
            ref = "[x]"
            extract_reference_parts(ref)

        # pyparsing attempts to evaluate this is a key first, so we get a key
        # related error message
        expected_err = "Error parsing [x]: ' expected at index 1"
        self.assertEqual(str(e.exception.msg), expected_err)

    def test_leading_plus(self):
        with self.assertRaises(ParseException) as e:
            ref = "[+1]"
            extract_reference_parts(ref)

        # pyparsing attempts to evaluate this is a key first, so we get a key
        # related error message
        expected_err = "Error parsing [+1]: ' expected at index 1"
        self.assertEqual(str(e.exception.msg), expected_err)

class MalformedSublistTests(unittest.TestCase):
    def test_doubleneg(self):
        with self.assertRaises(ParseException) as e:
            ref = "[--1:-1]"
            extract_reference_parts(ref)

        expected_err = "Error parsing [--1:-1]: digit expected at index 2"
        self.assertEqual(str(e.exception.msg), expected_err)

    def test_trailing_negative(self):
        with self.assertRaises(ParseException) as e:
            ref = "[1:-1-]"
            extract_reference_parts(ref)

        expected_err = "Error parsing [1:-1-]: ] expected at index 5"
        self.assertEqual(str(e.exception.msg), expected_err)

    def test_missing_trailing_bracket(self):
        with self.assertRaises(ParseException) as e:
            ref = "[1:-1"
            extract_reference_parts(ref)

        expected_err = "Error parsing [1:-1: ] expected at index 5"
        self.assertEqual(str(e.exception.msg), expected_err)

    def test_missing_leading_bracket(self):
        with self.assertRaises(ParseException) as e:
            ref = "1:-1]"
            extract_reference_parts(ref)

        expected_err = "Error parsing 1:-1]: [ expected at index 0"
        self.assertEqual(str(e.exception.msg), expected_err)

class MalformedSubdictTests(unittest.TestCase):
    def test_missing_trailing_quote(self):
        with self.assertRaises(ParseException) as e:
            ref = "{'something', 'something2}"
            extract_reference_parts(ref)

        expected_err = "Error parsing {'something', 'something2}: ' expected at index 25"
        self.assertEqual(str(e.exception.msg), expected_err)

    def test_extra_trailing_brace(self):
        with self.assertRaises(ParseException) as e:
            ref = "{'something', 'something2'}}"
            extract_reference_parts(ref)

        expected_err = "Error parsing {'something', 'something2'}}: unmatched } at index 27"
        self.assertEqual(str(e.exception.msg), expected_err)

    def test_extra_trailing_comma(self):
        with self.assertRaises(ParseException) as e:
            ref = "{'something', 'something2',}"
            extract_reference_parts(ref)

        expected_err = "Error parsing {'something', 'something2',}: } expected at index 26"
        self.assertEqual(str(e.exception.msg), expected_err)

    def test_extra_trailing_comma2(self):
        with self.assertRaises(ParseException) as e:
            ref = "{'mykey',}"
            extract_reference_parts(ref)

        expected_err = "Error parsing {'mykey',}: ' expected at index 9"
        self.assertEqual(str(e.exception.msg), expected_err)

    def test_extra_leading_comma(self):
        with self.assertRaises(ParseException) as e:
            ref = "{,'mykey'}"
            extract_reference_parts(ref)

        expected_err = "Error parsing {,'mykey'}: ' expected at index 1"
        self.assertEqual(str(e.exception.msg), expected_err)

class MalformedComplexTests(unittest.TestCase):
    def test_example1(self):
        with self.assertRaises(ParseException) as e:
            ref = "[1:2{'mykey'}]"
            extract_reference_parts(ref)

        expected_err = "Error parsing [1:2{'mykey'}]: ] expected at index 4"
        self.assertEqual(str(e.exception.msg), expected_err)

    def test_example2(self):
        with self.assertRaises(ParseException) as e:
            ref = "[1:2]{'mykey'}]"
            extract_reference_parts(ref)

        expected_err = "Error parsing [1:2]{'mykey'}]: unmatched ] at index 14"
        self.assertEqual(str(e.exception.msg), expected_err)

    def test_example3(self):
        with self.assertRaises(ParseException) as e:
            ref = "[1]{'mykey'}[]"
            extract_reference_parts(ref)

        expected_err = "Error parsing [1]{'mykey'}[]: Empty brackets are invalid - provide an index or key"
        self.assertEqual(str(e.exception.msg), expected_err)

    def test_example4(self):
        with self.assertRaises(ParseException) as e:
            ref = "[1]{'mykey'}[a]"
            extract_reference_parts(ref)

        expected_err = "Error parsing [1]{'mykey'}[a]: ' expected at index 13"
        self.assertEqual(str(e.exception.msg), expected_err)

    def test_example5(self):
        with self.assertRaises(ParseException) as e:
            ref = "[1]{'mykey'}[5:5-]"
            extract_reference_parts(ref)

        expected_err = "Error parsing [1]{'mykey'}[5:5-]: ] expected at index 16"
        self.assertEqual(str(e.exception.msg), expected_err)

    def test_example6(self):
        with self.assertRaises(ParseException) as e:
            ref = "[1]{'mykey'[5:5]"
            extract_reference_parts(ref)

        expected_err = "Error parsing [1]{'mykey'[5:5]: unmatched { at index 3"
        self.assertEqual(str(e.exception.msg), expected_err)

    def test_example7(self):
        with self.assertRaises(ParseException) as e:
            ref = "['test'][-1]{'key1', 'key2',}"
            extract_reference_parts(ref)

        expected_err = "Error parsing ['test'][-1]{'key1', 'key2',}: } expected at index 27"
        self.assertEqual(str(e.exception.msg), expected_err)

    def test_example8(self):
        with self.assertRaises(ParseException) as e:
            ref = "['test'][-1]{'key1', 'key2'[5:10]"
            extract_reference_parts(ref)

        expected_err = "Error parsing ['test'][-1]{'key1', 'key2'[5:10]: unmatched { at index 12"
        self.assertEqual(str(e.exception.msg), expected_err)

##############
# OLD TESTS
##############
class ReferenceBNFErrors(unittest.TestCase):
    def test_invalid_filter_function(self):
        rawJSON = """
        {
            "mykey1": "myvalue1",
            "timezone": "US/Central"
        }
        """
        reference = '${["mykey1"]|lolol}$'

        with self.assertRaises(RuntimeError) as e:
            extracted = extract_reference_value_from_json(reference, rawJSON)
        expected_err = "Filter function lolol not defined"
        self.assertEqual(str(e.exception), expected_err)

