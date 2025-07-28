import timeit
import matplotlib.pyplot as plt
from functools import lru_cache
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


class SplayTreeNode:
    """
    Represents a node in the Splay Tree.
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class SplayTree:
    """
    Splay Tree implementation for storing and retrieving Fibonacci numbers.
    """

    def __init__(self):
        self.root = None

    def _splay(self, root, key):
        """
        Splays the tree to bring the node with the given key to the root.
        """
        if root is None or root.key == key:
            return root

        if key < root.key:
            if root.left is None:
                return root

            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._rotate_right(root)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right:
                    root.left = self._rotate_left(root.left)

            return self._rotate_right(root) if root.left else root

        else:
            if root.right is None:
                return root

            if key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._rotate_left(root)
            elif key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left:
                    root.right = self._rotate_right(root.right)

            return self._rotate_left(root) if root.right else root

    def _rotate_left(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _rotate_right(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def insert(self, key, value):
        """
        Inserts a new key-value pair into the tree.
        """
        if self.root is None:
            self.root = SplayTreeNode(key, value)
            return

        self.root = self._splay(self.root, key)

        if self.root.key == key:
            return

        new_node = SplayTreeNode(key, value)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None

        self.root = new_node

    def search(self, key):
        """
        Searches for a key in the tree and returns its value.
        """
        self.root = self._splay(self.root, key)
        if self.root and self.root.key == key:
            return self.root.value
        return None


@lru_cache(maxsize=None)
def fibonacci_lru(n):
    """
    Computes Fibonacci number using LRU caching.
    """
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


def fibonacci_splay(n, tree):
    """
    Computes Fibonacci number using Splay Tree.
    """
    result = tree.search(n)
    if result is not None:
        return result
    if n < 2:
        tree.insert(n, n)
        return n
    result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, result)
    return result


def benchmark():
    """
    Runs a benchmark comparing Fibonacci computation using LRU Cache and Splay Tree.
    """
    test_values = list(range(0, 951, 50))
    results = []

    print(
        Fore.CYAN + f"{'n':<10}{'LRU Cache Time (s)':<25}{'Splay Tree Time (s)'}")
    print("-" * 50)

    for n in test_values:
        tree = SplayTree()

        lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=5) / 5
        splay_time = timeit.timeit(lambda: fibonacci_splay(n, tree),
                                   number=5) / 5

        results.append((n, lru_time, splay_time))
        print(Fore.YELLOW + f"{n:<10}{lru_time:<25.8f}{splay_time:.8f}")

    x_vals, lru_times, splay_times = zip(*results)

    plt.figure(figsize=(10, 5))
    plt.plot(x_vals, lru_times, label='LRU Cache', marker='o')
    plt.plot(x_vals, splay_times, label='Splay Tree', marker='s')
    plt.xlabel('n (Fibonacci number index)')
    plt.ylabel('Average Execution Time (seconds)')
    plt.title('Fibonacci Computation Performance: LRU Cache vs Splay Tree')
    plt.legend()
    plt.grid()
    plt.show()


if __name__ == "__main__":
    benchmark()
