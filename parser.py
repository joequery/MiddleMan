# Functions for parsing and condensing JSON based upon user preferences.

import json
import re

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
    """
    Extract the portions of a reference according to the following grammar:
    """
    return []
