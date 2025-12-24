#Resident class
class Resident:
    def __init__(self, name, student_id, contact):
        self.name = name
        self.student_id = student_id
        self.contact = contact

    def __str__(self):
        return f"{self.name} ({self.student_id}) - {self.contact}"

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
