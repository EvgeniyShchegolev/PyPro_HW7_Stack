from typing import Any


class Item:
    """Класс объекта для односвязанного списка"""
    def __init__(self, item: Any) -> None:
        self.item = item
        self.prev_item = None


class Stack:
    """Класс стека"""
    def __init__(self) -> None:
        self.last_item = None
        self.length = 0

    def is_empty(self) -> bool:
        """Проверяет является ли стек пустым, возвращает bool значение"""
        if self.last_item:
            return False
        else:
            return True

    def push(self, item: Any) -> None:
        """Добавляет элемент на входе к конец стека"""
        new_item = Item(item)
        if self.last_item is None:
            self.last_item = new_item
        else:
            new_item.prev_item = self.last_item
            self.last_item = new_item
        self.length += 1

    def pop(self) -> Any:
        """Удаляет верхний элемент стека и возвращает гео"""
        if self.last_item is None:
            return
        rm_item = self.last_item
        self.last_item = None
        self.last_item = rm_item.prev_item
        self.length -= 1
        return rm_item

    def peek(self) -> Any or None:
        """Возвращает верхний элемент стека"""
        if self.last_item:
            return self.last_item.item

    def size(self) -> int:
        """Возвращает текущий размер стека"""
        return self.length


def is_balance(sequence: str) -> bool:
    """Проверяет является ли последовательность скобок сбалансированной"""
    open_parenthesis = ['(', '[', '{']
    close_parenthesis = [')', ']', '}']
    s = Stack()

    for char in sequence:
        if char in open_parenthesis:
            s.push(char)
        if char in close_parenthesis:
            if s.pop() is None:
                return False

    if s.is_empty():
        return True
    else:
        return False


if __name__ == "__main__":
    # s = Stack()
    # print(s.is_empty())
    # s.push('1')
    # s.push('2')
    # print(s.is_empty())
    # s.pop()
    # s.push('3')
    # print(s.size())
    # print(s.peek())
    print(is_balance('(((([])){}))'))
