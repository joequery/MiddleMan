# Functions for parsing and condensing JSON based upon user preferences.

import json
import re
from pyparsing import (
    Literal, alphas, nums, alphanums, OneOrMore, Word, 
    ZeroOrMore, Forward, oneOf, Group, Optional, Combine
)

def extract_references(scheme):
    """
    Extract all references, which are of the form ${{mykey}}$, from the scheme.
    A scheme may look like

        {
            "time": ${{timestamp}}$,
            "id": ${{user_id}}$
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
    return {"key1":"myvalue1"}

def extract_reference_value_from_json(reference, rawJSON):
    """
    Extract the value of the key represented by reference from the JSON.
    For example, 
    >>> v = extract_reference_value_from_json("${{mykey}}", '{"mykey": "1"}')
    >>> v
    "1"
    """
    
    # Get 'mykey' from ${{mykey}}. This form is guaranteed, so we'll just 
    # hardcode it.
    referenceStr = reference[3:-3]
    print(referenceStr)
    print("*" * 90)

    return ""

def extract_reference_parts(reference):
    referenceGrammar = reference_bnf()
    parsed = referenceGrammar.parseString(reference)
    return parsed

def reference_bnf():
    """
    Grammar for the references allowed in the schemes:

    term     :: atom{subrange|index|dict|subdict}
    subrange :: '['{digit}':'[-]{digit}']'
    index    :: '['digit']'
    subdict  :: '{'atom{,atom}'}'

    atom  :: alnum{alnum}
    alpha :: a | b | ... | z | A | B | ... | Z
    digit :: 0 | 1 | ... | 9
    alnum :: alpha | digit
    key   :: alpha{alnum}
    """
    lbracket = Literal("[")
    rbracket = Literal("]")
    quote = Literal('\'').suppress()
    dblquote = Literal('"').suppress()
    lbrace = Literal("{")
    rbrace = Literal("}")
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
    dicts = Group(brackets(quotes(words)) ^ brackets(dblquotes(words)))

    # Indexes: [5]
    index = Group(brackets(number))

    # Subrange: [5:-1]
    subrange = Group(brackets(Optional(number) + colon + Optional(number)))

    # Subdictionary: {"some string", "some otherstring"}
    subdictSingle = braces(quotes(words) + ZeroOrMore(commaSep + quotes(words)))
    subdictDbl = braces(dblquotes(words) + ZeroOrMore(commaSep + dblquotes(words)))
    subdict = Group(subdictSingle ^ subdictDbl)

    item = dicts("dict") ^ \
           index("index") ^ \
           subrange("subrange") ^ \
           subdict("subdict")

    term = OneOrMore(item)
    return term
