##############################################################################
# This entire file is dedicated to generating helpful error messages when a
# syntax error is encountered in our parser.
##############################################################################

def _char_expected(e):
    missing_index = e.col
    missing_char = e.pstr[missing_index]
    reference_index = e.loc
    reference_char = e.pstr[reference_index]
    relative_pos = "before" if missing_index < reference_index else "after"

    fmt = "%s expected at index %s (%s '%s')"
    err_msg = fmt % (missing_char, missing_index, relative_pos, reference_char)

    return err_msg

def _string_end(e):
    problem_char = e.pstr[e.loc]
    if problem_char in "[{":
        err_msg = "unmatched %s at index %s" % (problem_char, e.loc)

    return err_msg

def parse_error_msg(e):
    orig_msg = e.msg
    err_msg = orig_msg
    orig_msg_lower = orig_msg.lower()
    full_err = 'Error parsing %s: ' % e.pstr

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

