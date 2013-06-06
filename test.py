import unittest
import sys

if __name__ == '__main__':
    # --all passed will test logins as well as scrapes.
    allTests = len(sys.argv) == 2 and sys.argv[1] == "--all"
    
    """
    if allTests:
        del sys.argv[1]
        print("*" * 80)
        print("Running api tests")
        print("*" * 80)
        from tests.v1.apitests import *
    """

    from tests.parser.errors import ReferenceBNFComplexErrors
    #from tests.parser.errors import *
    #from tests.parser.grammar import *
    unittest.main(verbosity=2)
