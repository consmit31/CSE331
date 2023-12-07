"""
Nathan Gu and Blake Potvin
Sorting Project - Starter
CSE 331 Fall 2023
"""

import random
import time
from typing import TypeVar, List, Callable, Dict, Tuple
from dataclasses import dataclass

T = TypeVar("T")  # represents generic type


# do_comparison is an optional helper function but HIGHLY recommended!!!
def do_comparison(first: T, second: T, comparator: Callable[[T, T], bool], descending: bool) -> bool:
    """
    Compare two elements, 'first' and 'second', using the provided 'comparator' function.

    :param first: The first element to compare.
    :param second: The second element to compare.
    :param comparator: A function that compares two elements and returns a boolean value.
    :param descending: If True, indicates descending order; if False, indicates ascending order.

    :returns: True if 'first' should be placed before 'second' based on the comparison criteria, False otherwise.
    """
    if descending:
        return comparator(second, first) > 0
    else:
        return comparator(first, second) > 0


def selection_sort(data: List[T], *, comparator: Callable[[T, T], bool] = lambda x, y: x < y,
                   descending: bool = False) -> None:
    """
    Given a list of values, sort that list in-place using the selection sort algorithm and the provided comparator, and
            perform the sort in descending order if descending is True.
    :param data: List of items to be sorted
    :param comparator: A function which takes two arguments of type T and returns True when the first argument should be
            treated as less than the second argument.
    :param descending: Perform the sort in descending order when this is True. Defaults to False.
    """
    first_unsorted = 0
    for i in range(len(data)):
        smallest = i
        for j in range(i+1, len(data)):
            if do_comparison(data[j], data[smallest], comparator, descending):
                smallest = j

        data[i], data[smallest] = data[smallest], data[i]
def bubble_sort(data: List[T], *, comparator: Callable[[T, T], bool] = lambda x, y: x < y,
                descending: bool = False) -> None:
    """
    Given a list of values, sort that list in-place using the bubble sort algorithm and the provided comparator, and
            perform the sort in descending order if descending is True.
    :param data: List of items to be sorted
    :param comparator: A function which takes two arguments of type T and returns True when the first argument should be treated as less than the second argument.
    :param descending: Perform the sort in descending order when this is True. Defaults to False.
    """
    for i in range(len(data)-1):
        for j in range(len(data)-i-1):
            if do_comparison(data[j+1], data[j], comparator, descending):
                data[j], data[j+1] = data[j+1], data[j]


def insertion_sort(data: List[T], *, comparator: Callable[[T, T], bool] = lambda x, y: x < y,
                   descending: bool = False) -> None:
    """
    Given a list of values, sort that list in-place using the insertion sort algorithm and the provided comparator,
            and perform the sort in descending order if descending is True.
    :param data: List of items to be sorted
    :param comparator: A function which takes two arguments of type T and returns True when the first argument should be
            treated as less than the second argument.
    :param descending: Perform the sort in descending order when this is True. Defaults to False.
    """
    for i in range(len(data)-1):
        curr = i
        for j in range(i+1, len(data)):
            if do_comparison(data[j], data[curr], comparator, descending):
                curr = j

        data[i], data[curr] = data[curr], data[i]

def hybrid_merge_sort(data: List[T], *, threshold: int = 12,
                      comparator: Callable[[T, T], bool] = lambda x, y: x < y, descending: bool = False) -> None:
    """
    Given a list of values, sort that list using a hybrid sort with the merge sort and insertion sort algorithms and the
     provided comparator, and perform the sort in descending order if descending is True. The function should
     use insertion_sort to sort lists once their size is less than or equal to threshold, and otherwise perform a merge
     sort.

    :param data: List of items to be sorted
    :param threshold: Maximum size at which insertion sort will be used instead of merge sort.
    :param comparator: A function which takes two arguments of type T and returns True when the first argument should
    be treated as less than the second argument.
    :param descending: Perform the sort in descending order when this is True. Defaults to False
    """
    n = len(data)
    if n == 1:
        return

    mergedNumbers = [0]*n
    if n <= threshold:
        insertion_sort(data, comparator=comparator, descending=descending)
        return
    else:
        mid = n // 2
        lower = data[:mid]
        upper = data[mid:]

        hybrid_merge_sort(lower, threshold=threshold, comparator=comparator, descending=descending)
        hybrid_merge_sort(upper, threshold=threshold, comparator=comparator, descending=descending)

        a = b = mergePos = 0
        while a < len(lower) and b < len(upper):
            if do_comparison(lower[a], upper[b], comparator, descending):
                mergedNumbers[mergePos] = lower[a]
                a += 1
            else:
                mergedNumbers[mergePos] = upper[b]
                b += 1
            mergePos += 1

        while a < len(lower):
            mergedNumbers[mergePos] = lower[a]
            a += 1
            mergePos += 1

        while b < len(upper):
            mergedNumbers[mergePos] = upper[b]
            b += 1
            mergePos += 1

        data[:] = mergedNumbers


def maximize_rewards(item_prices: List[int]) -> (List[Tuple[int, int]], int):
    """
    Each pair's combined item prices should equal a consistent amount. Additionally, compute the collective rewards
    points for all pairs

    :param item_prices: A list representing the price of each food item your friends wish to order.

    :return: A tuple comprising of a list of tuples, each tuple captures two item prices, ensuring the sum is consistent
    across all pairs with the smaller price preceding the larger within each tuple and An integer that represents the
    aggregated reward points.
    """
    order = []
    tot_rewards = 0

    if not item_prices or len(item_prices) % 2 == 1:
        return order, -1

    hybrid_merge_sort(item_prices)
    for index, item in enumerate(item_prices):
        back_item = item_prices[-1 * (index+1)]
        order.append((item, back_item))
        if len(order)*2 == len(item_prices):
            break

    com_sum = 2 * sum(item_prices) / len(item_prices)
    for tup in order:
        tot_rewards += tup[0] * tup[1]
        if sum(tup) != com_sum:
            return [], -1

    return order, tot_rewards


def quicksort(data) -> None:
    """
    Sorts a list in place using quicksort
    :param data: Data to sort
    """

    def quicksort_inner(first, last) -> None:
        """
        Sorts portion of list at indices in interval [first, last] using quicksort

        :param first: first index of portion of data to sort
        :param last: last index of portion of data to sort
        """
        # List must already be sorted in this case
        if first >= last:
            return

        left = first
        right = last

        # Need to start by getting median of 3 to use for pivot
        # We can do this by sorting the first, middle, and last elements
        midpoint = (right - left) // 2 + left
        if data[left] > data[right]:
            data[left], data[right] = data[right], data[left]
        if data[left] > data[midpoint]:
            data[left], data[midpoint] = data[midpoint], data[left]
        if data[midpoint] > data[right]:
            data[midpoint], data[right] = data[right], data[midpoint]
        # data[midpoint] now contains the median of first, last, and middle elements
        pivot = data[midpoint]
        # First and last elements are already on right side of pivot since they are sorted
        left += 1
        right -= 1

        # Move pointers until they cross
        while left <= right:
            # Move left and right pointers until they cross or reach values which could be swapped
            # Anything < pivot must move to left side, anything > pivot must move to right side
            #
            # Not allowing one pointer to stop moving when it reached the pivot (data[left/right] == pivot)
            # could cause one pointer to move all the way to one side in the pathological case of the pivot being
            # the min or max element, leading to infinitely calling the inner function on the same indices without
            # ever swapping
            while left <= right and data[left] < pivot:
                left += 1
            while left <= right and data[right] > pivot:
                right -= 1

            # Swap, but only if pointers haven't crossed
            if left <= right:
                data[left], data[right] = data[right], data[left]
                left += 1
                right -= 1

        quicksort_inner(first, left - 1)
        quicksort_inner(left, last)

    # Perform sort in the inner function
    quicksort_inner(0, len(data) - 1)
