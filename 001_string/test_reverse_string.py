#!/usr/bin/env python

import unittest
import os
import sys
import getopt

from reverse_string import reverse_string
from reverse_string import reverse_string_bad


def better():
    example = "abcdefghijklmnopqrstuvwxyz01234567890" * 100
    reverse_string(example)


def worse():
    example = "abcdefghijklmnopqrstuvwxyz01234567890" * 100
    reverse_string_bad(example)


class StringTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_rat_empty_string(self):
        "RAT: empty string"
        example = ""
        self.assertEqual(reverse_string(example), "")

    def test_fast_common_string(self):
        "RAT: common string"
        example = "hello world"
        expected = "dlrow olleh"
        self.assertEqual(reverse_string(example), expected)

    # def test_long_string(self):
    #     "PERF: long string reverse, pythonic is better"
    #     import timeit
    #     sec_better = timeit.timeit(stmt="better()",
    #                                setup="from __main__ import better",
    #                                number=100)
    #     sec_worse = timeit.timeit(stmt="worse()",
    #                               setup="from __main__ import worse",
    #                               number=100)
    #     self.assertLess(sec_better, sec_worse)
    #     print sec_better, "vs.", sec_worse


def print_usage(name):
    print "USAGE:"
    print "to list test cases:\n\t%s -l" % (name)
    print "to execute all test cases:\n\t%s" % (name)


def dump_testcase_list():
    testloader = unittest.TestLoader()
    list_testcases = testloader.getTestCaseNames(StringTest)
    total_case_nums = len(list_testcases)
    case_counter = 0
    for i in list_testcases:
        case_counter += 1
        print "%d/%d\t%s" %(case_counter, total_case_nums, i)


if __name__ == "__main__":
    scriptfilename = os.path.split(sys.argv[0])[1]
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hl")
    except getopt.GetoptError:
        print_usage(scriptfilename)
        sys.exit(-1)
    todo_list_testcase = False
    for opt, arg in opts:
        if opt == '-l':
            todo_list_testcase = True
        elif opt == '-h':
            print_usage(scriptfilename)
            sys.exit(-1)
    if todo_list_testcase:
        dump_testcase_list()
    else:
        testloader = unittest.TestLoader()
        testsuit = testloader.loadTestsFromTestCase(StringTest)
        testruner = unittest.TextTestRunner(verbosity=2)
        testruner.run(testsuit)
