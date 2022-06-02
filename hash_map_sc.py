# Name: Eric Bartanen
# OSU Email: bartanee@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - Hash Maps
# Due Date: May 30, 2022
# Description: Implement a hash map with chaining


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(LinkedList())

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
        Update key/value pair in hash map. If key doesn't exist, add it to hash map.
        """

        # Compute hash index
        hash = self._hash_function(key)
        hash_index = hash % self._capacity

        bucket = self._buckets[hash_index]

        # If index already has items, check if key exists and update. Else, insert new node.
        matching_key = bucket.contains(key)
        if matching_key is not None:
            matching_key.value = value
        else:
            bucket.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns number of empty buckets in hash table.
        """
        empty_buckets = 0

        for i in range(self._capacity):
            if self._buckets[i].length() == 0:
                empty_buckets += 1

        return empty_buckets

    def table_load(self) -> float:
        """
        Return current hash table load factor.
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clear hash map of all contents.
        """
        self._buckets = DynamicArray()
        self._size = 0
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

    def resize_table(self, new_capacity: int) -> None:
        """
        Change capacity of hash table, rehash all existing key/value pairs.
        """

        # Control for invalid new_capacity
        if new_capacity < 1:
            return

        # Create new hash map with new capacity
        new_hash_map = HashMap(new_capacity, self._hash_function)

        # Put each element from the original hash map into the new hash map
        for i in range(self._capacity):
            if self._buckets[i].length() > 0:
                for node in self._buckets[i]:
                    new_hash_map.put(node.key, node.value)

        # Replace old hash map with new hash map
        self._capacity = new_capacity
        self._buckets = new_hash_map._buckets

    def get(self, key: str) -> object:
        """
        Return value associated with given key.
        """

        # Compute hash index
        hash = self._hash_function(key)
        hash_index = hash % self._capacity

        bucket = self._buckets[hash_index]

        # If key exists, return value. Else, return none.
        matching_key = bucket.contains(key)
        if matching_key is not None:
            return matching_key.value
        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        If key exists, return True. Else, return False.
        """

        # Control for empty hash map
        if self._size == 0:
            return False

        # Compute hash index
        hash = self._hash_function(key)
        hash_index = hash % self._capacity

        bucket = self._buckets[hash_index]

        # If key exists, return True. Else, return False.
        matching_key = bucket.contains(key)
        if matching_key is not None:
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Remove given key and associated value from hash map.
        """
        # Compute hash index
        hash = self._hash_function(key)
        hash_index = hash % self._capacity

        bucket = self._buckets[hash_index]

        # If key exists, remove key/value pair.
        matching_key = bucket.contains(key)
        if matching_key is not None:
            bucket.remove(key)
            self._size -= 1

    def get_keys(self) -> DynamicArray:
        """
        Return a dynamic array with all keys from hashmap
        """

        # Initialize new array to store keys
        key_array = DynamicArray()

        # iterate through all keys in hashmap and append to key_array
        for i in range(self._capacity):
            if self._buckets[i].length() > 0:
                for node in self._buckets[i]:
                    key_array.append(node.key)

        # return key_array
        return key_array


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Find the mode of given array. Return a tuple showing an array with the mode value(s) and the
    frequency of that value.
    """

    # Initialize hash map, mode array, and mode frequency counter
    map = HashMap(da.length() // 3, hash_function_1)
    mode_array = DynamicArray()
    mode_frequency = 0

    # Build hashmap with unique array values as keys. Increment value, which represents frequency, when duplicate keys
    # are found.

    for i in range(da.length()):

        # Find value of key being evaluated
        current_frequency = map.get(da[i])

        # If this is the first instance of a key, add to hash map.
        if current_frequency is None:
            map.put(da[i], 1)
            current_frequency = 1

        # If this is a duplicate value, increase value (frequency) in hash map
        else:
            current_frequency += 1
            map.put(da[i], current_frequency)

        # If current value (frequency) of key is greater than mode counter, update counter and mode array.
        if current_frequency > mode_frequency:
            mode_array = DynamicArray()
            mode_array.append(da[i])
            mode_frequency = current_frequency

        # If multiple keys share a high value, add key to mode array
        elif current_frequency == mode_frequency:
            mode_array.append(da[i])

    # Return mode array and frequency counter as tuple
    return mode_array, mode_frequency

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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    # map = HashMap(da.length() // 3, hash_function_1)
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        # map = HashMap(da.length() // 3, hash_function_2)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}\n")
