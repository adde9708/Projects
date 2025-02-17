import threading
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class Node:
    value: int
    next: Optional["Node"] = None
    mutex: threading.Lock = field(default_factory=threading.Lock, init=False)
    _padding: bytes = field(default=b"\x00" * (64 - (8 + 8)), init=False)


@dataclass
class Queue:
    dummy_node: Node = field(default_factory=lambda: Node(0), init=False)
    head: Node = field(init=False)
    tail: Node = field(init=False)
    mutex: threading.Lock = field(default_factory=threading.Lock, init=False)

    def __post_init__(self):
        self.head = self.dummy_node
        self.tail = self.dummy_node


def help_finish_enq(queue: Queue) -> None:
    next_node: Optional[Node] = queue.tail.next
    if next_node is not None and next_node == queue.tail:
        with queue.tail.mutex:
            with queue.head.mutex:
                queue.tail.next = next_node
                queue.tail = next_node


def enqueue(queue: Queue, value: int) -> None:
    node: Node = Node(value)
    with queue.tail.mutex:
        queue.tail.next = node
        help_finish_enq(queue)


def try_remove_front(queue: Queue, front: int) -> bool:
    with queue.mutex:
        head: Node = queue.head
        if head.next is not None:
            with head.mutex:
                next_node: Node = head.next
                if next_node.value == front:
                    head.next = next_node.next
                    return True
    return False


def main() -> None:
    q: Queue = Queue()
    front_value: int = 10
    enqueue(q, front_value)
    result: bool = try_remove_front(q, front_value)
    if result:
        print(f"Successfully removed front node: {front_value}")
    else:
        print("Failed to remove front node")


if __name__ == "__main__":
    main()
