from collections.abc import MutableMapping

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, key, value):
        if self.head is None:
            self.head = Node(key, value)
            return True  # Indicates a new node was added

        current = self.head
        while current:
            if current.key == key:
                current.value = value
                return False  # Indicates an existing node was updated
            if current.next is None:
                break
            current = current.next

        current.next = Node(key, value)
        return True

    def find(self, key):
        current = self.head
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None

    def delete(self, key):
        current = self.head
        prev = None
        while current:
            if current.key == key:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return True
            prev = current
            current = current.next
        return False

class Hashtable(MutableMapping):
    # polynomial constant, used for _hash
    P_CONSTANT = 37

    def __init__(self, capacity, default_value, load_factor, growth_factor):
        self._items = [None] * capacity # Initialize the list with None
        self.capacity = int(capacity)
        self.default_value = default_value
        self.load_factor = float(load_factor)
        self.growth_factor = int(growth_factor)
        self.size = 0  # The size of cells
        self.occupied_cells = 0 # Number of occupied cells

    def _hash(self, key):
        """
        This method takes in a string and returns an integer value.

        This particular hash function uses Horner's rule to compute a large polynomial.

        See https://www.cs.umd.edu/class/fall2019/cmsc420-0201/Lects/lect10-hash-basics.pdf

        DO NOT CHANGE THIS FUNCTION
        """
        val = 0
        for letter in key:
            val = self.P_CONSTANT * val + ord(letter)
        return val
    
    def _rehash(self):
        old_items = self._items
        self.capacity *= self.growth_factor
        self._items = [None] * self.capacity
        self.size = 0  # Reset the size
        self.occupied_cells = 0 # Reset the count of occupied cells
        for item in old_items:
            if item is not None:
                current = item.head
                while current:
                    self.__setitem__(current.key, current.value)
                    current = current.next


    def __setitem__(self, key, value):
        index = self._hash(key) % self.capacity
        if self._items[index] is None:
            self._items[index] = LinkedList()
            self.occupied_cells += 1
        new_node_added = self._items[index].insert(key, value)
        if new_node_added:
            self.size += 1
        if self.occupied_cells / self.capacity > self.load_factor:
            self._rehash()
        

    def __getitem__(self, key):
        index = self._hash(key) % self.capacity
        if self._items[index] is not None:
            found_value = self._items[index].find(key)
            if found_value is not None:
                return found_value
        return self.default_value

    def __delitem__(self, key):
        index = self._hash(key) % self.capacity
        if self._items[index] is not None and self._items[index].delete(key):
            self.size -= 1
            return
        raise KeyError(key)

    def __len__(self):
        return self.size

    def __iter__(self):
        """
        You do not need to implement __iter__ for this assignment.
        This stub is needed to satisfy `MutableMapping` however.)

        Note, by not implementing __iter__ your implementation of Markov will
        not be able to use things that depend upon it,
        that shouldn't be a problem but you'll want to keep that in mind.
        """
        raise NotImplementedError("__iter__ not implemented")
       