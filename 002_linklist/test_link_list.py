#!/usr/bin/env python

import unittest
import os
import sys
import getopt
from link_list import ListNode
from link_list import LinkList


class LinkListTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_rat_empty_list(self):
        "RAT: empty list"
        example = LinkList([])
        self.assertEqual(example.dump_elements(), [])
        example.remove_elements(0)
        self.assertEqual(example.dump_elements(), [])

    def test_rat_list_1_remove_1(self):
        "FAST: [1] and remove 1"
        example = LinkList([1,])
        self.assertEqual(example.dump_elements(), [1,])
        example.remove_elements(1)
        self.assertEqual(example.dump_elements(), [])

    def test_rat_list_123_remove_2(self):
        "FAST: [1, 2, 3] and remove 2"
        example = LinkList([1,2, 3])
        self.assertEqual(example.dump_elements(), [1, 2, 3])
        example.remove_elements(2)
        self.assertEqual(example.dump_elements(), [1, 3])

    def test_rat_list_1232_remove_2(self):
        "FAST: [1, 2, 3, 2] and remove 2"
        example = LinkList([1, 2, 3, 2])
        self.assertEqual(example.dump_elements(), [1, 2, 3, 2])
        example.remove_elements(2)
        self.assertEqual(example.dump_elements(), [1, 3])

    def test_fet_list_1234_remove_5(self):
        "FET: [1, 2, 3, 4] and remove 5"
        example = LinkList([1, 2, 3, 4])
        self.assertEqual(example.dump_elements(), [1, 2, 3, 4])
        example.remove_elements(5)
        self.assertEqual(example.dump_elements(), [1, 2, 3, 4])


def print_usage(name):
    print "USAGE:"
    print "to list test cases:\n\t%s -l" % (name)
    print "to execute all test cases:\n\t%s" % (name)


def dump_testcase_list():
    testloader = unittest.TestLoader()
    list_testcases = testloader.getTestCaseNames(LinkListTest)
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
        testsuit = testloader.loadTestsFromTestCase(LinkListTest)
        testruner = unittest.TextTestRunner(verbosity=2)
        testruner.run(testsuit)
