# Convenient functions for testing
import os
def testfile(path):
    txt = ""
    with open(os.path.join("tests", "testfiles", path)) as f:
        txt = f.read()
    return txt

