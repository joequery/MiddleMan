import json

def codify_json(json_str):
    '''
    Return HTML <pre><code> block representing a json object. The portions of
    the html corresponding to key/values will contain specfic data-json
    attributes to aid with front-end traversal.
    '''
    def span(c, v, sel=''):
        if sel:
            return "<span class=\"hljs-%s\" data-json-selector=\"%s\">%s</span>" % (c,sel, v)
        else:
            return "<span class=\"hljs-%s\">%s</span>" % (c,v)

    def dquote(s):
        return '"%s"' % s

    def apply_attrs(d, s='', sel=''):
        if isinstance(d, basestring):
            s = span('value', dquote(span('string', d, sel)))

        elif isinstance(d, dict):
            s += "{\n"
            for k,v in d.iteritems():
                the_sel = sel + "['%s']" % k
                s += dquote(span('attribute', k)) + ': '
                s += apply_attrs(v, s, the_sel)
            s += "\n}"

        return s


    data = json.loads(json_str)
    pre = '<pre><code class=" hljs json">'
    end = '</code></pre>'
    return pre + apply_attrs(data) + end
