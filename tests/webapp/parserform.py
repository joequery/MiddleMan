from tests.testhelpers import MMTestCase
import json

class ParseFormTests(MMTestCase):
    def extra_setup(self):
        ### Borrowed from test_httpbin_get_example in tests/parser/usage.py
        self.rawJSON = """
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
        self.scheme = "${['headers']['Host']}$, ${['origin']}$"

    def test_valid_data(self):
        post_data = {'rawjson': self.rawJSON, 'scheme': self.scheme}
        resp = self.client.post('/process', data=post_data)
        resp_data = json.loads(resp.data)

        expected = "httpbin.org, 74.192.112.168"
        self.assertEqual(resp_data['result'], expected)

    def test_missing_data(self):
        post_data_missing_json = {'scheme': self.scheme}
        resp = self.client.post('/process', data=post_data_missing_json)
        resp_data = json.loads(resp.data)
        self.assertEqual(resp_data['errors'], {u'missing': [u'rawjson']})

        post_data_missing_scheme = {'rawjson': self.rawJSON}
        resp = self.client.post('/process', data=post_data_missing_scheme)
        resp_data = json.loads(resp.data)
        self.assertEqual(resp_data['errors'], {u'missing': [u'scheme']})

        empty_data = {}
        resp = self.client.post('/process', data=empty_data)
        resp_data = json.loads(resp.data)
        self.assertEqual(resp_data['errors'], {u'missing': [u'scheme', u'rawjson']})
