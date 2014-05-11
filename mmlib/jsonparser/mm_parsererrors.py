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


def parse_error_msg(e):
    orig_msg = e.msg
    full_err = 'Error parsing %s: ' % e.pstr

    if 'expected' in orig_msg.lower():
        err_msg = _char_expected(e)

    full_err += err_msg
    return full_err

