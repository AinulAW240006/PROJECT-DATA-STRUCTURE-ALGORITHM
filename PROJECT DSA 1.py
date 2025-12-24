#Resident class
class Resident:
    def __init__(self, name, student_id, contact):
        self.name = name
        self.student_id = student_id
        self.contact = contact

    def __str__(self):
        return f"{self.name} ({self.student_id}) - {self.contact}"

    
# Node for Singly Linked-List
class Node:
    def __init__(self, resident):
        self.resident = resident
        self.next = None

# Singly Linked List for current residents
class ResidentLinkedList:
    def __init__(self):
        self.head = None
#adding residents
    def add_resident(self, resident):
        new_node = Node(resident)
        new_node.next = self.head
        self.head = new_node
#removing residents
    def remove_resident(self, student_id):
        current = self.head
        previous = None

    

    # Queue for waiting list
    class WaitingQueue:
        def __init__(self):
            self.queue = []

        def enqueue(self, resident):
            self.queue.append(resident)

        def dequeue(self):
            if self.queue:
                return self.queue.pop(0)
            return None

        def is_empty(self):
            return len(self.queue) == 0

