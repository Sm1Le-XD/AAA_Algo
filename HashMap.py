class HashMap:
    def __init__(self):
        """Создаёт пустую таблицу"""
        self.capacity = 8
        self.table = [None] * self.capacity
        self.count = 0
        self.used = 0
        self.tombstone = object()

    def _hash(self, key):
        """Считает хеш ключа"""
        value = 0
        for char in key:
            value = value * 53 + ord(char) - 96
        return value

    def _index(self, hash_value):
        """Находит ячейку для хеша"""
        return hash_value % self.capacity

    def _check_load(self):
        """Проверяет заполненность таблицы"""
        if self.count * 4 > self.capacity * 3:
            self._rehash(self.capacity * 2)
        elif self.used * 4 > self.capacity * 3 or self.used - self.count > self.count:
            self._rehash(self.capacity)

    def _rehash(self, capacity):
        """Перестраивает таблицу"""
        old_table = self.table
        self.capacity = capacity
        self.table = [None] * self.capacity
        self.count = 0
        self.used = 0

        for item in old_table:
            if item is not None and item is not self.tombstone:
                hash_value, key, value = item
                index = self._index(hash_value)

                while self.table[index] is not None:
                    index = (index + 1) % self.capacity

                self.table[index] = item
                self.count += 1
                self.used += 1

    def put(self, key, value):
        """Добавляет или обновляет пару"""
        hash_value = self._hash(key)
        index = self._index(hash_value)
        first_tombstone = None

        if first_tombstone is not None:
            self.table[first_tombstone] = (hash_value, key, value)
            self.count += 1
            self._check_load()

        for _ in range(self.capacity):
            item = self.table[index]
            if item is None:
                if first_tombstone is not None:
                    index = first_tombstone
                else:
                    self.used += 1

                self.table[index] = (hash_value, key, value)
                self.count += 1
                self._check_load()
                return

            if item is self.tombstone:
                if first_tombstone is None:
                    first_tombstone = index
            elif item[0] == hash_value and item[1] == key:
                self.table[index] = (hash_value, key, value)
                return

            index = (index + 1) % self.capacity

    def get(self, key):
        """Возвращает значение по ключу"""
        hash_value = self._hash(key)
        index = self._index(hash_value)
        for _ in range(self.capacity):
            item = self.table[index]

            if item is None:
                return None
            if item is not self.tombstone and item[0] == hash_value and item[1] == key:
                return item[2]

            index = (index + 1) % self.capacity
        return None

    def delete(self, key):
        """Удаляет пару и возвращает значение"""
        hash_value = self._hash(key)
        index = self._index(hash_value)

        for _ in range(self.capacity):
            item = self.table[index]

            if item is None:
                return None
            if item is not self.tombstone and item[0] == hash_value and item[1] == key:
                self.table[index] = self.tombstone
                self.count -= 1
                return item[2]

            index = (index + 1) % self.capacity
        return None


hash_map = HashMap()
q = int(input())

for _ in range(q):
    c = input().split()
    if c[0] == "put":
        hash_map.put(c[1], int(c[2]))
    elif c[0] == "get":
        value = hash_map.get(c[1])
        print(value if value is not None else "Error")
    elif c[0] == "del":
        value = hash_map.delete(c[1])
        print(value if value is not None else "Error")
    else:
        print(hash_map.count)
