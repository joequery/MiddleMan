from tests.testhelpers import MMTestCase
import json

class ParseFormTests(MMTestCase):
    def test_valid_data(self):
        '''
        Borrowed from test_httpbin_get_example in tests/parser/usage.py
        '''

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

        post_data = {'rawjson': rawJSON, 'scheme': scheme}
        resp = self.client.post('/process', data=post_data)
        resp_data = json.loads(resp.data)

        expected = "httpbin.org, 74.192.112.168"
        self.assertEqual(resp_data['result'], expected)
