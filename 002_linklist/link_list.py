#!/usr/bin/env python

import sys


class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


class LinkList:
    def __init__(self, x):
        if isinstance(x, int):
            self.head = ListNode(x)
            return
        if isinstance(x, list):
            if len(x) == 0:
                self.head = ListNode(None)
                return
            self.head = ListNode(x[0])
            previous = self.head
            for i in x[1:]:
                previous.next = ListNode(i)
                previous = previous.next

    def add_element(self, x):
        if not self.head or not self.head.val:
            self.head = ListNode(x)
            return
        previous = self.head
        while previous.next:
            previous = previous.next
        previous.next = ListNode(x)

    def dump_elements(self):
        processing = self.head
        output_list = []
        while processing:
            if not processing.val:
                break
            output_list.append(processing.val)
            processing = processing.next
        return output_list

    # Remove all elements from a linked list of integers that have value val.
    def remove_elements(self, val):
        # 1st is the one to remove
        # need not to take care if 1st is the only one left
        # [1, 1] and remove all 1
        head = self.head
        while head and head.val == val:
            follower = head.next
            del head
            head = follower
        # empty list, [] or none
        if not head:
            self.head = None
            return
        # 2nd or others
        previous = head
        processing = previous.next
        while processing:
            if processing.val == val: # [1, 2, 3] and delete 2
                previous.next = processing.next
                del processing
                processing = previous.next
            else:
                previous = processing
                processing = processing.next
        # all done
        self.head = head


if __name__ == '__main__':
    example_1 = LinkList(1)
    print example_1.dump_elements()
    example_1.add_element(100)
    print example_1.dump_elements()
    print
    #
    example_1_2_3 = LinkList([1, 2, 3])
    print example_1_2_3.dump_elements()
    example_1_2_3.remove_elements(3)
    print example_1_2_3.dump_elements()
    print
    #
    example_2_4_6 = LinkList([2, 4, 6])
    print example_2_4_6.dump_elements()
    example_2_4_6.remove_elements(2)
    print example_2_4_6.dump_elements()
    print
    #
    example_1_2_3_2 = LinkList([1, 2, 3, 2])
    print example_1_2_3_2.dump_elements()
    example_1_2_3_2.remove_elements(2)
    print example_1_2_3_2.dump_elements()

