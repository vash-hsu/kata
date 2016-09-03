#!/usr/bin/env python

import sys
import os


def reverse_string(s):
    return s[::-1]


def reverse_string_bad(s):
    output_list = []
    for i in s:
        output_list.insert(0, i)
    return ''.join(output_list)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "Usage: {} hello world".format(os.path.split(sys.argv[0])[-1])
    for i in sys.argv[1:]:
        print "original: {}\nreversed: {}\n".format(i, reverse_string(i))
        print "---"

