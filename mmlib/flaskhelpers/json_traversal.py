import json

TAB_INDENT = "  "

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

    def tab(n):
        return TAB_INDENT * n

    def apply_attrs(d, sel='', depth=0):
        if isinstance(d, basestring):
            s = span('value', dquote(span('string', d, sel)))

        elif isinstance(d, dict):
            s = "{\n"
            num_keys = len(d)
            for i, (k,v) in enumerate(d.iteritems()):
                the_sel = sel + "['%s']" % k
                s += tab(depth+1)
                s += dquote(span('attribute', k)) + ': '
                s += apply_attrs(v, the_sel, depth+1)

                if i<num_keys-1:
                    s += ","
                    s += "\n"
            s += "\n" + tab(depth) + "}"

        return s


    data = json.loads(json_str)
    pre = '<pre><code class=" hljs json">'
    end = '</code></pre>'
    return pre + apply_attrs(data) + end
