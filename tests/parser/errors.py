# Tests that demonstrate errors in reference syntax that should cause our parser
# to raise an exception.
import unittest
from tests.testhelpers import testfile

from pyparsing import ParseException
import parser

class ReferenceBNFSimpleErrors(unittest.TestCase):
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

class ReferenceBNFComplexErrors(unittest.TestCase):
    def test_malformed_dicts(self):
        references = []
        valid = []
        references.append("[['hello']]")
        references.append("['hello'][")
        for r in references:
            try:
                extracted = parser.extract_reference_parts(r)
                valid.append((r, extracted.getName()))
            except ParseException:
                pass

        self.assertEqual(valid, [])

