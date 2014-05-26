import json

def codify_json(json_str):
    '''
    Return HTML <pre><code> block representing a json object. The portions of
    the html corresponding to key/values will contain specfic data-json
    attributes to aid with front-end traversal.
    '''
    def apply_attrs(d):
        return ''

    data = json.loads(json_str)
    pre = '<pre><code class=" hljs json">'
    end = '</code></pre>'
    return pre + apply_attrs(data) + end
