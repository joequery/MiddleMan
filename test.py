import unittest
import sys

if __name__ == '__main__':
    from tests.parser.errors import *
    from tests.parser.grammar import *
    from tests.parser.usage import *
    from tests.webapp.parserform import *
    unittest.main(verbosity=2)
