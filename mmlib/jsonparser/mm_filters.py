##################################################################
# Add filter functions here.
# See tests/parser/usage.py for examples of when these are used.
##################################################################

#########################################################
# NOTE: all filter functions should return a string!!!
#########################################################
def bool_filter(value):
    bool_val = bool(value)
    # This is the letter casing json expects
    if bool_val:
        return "true"
    else:
        return "false"

def boolint_filter(value):
    # makes things easier for the C people and just require them to check for a
    # "0" or "1" string instead of "True" and "False"
    return str(int(bool(value)))

def len_filter(value):
    return str(len(value))

def to_int_filter(value):
    return str(int(value))

def to_float_filter(value):
    return str(float(value))

def double_quote_filter(value):
    return "\"%s\"" % str(value)

def single_quote_filter(value):
    return "'%s'" % str(value)

FILTER_MAPPING = {
    "bool": bool_filter,
    "boolint": boolint_filter,
    "len": len_filter,
    "to_i": to_int_filter,
    "to_f": to_float_filter,
    "dquote": double_quote_filter,
    "squote": single_quote_filter,
}
