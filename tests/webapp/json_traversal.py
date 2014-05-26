from tests.testhelpers import MMTestCase
from mmlib.flaskhelpers.json_traversal import codify_json
import json

class JSONTraversalTests(MMTestCase):
    def test_very_simple_json(self):
        rawJSON = """
        {
          "url": "http://httpbin.org/get"
        }
        """
        code_html = codify_json(rawJSON)
        print(code_html)
