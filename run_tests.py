#!/usr/bin/python3

from unittest import TestLoader, TextTestRunner, TestSuite

from tests.loader_tests import TestELF
from tests.rop_tests import TestROP

if __name__ == '__main__':
    loader = TestLoader()
    suite = TestSuite((
        loader.loadTestsFromTestCase(TestELF),
        loader.loadTestsFromTestCase(TestROP),
        ))

    runner = TextTestRunner(verbosity = 2)
    runner.run(suite)
