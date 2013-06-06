# Tests that demonstrate errors in reference syntax that should cause our parser
# to raise an exception.
import unittest
from tests.testhelpers import testfile

from pyparsing import ParseException
import parser

class ReferenceBNFErrors(unittest.TestCase):
    def test_malformed_dicts(self):
        badreferences = []
        valid = []
        badreferences.append("[['hello']]")
        badreferences.append("['hello'][")
        badreferences.append("['hello']['hello']]")
        for r in badreferences:
            try:
                extracted = parser.extract_reference_parts(r)
                types = []
                for e in extracted:
                    types.append(e.getName())
                valid.append((r, extracted.asList(), types))
            except ParseException:
                pass

        self.assertEqual(valid, [])

    def test_malformed_indexes(self):
        badreferences = []
        valid = []
        badreferences.append("[1-]")
        badreferences.append("[--1]")
        badreferences.append("[x]")
        badreferences.append("[+1]")
        for r in badreferences:
            try:
                extracted = parser.extract_reference_parts(r)
                types = []
                for e in extracted:
                    types.append(e.getName())
                valid.append((r, extracted.asList(), types))
            except ParseException:
                pass

        self.assertEqual(valid, [])

    def test_malformed_sublists(self):
        badreferences = []
        valid = []
        badreferences.append("[--1:-1]")
        badreferences.append("[1:-1-]")
        badreferences.append("[1:-1")
        badreferences.append("1:-1]")
        for r in badreferences:
            try:
                extracted = parser.extract_reference_parts(r)
                types = []
                for e in extracted:
                    types.append(e.getName())
                valid.append((r, extracted.asList(), types))
            except ParseException:
                pass

        self.assertEqual(valid, [])

    def test_malformed_subdicts(self):
        badreferences = []
        valid = []
        badreferences.append("{'something', 'something2}")
        badreferences.append("{'something', 'something2}}")
        badreferences.append("{'something', 'something2',}")
        badreferences.append("{'mykey',}")
        badreferences.append("{,'mykey'}")
        for r in badreferences:
            try:
                extracted = parser.extract_reference_parts(r)
                types = []
                for e in extracted:
                    types.append(e.getName())
                valid.append((r, extracted.asList(), types))
            except ParseException:
                pass

        self.assertEqual(valid, [])

    def test_malformed_combinations(self):
        badreferences = []
        valid = []
        badreferences.append("[1:2{'mykey'}]")
        badreferences.append("[1:2]{'mykey'}]")
        badreferences.append("[1]{'mykey'}[]")
        badreferences.append("[1]{'mykey'}[a]")
        badreferences.append("[1]{'mykey'}[5:5-]")
        badreferences.append("[1]{'mykey'[5:5]")
        badreferences.append("['test'][-1]{'key1', 'key2',}")
        badreferences.append("['test'][-1]{'key1', 'key2'[5:10]")
        for r in badreferences:
            try:
                extracted = parser.extract_reference_parts(r)
                types = []
                for e in extracted:
                    types.append(e.getName())
                valid.append((r, extracted.asList(), types))
            except ParseException:
                pass

        self.assertEqual(valid, [])
