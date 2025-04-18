
## Cache util functions
##
## All the methods that allows to manipulate the cache used within the api 
##
## methods:
## - 
## 

import os
import json
import msgpack
import marisa_trie
import random
import string

class BinaryTrieCache:
    def __init__(self, trie_path_class, trie_path_specie, data_path):
        self.trie_class = marisa_trie.RecordTrie('Q')  # Trie for 'class' -> offset
        self.trie_specie = marisa_trie.RecordTrie('Q')  # Trie for 'specieName' -> offset
        self.trie_class.load(trie_path_class)
        self.trie_specie.load(trie_path_specie)
        self.data_file = open(data_path, "rb")

    def get_by_class_pattern(self, search_pattern):
        matching_records = []
        # Iterate over the class trie and find all records whose class contains the pattern
        for class_value in self.trie_class.keys():
            if search_pattern in class_value:
                matching_records.extend(self._get_records_by_class(class_value))
        return matching_records

    def get_by_specie_pattern(self, search_pattern):
        matching_records = []
        # Iterate over the specie trie and find all records whose specieName contains the pattern
        for specie_value in self.trie_specie.keys():
            if search_pattern in specie_value:
                matching_records.extend(self._get_records_by_specie(specie_value))
        return matching_records

    def _get_records_by_class(self, class_value):
        matching_records = []
        offsets = self.trie_class[class_value]
        for offset in offsets:
            matching_records.append(self._get_record_by_offset(offset))
        return matching_records

    def _get_records_by_specie(self, specie_value):
        matching_records = []
        offsets = self.trie_specie[specie_value]
        for offset in offsets:
            matching_records.append(self._get_record_by_offset(offset))
        return matching_records

    def _get_record_by_offset(self, offset):
        self.data_file.seek(offset)
        length_bytes = self.data_file.read(4)
        length = int.from_bytes(length_bytes, 'little')
        packed = self.data_file.read(length)
        return msgpack.unpackb(packed, strict_map_key=False)

    def close(self):
        self.data_file.close()


def random_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

def generate_dummy_data(n=10000):
    return {
        str(i): {"class": random.choice(["www", "abc", "xyz", "def"]),
                 "specieName": f"specie{random.randint(1, 100)}"}
        for i in range(n)
    }


def build_trie_and_data(data, data_path="data.bin", trie_class_path="index_class.trie", trie_specie_path="index_specie.trie"):
    offsets_class = {}
    offsets_specie = {}
    
    with open(data_path, "wb") as f:
        for key, record in data.items():
            class_value = record["class"]
            specie_value = record["specieName"]
            packed = msgpack.packb(record)
            offset = f.tell()
            # Prefix the length of the packed data
            f.write(len(packed).to_bytes(4, 'little'))
            f.write(packed)
            
            # Add offset to the class and specie index
            offsets_class.setdefault(class_value, []).append(offset)
            offsets_specie.setdefault(specie_value, []).append(offset)

    # Build MARISA trie for class and specie indexes
    class_items = [(k, tuple(v)) for k, v in offsets_class.items()]
    specie_items = [(k, tuple(v)) for k, v in offsets_specie.items()]

    trie_class = marisa_trie.RecordTrie('Q', class_items)
    trie_specie = marisa_trie.RecordTrie('Q', specie_items)

    trie_class.save(trie_class_path)
    trie_specie.save(trie_specie_path)


if __name__ == "__main__":
    # 1. Generate & build
    # json_data = generate_dummy_data(n=10000)
    with open("test.json", "w") as f:
        json_data = json.load(f)
    build_trie_and_data(json_data)

    # 2. Use the cache
    cache = BinaryTrieCache("index_class.trie", "index_specie.trie", "data.bin")

    # 3. Test search by pattern
    search_pattern = "abc"  # Try any pattern for class or specie name

    # Search for classes and species containing the pattern
    result_class = cache.get_by_class_pattern(search_pattern)
    result_specie = cache.get_by_specie_pattern(search_pattern)

    # Combine results
    results = result_class + result_specie

    # Print results as JSON
    print(json.dumps(results, indent=4))

    cache.close()
