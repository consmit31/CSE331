"""
Project 2
CSE 331 F23 (Onsay)
Authored By: Hank Murdock
Originally Authored By: Andrew McDonald & Alex Woodring & Andrew Haas & Matt Kight & Lukas Richters & Sai Ramesh
solution.py
"""

from typing import TypeVar, List

# for more information on type hinting, check out https://docs.python.org/3/library/typing.html
T = TypeVar("T")  # represents generic type
Node = TypeVar("Node")  # represents a Node object (forward-declare to use in Node __init__)


# pro tip: PyCharm auto-renders docstrings (the multiline strings under each function definition)
# in its "Documentation" view when written in the format we use here. Open the "Documentation"
# view to quickly see what a function does by placing your cursor on it and using CTRL + Q.
# https://www.jetbrains.com/help/pycharm/documentation-tool-window.html


class Node:
    """
    Implementation of a doubly linked list node.
    Do not modify.
    """
    __slots__ = ["value", "next", "prev", "child"]

    def __init__(self, value: T, next: Node = None, prev: Node = None, child: Node = None) -> None:
        """
        Construct a doubly linked list node.

        :param value: value held by the Node.
        :param next: reference to the next Node in the linked list.
        :param prev: reference to the previous Node in the linked list.
        :return: None.
        """
        self.next = next
        self.prev = prev
        self.value = value

        # The child attribute is only used for the application problem
        self.child = child

    def __repr__(self) -> str:
        """
        Represents the Node as a string.

        :return: string representation of the Node.
        """
        return f"Node({str(self.value)})"

    __str__ = __repr__


class DLL:
    """
    Implementation of a doubly linked list without padding nodes.
    Modify only below indicated line.
    """
    __slots__ = ["head", "tail", "size"]

    def __init__(self) -> None:
        """
        Construct an empty doubly linked list.

        :return: None.
        """
        self.head = self.tail = None
        self.size = 0

    def __repr__(self) -> str:
        """
        Represent the DLL as a string.

        :return: string representation of the DLL.
        """
        result = []
        node = self.head
        while node is not None:
            result.append(str(node))
            node = node.next
        return " <-> ".join(result)

    def __str__(self) -> str:
        """
        Represent the DLL as a string.

        :return: string representation of the DLL.
        """
        return repr(self)

    # MODIFY BELOW #

    def empty(self) -> bool:
        """
        Returns a boolean indicating whether the DLL is empty.

        :return: True if DLL is empty, else False.
        """
        if self.head is None and self.tail is None:
            return True
        return False

    def push(self, val: T, back: bool = True) -> None:
        """
        Adds a Node containing val to the back (or front) of the DLL and updates size accordingly.

        :param val: Value to be added to the DLL.
        :param back: If True, add val to the back of the DLL. If False, add to the front.
        :return: None.
        """
        self.size += 1

        if self.empty():
            self.head = self.tail = Node(val)
            return None

        if back:
            self.tail.next = Node(val, None, self.tail, None)
            self.tail = self.tail.next
        else:
            self.head.prev = Node(val, self.head, None, None)
            self.head = self.head.prev

    def pop(self, back: bool = True) -> None:
        """
        Removes a Node from the back (or front) of the DLL and updates size accordingly

        :param back: If True, remove from the back of the DLL. If False, remove from the front.
        :returns: None.
        """
        if self.empty():
            return None
        if self.size == 1:
            self.head = self.tail = None
            self.size = 0
        elif back:
            self.tail = self.tail.prev
            self.tail.next = None
            self.size -= 1
        else:
            self.head = self.head.next
            self.head.prev = None
            self.size -= 1

    def list_to_dll(self, source: List[T]) -> None:
        """
        Creates a DLL from a standard Python list. If there are already nodes in the DLL, the DLL should be cleared and
        replaced by source.

        :param source: Standard Python list from which to construct DLL.
        :return: None.
        """
        if not self.empty():
            self.head = self.tail = None
            self.size = 0

        for i in source:
            self.push(i)

    def dll_to_list(self) -> List[T]:
        """
        Creates a standard Python list from a DLL.

        :return: list[T] containing the values of the nodes in the DLL.
        """
        dll_list = []
        if self.empty():
            return dll_list

        curNode = self.head
        while curNode is not None:
            dll_list.append(curNode.value)
            curNode = curNode.next

        return dll_list

    def _find_nodes(self, val: T, find_first: bool = False) -> List[Node]:
        """
        Construct list of Node with value val in the DLL and returns the associated Node object list

        :param val: Value to be found in the DLL.
        :param find_first: if True find only the first element in the DLL, it false find all instances of the elements
        in the DLL.
        :return: list of Node objects in the DLL whose value is val. If val does not exist in the DLL, returns empty
        list.
        """
        node_list = []
        if self.empty():
            return node_list

        curNode = self.head
        while curNode is not None:
            if curNode.value == val:
                node_list.append(curNode)
                if find_first:
                    return node_list
            curNode = curNode.next

        return node_list

    def find(self, val: T) -> Node:
        """
        Finds first Node with value val in the DLL and returns the associated Node object.

        :param val: Value to be found in the DLL.
        :return: first Node object in the DLL whose value is val. If val does not exist in the DLL, return None.
        """
        node_list = self._find_nodes(val, True)
        if node_list:
            return node_list[0]
        else:
            return None

    def find_all(self, val: T) -> List[Node]:
        """
        Finds all Node objects with value val in the DLL and returns a standard Python list of the associated Node
        objects.

        :param val: Value to be found in the DLL.
        :return: standard Python list of all Node objects in the DLL whose value is val. If val does not exist in the
        DLL, returns an empty list.
        """
        return self._find_nodes(val)

    def _remove_node(self, to_remove: Node) -> None:
        """
        Given a reference to a node in the linked list, remove it

        :param to_remove: Node to be removed from the DLL.
        :return: None.
        """
        prevNode = to_remove.prev
        sucNode = to_remove.next
        self.size -= 1

        if prevNode and sucNode:
            prevNode.next = sucNode
            sucNode.prev = prevNode
        elif not prevNode and not sucNode:
            self.head = self.tail = None
        elif prevNode is None:
            self.head = sucNode
            self.head.prev = None
        elif sucNode is None:
            self.tail = prevNode
            self.tail.next = None

    def remove(self, val: T) -> bool:
        """
        removes first Node with value val in the DLL.

        :param val: Value to be removed from the DLL.
        :return: True if a Node with value val was found and removed from the DLL, else False.
        """
        del_node = self.find(val)
        if del_node:
            self._remove_node(del_node)
            return True
        else:
            return False

    def remove_all(self, val: T) -> int:
        """
        removes all Node objects with value val in the DLL. See note 7.

        :param val: T: Value to be removed from the DLL.
        :return: number of Node objects with value val removed from the DLL. If no node containing val exists in the
        DLL, returns 0.
        """
        del_list = self.find_all(val)
        for node in del_list:
            self._remove_node(node)

        return len(del_list)

    def reverse(self) -> None:
        """
        Reverses the DLL in-place by modifying all next and prev references of Node objects in DLL.
        Updates self.head and self.tail accordingly.

        :return: None.
        """
        if self.empty():
            return None

        curNode = self.head
        while curNode:
            temp = curNode.prev
            curNode.prev = curNode.next
            curNode.next = temp
            curNode = curNode.prev

        self.head, self.tail = self.tail, self.head


class BrowserHistory:

    def __init__(self, homepage: str):
        """
        Construct an empty browser history

        :param homepage: The first page visited
        """
        self.homepage = homepage
        self.sites = DLL()
        self.sites.push(homepage)
        self.current_site = self.sites.head

    def get_current_url(self) -> str:
        """
        Returns the URL the browser is currently on

        :return: The URL the browser is currently set to.
        """
        return self.current_site.value

    def visit(self, url: str) -> None:
        """
        Visit the URL supplied to the method.

        :param url: URL address to be visited.
        :return: None.
        """
        self.sites.tail = self.current_site
        self.sites.tail.next = None
        self.sites.push(url, True)
        self.current_site = self.current_site.next

    def backward(self) -> None:
        """
        Return to the last page in history, if there is no previous page don't go back.

        :return: None.
        """
        prevSite = self.current_site.prev

        if not prevSite:
            return None
        while prevSite is not self.sites.head:
            if prevSite.value in intervention_set:
                prevSite = prevSite.prev
            else:
                self.current_site = prevSite
                return None

        self.current_site = prevSite


    def forward(self) -> None:
        """
        Visit the page ahead of the current one in history, if currently on the most recent page then stay at the same
        page.

        :return: None.
        """
        nextSite = self.current_site.next

        if not nextSite:
            return None

        while nextSite is not self.sites.tail:
            if nextSite.value in intervention_set:
                nextSite = nextSite.next
            else:
                self.current_site = nextSite
                return None

        if nextSite.value not in intervention_set:
            self.current_site = nextSite




# DO NOT MODIFY
intervention_set = set(['https://malicious.com', 'https://phishing.com', 'https://malware.com'])
def metrics_api(url: str) -> bool:
    """
    Uses the intervention_set to determine what URLs are bad and which are good. 

    :param url: The url to check.
    :returns: True if this is a malicious website, False otherwise.
    """
    if url in intervention_set:
        return True
    return False
