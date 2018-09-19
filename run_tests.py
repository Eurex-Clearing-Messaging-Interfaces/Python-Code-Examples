#!/usr/bin/env python

import inspect
import unittest
import xmlrunner
import sys
import tests.test_PurePython
import tests.test_Proton

if __name__ == '__main__':
    suites = []
    suites.append(unittest.TestLoader().loadTestsFromModule(tests.test_PurePython))
    suites.append(unittest.TestLoader().loadTestsFromModule(tests.test_Proton))
    allTests = unittest.TestSuite(suites)
    if 'verbose' in inspect.getargspec(xmlrunner.XMLTestRunner.__init__).args:
        result = xmlrunner.XMLTestRunner(output='test-reports', verbose=True).run(allTests)
    else:
        result = xmlrunner.XMLTestRunner(output='test-reports', verbosity=2).run(allTests)
    sys.exit(result.wasSuccessful() != True)
