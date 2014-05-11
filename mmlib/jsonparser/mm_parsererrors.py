##############################################################################
# This entire file is dedicated to generating helpful error messages when a
# syntax error is encountered in our parser.
##############################################################################
_HARCODED_ERRORS = {
    "[]": "Empty brackets are invalid - an provide index or key"
}

def _get_missing_char(missing_char):
    '''
    Get rid of the doublequotes from the PyParsing Literal object (but keep a
    double quote if that's the actual missing character!)
    '''
    char = str(missing_char)
    if char == "\"\"\"":
        return "\""
    else:
        return char.replace("\"", "")

def _char_expected(e):
    if e.col >= len(e.pstr) or e.loc >= len(e.pstr):
        missing_char = _get_missing_char(e.parserElement)
        err_msg = "%s expected at index %s" % (missing_char, e.loc)
    else:
        missing_index = e.col
        reference_index = e.loc
        missing_char = e.pstr[missing_index]
        reference_char = e.pstr[reference_index]
        relative_pos = "before" if missing_index < reference_index else "after"

        fmt = "%s expected at index %s (%s '%s')"
        err_msg = fmt % (missing_char, missing_index, relative_pos, reference_char)

    return err_msg

def _string_end(e):
    problem_char = e.pstr[e.loc]
    if problem_char in "[]{}":
        err_msg = "unmatched %s at index %s" % (problem_char, e.loc)
    else:
        err_msg = "unexpected %s at index %s" % (problem_char, e.loc)

    return err_msg

def parse_error_msg(e):
    section = e.pstr
    orig_msg = e.msg
    err_msg = orig_msg
    orig_msg_lower = orig_msg.lower()
    full_err = 'Error parsing %s: ' % section

    hardcoded_err = _HARCODED_ERRORS.get(section)
    if hardcoded_err is not None:
        err_msg = full_err + hardcoded_err
        return err_msg

    # Don't let our bad attempts to display an error message crash the program
    # entirely.
    try:
        if 'expected' in orig_msg_lower:
            if 'stringend' in orig_msg_lower:
                err_msg = _string_end(e)
            else:
                err_msg = _char_expected(e)
    except Exception:
        err_msg = orig_msg

    full_err += err_msg
    return full_err

