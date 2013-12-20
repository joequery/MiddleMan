# Functions for parsing and condensing JSON based upon user preferences.

import json
import re
from pyparsing import (
    Literal, alphas, nums, alphanums, OneOrMore, Word, 
    ZeroOrMore, Forward, oneOf, Group, Optional, Combine, stringEnd
)
from copy import deepcopy

def extract_reference_strings(scheme):
    """
    Extract all references, which are of the form ${reference}$, from the scheme.
    A scheme may look like

        {
            "time": ${['timestamp']}$,
            "id": ${['user_id']}$
        }

    Where timestamp and user_id are keys in a JSON result.
    """
    pattern = "\${[^$]+}\$"
    results = re.findall(pattern, scheme)
    return results

def apply_filter(filter_fn, value):
    '''
    Apply a filter function with name `filter_fn` to the value.
    '''
    if filter_fn == "bool":
        # Let's make things easier for the C people and just require them to
        # check for a "0" or "1" string instead of "True" and "False"
        return str(int(bool(value)))

    # elifs for more filter functions. We can clean up later if this gets to be
    # too big.
    else:
        raise RuntimeError("Filter function %s not defined" % filter_fn)

def apply_scheme_to_json(scheme, rawJSON):
    """
    Apply a user specified scheme to JSON. The references in the scheme will
    have their corresponding values replaced. Returns the dict representing the
    json.
    """
    referenceStrings = extract_reference_strings(scheme)
    referenceData = []
    for rs in referenceStrings:
        value = extract_reference_value_from_json(rs, rawJSON)

        # Don't json encode normal strings, otherwise we end up with extra
        # (possibly unwanted) quotes. Users can surround references in their
        # scheme with quotes if they want them.
        if not isinstance(value, str) and not isinstance(value, unicode):
            value = json.dumps(value)
        referenceData.append((rs, value))

    for referenceString, value in referenceData:
        scheme = scheme.replace(referenceString, value)
    return scheme

def extract_reference_value_from_json(referenceStr, rawJSON):
    """
    Extract the value of the key represented by reference from the JSON.
    For example, 
    >>> v = extract_reference_value_from_json("${['mykey']}", '{"mykey": "1"}')
    >>> v
    "1"
    """

    # Extraction helper functions for the various reference types. 
    # All helper functions should have two parameters: the reference, and the
    # data
    def extract_via_key(ref, data):
        # A ref of length 1 is just the key ex:['mykey']
        # A ref of length 2 means a filter was specified ex: ['mykey', 'bool']
        if len(ref) == 1:
            return data.get(ref[0])
        else:
            return apply_filter(ref[1], data.get(ref[0]))

    def extract_via_index(ref, data):
        index = int(ref[0])
        return data[index]

    def extract_via_sublist(ref, data):
        size = len(ref)
        # Example - ['5', ':', '-5'] => [5:-5]
        if size == 3:
            lidx = int(ref[0])
            ridx = int(ref[2])

        # Example - ['2', ':'] => [2:] OR [':', '-1'] => [:-1]
        elif size == 2:
            if ref[0] == ":":
                lidx = 0
                ridx = int(ref[1])
            else:
                lidx = int(ref[0])
                ridx = len(data)

        # Only possibility - [':'] => [:]
        elif size == 1:
            lidx = 0
            ridx = len(data)

        return data[lidx:ridx]

    def extract_via_subdict(ref, data):
        # If data is a dict, assume the user wants a simple subdict in return.
        # If data is a list, assume the list is a list of identically structured
        # dictionaries, and the user wants to extract particular elements
        # from each dictionary. We will then return a list of dicts.
        if isinstance(data, dict):
            newDict = {}
            for key in ref:
                newDict[key] = data[key]
            return newDict
        elif isinstance(data, list):
            newList = []
            for d in data:
                newDict = {}
                for key in ref:
                    newDict[key] = d[key]
                newList.append(newDict)
            return newList



    # Mapping of reference types to their extraction helper functions.
    referenceTypeMap = {
        "key": extract_via_key,
        "index": extract_via_index,
        "sublist": extract_via_sublist,
        "subdict": extract_via_subdict,
    }
    
    # Get 'mykey' from ${mykey}. This form is guaranteed, so we'll just 
    # hardcode it.
    reference = referenceStr[2:-2]
    data = json.loads(rawJSON)
    referenceParts = extract_reference_parts(reference)
    for r in referenceParts:
        fn = referenceTypeMap.get(r.getName())
        data = fn(r, data)

    return data


def extract_reference_parts(reference):
    referenceGrammar = reference_bnf()
    parsed = referenceGrammar.parseString(reference)
    return parsed

def reference_bnf():
    """
    Grammar for the references allowed in the schemes:

    item     :: {sublist|index|key|subdict}
    sublist :: '['{digit}':'[-]{digit}']'
    index    :: '['digit']'
    subdict  :: '{'words{,words}'}'

    words  :: alnum{alnum}
    alpha :: a | b | ... | z | A | B | ... | Z
    digit :: 0 | 1 | ... | 9
    alnum :: alpha | digit
    """
    lbracket = Literal("[").suppress()
    rbracket = Literal("]").suppress()
    quote = Literal('\'').suppress()
    dblquote = Literal('"').suppress()
    lbrace = Literal("{").suppress()
    rbrace = Literal("}").suppress()
    dash = Literal("-")
    colon = Literal(":")
    words = OneOrMore(Word(alphanums))
    number = Combine(Optional(dash) + Word(nums))
    space = Literal(" ")
    commaSep = (Literal(",") + Optional(space)).suppress()
    bar = Literal("|").suppress()
    filter_fn = Combine(bar + words)

    # Wrapper functions for readability
    def braces(s):
        return lbrace + s + rbrace

    def brackets(s):
        return lbracket + s + rbracket

    def quotes(s):
        return quote + s + quote

    def dblquotes(s):
        return dblquote + s + dblquote

    # Dictionaries: ["some string"]
    # With optional filter function: ["some string"]|bool
    key = Group(\
            (brackets(quotes(words)) + Optional(filter_fn)) ^\
            (brackets(dblquotes(words)) + Optional(filter_fn))\
            )

    # Indexes: [5]
    index = Group(brackets(number))

    # Subrange: [5:-1]
    sublist = Group(brackets(Optional(number) + colon + Optional(number)))

    # Subdictionary: {"some string", "some otherstring"}
    subdictSingle = braces(quotes(words) + ZeroOrMore(commaSep + quotes(words)))
    subdictDbl = braces(dblquotes(words) + ZeroOrMore(commaSep + dblquotes(words)))
    subdict = Group(subdictSingle ^ subdictDbl)

    item = key("key") ^ \
           index("index") ^ \
           sublist("sublist") ^ \
           subdict("subdict")

    term = OneOrMore(item) + stringEnd
    return term
