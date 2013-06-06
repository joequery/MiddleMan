# Tests that demonstrate direct usage of the parser and the reference grammar
# for substituting JSON values
import unittest
from tests.testhelpers import testfile
import parser
import json

class ReferenceHelpers(unittest.TestCase):
    def test_extract_references_simple(self):
        scheme = """
        {
            "key1": "${['mykey1']}$",
            "key2": "some hardcoded value",
            "time": "${['timezone']}$"
        }
        """
        references = parser.extract_reference_strings(scheme)
        expected = ["${['mykey1']}$", "${['timezone']}$"]
        self.assertListEqual(expected, references)

    def test_extract_simple_key_value_pair(self):
        rawJSON = """
        {
            "mykey1": "myvalue1",
            "timezone": "US/Central"
        }
        """
        reference = '${["mykey1"]}$'
        expected = "myvalue1"
        extracted = parser.extract_reference_value_from_json(reference, rawJSON)
        self.assertEqual(expected, extracted)


class SchemeApplication(unittest.TestCase):
    def test_simple(self):
        scheme = """
        {
            "key1": "${['mykey1']}$",
            "key2": "some hardcoded value",
            "time": "${['timezone']}$"
        }
        """
        rawJSON = """
        {
            "mykey1": "myvalue1",
            "timezone": "US/Central"
        }
        """

        jsonAfterApplication = parser.apply_scheme_to_json(scheme, rawJSON)
        js = json.loads(jsonAfterApplication)
        expected = {
            "key1": "myvalue1", 
            "key2": "some hardcoded value", 
            "time": "US/Central"
        }
        self.assertDictEqual(expected, js)

    def test_httpbin_get_example(self):
        rawJSON = """
        {
          "url": "http://httpbin.org/get",
          "headers": {
            "Host": "httpbin.org",
            "Connection": "close",
            "Accept": "*/*",
            "User-Agent": "Wget/1.13.4 (linux-gnu)"
          },
          "args": {},
          "origin": "74.192.112.168"
        }
        """
        scheme = "${['headers']['Host']}$, ${['origin']}$"

        result = parser.apply_scheme_to_json(scheme, rawJSON).strip()
        expected = "httpbin.org, 74.192.112.168"
        self.assertEqual(expected, result)

    def test_index_with_simple_list(self):
        rawJSON = '{"key2": [0, 1, 2, 3], "key1": "value1"}'
        scheme = "${['key1']}$${['key2'][2]}$"
        result = parser.apply_scheme_to_json(scheme, rawJSON)
        expected = "value12"
        self.assertEqual(expected, result)

        scheme = "${['key1']}$${['key2'][-1]}$"
        result = parser.apply_scheme_to_json(scheme, rawJSON)
        expected = "value13"
        self.assertEqual(expected, result)

    def test_sublist_with_simple_list(self):
        rawJSON = '{"key2": [0, 1, 2, 3], "key1": "value1"}'
        scheme = '{"numbers": ${["key2"][1:3]}$}'
        result = parser.apply_scheme_to_json(scheme, rawJSON)
        expected = '{"numbers": [1, 2]}'
        self.assertEqual(expected, result)

        scheme = '{"numbers": ${["key2"][1:]}$}'
        result = parser.apply_scheme_to_json(scheme, rawJSON)
        expected = '{"numbers": [1, 2, 3]}'
        self.assertEqual(expected, result)

        scheme = '{"numbers": ${["key2"][:-1]}$}'
        result = parser.apply_scheme_to_json(scheme, rawJSON)
        expected = '{"numbers": [0, 1, 2]}'
        self.assertEqual(expected, result)

        scheme = '{"numbers": ${["key2"][:]}$}'
        result = parser.apply_scheme_to_json(scheme, rawJSON)
        expected = '{"numbers": [0, 1, 2, 3]}'
        self.assertEqual(expected, result)

        scheme = '{"numbers": ${["key2"]}$}'
        result = parser.apply_scheme_to_json(scheme, rawJSON)
        expected = '{"numbers": [0, 1, 2, 3]}'
        self.assertEqual(expected, result)
