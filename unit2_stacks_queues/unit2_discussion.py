"""
===========================================================
UNIT 2 DISCUSSION: STACKS AND QUEUES (PYTHON)
===========================================================
OVERVIEW:
This assignment introduces two fundamental data structures:
the Stack (LIFO) and the Queue (FIFO).
You will complete, modify, and extend the starter code while
explaining key concepts through comments and improved output.

SCENARIO USED IN THIS SUBMISSION:
An IT Service Desk console. The stack holds a configuration
change log that must be rolled back newest-first, and the
queue holds support tickets that must be served oldest-first.
"""

from collections import deque


class Stack:
    def __init__(self):
        # TODO (Student): Create the internal data structure for the stack.
        # Hint: A Python list can be used to store stack values.
        # A list is a good fit because append() and pop() both act on the END
        # of the list in O(1) time, and the end of the list is the "top" of
        # the stack. Index -1 is always the top; index 0 is the bottom.
        self._items = []

    def push(self, value):
        # TODO (Student): Add value to the stack.
        # Add a short comment explaining why this operation supports LIFO behavior.
        # LIFO: every new value is appended to the TOP of the stack, burying the
        # previous top. Because insertion and removal both happen at that same
        # single open end, the most recently pushed value is always the first
        # one available to leave.
        self._items.append(value)
        return value

    def pop(self):
        # TODO (Student): Remove and return the most recently added value.
        # Improve or explain empty-stack handling.
        # What should happen if the stack is empty?
        # Calling pop() on an empty list raises IndexError, which is a stack
        # underflow. Rather than crashing the program, this method checks first
        # and returns None so the caller can decide what to do. The demo below
        # prints a clear message when None comes back.
        if self.is_empty():
            return None
        return self._items.pop()  # removes from the top (last index)

    def peek(self):
        # TODO (Student): Return the top value without removing it.
        # Add a comment explaining what peek does.
        # peek() is a read-only look at the top value. It answers "what would
        # pop() give me?" without changing the stack, so the size is unchanged
        # after the call. It returns None on an empty stack for the same reason
        # pop() does.
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self):
        # TODO (Student): Return True if the stack has no values.
        return len(self._items) == 0

    def size(self):
        # Helper: number of values currently stored (used by the demos).
        return len(self._items)

    def display(self):
        # Helper: show contents bottom -> top so LIFO ordering is visible.
        if self.is_empty():
            return "[ empty ]"
        return f"{self._items}  <-- top"


class Queue:
    def __init__(self):
        # TODO (Student): Create the internal data structure for the queue.
        # Hint: collections.deque is useful for efficient queue operations.
        # A deque is a double-ended queue. Unlike a list, removing from the
        # front with popleft() is O(1) instead of O(n), because no elements
        # have to shift left to fill the gap. Index 0 is the front, index -1
        # is the rear.
        self._items = deque()

    def enqueue(self, value):
        # TODO (Student): Add value to the back of the queue.
        # Add a short comment explaining why this operation supports FIFO behavior.
        # FIFO: values enter at the REAR and leave from the FRONT. Because the
        # two ends are separate, a new arrival can never jump ahead of someone
        # already waiting, so the value that has waited longest is always the
        # next one served.
        self._items.append(value)
        return value

    def dequeue(self):
        # TODO (Student): Remove and return the value from the front of the queue.
        # Explain or improve empty-queue handling.
        # An empty queue simply means there is no work to do right now, which is
        # a normal state for a service loop rather than an error. popleft() on an
        # empty deque raises IndexError, so this method guards against that and
        # returns None instead, leaving the queue untouched.
        if self.is_empty():
            return None
        return self._items.popleft()  # removes from the front

    def front(self):
        # TODO (Student): Return the front value without removing it.
        # Add a comment explaining what front returns.
        # front() returns the value that has been waiting longest, i.e. the one
        # dequeue() would remove next. It is read-only, so the queue length does
        # not change, and it returns None when nothing is waiting.
        if self.is_empty():
            return None
        return self._items[0]

    def is_empty(self):
        # TODO (Student): Return True if the queue has no values.
        return len(self._items) == 0

    def size(self):
        # Helper: number of values currently waiting (used by the demos).
        return len(self._items)

    def display(self):
        # Helper: show contents front -> rear so FIFO ordering is visible.
        if self.is_empty():
            return "[ empty ]"
        return f"front --> {list(self._items)} <-- rear"


def custom_scenario():
    """
    TODO (Student): Real-world scenario.

    IT SERVICE DESK - one shift, two structures, opposite ordering rules.

    Stack  -> configuration change log. Each change an engineer applies is
              pushed on top of earlier changes. When something breaks, the
              rollback must undo the NEWEST change first, because later
              changes were built on top of earlier ones. Undoing out of
              order would leave the system in a state that never existed.

    Queue  -> support tickets. Users are served in the order they reported
              their issue, so nobody is starved by a newer arrival.
    """
    print("\n=== CUSTOM SCENARIO: IT SERVICE DESK ===")

    change_log = Stack()
    tickets = Queue()

    print("\nEngineer applies four configuration changes during the shift:")
    for change in ["Open firewall port 443",
                   "Update DNS record for portal",
                   "Increase DB pool to 200",
                   "Deploy release v2.4.1"]:
        change_log.push(change)
        print(f"  PUSH    -> logged '{change}'")
    print(f"  Change log: {change_log.display()}")

    print("\nMeanwhile five tickets arrive from users:")
    for ticket in ["T-101 Password reset",
                   "T-102 Printer offline",
                   "T-103 VPN drops",
                   "T-104 Portal returns 502",
                   "T-105 Mailbox full"]:
        tickets.enqueue(ticket)
        print(f"  ENQUEUE -> '{ticket}' joined the line")
    print(f"  Ticket queue: {tickets.display()}")

    print("\nThe portal breaks, so the rollback runs on the change log (LIFO):")
    print(f"  PEEK    -> newest change is '{change_log.peek()}'")
    print(f"  POP     -> reversed '{change_log.pop()}'")
    print(f"  POP     -> reversed '{change_log.pop()}'")
    print(f"  Change log: {change_log.display()}")
    print("  Only the two newest changes were undone. The older, working changes")
    print("  stayed in place - reverse order is exactly what makes rollback safe.")

    print("\nTickets are worked in arrival order (FIFO):")
    print(f"  FRONT   -> longest waiting is '{tickets.front()}'")
    print(f"  DEQUEUE -> served '{tickets.dequeue()}'")
    print(f"  DEQUEUE -> served '{tickets.dequeue()}'")
    print(f"  Ticket queue: {tickets.display()}")
    print(f"  {tickets.size()} tickets still waiting. T-105 arrived last, so it is served last.")


def main():
    print("=== UNIT 2: STACKS AND QUEUES ===")

    # ===============================
    # TODO (Student): STACK DEMO
    # ===============================
    # Requirements:
    # 1. Create a Stack object.
    # 2. Add at least 4 values to the stack.
    # 3. Improve the print statements so they clearly explain what is happening.
    # 4. Demonstrate LIFO behavior.
    # 5. Show what happens when pop() is used on an empty stack.
    #
    # Edge Cases:
    # 6. Show what happens when peek() is used on an empty stack.
    # 7. Create a stack with only one item, remove it,
    #    and verify the stack is empty afterward.

    print("\n=== STACK DEMO ===")
    print("A text editor's undo history. Each action is pushed onto the stack,")
    print("and undo always reverses the most recent action first.\n")

    undo_stack = Stack()

    # (1) and (2): six actions pushed, oldest first.
    actions = ["Type heading", "Bold heading", "Insert table",
               "Paste chart", "Delete row 4", "Change font size"]
    for i, action in enumerate(actions, start=1):
        undo_stack.push(action)
        print(f"  PUSH #{i} -> '{action}' placed on TOP of the stack")
    print(f"  Stack now holds {undo_stack.size()} actions: {undo_stack.display()}")

    # peek() is read-only.
    print(f"\n  PEEK    -> top action is '{undo_stack.peek()}'")
    print(f"  Size after peek = {undo_stack.size()} (unchanged, because peek only reads)")

    # (4) Demonstrate LIFO: pops come back in reverse of push order.
    print("\n  Pressing UNDO three times:")
    for n in range(1, 4):
        print(f"  POP #{n}  -> undid '{undo_stack.pop()}'")
    print(f"  Stack now holds {undo_stack.size()} actions: {undo_stack.display()}")
    print("  Pushed 1-2-3-4-5-6 but popped 6-5-4. That reversal IS LIFO:")
    print("  the last value in was the first value out.")

    # (5) and (6) Edge cases on a stack that was never filled.
    print("\n  EDGE CASE - operations on a brand-new, empty stack:")
    empty_stack = Stack()
    print(f"  is_empty() = {empty_stack.is_empty()}")
    print(f"  POP     -> returned {empty_stack.pop()}  (underflow avoided, no crash)")
    print(f"  PEEK    -> returned {empty_stack.peek()}  (there is no top value to read)")
    print(f"  Size is still {empty_stack.size()}, so the failed calls changed nothing.")

    # (7) Edge case: single item stack drained back to empty.
    print("\n  EDGE CASE - a single-item stack, emptied and re-tested:")
    single_stack = Stack()
    single_stack.push("only-item")
    print(f"  After one push:  size = {single_stack.size()}, is_empty() = {single_stack.is_empty()}")
    print(f"  POP     -> removed '{single_stack.pop()}'")
    print(f"  After the pop:   size = {single_stack.size()}, is_empty() = {single_stack.is_empty()}")
    print(f"  POP again -> returned {single_stack.pop()}")
    print("  A drained stack behaves exactly like a new one, which is the correct result.")

    # ===============================
    # TODO (Student): QUEUE DEMO
    # ===============================
    # Requirements:
    # 1. Create a Queue object.
    # 2. Add at least 4 values to the queue.
    # 3. Improve the print statements so they clearly explain what is happening.
    # 4. Demonstrate FIFO behavior.
    # 5. Show what happens when dequeue() is used on an empty queue.
    #
    # Edge Cases:
    # 6. Show what happens when front() is used on an empty queue.
    # 7. Create a queue with only one item, remove it,
    #    and verify the queue is empty afterward.

    print("\n=== QUEUE DEMO ===")
    print("A shared office printer. Jobs are printed in the order they were sent,")
    print("so a job submitted later can never cut ahead of one already waiting.\n")

    print_queue = Queue()

    # (1) and (2): six jobs enqueued in submission order.
    jobs = ["Invoice_0912.pdf", "Payroll_Aug.xlsx", "Contract_draft.docx",
            "Site_map.png", "Board_pack.pdf", "Labels.pdf"]
    for i, job in enumerate(jobs, start=1):
        print_queue.enqueue(job)
        print(f"  ENQUEUE #{i} -> '{job}' joined the REAR of the queue")
    print(f"  Queue now holds {print_queue.size()} jobs: {print_queue.display()}")

    # front() is read-only.
    print(f"\n  FRONT    -> next job is '{print_queue.front()}'")
    print(f"  Size after front = {print_queue.size()} (unchanged, because front only reads)")

    # (4) Demonstrate FIFO: dequeues come back in the same order they arrived.
    print("\n  The printer processes three jobs:")
    for n in range(1, 4):
        print(f"  DEQUEUE #{n} -> printed '{print_queue.dequeue()}'")
    print(f"  Queue now holds {print_queue.size()} jobs: {print_queue.display()}")
    print("  Enqueued 1-2-3-4-5-6 and dequeued 1-2-3. That preserved order IS FIFO:")
    print("  the first value in was the first value out.")

    # (5) and (6) Edge cases on a queue that was never filled.
    print("\n  EDGE CASE - operations on a brand-new, empty queue:")
    empty_queue = Queue()
    print(f"  is_empty() = {empty_queue.is_empty()}")
    print(f"  DEQUEUE  -> returned {empty_queue.dequeue()}  (nothing is waiting to be served)")
    print(f"  FRONT    -> returned {empty_queue.front()}  (there is no next value to read)")
    print(f"  Size is still {empty_queue.size()}, so the failed calls changed nothing.")

    # (7) Edge case: single item queue drained back to empty.
    print("\n  EDGE CASE - a single-item queue, emptied and re-tested:")
    single_queue = Queue()
    single_queue.enqueue("only-job")
    print(f"  After one enqueue: size = {single_queue.size()}, is_empty() = {single_queue.is_empty()}")
    print(f"  DEQUEUE  -> removed '{single_queue.dequeue()}'")
    print(f"  After the dequeue: size = {single_queue.size()}, is_empty() = {single_queue.is_empty()}")
    print(f"  DEQUEUE again -> returned {single_queue.dequeue()}")
    print("  The queue returns cleanly to its empty state instead of raising an error.")

    # Real-world application of both structures together.
    custom_scenario()

    print("\n=== SUMMARY ===")
    print("Stack: ONE open end  -> newest value leaves first (LIFO).")
    print("Queue: TWO open ends -> oldest value leaves first (FIFO).")
    print("Both store one reference per value, so memory grows linearly, O(n).")


if __name__ == "__main__":
    main()
