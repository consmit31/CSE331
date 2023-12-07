"""
Project 5: Deque
CSE 331 FS23
Authored by Gabriel Sotelo
starter.py
"""

import gc
from typing import TypeVar, List
from random import randint, shuffle
from timeit import default_timer
# COMMENT OUT THIS LINE (and `plot_speed`) if you don't want matplotlib
#from matplotlib import pyplot as plt
import os
os.environ['MPLCONFIGDIR'] = "/home/codio/workspace/config"

T = TypeVar('T')
CDLLNode = type('CDLLNode')

class CircularDeque:
    """
    Representation of a Circular Deque using an underlying python list
    """

    __slots__ = ['capacity', 'size', 'queue', 'front', 'back']

    def __init__(self, data: List[T] = None, front: int = 0, capacity: int = 4):
        """
        Initializes an instance of a CircularDeque
        :param data: starting data to add to the deque, for testing purposes
        :param front: where to begin the insertions, for testing purposes
        :param capacity: number of slots in the Deque
        """
        if data is None and front != 0:
            # front will get set to 0 by front_enqueue if the initial data is empty
            data = ['Start']
        elif data is None:
            data = []

        self.capacity: int = capacity
        self.size: int = len(data)
        self.queue: List[T] = [None] * capacity
        self.back: int = None if not data else self.size + front - 1
        self.front: int = front if data else None

        for index, value in enumerate(data):
            self.queue[index + front] = value

    def __str__(self) -> str:
        """
        Provides a string representation of a CircularDeque
        'F' indicates front value
        'B' indicates back value
        :return: the instance as a string
        """
        if self.size == 0:
            return "CircularDeque <empty>"

        str_list = [f"CircularDeque <"]
        for i in range(self.capacity):
            str_list.append(f"{self.queue[i]}")
            if i == self.front:
                str_list.append('(F)')
            elif i == self.back:
                str_list.append('(B)')
            if i < self.capacity - 1:
                str_list.append(',')

        str_list.append(">")
        return "".join(str_list)

    __repr__ = __str__

    # ============ Modifiy Functions Below ============#

    def __len__(self) -> int:
        """
        Returns the length/size of the circular deque

        :param: None
        """
        return self.size

    def is_empty(self) -> bool:
        """
        Returns a boolean indicating if the circular deque is empty

        :param: None
        """
        if self.size == 0:
            return True
        return False

    def front_element(self) -> T:
        """
        Returns the first element in the circular deque

        :return: None
        """
        if self.size != 0:
            return self.queue[self.front]
        return None

    def back_element(self) -> T:
        """
        Returns the back element in the circular deque

        :return: None
        """
        if self.size != 0:
            return self.queue[self.back]
        return None

    def grow(self) -> None:
        """
        Doubles the capacity of CD by creating a new underlying python list with double the capacity of the old one and
        copies the values over from the current list. The new copied list will be 'unrolled' s.t. the front element will
        be at index 0 and the tail element will be at index [size - 1].

        :return: None
        """

        new_deque = [None] * (self.capacity*2)
        if self.size != 0:
            for i in range(self.capacity):
                new_deque[i] = self.queue[(self.front+i) % self.capacity]

        self.front = 0
        self.back = self.size-1
        self.queue = new_deque
        self.capacity *= 2

    def shrink(self) -> None:
        """
        Cuts the capacity of the queue in half using the same idea as grow. Copy over contents of the old list to a new
        list with half the capacity. The new copied list will be 'unrolled' s.t. the front element will be at index 0
        and the tail element will be at index [size - 1].

        :return: None
        """

        new_queue = [None] * (self.capacity//2)
        for i in range(self.size):
            new_queue[i] = self.queue[(self.front + i) % self.capacity]

        self.front = 0
        self.back = self.size-1
        self.queue = new_queue
        self.capacity //= 2

    def enqueue(self, value: T, front: bool = True) -> None:
        """
        Add a value to either the front or back of the circular deque based off the parameter front

        :return: None.
        """
        if self.size == 0:
            self.front = 0
            self.back = 0
            self.queue[0] = value
        elif front:
            self.front = (self.front+self.capacity-1) % self.capacity
            self.queue[self.front] = value
        else:
            self.back = (self.back+1) % self.capacity
            self.queue[self.back] = value

        if (self.size+1) == self.capacity:
            self.grow()
            self.back += 1
        self.size += 1

    def dequeue(self, front: bool = True) -> T:
        """
        Deletes a value from either the front or back of the circular deque based off the parameter front

        :return: Value dequeued
        """
        if self.size == 0:
            return None
        elif front:
            ret = self.queue[self.front]
            self.front = (self.front+self.capacity+1) % self.capacity
        else:
            ret = self.queue[self.back]
            self.back = (self.back-1) % self.capacity

        self.size -= 1
        if self.size <= self.capacity//4 and (self.capacity // 2) >= 4:
            self.shrink()

        return ret

class CDLLNode:
    """
    Node for the CDLL
    """

    __slots__ = ['val', 'next', 'prev']

    def __init__(self, val: T, next: CDLLNode = None, prev: CDLLNode = None) -> None:
        """
        Creates a CDLL node
        :param val: value stored by the next
        :param next: the next node in the list
        :param prev: the previous node in the list
        :return: None
        """
        self.val = val
        self.next = next
        self.prev = prev

    def __eq__(self, other: CDLLNode) -> bool:
        """
        Compares two CDLLNodes by value
        :param other: The other node
        :return: true if comparison is true, else false
        """
        return self.val == other.val

    def __str__(self) -> str:
        """
        Returns a string representation of the node
        :return: string
        """
        return "<= (" + str(self.val) + ") =>"

    __repr__ = __str__


class CDLL:
    """
    A (C)ircular (D)oubly (L)inked (L)ist
    """

    __slots__ = ['head', 'size']

    def __init__(self) -> None:
        """
        Creates a CDLL
        :return: None
        """
        self.size = 0
        self.head = None

    def __len__(self) -> int:
        """
        :return: the size of the CDLL
        """
        return self.size

    def __eq__(self, other: 'CDLL') -> bool:
        """
        Compares two CDLLs by value
        :param other: the other CDLL
        :return: true if comparison is true, else false
        """
        n1: CDLLNode = self.head
        n2: CDLLNode = other.head
        for _ in range(self.size):
            if n1 != n2:
                return False
            n1, n2 = n1.next, n2.next
        return True

    def __str__(self) -> str:
        """
        :return: a string representation of the CDLL
        """
        n1: CDLLNode = self.head
        joinable: List[str] = []
        while n1 is not self.head:
            joinable.append(str(n1))
            n1 = n1.next
        return ''.join(joinable)

    __repr__ = __str__

    # ============ Modifiy Functions Below ============#

    def insert(self, val: T, front: bool = True) -> None:
        """
        inserts a node with value val in the front or back of the CDLL

        :param val: the value to insert
        :param front: whether to insert in the front of the list, or the back
        :return: None
        """

        temp = CDLLNode(val)
        if self.size == 0:
            self.head = temp
            self.head.next = self.head
            self.head.prev = self.head
        elif front:
            temp.next = self.head
            self.head.prev.next = temp
            temp.prev = self.head.prev
            self.head.prev = temp
            self.head = temp
        else:
            temp.next = self.head
            self.head.prev.next = temp
            temp.prev = self.head.prev
            self.head.prev = temp

        self.size += 1

    def remove(self, front: bool = True) -> None:
        """
        removes a node from the CDLL

        :param front: whether to remove from the front of the list, or the back
        :return: None
        """
        if self.size == 0:
            return None
        if self.size == 1:
            self.head = None
            self.size = 0
            return None
        elif front:
            self.head.next.prev = self.head.prev
            self.head.prev.next = self.head.next
            self.head = self.head.next
        else:
            self.head.prev = self.head.prev.prev
            self.head.prev.next = self.head


        self.size -= 1


class CDLLCD:
    """
    (C)ircular (D)oubly (L)inked (L)ist (C)ircular (D)equeue
    This is essentially just an interface for the above
    """

    def __init__(self) -> None:
        """
        Initializes the CDLLCD to an empty CDLL
        :return: None
        """
        self.CDLL: CDLL = CDLL()

    def __eq__(self, other: 'CDLLCD') -> bool:
        """
        Compares two CDLLCDs by value
        :param other: the other CDLLCD
        :return: true if equal, else false
        """
        return self.CDLL == other.CDLL

    def __str__(self) -> str:
        """
        :return: string representation of the CDLLCD
        """
        return str(self.CDLL)

    __repr__ = __str__

    # ============ Modifiy Functions Below ============#
    def __len__(self) -> int:
        """
        Gives length of CDLLCD
        """
        return self.CDLL.size

    def is_empty(self) -> bool:
        """
        Returns True if CDLLCD is empty, False if else
        """
        if self.CDLL.size == 0:
            return True
        return False

    def front_element(self) -> T:
        """
        Returns front element of CDLLCD
        """
        if self.CDLL.head:
            return self.CDLL.head.val

    def back_element(self) -> T:
        """
        FILL OUT DOCSTRING
        """
        if self.CDLL.head:
            return self.CDLL.head.prev.val

    def enqueue(self, val: T, front: bool = True) -> None:
        """
        Adds a value to the CDLLCD

        :param val: value to be added to CDLLCD
        :param front: determines whether to add to the front or back of list
        """
        self.CDLL.insert(val, front)

    def dequeue(self, front: bool = True) -> T:
        """
        FILL OUT DOCSTRING
        """
        if front:
            ret = self.front_element()
        else:
            ret = self.back_element()

        self.CDLL.remove(front)

        return ret


def plot_speed():
    """
    Compares performance of the CDLLCD and the standard array based deque
    """

    # First we'll test sequences of basic operations

    sizes = [100*i for i in range(0, 200, 5)]

    # (1) Grow large
    grow_avgs_array = []
    grow_avgs_CDLL = []

    for size in sizes:
        grow_avgs_array.append(0)
        grow_avgs_CDLL.append(0)
        data = list(range(size))
        for trial in range(3):

            gc.collect()  # What happens if you remove this? Hint: memory fragmention
            cd_array = CircularDeque()
            cd_DLL = CDLLCD()

            # randomize data
            shuffle(data)

            start = default_timer()
            for item in data:
                cd_array.enqueue(item, item % 2)
            grow_avgs_array[-1] += (default_timer() - start)/3

            start = default_timer()
            for item in data:
                cd_DLL.enqueue(item, item % 2)
            grow_avgs_CDLL[-1] += (default_timer() - start)/3

    plt.plot(sizes, grow_avgs_array, color='blue', label='Array')
    plt.plot(sizes, grow_avgs_CDLL, color='red', label='CDLL')
    plt.title("Enqueue and Grow")
    plt.legend(loc='best')
    plt.show()

    # (2) Grow Large then Shrink to zero

    shrink_avgs_array = []
    shrink_avgs_CDLL = []

    for size in sizes:
        shrink_avgs_array.append(0)
        shrink_avgs_CDLL.append(0)
        data = list(range(size))

        for trial in range(3):

            gc.collect()
            cd_array = CircularDeque()
            cd_DLL = CDLLCD()

            # randomize data
            shuffle(data)

            start = default_timer()
            for item in data:
                cd_array.enqueue(item, item % 2)
            for item in data:
                cd_array.dequeue(not item % 2)
            shrink_avgs_array[-1] += (default_timer() - start)/3

            start = default_timer()
            for item in data:
                cd_DLL.enqueue(item, item % 2)
            for item in data:
                cd_DLL.dequeue(not item % 2)
            shrink_avgs_CDLL[-1] += (default_timer() - start)/3

    plt.plot(sizes, shrink_avgs_array, color='blue', label='Array')
    plt.plot(sizes, shrink_avgs_CDLL, color='red', label='CDLL')
    plt.title("Enqueue, Grow, Dequeue, Shrink")
    plt.legend(loc='best')
    plt.show()

    # (3) Test with random operations

    random_avgs_array = []
    random_avgs_CDLL = []

    for size in sizes:
        random_avgs_array.append(0)
        random_avgs_CDLL.append(0)
        data = list(range(size))

        for trial in range(3):

            gc.collect()
            cd_array = CircularDeque()
            cd_DLL = CDLLCD()

            shuffle(data)

            start = default_timer()
            for item in data:
                if randint(0, 3) <= 2:
                    cd_array.enqueue(item, item % 2)
                else:
                    cd_array.dequeue(item % 2)
            random_avgs_array[-1] += (default_timer() - start)/3

            start = default_timer()
            for item in data:
                if randint(0, 3) <= 2:
                    cd_DLL.enqueue(item, item % 2)
                else:
                    cd_DLL.dequeue(item % 2)
            random_avgs_CDLL[-1] += (default_timer() - start)/3

    plt.plot(sizes, random_avgs_array, color='blue', label='Array')
    plt.plot(sizes, random_avgs_CDLL, color='red', label='CDLL')
    plt.title("Operations in Random Order")
    plt.legend(loc='best')
    plt.show()

    def max_len_subarray(data, bound, structure):
        """
        returns the length of the largest subarray of `data` with sum less or eq to than `bound`
        :param data: list of integers to operate on
        :param bound: largest allowable sum
        :param structure: either a CircularDeque or a CDLLCD
        :return: the length
        """
        index, max_len, subarray_sum = 0, 0, 0
        while index < len(data):

            while subarray_sum <= bound and index < len(data):
                structure.enqueue(data[index])
                subarray_sum += data[index]
                index += 1
            max_len = max(max_len, subarray_sum)

            while subarray_sum > bound:
                subarray_sum -= structure.dequeue(False)

        return max_len

    # (4) A common application

    application_avgs_array = []
    application_avgs_CDLL = []

    data = [randint(0, 1) for i in range(5000)]
    window_lengths = list(range(0, 200, 5))

    for length in window_lengths:
        application_avgs_array.append(0)
        application_avgs_CDLL.append(0)

        for trial in range(3):

            gc.collect()
            cd_array = CircularDeque()
            cd_DLL = CDLLCD()

            start = default_timer()
            max_len_subarray(data, length, cd_array)
            application_avgs_array[-1] += (default_timer() - start)/3

            start = default_timer()
            max_len_subarray(data, length, cd_DLL)
            application_avgs_CDLL[-1] += (default_timer() - start)/3

    plt.plot(window_lengths, application_avgs_array,
             color='blue', label='Array')
    plt.plot(window_lengths, application_avgs_CDLL, color='red', label='CDLL')
    plt.title("Sliding Window Application")
    plt.legend(loc='best')
    plt.show()
