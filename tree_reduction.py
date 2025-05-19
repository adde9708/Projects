from typing import List, Callable, Optional
from dataclasses import dataclass, field
from functools import partial


@dataclass(frozen=True)
class Rule:
    lhs: str
    rhs: List[str]
    action: Callable[[List["Node"]], "Node"]


@dataclass(frozen=True)
class Grammar:
    rules: List[Rule]


@dataclass
class Node:
    op: str
    children: List["Node"] = field(default_factory=list)
    value: Optional[int] = None


def action_addition(children: List["Node"]) -> "Node":

    if len(children) < 3:
        raise ValueError("Addition action requires exactly 3 children.")

    left_value = children[0].value if children[0].value is not None else 0
    right_value = children[2].value if children[2].value is not None else 0

    node = Node("E", children)
    node.value = left_value + right_value
    return node


def action_multiplication(children: List["Node"]) -> "Node":

    if len(children) < 3:
        raise ValueError("Multiplication action requires exactly 3 children.")

    left_value = children[0].value if children[0].value is not None else 1
    right_value = children[2].value if children[2].value is not None else 1

    node = Node("T", children)
    node.value = left_value * right_value
    return node


def action_parenthesis(children: List["Node"]) -> "Node":

    if len(children) < 3:
        raise ValueError("Parenthesis action requires exactly 3 children.")

    return children[1]  # Assuming it's ( E ) → return E


def action_id(children: List["Node"]) -> "Node":
    node = Node("F", children)
    node.value = 1  # Assuming ID evaluates to 1
    return node


def identity_action(children: List["Node"]) -> "Node":
    return children[0]


def shift_reduce_parser(tokens: List[str]) -> Node:
    stack: List[Node] = []
    index = 0

    rules = Grammar(
        [
            Rule("E", ["E", "+", "T"], action_addition),
            Rule("E", ["T"], partial(identity_action)),
            Rule("T", ["T", "*", "F"], action_multiplication),
            Rule("T", ["F"], partial(identity_action)),
            Rule("F", ["(", "E", ")"], action_parenthesis),
            Rule("F", ["id"], action_id),
        ]
    )

    rules = rules.rules

    while index < len(tokens) or not stack:
        reduced = False
        # Try reducing from largest match
        for rule in range(len(rules)):
            rule = rules[rule]
            if (
                len(stack) >= len(rule.rhs)
                and {n.op for n in stack[-len(rule.rhs) :]} == rule.rhs
            ):
                children = stack[-len(rule.rhs) :]
                stack = stack[: -len(rule.rhs)]
                stack.append(rule.action(children))
                reduced = True
                break  # Stop after a successful reduction

        # If no reduction happened, shift next token
        if not reduced:
            if index >= len(tokens):
                raise ValueError("Parsing error: unable to reduce or shift.")

            stack.append(Node(tokens[index], [], 1 if tokens[index] == "id" else None))
            index += 1

    return stack[0]


def main():
    expression = ["id", "+", "(", "id", "*", "id", ")"]
    tree = shift_reduce_parser(expression)
    print(f"Final result: {tree}")


if __name__ == "__main__":
    main()
