"""
Project 2
CSE 331 S23 (Onsay)
Authored By: Matt Kight & Lukas Richters & Sai Ramesh
Originally Authored By: Andrew McDonald, Alex Woodring & Andrew Haas
tests.py
"""

from solution import DLL, Node, BrowserHistory
from typing import TypeVar, List
from random import seed, randint, shuffle
import copy
import unittest
import string

# for more information on typehinting, check out https://docs.python.org/3/library/typing.html
T = TypeVar("T")  # represents generic type


class DLLTests(unittest.TestCase):

    def check_dll(self, expected: List[T], dll: DLL, multilevel: bool = False):
        """
        Assert structure of dll is proper and contains the values of result.
        Used as helper function throughout testcases. Not an actual testcase itself.
        Collapse/hide this by clicking the minus arrow on the left sidebar.

        :param expected: list of expected values in dll
        :param dll: DLL to be validated
        :param multilevel: remove the size check for multilevel DLLs
        :return: None. Raises exception and fails testcase if structure is DLL is not properly structured
                 or contains values different from those in result.
        """
        # check size
        if not multilevel:
            self.assertEqual(len(expected), dll.size)

        # short-circuit if empty list
        if len(expected) == 0:
            self.assertIsNone(dll.head)
            self.assertIsNone(dll.tail)
            return

        # check head and tail
        self.assertIsNone(dll.head.prev)
        self.assertIsNone(dll.tail.next)
        if isinstance(expected[0], tuple):
            for j, element in enumerate(expected[0]):
                self.assertEqual(element, dll.head.value[j])
            for j, element in enumerate(expected[-1]):
                self.assertEqual(element, dll.tail.value[j])
        else:
            self.assertEqual(expected[0], dll.head.value)
            self.assertEqual(expected[-1], dll.tail.value)

        # check all intermediate connections and values
        left, right = dll.head, dll.head.next
        i = 0
        while right is not None:
            self.assertIs(left.next, right)
            self.assertIs(left, right.prev)
            if isinstance(expected[i], tuple):
                for j, element in enumerate(expected[i]):
                    self.assertEqual(element, left.value[j])
                for j, element in enumerate(expected[i + 1]):
                    self.assertEqual(element, right.value[j])
            else:
                self.assertEqual(expected[i], left.value)
                self.assertEqual(expected[i + 1], right.value)
            left, right = left.next, right.next
            i += 1

        # check size after iteration with manual count
        if not multilevel:
            self.assertEqual(len(expected), i + 1)

    def test_empty(self):

        # (1) empty DLL
        dll = DLL()
        self.assertTrue(dll.empty())

        # (2) DLL with one node
        dll.head = dll.tail = Node(1)
        dll.size += 1
        self.assertFalse(dll.empty())

        # (3) DLL with multiple nodes
        for i in range(0, 50):
            dll.tail.next = Node(i, None, dll.tail)
            dll.tail = dll.tail.next
            dll.size += 1
            self.assertFalse(dll.empty())

        # (4) DLL after removing all nodes
        dll.head = dll.tail = None
        dll.size = 0
        self.assertTrue(dll.empty())

    def test_push(self):

        # (1) push single node on back
        dll = DLL()
        dll.push(0)
        self.assertIs(dll.head, dll.tail)  # see note 8 in specs for `is` vs `==`
        self.check_dll([0], dll)  # if failure here, see (1).
        # pro tip: use CTRL + B with your cursor on check_dll to jump to its definition at the top of the file.
        # then, use CTRL + Alt + RightArrow to jump back here!
        # https://www.jetbrains.com/help/pycharm/navigating-through-the-source-code.html

        # (2) push single node on front
        dll = DLL()
        dll.push(0, back=False)
        self.assertIs(dll.head, dll.tail)
        self.check_dll([0], dll)  # if failure here, see (2)

        # (3) push multiple nodes on back
        dll = DLL()
        lst = []
        for i in range(5):
            dll.push(i)
            lst.append(i)
            self.check_dll(lst, dll)  # if failure here, see (3)

        # (4) push multiple nodes on front
        dll = DLL()
        lst = []
        for i in range(5):
            dll.push(i, back=False)
            lst.insert(0, i)
            self.check_dll(lst, dll)  # if failure here, see (4)

        # (5) alternate pushing onto front and back
        dll = DLL()
        lst = []
        for i in range(50):
            dll.push(i, i % 2 == 0)  # push back if i is even, else push front
            if i % 2 == 0:  # pushed back, new tail
                lst.append(i)
                self.check_dll(lst, dll)  # if failure here, see (5)
            else:  # pushed front, new head
                lst.insert(0, i)
                self.check_dll(lst, dll)  # if failure here, see (5)

    def test_pop(self):

        # (1) pop back on empty list (should do nothing)
        dll = DLL()
        try:
            dll.pop()
        except Exception as e:
            self.fail(msg=f"Raised {type(e)} when popping from back of empty list.")

        # (2) pop front on empty list (should do nothing)
        dll = DLL()
        try:
            dll.pop(back=False)
        except Exception as e:
            self.fail(msg=f"Raised {type(e)} when popping from front of empty list.")

        # (3) pop back on multiple node list
        dll = DLL()
        lst = []
        for i in range(5):  # construct list
            dll.push(i)
            lst.append(i)
        for i in range(5):  # destruct list
            dll.pop()
            lst.pop()
            self.check_dll(lst, dll)  # if failure here, see (3)

        # (4) pop front on multiple node list
        dll = DLL()
        lst = []
        for i in range(5):  # construct list
            dll.push(i)
            lst.append(i)
        for i in range(5):  # destruct list
            dll.pop(back=False)
            lst.pop(0)
            self.check_dll(lst, dll)  # if failure here, see (4)

        # (5) alternate popping from front, back
        dll = DLL()
        lst = []
        for i in range(50):
            dll.push(i)
            lst.append(i)
        for end in range(49):  # remove all but one node
            dll.pop(end % 2 == 0)  # pop back if even, front if odd
            if end % 2 == 0:  # removed tail
                lst.pop()
                self.check_dll(lst, dll)  # if failure here, see (5)
            else:  # removed head
                lst.pop(0)
                self.check_dll(lst, dll)  # if failure here, see (5)

        # (6) check there is exactly one node left in DLL (middle of original), then remove
        self.check_dll([24], dll)  # if failure here, see (6)
        dll_copy = copy.deepcopy(dll)
        dll.pop()  # remove tail
        dll_copy.pop(back=False)  # remove head
        self.check_dll([], dll)  # if failure here, see (6)
        self.check_dll([], dll_copy)  # if failure here, see (6)

    def test_list_to_dll(self):

        # (1) create DLL from empty list
        dll = DLL()
        dll.list_to_dll([])
        self.check_dll([], dll)  # if failure here, see (1)

        # (2) create DLL from longer lists
        for i in range(50):
            source = list(range(i))
            dll = DLL()
            dll.list_to_dll(source)
            self.check_dll(source, dll)  # if failure here, see (2)

        # (3) check DLL is cleared and size is reset for each call to list_to_dll
        source = [1, 2, 3, 4]
        dll = DLL()
        dll.list_to_dll(source)
        self.check_dll(source, dll)  # if failure here, see (3)

        source = [5, 6, 7, 8]
        dll.list_to_dll(source)
        self.check_dll(source, dll)  # if failure here, see (3)

    def test_dll_to_list(self):

        # (1) create list from empty DLL
        dll = DLL()
        output = dll.dll_to_list()
        self.check_dll(output, dll)  # if failure here, see (1)

        # (2) create list from longer DLLs
        for i in range(50):
            dll = DLL()
            for j in range(i):
                dll.push(j)
            output = dll.dll_to_list()
            self.check_dll(output, dll)  # if failure here, see (2)

    def test_find(self):

        # (1) find in empty DLL
        dll = DLL()
        node = dll.find(331)
        self.assertIsNone(node)

        # (2) find existing value in single-node DLL
        dll = DLL()
        dll.push(0)
        node = dll.find(0)
        self.assertIsInstance(node, Node)
        self.assertEqual(0, node.value)
        self.assertIsNone(node.next)
        self.assertIsNone(node.prev)

        # (3) find non-existing value in single-node DLL
        node = dll.find(331)
        self.assertIsNone(node)

        # (4) find in longer DLL with all unique values
        dll = DLL()
        for i in range(10):
            dll.push(i)

        node = dll.find(0)
        self.assertIsInstance(node, Node)
        self.assertIs(dll.head, node)
        self.assertIsNone(node.prev)
        self.assertEqual(0, node.value)
        self.assertEqual(1, node.next.value)

        node = dll.find(9)
        self.assertIsInstance(node, Node)
        self.assertIs(dll.tail, node)
        self.assertIsNone(node.next)
        self.assertEqual(9, node.value)
        self.assertEqual(8, node.prev.value)

        node = dll.find(4)
        self.assertIsInstance(node, Node)
        self.assertEqual(4, node.value)
        self.assertEqual(3, node.prev.value)
        self.assertEqual(5, node.next.value)

        node = dll.find(331)
        self.assertIsNone(node)

        # (5) find first instance in longer DLL with duplicated values
        for i in range(9, 0, -1):  # DLL will be 0, 1, ..., 9, 9, 8, ..., 0
            dll.push(i)

        node = dll.find(0)  # should find head 0, not tail 0
        self.assertIsInstance(node, Node)
        self.assertIs(dll.head, node)
        self.assertIsNone(node.prev)
        self.assertEqual(0, node.value)
        self.assertEqual(1, node.next.value)

        node = dll.find(9)  # should find first 9
        self.assertIsInstance(node, Node)
        self.assertEqual(9, node.value)
        self.assertEqual(8, node.prev.value)
        self.assertEqual(9, node.next.value)

        node = dll.find(4)  # should find first 4
        self.assertIsInstance(node, Node)
        self.assertEqual(4, node.value)
        self.assertEqual(3, node.prev.value)
        self.assertEqual(5, node.next.value)

        node = dll.find(331)
        self.assertIsNone(node)

    def test_find_all(self):
        # (1) find_all in empty DLL
        dll = DLL()
        nodes = dll.find_all(331)
        self.assertEqual([], nodes)

        # (2) find_all existing value in single-node DLL
        dll = DLL()
        dll.push(0)
        nodes = dll.find_all(0)
        self.assertIsInstance(nodes, List)
        self.assertEqual(1, len(nodes))
        self.assertEqual(0, nodes[0].value)
        self.assertIsNone(nodes[0].next)
        self.assertIsNone(nodes[0].prev)

        # (3) find non-existing value in single-node DLL
        nodes = dll.find_all(331)
        self.assertEqual([], nodes)

        # (4) find_all in longer DLL with all unique values
        dll = DLL()
        for i in range(10):
            dll.push(i)

        nodes = dll.find_all(0)
        self.assertIsInstance(nodes, List)
        self.assertEqual(1, len(nodes))
        self.assertIs(dll.head, nodes[0])
        self.assertIsNone(nodes[0].prev)
        self.assertEqual(0, nodes[0].value)
        self.assertEqual(1, nodes[0].next.value)

        nodes = dll.find_all(9)
        self.assertIsInstance(nodes, List)
        self.assertEqual(1, len(nodes))
        self.assertIs(dll.tail, nodes[0])
        self.assertIsNone(nodes[0].next)
        self.assertEqual(9, nodes[0].value)
        self.assertEqual(8, nodes[0].prev.value)

        nodes = dll.find_all(4)
        self.assertIsInstance(nodes, List)
        self.assertEqual(1, len(nodes))
        self.assertEqual(4, nodes[0].value)
        self.assertEqual(3, nodes[0].prev.value)
        self.assertEqual(5, nodes[0].next.value)

        nodes = dll.find_all(331)
        self.assertEqual([], nodes)

        # (5) find all instances in longer DLL with duplicated values
        for i in range(9, -1, -1):  # DLL will be 0, 1, ..., 9, 9, 8, ..., 0
            dll.push(i)

        nodes = dll.find_all(0)
        self.assertIsInstance(nodes, List)
        self.assertEqual(2, len(nodes))
        self.assertIs(dll.head, nodes[0])
        self.assertIsNone(nodes[0].prev)
        self.assertEqual(0, nodes[0].value)
        self.assertEqual(1, nodes[0].next.value)
        self.assertIs(dll.tail, nodes[1])
        self.assertIsNone(nodes[1].next)
        self.assertEqual(0, nodes[1].value)
        self.assertEqual(1, nodes[1].prev.value)

        nodes = dll.find_all(9)
        self.assertIsInstance(nodes, List)
        self.assertEqual(2, len(nodes))
        self.assertEqual(9, nodes[0].value)
        self.assertEqual(8, nodes[0].prev.value)
        self.assertEqual(9, nodes[0].next.value)
        self.assertEqual(9, nodes[1].value)
        self.assertEqual(9, nodes[1].prev.value)
        self.assertEqual(8, nodes[1].next.value)

        nodes = dll.find_all(4)
        self.assertIsInstance(nodes, List)
        self.assertEqual(2, len(nodes))
        self.assertEqual(4, nodes[0].value)
        self.assertEqual(3, nodes[0].prev.value)
        self.assertEqual(5, nodes[0].next.value)
        self.assertEqual(4, nodes[1].value)
        self.assertEqual(5, nodes[1].prev.value)
        self.assertEqual(3, nodes[1].next.value)

        nodes = dll.find_all(331)
        self.assertEqual([], nodes)

    def test_remove(self):

        # (1) remove from empty DLL
        dll = DLL()
        result = dll.remove(331)
        self.assertFalse(result)

        # (2) remove existing value in single-node DLL
        dll = DLL()
        dll.push(0)
        result = dll.remove(0)
        self.assertTrue(result)
        self.check_dll([], dll)  # if failure here, see (2)

        # (3) remove non-existing value in single-node DLL
        dll = DLL()
        dll.push(0)
        result = dll.remove(331)
        self.assertFalse(result)
        self.check_dll([0], dll)  # if failure here, see (3)

        # (4) remove from longer DLL with all unique values
        dll = DLL()
        lst = []
        for i in range(10):
            dll.push(i)
            lst.append(i)

        to_remove = [1, 4, 7, 5, 6, 3, 2, 9, 0, 8]
        for i in range(10):
            result = dll.remove(to_remove[i])
            self.assertTrue(result)
            result = dll.remove(331)
            self.assertFalse(result)

            lst.remove(to_remove[i])
            self.check_dll(lst, dll)  # if failure here, see (4)

        # (5) remove first instance in longer DLL with duplicated values
        dll = DLL()
        lst = []
        for i in range(10):
            dll.push(i)
            lst.append(i)
        for i in range(9, -1, -1):  # DLL will be 0, 1, ..., 9, 9, 8, ..., 0
            dll.push(i)
            lst.append(i)

        to_remove = [1, 4, 7, 5, 6, 3, 2, 9, 0, 8]
        for i in range(10):
            result = dll.remove(to_remove[i])
            self.assertTrue(result)
            result = dll.remove(331)
            self.assertFalse(result)

            lst.remove(to_remove[i])
            self.check_dll(lst, dll)  # if failure here, see (5)

        # (6) sanity check after deletions
        lst = list(range(9, -1, -1))
        self.check_dll(lst, dll)  # if failure here, see (6)

    def test_remove_all(self):

        # (1) remove all from empty DLL
        dll = DLL()
        count = dll.remove_all(331)
        self.assertEqual(0, count)

        # (2) remove existing value in single-node DLL
        dll = DLL()
        dll.push(0)
        count = dll.remove_all(0)
        self.assertEqual(1, count)
        self.check_dll([], dll)  # if failure here, see (2)

        # (3) remove non-existing value in single-node DLL
        dll = DLL()
        dll.push(0)
        count = dll.remove_all(331)
        self.assertEqual(0, count)
        self.check_dll([0], dll)  # if failure here, see (3)

        # (4) remove from longer DLL with all unique values
        dll = DLL()
        lst = []
        for i in range(10):
            dll.push(i)
            lst.append(i)

        to_remove = [1, 4, 7, 5, 6, 3, 2, 9, 0, 8]
        for i in range(10):
            count = dll.remove_all(to_remove[i])
            self.assertEqual(1, count)
            count = dll.remove_all(331)
            self.assertEqual(0, count)

            lst.remove(to_remove[i])
            self.check_dll(lst, dll)  # if failure here, see (4)

        # (5) remove all in longer DLL with duplicated values
        dll = DLL()
        lst = []
        for i in range(10):
            dll.push(i)
            lst.append(i)
        for i in range(9, -1, -1):  # DLL will be 0, 1, ..., 9, 9, 8, ..., 0
            dll.push(i)
            lst.append(i)

        to_remove = [1, 4, 7, 5, 6, 3, 2, 9, 0, 8]
        for i in range(10):
            count = dll.remove_all(to_remove[i])
            self.assertEqual(2, count)
            count = dll.remove_all(331)
            self.assertEqual(0, count)

            lst.remove(to_remove[i])
            lst.remove(to_remove[i])  # remove both instances
            self.check_dll(lst, dll)  # if failure here, see (5)

        # (6) sanity check empty list after all deletions
        self.check_dll([], dll)  # if failure here, see (6)

    def test_reverse(self):

        # (1) reverse empty DLL
        dll = DLL()
        dll.reverse()
        self.check_dll([], dll)  # if failure here, see (1)

        # (2) reverse single-node DLL
        dll = DLL()
        dll.push(0)
        dll.reverse()
        self.check_dll([0], dll)  # if failure here, see (2)

        # (3) reverse longer DLL
        dll = DLL()
        lst = []
        for i in range(10):
            dll.push(i)
            lst.append(i)
        old_head, old_tail = dll.head, dll.tail
        dll.reverse()
        new_head, new_tail = dll.head, dll.tail
        lst.reverse()

        self.check_dll(lst, dll)
        self.assertIs(new_head, old_tail)
        self.assertIs(new_tail, old_head)

        # (4) reverse palindrome DLL
        dll = DLL()
        lst = []
        for i in range(10):
            dll.push(i)
            lst.append(i)
        for i in range(9, -1, -1):
            dll.push(i)
            lst.append(i)
        old_head, old_tail = dll.head, dll.tail
        dll.reverse()
        new_head, new_tail = dll.head, dll.tail
        lst.reverse()

        self.check_dll(lst, dll)
        self.assertIs(new_head, old_tail)
        self.assertIs(new_tail, old_head)

    def test_DLL_comprehensive(self):
        # test empty, append, prepend, pop, search, search_all, remove, remove_all
        dll = DLL()
        self.assertTrue(dll.empty())

        try:
            dll.pop()
        except:
            self.fail(msg="Exception not raised when popping from empty DLL")

        # test functions on large, randomly populated DLL containing 0-499 and duplicate values
        seed(331)

        dll = DLL()
        dll_rev = DLL()

        source = [randint(0, 499) for _ in range(500)]
        for i in range(500):
            dll.push(source[i])
            dll_rev.push(source[i], False)
        self.assertFalse(dll.empty())
        self.assertFalse(dll_rev.empty())
        self.assertEqual(dll.size, 500)
        self.assertEqual(dll_rev.size, 500)

        # test search
        for i in range(500):
            found = dll.find(source[i])
            self.assertIsInstance(found, Node)
            self.assertEqual(found.value, source[i])

        # test search_all
        for i in range(500):
            found = list(dll.find_all(source[i]))
            self.assertEqual(len(found), source.count(source[i]))
            for node in found:
                self.assertEqual(node.value, source[i])

        # test pop
        for i in range(500):
            dll.pop()
            dll_rev.pop()
        self.assertTrue(dll.empty())
        self.assertTrue(dll_rev.empty())

        # repopulate
        for i in range(500):
            dll.push(source[i])

        # test remove and remove_all
        for i in range(500):
            dll.remove(source[i])
            dll_rev.remove_all(source[i])
            self.assertEqual(dll.size, 499 - i)


class BrowserHistoryTests(unittest.TestCase):
    # Browser History Tests
    def test_get_current_url(self):
        # (1) Check for simple homepage return.
        homepage = 'https://google.com'
        bh = BrowserHistory(homepage)
        self.assertEqual('https://google.com', bh.get_current_url())

    def test_visit(self):

        # (1) Check that we can visit a new page from the homepage and get the 
        # correct url. Since the get current url test already tests for 
        # homepage return we can immediately check whether the visit method is 
        # working correctly.
        homepage = 'https://google.com'
        bh = BrowserHistory(homepage)
        bh.visit('https://linkedin.com')
        self.assertEqual('https://linkedin.com', bh.get_current_url())

        # (2) Check another website to ensure we can correctly visit new sites 
        # from other non-homepage sites.
        bh.visit('https://gm.com')
        self.assertEqual('https://gm.com', bh.get_current_url())

    def test_backward(self):
        homepage = 'https://google.com'
        bh = BrowserHistory(homepage)
        bh.visit('https://linkedin.com')
        bh.visit('https://gm.com')
        
        # (1) Test simple backwards command.
        bh.backward()
        self.assertEqual('https://linkedin.com', bh.get_current_url())

        # (2) Test that back won't generate an error when using from homepage.
        bh.backward()
        self.assertEqual('https://google.com', bh.get_current_url())
        bh.backward()
        self.assertEqual('https://google.com', bh.get_current_url())

    def test_forward(self):
        homepage = 'https://google.com'
        bh = BrowserHistory(homepage)
        bh.visit('https://linkedin.com')
        bh.visit('https://gm.com')

        # (1) Test simple forward command, back method should already be 
        # working.
        bh.backward()
        bh.forward()
        self.assertEqual('https://gm.com', bh.get_current_url())

        # (2) Test that for forward command does not surpass the newest url visited.
        bh.forward()
        self.assertEqual('https://gm.com', bh.get_current_url())

    def test_comprehensive_good_sites(self):
        homepage = 'https://google.com'
        bh = BrowserHistory(homepage)
        bh.visit('https://linkedin.com')
        bh.visit('https://gm.com')

        # (1) Test simple forward backward pass.
        bh.backward()
        bh.forward()
        self.assertEqual('https://gm.com', bh.get_current_url())

        # (2) Test visiting new site from non latest page.
        bh.backward()
        self.assertEqual('https://linkedin.com', bh.get_current_url())
        bh.visit('https://ford.com')
        self.assertEqual('https://ford.com', bh.get_current_url())

        # (3) Test that visiting a new site from non latest page uses the 
        # new visited site instead for forward history.
        bh.backward()
        self.assertEqual('https://linkedin.com', bh.get_current_url())
        bh.forward()
        self.assertEqual('https://ford.com', bh.get_current_url())
        bh.forward()
        self.assertEqual('https://ford.com', bh.get_current_url())

        # (4) Test that user removed all websites from non latest history branch
        # when visiting a new one
        bh.visit('https://apple.com')
        bh.visit('https://netflix.com')
        self.assertEqual('https://netflix.com', bh.get_current_url())
        bh.backward()
        bh.backward()
        bh.backward()
        self.assertEqual('https://linkedin.com', bh.get_current_url())
        bh.visit('https://gmail.com')
        self.assertEqual('https://gmail.com', bh.get_current_url())
        bh.forward()
        self.assertEqual('https://gmail.com', bh.get_current_url())
        bh.forward()
        self.assertEqual('https://gmail.com', bh.get_current_url())

        # (5) Test that if visit is same as next in history it still overides history
        bh.backward()
        bh.backward()
        self.assertEqual('https://google.com', bh.get_current_url())
        bh.visit('https://linkedin.com')
        bh.backward()
        bh.forward()
        self.assertEqual('https://linkedin.com', bh.get_current_url())
        bh.forward()
        self.assertEqual('https://linkedin.com', bh.get_current_url())
        
    def test_malicious_sites(self):
        homepage = 'https://google.com'
        bh = BrowserHistory(homepage)
        bh.visit('https://linkedin.com')
        bh.visit('https://malicious.com')

        # (1) Malicious sites should still be visited on visit command.
        self.assertEqual('https://malicious.com', bh.get_current_url())

        # (2) Test for a simple skip case.
        bh.visit('https://gm.com')

        bh.backward()
        self.assertEqual('https://linkedin.com', bh.get_current_url())

        bh.forward()
        self.assertEqual('https://gm.com', bh.get_current_url())

        # (2) Test for longer sequence of malicious sites.
        bh.visit('https://malware.com')
        bh.visit('https://phishing.com')
        bh.visit('https://malicious.com')
        bh.visit('https://ford.com')

        bh.backward()
        self.assertEqual('https://gm.com', bh.get_current_url())

        bh.forward()
        self.assertEqual('https://ford.com', bh.get_current_url())

        # (3) Rebase with malicious sites.
        bh.backward()
        bh.visit('https://apple.com')
        self.assertEqual('https://apple.com', bh.get_current_url())
        bh.forward()
        self.assertEqual('https://apple.com', bh.get_current_url())
        bh.backward()
        self.assertEqual('https://gm.com', bh.get_current_url())

        # (4) Test for ending in malicious site.
        bh.visit('https://malicious.com')
        bh.visit('https://phishing.com')
        self.assertEqual('https://phishing.com', bh.get_current_url())

        bh.backward()
        bh.forward()
        self.assertEqual('https://gm.com', bh.get_current_url())
        

if __name__ == '__main__':
    unittest.main()
