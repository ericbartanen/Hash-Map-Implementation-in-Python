# Name: Eric Bartanen
# OSU Email: bartanee@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - Hash Maps
# Due Date: May 30, 2022
# Description: Implement a hash map with open addressing


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(None)

        self._capacity = capacity
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Update key/value pair in hash map. If key doesn't exist, add it to hash map. If load factor is >= 0.5, resize
        hash table.
        """

        if self.table_load() >= 0.5:
            new_capacity = self._capacity * 2
            self.resize_table(new_capacity)

        # Compute initial hash index
        hash = self._hash_function(key)
        hash_index = hash % self._capacity
        probe_index = hash_index

        # Look for available spot in hash table
        for i in range(1, self._capacity):

            # Empty spot in array
            if self._buckets[probe_index] is None:
                self._buckets[probe_index] = HashEntry(key, value)
                self._size += 1
                return

            # Tombstone in array
            if self._buckets[probe_index].is_tombstone is True:
                self._buckets[probe_index] = HashEntry(key, value)
                self._size += 1
                return

            # Duplicate key, update value
            if self._buckets[probe_index].key == key:
                self._buckets[probe_index].value = value
                return

            # Update probe index using quadratic probing
            probe_index = hash_index + (i ** 2)

            # If index goes off end of array, wrap around to beginning
            if probe_index > (self.get_capacity() - 1):
                probe_index = probe_index % self._capacity

    def table_load(self) -> float:
        """
        Return current hash table load factor.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Return number of empty buckets in hash table.
        """
        return self._capacity - self._size

    def resize_table(self, new_capacity: int) -> None:
        """
        Resize hash table with given capacity. All existing entries will be rehashed.
        """

        # control for invalid capacity
        if new_capacity < 1 or new_capacity < self._size:
            return

        new_hash_table = HashMap(new_capacity, self._hash_function)

        for i in range(self._capacity):
            entry = self._buckets[i]
            if entry is not None and entry.is_tombstone is False:
                new_hash_table.put(entry.key, entry.value)

        self._buckets = new_hash_table._buckets
        self._capacity = new_hash_table._capacity

    def get(self, key: str) -> object:
        """
        Return value of given key.
        """

        # Compute initial hash index
        hash = self._hash_function(key)
        hash_index = hash % self._capacity
        probe_index = hash_index

        # Look for key in array
        for i in range(self._capacity):

            # If key is found at initial hash index, return value
            if self._buckets[probe_index] is not None and self._buckets[probe_index].key == key and self._buckets[probe_index].is_tombstone is False:
                return self._buckets[probe_index].value

            # If key is not found, update probe index using quadratic probing
            probe_index = hash_index + (i ** 2)

            # If index goes off end of array, wrap around to beginning
            if probe_index > (self.get_capacity() - 1):
                probe_index = probe_index % self._capacity

        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if key is in hash table.
        """

        # Control for empty hash table
        if self._size == 0:
            return False

        # Compute initial hash index
        hash = self._hash_function(key)
        hash_index = hash % self._capacity
        probe_index = hash_index

        # Look for spot to place to hash entry
        for i in range(self._capacity):

            # Return True if key found
            if self._buckets[probe_index] is not None and self._buckets[probe_index].key == key and self._buckets[probe_index].is_tombstone is False:
                return True

            # Update probe index using quadratic probing
            probe_index = hash_index + (i ** 2)

            # If index goes off end of array, wrap around to beginning
            if probe_index > (self.get_capacity() - 1):
                probe_index = probe_index % self._capacity

        return False

    def remove(self, key: str) -> None:
        """
        Remove given key and associated value from hash table.
        """

        # Compute initial hash index
        hash = self._hash_function(key)
        hash_index = hash % self._capacity
        probe_index = hash_index

        # Look for spot to place to hash entry
        for i in range(self._capacity):

            # Remove key/value pair if key is found
            if self._buckets[probe_index] is not None and self._buckets[probe_index].key == key and self._buckets[probe_index].is_tombstone is False:
                self._buckets[probe_index].is_tombstone = True
                self._size -= 1
                return

            # Update probe index using quadratic probing
            probe_index = hash_index + (i ** 2)

            # If index goes off end of array, wrap around to beginning
            if probe_index > (self.get_capacity() - 1):
                probe_index = probe_index % self._capacity

    def clear(self) -> None:
        """
        Remove all elements from hash table. Capacity remains the same.
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._size = 0

    def get_keys(self) -> DynamicArray:
        """
        Return array with all keys in hash table
        """

        # Initialize new array to store keys
        key_array = DynamicArray()

        # iterate through all keys in hashmap and append to key_array
        for i in range(self._capacity):
            if self._buckets[i] is not None and self._buckets[i].is_tombstone is False:
                key_array.append(self._buckets[i].key)

        # return key_array
        return key_array

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() >= 0.5:
            print("Check that capacity gets updated during resize(); "
                  "don't wait until the next put()")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
