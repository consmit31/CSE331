import unittest
from solution import SinglyLinkedList as SLL, help_mario, SLLNode
from random import seed, randint, shuffle
from typing import Tuple
import string


class MyTestCase(unittest.TestCase):

    def test_append(self):
        sll = SLL()  # SLL: Empty

        # 1. Insert into an empty list
        sll.append(15)  # SLL: 15
        self.assertEqual(15, sll.head.data)  # 1
        self.assertIs(None, sll.head.next)  # 1
        self.assertEqual(15, sll.tail.data)  # 1
        self.assertIs(sll.head, sll.tail)  # 1

        # 2. Insert into a one-element list
        sll.append(7)  # SLL: 15 --> 7
        self.assertEqual(15, sll.head.data)  # 2
        self.assertEqual(7, sll.head.next.data)  # 2
        self.assertIs(None, sll.head.next.next)  # 2
        self.assertEqual(7, sll.tail.data)  # 2
        self.assertIs(sll.head.next, sll.tail)  # 2

        # 3. Insert into an SLL with multiple nodes
        sll.append(8)  # SLL: 15 --> 7 --> 8
        self.assertEqual(15, sll.head.data)  # 3
        self.assertEqual(7, sll.head.next.data)  # 3
        self.assertEqual(8, sll.head.next.next.data)  # 3
        self.assertIs(None, sll.head.next.next.next)  # 3
        self.assertEqual(8, sll.tail.data)  # 3
        self.assertIs(sll.head.next.next, sll.tail)  # 3

        # 4. Type agnostic test
        sll = SLL()  # SLL: Empty

        sll.append('CSE331')  # SLL: CSE331
        self.assertEqual('CSE331', sll.head.data)  # 4
        self.assertIs(None, sll.head.next)  # 4
        self.assertEqual('CSE331', sll.tail.data)  # 4
        self.assertIs(sll.head, sll.tail)  # 4

        # 5. Type agnostic test 2
        sll.append(867)  # SLL: CSE331 --> 867
        self.assertEqual('CSE331', sll.head.data)  # 5
        self.assertEqual(867, sll.head.next.data)  # 5
        self.assertIs(None, sll.head.next.next)  # 5
        self.assertEqual(867, sll.tail.data)  # 5
        self.assertIs(sll.head.next, sll.tail)  # 5

        # 6. Type agnostic test 3
        sll.append(53.09)  # SLL: CSE331 --> 867 --> 53.09
        self.assertEqual('CSE331', sll.head.data)  # 6
        self.assertEqual(867, sll.head.next.data)  # 6
        self.assertEqual(53.09, sll.head.next.next.data)  # 6
        self.assertIs(None, sll.head.next.next.next)  # 6
        self.assertEqual(53.09, sll.tail.data)  # 6
        self.assertIs(sll.head.next.next, sll.tail)  # 6

    def test_to_string(self):
        sll = SLL()

        # 1. Get the string representation of an empty list
        self.assertEqual("None", sll.to_string())  # 1

        # 2. Get the string representation of a one-element list
        sll.head = SLLNode('C')
        sll.tail = sll.head
        self.assertEqual("C", sll.to_string())  # 2

        # 3. Get the string representation of a two-element list
        sll.append('S')
        self.assertEqual("C --> S", sll.to_string())  # 3

        # 4. Get the string representation of a multi-element list
        sll.append('E')
        self.assertEqual("C --> S --> E", sll.to_string())  # 4

        # 5. Get the string representation of another multi-element list
        sll.append('3')
        self.assertEqual("C --> S --> E --> 3", sll.to_string())  # 5

        # 6. Get the string representation of another multi-element list
        sll.append('3')
        self.assertEqual("C --> S --> E --> 3 --> 3", sll.to_string())  # 6

        # 7. Get the string representation of another multi-element list
        sll.append('1')
        self.assertEqual("C --> S --> E --> 3 --> 3 --> 1", sll.to_string())  # 7

    def test_length(self):
        sll = SLL()

        # 1. Get the length of an empty list
        self.assertEqual(0, sll.length())  # 1

        # 2. Get the length of a one-element list
        sll.append(2)
        self.assertEqual(1, sll.length())  # 2, SLL: 2

        # 3. Get the length of a two-element list
        sll.append(5)
        self.assertEqual(2, sll.length())  # 3, SLL: 2 --> 5

        # 4. Get the length of a multi-element list
        sll.append(3)
        self.assertEqual(3, sll.length())  # 4, SLL: 2 --> 5 --> 3

        # 5. Get the length of another multi-element list
        sll.append(0)
        self.assertEqual(4, sll.length())  # 5, SLL: 2 --> 5 --> 3 --> 0

    def test_total(self):
        sll = SLL()

        # 1. Get the sum total of an empty list
        self.assertIs(None, sll.total())  # 1

        # 2. Get the sum total of an SLL with one node
        sll.append(5)
        self.assertEqual(5, sll.total())  # 2

        # 3. Get the sum total of an SLL with two nodes
        sll.append(8)
        self.assertEqual(13, sll.total())  # 3, notice 5 + 8 = 13

        # 4. Get the sum total of a multi-element SLL
        sll.append(2)
        self.assertEqual(15, sll.total())  # 4

        # 5. Get the sum of another multi-element SLL
        sll.append(5)
        self.assertEqual(20, sll.total())  # 5

        # 6. Type agnostic test
        sll = SLL()
        sll.append('Hello')
        sll.append('World!')
        sll.append('ThereShouldBeNoSpaces')
        self.assertEqual('HelloWorld!ThereShouldBeNoSpaces', sll.total())  # 6

    def test_delete(self):
        sll = SLL()

        # 1. Delete from an empty list
        self.assertEqual(False, sll.delete(331))  # 1, SLL: Empty
        self.assertIs(None, sll.head)  # 1
        self.assertIs(None, sll.tail)  # 1

        sll.append(4)
        sll.append(2)
        sll.append(4)
        sll.append(1)  # SLL: 4 --> 2 --> 4 --> 1

        # 2. Try to delete an element that isn't in the SLL
        self.assertEqual(False, sll.delete(6))  # 2, SLL: 4 --> 2 --> 4 --> 1
        self.assertEqual(4, sll.head.data)  # 2
        self.assertEqual(2, sll.head.next.data)  # 2
        self.assertEqual(4, sll.head.next.next.data)  # 2
        self.assertEqual(1, sll.head.next.next.next.data)  # 2
        self.assertIs(None, sll.head.next.next.next.next)  # 2
        self.assertEqual(1, sll.tail.data)  # 2
        self.assertIs(sll.tail, sll.head.next.next.next)  # 2

        # 3. Delete from the middle of the list
        self.assertEqual(True, sll.delete(2))  # 3, SLL: 4 --> 4 --> 1
        self.assertEqual(4, sll.head.data)  # 3
        self.assertEqual(4, sll.head.next.data)  # 3
        self.assertEqual(1, sll.head.next.next.data)  # 3
        self.assertIs(None, sll.head.next.next.next)  # 3
        self.assertEqual(1, sll.tail.data)  # 3
        self.assertIs(sll.tail, sll.head.next.next)  # 3

        # 4. Delete from the end of the list
        self.assertEqual(True, sll.delete(1))  # 4, SLL: 4 --> 4
        self.assertEqual(4, sll.head.data)  # 4
        self.assertEqual(4, sll.head.next.data)  # 4
        self.assertIs(None, sll.head.next.next)  # 4
        self.assertEqual(4, sll.tail.data)  # 4
        self.assertIs(None, sll.tail.next)  # 4
        self.assertEqual(sll.tail, sll.head.next)  # 4

        # 5. Delete from the front of the list (ONLY the first occurrence)
        self.assertEqual(True, sll.delete(4))  # 5, SLL: 4
        self.assertEqual(4, sll.head.data)  # 5
        self.assertIs(None, sll.head.next)  # 5
        self.assertEqual(4, sll.tail.data)  # 5
        self.assertIs(sll.head, sll.tail)  # 5

        # 6. Delete the last node in the list
        self.assertEqual(True, sll.delete(4))  # 6, SLL: Empty
        self.assertIs(None, sll.head)  # 6
        self.assertIs(None, sll.tail)  # 6

    def test_delete_all(self):
        sll = SLL()

        # 1. Deleting from an empty list
        self.assertEqual(False, sll.delete_all(331))  # 1, SLL: Empty
        self.assertIs(None, sll.head)  # 1
        self.assertIs(None, sll.tail)  # 1

        sll.append(8)
        sll.append(5)
        sll.append(3)
        sll.append(5)
        sll.append(9)
        sll.append(3)
        sll.append(7)
        sll.append(0)
        # SLL: 8 --> 5 --> 3 --> 5 --> 9 --> 3 --> 7 --> 0

        # 2. Delete all the 5's
        self.assertEqual(True, sll.delete_all(5))  # 2, SLL: 8 --> 3 --> 9 --> 3 --> 7 --> 0
        self.assertEqual(8, sll.head.data)  # 2
        self.assertEqual(3, sll.head.next.data)  # 2
        self.assertEqual(9, sll.head.next.next.data)  # 2
        self.assertEqual(3, sll.head.next.next.next.data)  # 2
        self.assertEqual(7, sll.head.next.next.next.next.data)  # 2
        self.assertEqual(0, sll.head.next.next.next.next.next.data)  # 2
        self.assertIs(None, sll.head.next.next.next.next.next.next)  # 2
        self.assertEqual(0, sll.tail.data)  # 2
        self.assertIs(sll.tail, sll.head.next.next.next.next.next)  # 2

        # 3. Delete from the front of the list
        self.assertEqual(True, sll.delete_all(8))  # 3, SLL: 3 --> 9 --> 3 --> 7 --> 0
        self.assertEqual(3, sll.head.data)  # 3
        self.assertEqual(9, sll.head.next.data)  # 3
        self.assertEqual(3, sll.head.next.next.data)  # 3
        self.assertEqual(7, sll.head.next.next.next.data)  # 3
        self.assertEqual(0, sll.head.next.next.next.next.data)  # 3
        self.assertIs(None, sll.head.next.next.next.next.next)  # 3
        self.assertEqual(0, sll.tail.data)  # 3
        self.assertIs(sll.tail, sll.head.next.next.next.next)  # 3

        # 4. Delete from the end of the list
        self.assertEqual(True, sll.delete_all(0))  # 4, SLL: 3 --> 9 --> 3 --> 7
        self.assertEqual(3, sll.head.data)  # 4
        self.assertEqual(9, sll.head.next.data)  # 4
        self.assertEqual(3, sll.head.next.next.data)  # 4
        self.assertEqual(7, sll.head.next.next.next.data)  # 4
        self.assertIs(None, sll.head.next.next.next.next)  # 4
        self.assertEqual(7, sll.tail.data)  # 4
        self.assertIs(None, sll.tail.next)  # 4
        self.assertIs(sll.tail, sll.head.next.next.next)  # 4

        # 5. Try to delete an element that isn't in the list
        self.assertEqual(False, sll.delete_all(5))  # 5, SLL: 3 --> 9 --> 3 --> 7
        self.assertEqual(3, sll.head.data)  # 5
        self.assertEqual(9, sll.head.next.data)  # 5
        self.assertEqual(3, sll.head.next.next.data)  # 5
        self.assertEqual(7, sll.head.next.next.next.data)  # 5
        self.assertIs(None, sll.head.next.next.next.next)  # 5
        self.assertEqual(7, sll.tail.data)  # 5
        self.assertIs(None, sll.tail.next)  # 5
        self.assertIs(sll.tail, sll.head.next.next.next)  # 5

        # 6. Delete from the middle of the list
        self.assertEqual(True, sll.delete_all(9))  # 6, SLL: 3 --> 3 --> 7
        self.assertEqual(3, sll.head.data)  # 6
        self.assertEqual(3, sll.head.next.data)  # 6
        self.assertEqual(7, sll.head.next.next.data)  # 6
        self.assertIs(None, sll.head.next.next.next)  # 6
        self.assertEqual(7, sll.tail.data)  # 6
        self.assertIs(sll.tail, sll.head.next.next)  # 6

        # 7. Delete all the 3's from the list
        self.assertEqual(True, sll.delete_all(3))  # 7, SLL: 7
        self.assertEqual(7, sll.head.data)  # 7
        self.assertEqual(7, sll.tail.data)  # 7
        self.assertIs(None, sll.head.next)  # 7
        self.assertIs(sll.head, sll.tail)  # 7

        # 8. Delete the last element from the list
        self.assertEqual(True, sll.delete_all(7))  # 8, SLL: Empty
        self.assertIs(None, sll.head)  # 8
        self.assertIs(None, sll.tail)  # 8

    def test_find(self):
        sll = SLL()

        # 1. Try to find an element in an empty list
        self.assertEqual(False, sll.find(331))  # 1

        sll.append(4)
        sll.append(2)
        sll.append(0)  # SLL: 4 --> 2 --> 0

        # 2. Look for a node at the start of the list
        self.assertEqual(True, sll.find(4))  # 2

        # 3. Look for a node that isn't in the list
        self.assertEqual(False, sll.find(3))  # 3

        # 4. Look for a node in the middle of the list
        self.assertEqual(True, sll.find(2))  # 4

        # 5. Look for a node at the end of the list
        self.assertEqual(True, sll.find(0))  # 5

        # 6. Type agnostic test
        sll = SLL()
        sll.append('Hello')
        sll.append('World!')
        sll.append('WhatsUp?')
        self.assertEqual(True, sll.find('World!'))  # 6

    def test_find_sum(self):
        sll = SLL()

        # 1. Try to sum up occurrences in an empty list
        self.assertEqual(0, sll.find_sum(7))  # 1

        # 2. Get the number of 5's in a one-element list
        sll.append(5)
        self.assertEqual(1, sll.find_sum(5))  # 2

        # 3. Get the number of 5's in the two-element list
        sll.append(7)  # SLL: 5 --> 7
        self.assertEqual(1, sll.find_sum(5))  # 3

        # 4. Get the number of 7's in the multi-element list
        sll.append(4)
        sll.append(7)  # SLL: 5 --> 7 --> 4 --> 7
        self.assertEqual(2, sll.find_sum(7))  # 4

        # 5. Get the number of 0's in a list without any 0's
        self.assertEqual(0, sll.find_sum(0))  # 5

        # 6. Type agnostic test
        sll = SLL()
        sll.append('Hello')
        sll.append('World!')
        sll.append('Hello')
        self.assertEqual(2, sll.find_sum('Hello'))  # 6

    def test_help_mario(self):
        roster = SLL()

        # 1. Try to help when there are no racers
        ans = help_mario(roster, 'Princess Peach')
        self.assertIs(False, ans)  # 1

        # 2. Try to help when the ally is not in the roster
        roster.append('Luigi')
        roster.append('King Boo')
        roster.append('Toad')
        roster.append('Morton Koopa Jr.')
        ans = help_mario(roster, 'Yoshi')
        self.assertIs(False, ans)  # 2
        self.assertEqual('Luigi', roster.head.data)  # 2
        self.assertEqual('Morton Koopa Jr.', roster.head.next.next.next.data)  # 2
        self.assertIs(roster.tail, roster.head.next.next.next)  # 2

        # 3. Try to help when the ally is already first in the roster
        ans = help_mario(roster, 'Luigi')
        self.assertIs(False, ans)  # 3
        self.assertEqual('Luigi', roster.head.data)  # 3
        self.assertEqual('Morton Koopa Jr.', roster.head.next.next.next.data)  # 3
        self.assertIs(roster.tail, roster.head.next.next.next)  # 3

        # 4. Try to help when the ally is in the middle of the roster
        ans = help_mario(roster, 'Toad')
        self.assertIs(True, ans)  # 4
        self.assertEqual('Toad', roster.head.data)  # 4
        self.assertEqual('Morton Koopa Jr.', roster.head.next.data)  # 4
        self.assertEqual('Luigi', roster.head.next.next.data)  # 4
        self.assertEqual('King Boo', roster.head.next.next.next.data)  # 4
        self.assertIs(None, roster.head.next.next.next.next)  # 4
        self.assertIs(roster.tail, roster.head.next.next.next)  # 4

        # 5. Try to help when the ally is at the tail of the roster
        roster = SLL()
        roster.append('Yoshi')
        roster.append('Shy Guy')
        roster.append('Ludwig von Koopa')
        roster.append('Lakitu')
        roster.append('Toadette')
        ans = help_mario(roster, 'Toadette')
        self.assertIs(True, ans)  # 5
        self.assertEqual('Toadette', roster.head.data)  # 5
        self.assertEqual('Yoshi', roster.head.next.data)  # 5
        self.assertEqual('Shy Guy', roster.head.next.next.data)  # 5
        self.assertEqual('Ludwig von Koopa', roster.head.next.next.next.data)  # 5
        self.assertEqual('Lakitu', roster.head.next.next.next.next.data)  # 5
        self.assertIs(None, roster.head.next.next.next.next.next)  # 5
        self.assertIs(roster.tail, roster.head.next.next.next.next)  # 5

        # 6. Try to help with another ally from the changed roster in (5)
        # *** requires 5 to have passed! ***
        ans = help_mario(roster, 'Yoshi')
        self.assertIs(True, ans)  # 6
        self.assertEqual('Yoshi', roster.head.data)  # 6
        self.assertEqual('Shy Guy', roster.head.next.data)  # 6
        self.assertEqual('Ludwig von Koopa', roster.head.next.next.data)  # 6
        self.assertEqual('Lakitu', roster.head.next.next.next.data)  # 6
        self.assertEqual('Toadette', roster.head.next.next.next.next.data)  # 6
        self.assertIs(None, roster.head.next.next.next.next.next)  # 6
        self.assertIs(roster.tail, roster.head.next.next.next.next)  # 6

        # 7. Larger case, ally in middle
        roster = SLL()
        roster.append('Bowser')
        roster.append('Koopa Troopa')
        roster.append('Iggy Koopa')
        roster.append('Larry Koopa')
        roster.append('Mario')
        roster.append('Wendy O. Koopa')
        roster.append('Roy Koopa')
        roster.append('Princess Peach')
        roster.append('Lemmy Koopa')
        roster.append('Princess Daisy')
        ans = help_mario(roster, 'Mario')
        self.assertIs(True, ans)  # 7
        self.assertEqual('Mario', roster.head.data)  # 7
        self.assertEqual('Wendy O. Koopa', roster.head.next.data)  # 7
        self.assertEqual('Roy Koopa', roster.head.next.next.data)  # 7
        self.assertEqual('Princess Peach', roster.head.next.next.next.data)  # 7
        self.assertEqual('Lemmy Koopa', roster.head.next.next.next.next.data)  # 7
        self.assertEqual('Princess Daisy', roster.head.next.next.next.next.next.data)  # 7
        self.assertEqual('Bowser', roster.head.next.next.next.next.next.next.data)  # 7
        self.assertEqual('Koopa Troopa', roster.head.next.next.next.next.next.next.next.data)  # 7
        self.assertEqual('Iggy Koopa', roster.head.next.next.next.next.next.next.next.next.data)  # 7
        self.assertEqual('Larry Koopa', roster.head.next.next.next.next.next.next.next.next.next.data)  # 7
        self.assertIs(roster.tail, roster.head.next.next.next.next.next.next.next.next.next)  # 7
        self.assertIs(None, roster.head.next.next.next.next.next.next.next.next.next.next)  # 7

        # 8. Help another ally in the middle from (7)
        # *** requires 7 to have passed! ***
        ans = help_mario(roster, 'Princess Daisy')
        self.assertIs(True, ans)  # 8
        self.assertEqual('Princess Daisy', roster.head.data)  # 8
        self.assertEqual('Bowser', roster.head.next.data)  # 8
        self.assertEqual('Koopa Troopa', roster.head.next.next.data)  # 8
        self.assertEqual('Iggy Koopa', roster.head.next.next.next.data)  # 8
        self.assertEqual('Larry Koopa', roster.head.next.next.next.next.data)  # 8
        self.assertEqual('Mario', roster.head.next.next.next.next.next.data)  # 8
        self.assertEqual('Wendy O. Koopa', roster.head.next.next.next.next.next.next.data)  # 8
        self.assertEqual('Roy Koopa', roster.head.next.next.next.next.next.next.next.data)  # 8
        self.assertEqual('Princess Peach', roster.head.next.next.next.next.next.next.next.next.data)  # 8
        self.assertEqual('Lemmy Koopa', roster.head.next.next.next.next.next.next.next.next.next.data)  # 8
        self.assertIs(roster.tail, roster.head.next.next.next.next.next.next.next.next.next)  # 8
        self.assertIs(None, roster.head.next.next.next.next.next.next.next.next.next.next)  # 8

    def test_help_mario_comprehensive(self):
        seed(33131)

        def run_comprehensive(num_tests: int):
            """
            Comprehensive test helper function
            """

            def generate_roster(ally_pos: int = None) -> Tuple[SLL, str]:
                """
                Data generation helper function
                """
                # Generate random strings
                char_list = []
                for char in string.ascii_lowercase:
                    char_list.append(char)
                shuffle(char_list)
                # choose random ally
                if ally_pos is None:
                    ally_pos = randint(1, 24)
                ally = char_list[ally_pos]
                # create roster
                roster = SLL()
                for char in char_list:
                    roster.append(char)
                return roster, ally

            # test ally at head
            for _ in range(num_tests):
                roster, ally = generate_roster(ally_pos=0)
                ans = help_mario(roster, ally)
                self.assertEqual(ans, False)
                self.assertEqual(roster.head.data, ally)

            # test ally at tail
            for _ in range(num_tests):
                roster, ally = generate_roster(ally_pos=-1)
                ans = help_mario(roster, ally)
                self.assertEqual(ans, True)
                self.assertEqual(roster.head.data, ally)

            # test ally in middle
            for _ in range(num_tests):
                roster, ally = generate_roster()
                ans = help_mario(roster, ally)
                self.assertEqual(ans, True)
                self.assertEqual(roster.head.data, ally)

        for k in range(5):
            try:
                run_comprehensive(num_tests=100)
            except AssertionError as e:
                print(f'Failed on application comprehensive test {k + 1}/5. Error output is shown '
                      f'below.')
                raise e


if __name__ == '__main__':
    unittest.main()