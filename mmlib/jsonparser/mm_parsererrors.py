##############################################################################
# This entire file is dedicated to generating helpful error messages when a
# syntax error is encountered in our parser.
##############################################################################
import pyparsing

_HARDCODED_ERRORS = {
    "[]": "Empty brackets are invalid - provide an index or key"
}

_CHARSETS = {
    pyparsing.alphas: "letter",
    pyparsing.nums: "digit",
    pyparsing.alphanums: "alphanum"
}

def _get_missing_char(parserElement):
    '''
    Correctly display the missing character
    '''
    if isinstance(parserElement, pyparsing.Literal):
        chars = str(parserElement)
    else:
        chars = str(parserElement.initCharsOrig)

    charset_entry =  _CHARSETS.get(chars)
    if charset_entry is not None:
        return charset_entry
    elif chars == "\"\"\"":
        return "\""
    else:
        return chars.replace("\"", "")

def _char_expected(e):
    missing_char = _get_missing_char(e.parserElement)
    err_msg = "%s expected at index %s" % (missing_char, e.loc)

    return err_msg

def _string_end(e):
    problem_char = e.pstr[e.loc]
    if problem_char in "[]{}":
        err_msg = "unmatched %s at index %s" % (problem_char, e.loc)
    else:
        err_msg = "unexpected %s at index %s" % (problem_char, e.loc)

    return err_msg

def parse_error_msg(e, ref):
    section = e.pstr
    orig_msg = e.msg
    err_msg = orig_msg
    orig_msg_lower = orig_msg.lower()
    full_err = 'Error parsing %s: ' % section

    # check for hardcoded errors
    for substr in _HARDCODED_ERRORS.keys():
        if substr in section:
            full_err = 'Error parsing %s: ' % ref
            hardcoded_err = _HARDCODED_ERRORS[substr]
            err_msg = full_err + hardcoded_err
            return err_msg

    # Don't let our bad attempts to display an error message crash the program
    # entirely.
    try:
        if 'expected' in orig_msg_lower:
            if 'end of text' in orig_msg_lower:
                err_msg = _string_end(e)
            else:
                err_msg = _char_expected(e)
    except Exception:
        err_msg = orig_msg

    full_err += err_msg
    return full_err

def has_balanced_tokens(open_token, close_token, thestr):
    balance = 0
    in_quotes =  False

    if open_token not in thestr or close_token not in thestr:
        return False

    # Ignore quotes for token matching
    for char in thestr:
        if char in ['"', "'"]:
            in_quotes = not in_quotes
            continue
        if not in_quotes:
            if char == open_token:
                balance += 1
            elif char == close_token:
                balance -= 1

    return balance == 0

def is_mismatched_string_error(err_msg, reference, e):
    if "unmatched" not in err_msg:
        return False

    for open_token, close_token in [("[", "]"), ("{", "}")]:
        if not has_balanced_tokens(open_token, close_token, reference):
            return True

    return False

