class Node:
    def __init__(self, value, parent=None):
        self.value = value
        self.left = None
        self.right = None
        self.parent = parent
        self.height = 1


class AVLTree:
    """
    Реализация AVL-tree(Итеративная версия)
    Для выполнения я использовал материалы с сайта neerc.ifmo.ru
    ССылки:
    https://neerc.ifmo.ru/wiki/index.php?title=Дерево_поиска,_наивная_реализация
    https://neerc.ifmo.ru/wiki/index.php?title=АВЛ-дерево
    """

    def __init__(self):
        self.root = None

    @staticmethod
    def _height(node):
        return node.height if node is not None else 0

    def _update_height(self, node):
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node):
        return self._height(node.right) - self._height(node.left)

    def _replace_parent_child(self, parent, old_child, new_child):
        if parent is None:
            self.root = new_child
        elif parent.left is old_child:
            parent.left = new_child
        else:
            parent.right = new_child
        if new_child is not None:
            new_child.parent = parent

    def _rotate_left(self, node):
        new_root = node.right
        parent = node.parent
        middle = new_root.left

        self._replace_parent_child(parent, node, new_root)
        new_root.left = node
        node.parent = new_root
        node.right = middle
        if middle is not None:
            middle.parent = node

        self._update_height(node)
        self._update_height(new_root)
        return new_root

    def _rotate_right(self, node):
        new_root = node.left
        parent = node.parent
        middle = new_root.right

        self._replace_parent_child(parent, node, new_root)
        new_root.right = node
        node.parent = new_root
        node.left = middle
        if middle is not None:
            middle.parent = node

        self._update_height(node)
        self._update_height(new_root)
        return new_root

    def _rebalance_from(self, node):
        while node is not None:
            self._update_height(node)
            balance = self._balance_factor(node)

            if balance > 1:
                if self._balance_factor(node.right) < 0:
                    self._rotate_right(node.right)
                subtree_root = self._rotate_left(node)
            elif balance < -1:
                if self._balance_factor(node.left) > 0:
                    self._rotate_left(node.left)
                subtree_root = self._rotate_right(node)
            else:
                subtree_root = node

            node = subtree_root.parent

    def add(self, value):
        if self.root is None:
            self.root = Node(value)
            return

        parent = None
        current = self.root
        while current is not None:
            parent = current
            if value == current.value:
                return
            if value < current.value:
                current = current.left
            else:
                current = current.right

        new_node = Node(value, parent)
        if value < parent.value:
            parent.left = new_node
        else:
            parent.right = new_node
        self._rebalance_from(parent)

    def delete(self, value):
        node = self.root
        while node is not None and node.value != value:
            if value < node.value:
                node = node.left
            else:
                node = node.right

        if node is None:
            return

        if node.left is not None and node.right is not None:
            successor = node.right
            while successor.left is not None:
                successor = successor.left
            node.value = successor.value
            node = successor

        child = node.left if node.left is not None else node.right
        parent = node.parent
        self._replace_parent_child(parent, node, child)
        self._rebalance_from(parent)

    def exists(self, value):
        node = self.root
        while node is not None:
            if value == node.value:
                return True
            if value < node.value:
                node = node.left
            else:
                node = node.right
        return False

    def next(self, value):
        node = self.root
        candidate = None
        while node is not None:
            if node.value >= value:
                candidate = node.value
                node = node.left
            else:
                node = node.right
        return candidate

    def prev(self, value):
        node = self.root
        candidate = None
        while node is not None:
            if node.value <= value:
                candidate = node.value
                node = node.right
            else:
                node = node.left
        return candidate

    def height(self):
        return self._height(self.root)

    def preorder(self):
        if self.root is None:
            return ""

        values = []
        stack = [self.root]
        while stack:
            node = stack.pop()
            values.append(str(node.value))
            if node.right is not None:
                stack.append(node.right)
            if node.left is not None:
                stack.append(node.left)
        return " ".join(values)


def main():
    q = int(input())
    tree = AVLTree()

    for _ in range(q):
        req = input().split()
        com = req[0]

        if com == "add":
            tree.add(int(req[1]))
        elif com == "del":
            tree.delete(int(req[1]))
        elif com == "exists":
            print("YES" if tree.exists(int(req[1])) else "NO")
        elif com == "next":
            result = tree.next(int(req[1]))
            print(result if result is not None else "None")
        elif com == "prev":
            result = tree.prev(int(req[1]))
            print(result if result is not None else "None")
        elif com == "root":
            print(tree.root.value if tree.root is not None else "Empty")
        elif com == "height":
            print(tree.height())
        elif com == "print":
            print(tree.preorder())


if __name__ == "__main__":
    main()
