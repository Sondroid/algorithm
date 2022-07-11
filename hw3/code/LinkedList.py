from ListNode import ListNode

class LinkedList:
    def __init__(self):
        self.head = None

    def add(self, number):
        if self.head is None:
            self.head = ListNode(number, None)
        else:
            self.head = ListNode(number, self.head)