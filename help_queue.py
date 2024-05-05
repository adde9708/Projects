import threading


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.lock = threading.Lock()


class Queue:
    def __init__(self):
        dummy_value = 0
        dummy_node = self.create_node(dummy_value)
        if dummy_node is not None:
            self.head = dummy_node
            self.tail = dummy_node
        else:
            self.head = None
            self.tail = None

    def create_node(self, value):
        node = Node(value)
        return node

    def try_remove_front(self, front):
        with self.head.lock:
            head = self.head
        with head.lock:
            next_node = head.next
        if next_node is not None:
            with next_node.lock:
                if next_node.value == front:
                    head.next = next_node.next
                    return True
        return False

    def help_finish_enq(self):
        with self.tail.lock:
            tail = self.tail
        with tail.lock:
            next_node = tail.next
            if next_node is not None:
                with next_node.lock:
                    if next_node == self.tail:
                        self.tail = next_node

    def enqueue(self, value):
        new_node = self.create_node(value)
        if new_node is not None:
            with self.tail.lock:
                self.tail.next = new_node
        else:
            self.tail = new_node


def main():
    q = Queue()

    front_value = 10
    q.enqueue(front_value)

    result = q.try_remove_front(front_value)
    print("Successfully removed front node:", result)


if __name__ == "__main__":
    main()
