"""
Project 3 - Hybrid Sorting - Tests
CSE 331 Fall 2023
Nathan and Blake
"""

from collections import Counter, defaultdict
import unittest
import time
from random import seed, shuffle
from typing import List

from solution import selection_sort, bubble_sort, insertion_sort, hybrid_merge_sort, maximize_rewards
from itertools import combinations

seed(331)


class Project3Tests(unittest.TestCase):

    def test_selection_sort_basic(self):
        # (1) test with basic list of integers - default comparator
        data = [7, 4, 1, 0, 8, 9, 3, 2, 12]
        expected = sorted(data)
        selection_sort(data)
        self.assertEqual(expected, data)

        # (2) test with basic list of strings - default comparator
        data = ["dog", "banana", "orange", "tree", "clutter", "candy", "silence"]
        expected = sorted(data)
        selection_sort(data)
        self.assertEqual(expected, data)

        # (3) test with already sorted data - default comparator
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        expected = sorted(data)
        selection_sort(data)
        self.assertEqual(expected, data)

        # (4) test empty
        data = []
        selection_sort(data)
        self.assertEqual([], data)

        # (5) check that function does not return anything
        data = [5, 6, 3, 2]
        self.assertIsNone(selection_sort(data))

    def test_selection_sort_comparator(self):
        # (1) sort powers of ten by number of digits, in reverse
        data = [10 ** i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: -1 * len(str(x)))
        selection_sort(data, comparator=lambda x, y: len(str(x)) > len(str(y)))
        self.assertEqual(expected, data)

        # (2) sort strings by length
        data = ['a' * i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(x))
        selection_sort(data, comparator=lambda x, y: len(x) < len(y))
        self.assertEqual(expected, data)

    def test_selection_sort_descending(self):
        # (1) sort powers of ten by number of digits, in reverse
        data = [10 ** i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(str(x)), reverse=True)
        selection_sort(data, comparator=lambda x, y: len(str(x)) < len(str(y)), descending=True)
        self.assertEqual(expected, data)

        # (2) sort strings by length
        data = ['a' * i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(x), reverse=True)
        selection_sort(data, comparator=lambda x, y: len(x) < len(y), descending=True)
        self.assertEqual(expected, data)

    def test_selection_sort_comprehensive(self):
        # *********************************************************
        # ***WORTH NO POINTS, FOR PERSONAL TESTING PURPOSES ONLY***
        # *********************************************************

        # (1) sort a lot of integers
        data = list(range(1500))
        shuffle(data)
        expected = sorted(data)
        selection_sort(data)
        self.assertEqual(expected, data)

        # (3) sort a lot of integers with alternative comparator
        # this comparator (defined as a named lambda) compares values as follows:
        #   x < y
        #   if and only if
        #   sum(digits(x)) < sum(digits(y))
        # ex: 12 < 15 since 1 + 2 = 3 < 6 = 1 + 5
        def comp(x, y): return sum([int(digit) for digit in str(x)]) < sum([int(digit) for digit in str(y)])

        data = list(range(1500))
        expected = sorted(data, key=lambda x: sum([int(digit) for digit in str(x)]))
        selection_sort(data, comparator=comp)
        # there are multiple possible orderings, thus we must compare via sums of digits
        for index, item in enumerate(expected):
            expected_sum = sum([int(digit) for digit in str(item)])
            actual_sum = sum([int(digit) for digit in str(data[index])])
            self.assertEqual(expected_sum, actual_sum)

    def test_bubble_sort_basic(self):
        # (1) test with basic list of integers - default comparator
        data = [7, 4, 1, 0, 8, 9, 3, 2, 12]
        expected = sorted(data)
        bubble_sort(data)
        self.assertEqual(expected, data)

        # (2) test with basic list of strings - default comparator
        data = ["dog", "banana", "orange", "tree", "clutter", "candy", "silence"]
        expected = sorted(data)
        bubble_sort(data)
        self.assertEqual(expected, data)

        # (3) test with already sorted data - default comparator
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        expected = sorted(data)
        bubble_sort(data)
        self.assertEqual(expected, data)

        # (4) test empty
        data = []
        bubble_sort(data)
        self.assertEqual([], data)

        # (5) check that function does not return anything
        data = [5, 6, 3, 2]
        self.assertIsNone(bubble_sort(data))

    def test_bubble_sort_comparator(self):
        # (1) sort powers of ten by number of digits, in reverse
        data = [10 ** i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: -1 * len(str(x)))
        bubble_sort(data, comparator=lambda x, y: len(str(x)) > len(str(y)))
        self.assertEqual(expected, data)

        # (2) sort strings by length
        data = ['a' * i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(x))
        bubble_sort(data, comparator=lambda x, y: len(x) < len(y))
        self.assertEqual(expected, data)

    def test_bubble_sort_descending(self):
        # (1) sort powers of ten by number of digits, in reverse
        data = [10 ** i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(str(x)), reverse=True)
        bubble_sort(data, comparator=lambda x, y: len(str(x)) < len(str(y)), descending=True)
        self.assertEqual(expected, data)

        # (2) sort strings by length
        data = ['a' * i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(x), reverse=True)
        bubble_sort(data, comparator=lambda x, y: len(x) < len(y), descending=True)
        self.assertEqual(expected, data)

    def test_bubble_sort_comprehensive(self):
        # *********************************************************
        # ***WORTH NO POINTS, FOR PERSONAL TESTING PURPOSES ONLY***
        # *********************************************************

        # (1) sort a lot of integers
        # Smaller than the other comprehensive tests; bubble sort is slow!
        data = list(range(500))
        shuffle(data)
        expected = sorted(data)
        bubble_sort(data)
        self.assertEqual(expected, data)

        # (2) sort a lot of integers with alternative comparator
        # this comparator (defined as a named lambda) compares values as follows:
        #   x < y
        #   if and only if
        #   sum(digits(x)) < sum(digits(y))
        # ex: 12 < 15 since 1 + 2 = 3 < 6 = 1 + 5
        def comp(x, y): return sum([int(digit) for digit in str(x)]) < sum([int(digit) for digit in str(y)])

        data = list(range(500))
        expected = sorted(data, key=lambda x: sum([int(digit) for digit in str(x)]))
        bubble_sort(data, comparator=comp)
        # there are multiple possible orderings, thus we must compare via sums of digits
        for index, item in enumerate(expected):
            expected_sum = sum([int(digit) for digit in str(item)])
            actual_sum = sum([int(digit) for digit in str(data[index])])
            self.assertEqual(expected_sum, actual_sum)

    def test_insertion_sort_basic(self):
        # (1) test with basic list of integers - default comparator
        data = [7, 4, 1, 0, 8, 9, 3, 2, 12]
        expected = sorted(data)
        insertion_sort(data)
        self.assertEqual(expected, data)

        # (2) test with basic list of strings - default comparator
        data = ["dog", "banana", "orange", "tree", "clutter", "candy", "silence"]
        expected = sorted(data)
        insertion_sort(data)
        self.assertEqual(expected, data)

        # (3) test with already sorted data - default comparator
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        expected = sorted(data)
        insertion_sort(data)
        self.assertEqual(expected, data)

        # (4) test empty
        data = []
        insertion_sort(data)
        self.assertEqual([], data)

        # (5) check that function does not return anything
        data = [5, 6, 3, 2]
        self.assertIsNone(insertion_sort(data))

    def test_insertion_sort_comparator(self):
        # (1) sort powers of ten by number of digits, in reverse
        data = [10 ** i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: -1 * len(str(x)))
        insertion_sort(data, comparator=lambda x, y: len(str(x)) > len(str(y)))
        self.assertEqual(expected, data)

        # (2) sort strings by length
        data = ['a' * i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(x))
        insertion_sort(data, comparator=lambda x, y: len(x) < len(y))
        self.assertEqual(expected, data)

    def test_insertion_sort_descending(self):
        # (1) sort powers of ten by number of digits, in reverse
        data = [10 ** i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(str(x)), reverse=True)
        insertion_sort(data, comparator=lambda x, y: len(str(x)) < len(str(y)), descending=True)
        self.assertEqual(expected, data)

        # (2) sort strings by length
        data = ['a' * i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(x), reverse=True)
        insertion_sort(data, comparator=lambda x, y: len(x) < len(y), descending=True)
        self.assertEqual(expected, data)

    def test_insertion_sort_comprehensive(self):
        # *********************************************************
        # ***WORTH NO POINTS, FOR PERSONAL TESTING PURPOSES ONLY***
        # *********************************************************

        # (1) sort a lot of integers
        data = list(range(1500))
        shuffle(data)
        expected = sorted(data)
        insertion_sort(data)
        self.assertEqual(expected, data)

        # (2) sort a lot of integers with alternative comparator
        # this comparator (defined as a named lambda) compares values as follows:
        #   x < y
        #   if and only if
        #   sum(digits(x)) < sum(digits(y))
        # ex: 12 < 15 since 1 + 2 = 3 < 6 = 1 + 5
        def comp(x, y): return sum([int(digit) for digit in str(x)]) < sum([int(digit) for digit in str(y)])

        data = list(range(1500))
        expected = sorted(data, key=lambda x: sum([int(digit) for digit in str(x)]))
        insertion_sort(data, comparator=comp)
        # there are multiple possible orderings, thus we must compare via sums of digits
        for index, item in enumerate(expected):
            expected_sum = sum([int(digit) for digit in str(item)])
            actual_sum = sum([int(digit) for digit in str(data[index])])
            self.assertEqual(expected_sum, actual_sum)

    def test_hybrid_merge_sort_basic(self):
        # (1) test with basic list of integers - default comparator and threshold
        data = [7, 4, 1, 0, 8, 9, 3, 2, 12]
        expected = sorted(data)
        hybrid_merge_sort(data)
        self.assertEqual(expected, data)

        # (2) test with basic set of strings - default comparator and threshold
        data = ["dog", "banana", "orange", "tree", "clutter", "candy", "silence"]
        expected = sorted(data)
        hybrid_merge_sort(data)
        self.assertEqual(expected, data)

        # (3) test with already sorted data - default comparator and threshold
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        expected = sorted(data)
        hybrid_merge_sort(data)
        self.assertEqual(expected, data)

        # (4) test empty - default comparator and threshold
        data = []
        hybrid_merge_sort(data)
        self.assertEqual([], data)

        # (5) check that function does not return anything
        data = [5, 6, 3, 2]
        self.assertIsNone(hybrid_merge_sort(data, threshold=0))

    def test_hybrid_merge_sort_threshold(self):

        # first, all the tests from basic should work with higher thresholds

        # (1) test with basic list of integers - default comparator
        data = [7, 4, 1, 0, 8, 9, 3, 2, 12]
        expected = sorted(data)
        hybrid_merge_sort(data, threshold=2)
        self.assertEqual(expected, data)

        # (2) test with basic set of strings - default comparator
        data = ["dog", "banana", "orange", "tree", "clutter", "candy", "silence"]
        expected = sorted(data)
        hybrid_merge_sort(data, threshold=2)
        self.assertEqual(expected, data)

        # (3) test with already sorted data - default comparator
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        expected = sorted(data)
        hybrid_merge_sort(data, threshold=2)
        self.assertEqual(expected, data)

        # (4) now, for a longer test - a bunch of thresholds
        data = list(range(25))
        expected = sorted(data)
        for t in range(11):
            shuffle(data)
            hybrid_merge_sort(data, threshold=t)
            self.assertEqual(expected, data)

    def test_hybrid_merge_sort_comparator(self):
        # (1) sort powers of ten by number of digits, in reverse
        data = [10 ** i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: -1 * len(str(x)))
        hybrid_merge_sort(data, comparator=lambda x, y: len(str(x)) > len(str(y)))
        self.assertEqual(expected, data)

        # (2) sort strings by length
        data = ['a' * i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(x))
        hybrid_merge_sort(data, comparator=lambda x, y: len(x) < len(y))
        self.assertEqual(expected, data)

    def test_hybrid_merge_sort_descending(self):
        # (1) test with basic list of integers - default comparator, threshold of zero
        data = [7, 4, 1, 0, 8, 9, 3, 2, 12]
        expected = sorted(data, reverse=True)
        hybrid_merge_sort(data, threshold=0, descending=True)
        self.assertEqual(expected, data)

        # (2) test with basic list of strings - default comparator, threshold
        data = ["dog", "banana", "orange", "tree", "clutter", "candy", "silence"]
        expected = sorted(data, reverse=True)
        hybrid_merge_sort(data, threshold=0, descending=True)
        self.assertEqual(expected, data)

        # (3) test with already sorted data - default comparator, threshold
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        expected = sorted(data, reverse=True)
        hybrid_merge_sort(data, threshold=0, descending=True)
        self.assertEqual(expected, data)

        # (4) test empty
        data = []
        hybrid_merge_sort(data, threshold=0, descending=True)
        self.assertEqual([], data)

        # (5) check that function does not return anything
        data = [5, 6, 3, 2]
        self.assertIsNone(hybrid_merge_sort(data, threshold=0, descending=True))

        # (6) now let's test with multiple thresholds
        data = list(range(50))
        expected = sorted(data, reverse=True)
        for t in range(20):
            shuffle(data)
            hybrid_merge_sort(data, threshold=t, descending=True)
            self.assertEqual(expected, data)

    def test_hybrid_merge_sort_comprehensive(self):
        # *********************************************************
        # ***WORTH NO POINTS, FOR PERSONAL TESTING PURPOSES ONLY***
        # *********************************************************

        # (1) sort a lot of integers, with a lot of thresholds
        data = list(range(500))
        for t in range(100):
            shuffle(data)
            expected = sorted(data)
            hybrid_merge_sort(data, threshold=t)
            self.assertEqual(expected, data)

        # (2) sort a lot of integers with alternative comparator, threshold of 8
        # this comparator (defined as a named lambda) compares values as follows:
        #   x < y
        #   if and only if
        #   sum(digits(x)) < sum(digits(y))
        # ex: 12 < 15 since 1 + 2 = 3 < 6 = 1 + 5
        def comp(x, y):
            return sum([int(digit) for digit in str(x)]) < sum([int(digit) for digit in str(y)])

        data = list(range(1500))
        expected = sorted(data, key=lambda x: sum([int(digit) for digit in str(x)]))
        hybrid_merge_sort(data, threshold=8, comparator=comp)
        # there are multiple possible orderings, thus we must compare via sums of digits
        for index, item in enumerate(expected):
            expected_sum = sum([int(digit) for digit in str(item)])
            actual_sum = sum([int(digit) for digit in str(data[index])])
            self.assertEqual(expected_sum, actual_sum)

        # (3) sort a lot of integers with alternative comparator, thresholds in [1,...,49]
        # this comparator (defined as a named lambda) compares values as follows:
        #   x < y
        #   if and only if
        #   sum(digits(x)) < sum(digits(y))
        # ex: 12 < 15 since 1 + 2 = 3 < 6 = 1 + 5
        def comp(x, y):
            return sum([int(digit) for digit in str(x)]) < sum([int(digit) for digit in str(y)])

        data = list(range(1000))
        expected = sorted(data, key=lambda x: sum([int(digit) for digit in str(x)]))
        for t in range(50):
            shuffle(data)
            hybrid_merge_sort(data, threshold=t, comparator=comp)
            for index, item in enumerate(expected):
                expected_sum = sum([int(digit) for digit in str(item)])
                actual_sum = sum([int(digit) for digit in str(data[index])])
                self.assertEqual(expected_sum, actual_sum)

    def test_hybrid_merge_sort_speed(self):
        # *********************************************************
        # ***WORTH NO POINTS, FOR PERSONAL TESTING PURPOSES ONLY***
        # *********************************************************
        # the point of this sort is to be fast, right?
        # this (probably) won't finish if you're not careful with time complexity
        # but it isn't a guarantee
        data = list(range(300000))
        expected = data[:]
        shuffle(data)
        hybrid_merge_sort(data)
        self.assertEqual(expected, data)

    def test_hybrid_merge_actually_hybrid(self):
        # *********************************************************
        # ***WORTH NO POINTS, FOR PERSONAL TESTING PURPOSES ONLY***
        # *********************************************************
        # this test is to make sure that the hybrid merge sort is actually
        # hybrid, i.e calls insertion sort when appropriate

        from collections.abc import MutableSequence
        from collections import defaultdict
        calling_functions = defaultdict(set)

        class MyList(MutableSequence):
            # This class was taken from
            # https://stackoverflow.com/questions/6560354/how-would-i-create-a-custom-list-class-in-python
            def __init__(self, data=None):
                super(MyList, self).__init__()
                self._list = list(data)

            def __delitem__(self, ii):
                """Delete an item"""
                del self._list[ii]

            def __setitem__(self, ii, val):
                self._list[ii] = val

            def insert(self, ii, val):
                self._list.insert(ii, val)

            def __len__(self):
                """List length"""
                return len(self._list)

            def __getitem__(self, ii):
                import inspect
                calling_functions[inspect.stack()[1].function].add(len(self))
                if isinstance(ii, slice):
                    return self.__class__(self._list[ii])
                else:
                    return self._list[ii]

        data = MyList(range(50))
        hybrid_merge_sort(data, threshold=2)
        self.assertIn('insertion_sort', calling_functions)
        self.assertIn('hybrid_merge_sort', calling_functions)
        self.assertTrue(all(length <= 2 for length in calling_functions['insertion_sort']))
        self.assertAlmostEqual(len(calling_functions['hybrid_merge_sort']), 10, delta=2)

    def test_maximize_rewards(self):
        # (1) Empty Case
        prices = []
        output = maximize_rewards(prices)
        expected = ([], -1)
        self.assertEqual(output, expected)

        # (2) Single Input Case
        prices = [10]
        output = maximize_rewards(prices)
        expected = ([], -1)
        self.assertEqual(output, expected)

        # (3) Odd Case
        prices = [10, 1, 22]
        output = maximize_rewards(prices)
        expected = ([], -1)
        self.assertEqual(output, expected)

        # (4) Odd Case Longer
        prices = [10, 1, 22, 2, 14, 16, 19, 58, 49]
        output = maximize_rewards(prices)
        expected = ([], -1)
        self.assertEqual(output, expected)

        # (5) Even Case Medium Length
        prices = [3, 2, 5, 1, 3, 4]
        output = maximize_rewards(prices)
        expected = ([(1, 5), (2, 4), (3, 3)], 22)
        self.assertEqual(output, expected)

        # (6) Even Case Short Length
        prices = [3, 4]
        output = maximize_rewards(prices)
        expected = ([(3, 4)], 12)
        self.assertEqual(output, expected)

        # (7) Even Case Long Length
        prices = [4, 5, 6, 3, 1, 8, 2, 7, 9, 0]
        output = maximize_rewards(prices)
        expected = ([(0, 9), (1, 8), (2, 7), (3, 6), (4, 5)], 60)
        self.assertEqual(output, expected)

        # (8) Even Case No Common Sum Short Length
        prices = [1, 9, 10, 4]
        output = maximize_rewards(prices)
        expected = ([], -1)
        self.assertEqual(output, expected)

        # (9) Even Case No Common Sum Medium Length
        prices = [1, 1, 2, 3, 7, 4, 6, 10]
        output = maximize_rewards(prices)
        expected = ([], -1)
        self.assertEqual(output, expected)

        # (10) Even Case No Common Sum Long Length
        prices = [837, 125, 449, 742, 612, 389, 946, 208, 571, 690, 297, 876, 164, 733, 523, 961, 418, 752, 683, 335,
                  578, 874, 216, 492, 811, 119, 670, 556, 295, 944]
        output = maximize_rewards(prices)
        expected = ([], -1)
        self.assertEqual(output, expected)

        # (11) Even Case All Same Numbers
        prices = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
        output = maximize_rewards(prices)
        expected = ([(3, 3), (3, 3), (3, 3), (3, 3), (3, 3)], 45)
        self.assertEqual(output, expected)

        # (12) Even Case Competence Check 1
        prices = [17, 33, 19, 31, 24, 26, 11, 39, 5, 45, 7, 43, 1, 49, 9, 41, 4, 46, 3, 47, 8, 42, 22, 28, 25, 25, 10,
                  40, 18, 32, 12, 38, 16, 34, 13, 37, 21, 29, 6, 44, 23, 27, 15, 35, 20, 30, 2, 48, 14, 36]
        output = maximize_rewards(prices)
        expected = ([(1, 49), (2, 48), (3, 47), (4, 46), (5, 45), (6, 44), (7, 43), (8, 42), (9, 41), (10, 40),
                     (11, 39), (12, 38), (13, 37), (14, 36), (15, 35), (16, 34), (17, 33), (18, 32), (19, 31),
                     (20, 30), (21, 29), (22, 28), (23, 27), (24, 26), (25, 25)], 10725)
        self.assertEqual(output, expected)

        # (13) Even Case Competence Check 2
        prices = [15, 45, 27, 33, 4, 56, 23, 37, 26, 34, 7, 53, 5, 55, 28, 32, 30, 30, 9, 51, 18, 42, 25, 35, 14, 46,
                  2, 58, 11, 49, 17, 43, 22, 38, 13, 47, 6, 54, 12, 48, 10, 50, 8, 52, 29, 31, 19, 41, 21, 39, 20,
                  40, 16, 44, 1, 59, 3, 57, 24, 36]
        output = maximize_rewards(prices)
        expected = ([(1, 59), (2, 58), (3, 57), (4, 56), (5, 55), (6, 54), (7, 53), (8, 52), (9, 51), (10, 50),
                     (11, 49), (12, 48), (13, 47), (14, 46), (15, 45), (16, 44), (17, 43), (18, 42), (19, 41),
                     (20, 40), (21, 39), (22, 38), (23, 37), (24, 36), (25, 35), (26, 34), (27, 33), (28, 32),
                     (29, 31), (30, 30)], 18445)
        self.assertEqual(output, expected)

        # (14) Long Case, two outlier
        prices = [15, 45, 27, 33, 4, 56, 23, 37, 26, 34, 7, 53, 5, 55, 28, 32, 30, 30, 9, 51, 18, 42, 25, 35, 14, 46,
                  2, 58, 11, 49, 17, 43, 22, 38, 13, 47, 6, 54, 12, 48, 10, 50, 8, 52, 29, 31, 19, 41, 21, 39, 20,
                  40, 16, 44, 1, 59, 3, 57, 24, 36, 220, 300]
        output = maximize_rewards(prices)
        expected = ([], -1)
        self.assertEqual(output, expected)


if __name__ == '__main__':
    unittest.main()
