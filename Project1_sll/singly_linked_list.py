from typing import TypeVar  # For use in type hinting

# Type declarations
T = TypeVar('T')        # generic type
SLL = TypeVar('SLL')    # forward declared Singly Linked List type
Node = TypeVar('Node')  # forward declared Node type


class SLLNode:
    """
    Node implementation
    Do not modify
    """

    __slots__ = ['data', 'next']

    def __init__(self, data: T, next: Node = None) -> None:
        """
        Initialize an SLL Node
        :param data: data value held by the node
        :param next: reference to the next node in the SLL
        :return: None
        """
        self.data = data
        self.next = next

    def __str__(self) -> str:
        """
        Overloads `str()` method, casts SLL nodes to strings
        :return: string representation of node
        """
        return '(Node: ' + str(self.data) + ' )'

    def __repr__(self) -> str:
        """
        Overloads `repr()` method for use in debugging
        :return: string representation of node
        """
        return '(Node: ' + str(self.data) + ' )'

    def __eq__(self, other: Node) -> bool:
        """
        Overloads `==` operator to compare nodes
        :param other: right operand of `==`
        :return: True if the nodes are ==, else False
        """
        return self is other if other is not None else False


class SinglyLinkedList:
    """
    SLL implementation
    """

    __slot__ = ['head', 'tail']

    def __init__(self) -> None:
        """
        Initializes an SLL
        return: None
        DO NOT MODIFY THIS FUNCTION
        """
        self.head = None
        self.tail = None

    def __repr__(self) -> str:
        """
        Represents an SLL as a string
        DO NOT MODIFY THIS FUNCTION
        :return: string representation of SLL
        """
        return self.to_string()

    def __eq__(self, other: SLL) -> bool:
        """
        Overloads `==` operator to compare SLLs
        :param other: right operand of `==`
        :return: True if equal, else False
        DO NOT MODIFY THIS FUNCTION
        """
        comp = lambda n1, n2: n1 == n2 and (comp(n1.next, n2.next) if (n1 and n2) else True)
        return comp(self.head, other.head)

    # ========== Modify below ========== #

    def append(self, data: T) -> None:
        """
        Append an SLLNode to the end of the SLL
        :param data: data to append
        :return: None
        """
        newNode = SLLNode(data)
        if self.head is None:
            self.head = newNode
            self.tail = newNode
        else:
            self.tail.next = newNode
            self.tail = newNode

    def to_string(self) -> str:
        """
        Converts an SLL to a string
        :return: string representation of SLL
        """
        if self.head is None:
            return "None"
        else:
            curNode = self.head
            out_str = ""

        while curNode is not None:
            out_str += str(curNode.data)
            if curNode.next is not None:
                out_str += " --> "
            curNode = curNode.next
        return out_str


    def length(self) -> int:
        """
        Determines number of nodes in the list
        :return: number of nodes in list
        """
        if self.head is None:
            return 0
        else:
            curNode = self.head
            count = 0

        while curNode is not None:
            count += 1
            curNode = curNode.next
        return count

    def total(self) -> T:
        """
        Sums up the values in the list
        :return: total sum of values in the list
        """
        if self.head is None:
            return None
        else:
            curNode = self.head
            sum = type(curNode.data)()

        while curNode is not None:
            sum += curNode.data
            curNode = curNode.next
        return sum

    def delete(self, data: T) -> bool:
        """
        Deletes the first node containing `data` from the SLL
        :param data: data to remove
        :return: True if a node was removed, else False
        """
        if self.head is None:
            return False
        else:
            curNode = self.head
            prevNode = None
            sucNode = curNode.next

        while curNode is not None:
            if curNode.data is data:
                if prevNode is None:
                    self.head = sucNode
                    if sucNode is None:
                        self.tail = None
                    return True
                if sucNode is None:
                    self.tail = prevNode
                    self.tail.next = None
                    return True
                prevNode.next = sucNode
                return True
            prevNode = curNode
            curNode = sucNode
            if sucNode is None:
                return False
            sucNode = sucNode.next
        return False


    def delete_all(self, data: T) -> bool:
        """
        Deletes all instances of a node containing `data` from the SLL
        :param data: data to remove
        :return: True if a node was removed, else False
        """
        delete = False
        if self.head is None:
            return delete

        while self.head.data is data:
            self.head = self.head.next
            delete = True
            if self.head is None:
                self.tail = None
                return delete

        curNode = self.head
        prevNode = None
        sucNode = curNode.next

        while curNode is not None:
            if curNode.data is data:
                if sucNode is None:
                    self.tail = prevNode
                    self.tail.next = None
                    delete = True
                prevNode.next = sucNode
                delete = True
            prevNode = curNode
            curNode = sucNode
            if sucNode is None:
                return delete
            sucNode = sucNode.next
        return delete


    def find(self, data: T) -> bool:
        """
        Looks through the SLL for a node containing `data`
        :param data: data to search for
        :return: True if found, else False
        """
        if self.head is None:
            return False

        curNode = self.head

        while curNode is not None:
            if curNode.data is data:
                return True
            curNode = curNode.next
        return False

    def find_sum(self, data: T) -> int:
        """
        Returns the number of occurrences of `data` in this list
        :param data: data to find and sum up
        :return: number of times the data occurred
        """
        sum = 0

        if self.head is None:
            return False

        curNode = self.head
        while curNode is not None:
            if curNode.data is data:
                sum += 1
            curNode = curNode.next
        return sum


def help_mario(roster: SLL, ally: str) -> bool:
    """
    Updates the roster of racers to put Mario's ally at the front
    Preserves relative order of racers around ally
    :param roster: initial order of racers
    :param ally: the racer that needs to go first
    :return: True if the roster was changed, else False
    """
    if roster.head is None or not roster.find(ally) or roster.head.data is ally:
        return False

    curRacer = roster.head
    while curRacer is not None:
        curRacer = roster.head
        if curRacer.data is ally:
            return True
        else:
            roster.head = curRacer.next
            roster.append(curRacer.data)