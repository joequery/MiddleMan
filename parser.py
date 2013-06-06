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
    Extract all references, which are of the form ${{reference}}$, from the scheme.
    A scheme may look like

        {
            "time": ${{['timestamp']}}$,
            "id": ${{['user_id']}}$
        }

    Where timestamp and user_id are keys in a JSON result.
    """
    pattern = "\${{[^}]+}}\$"
    results = re.findall(pattern, scheme)
    return results

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
        valueJSON = json.dumps(value)
        referenceData.append((rs, valueJSON))

    for referenceString, value in referenceData:
        scheme = scheme.replace(referenceString, value)
    return scheme

def extract_reference_value_from_json(referenceStr, rawJSON):
    """
    Extract the value of the key represented by reference from the JSON.
    For example, 
    >>> v = extract_reference_value_from_json("${{['mykey']}}", '{"mykey": "1"}')
    >>> v
    "1"
    """

    # Extraction helper functions for the various reference types. 
    # All helper functions should have two parameters: the reference, and the
    # data
    def extract_via_key(ref, data):
        return data.get(ref[0])

    # Mapping of reference types to their extraction helper functions.
    referenceTypeMap = {
        "key": extract_via_key
    }
    
    # Get 'mykey' from ${{mykey}}. This form is guaranteed, so we'll just 
    # hardcode it.
    reference = referenceStr[3:-3]
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
    key = Group(brackets(quotes(words)) ^ brackets(dblquotes(words)))

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
