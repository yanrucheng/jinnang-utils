Hash Module
===========

.. automodule:: jinnang.hash
   :members:
   :undoc-members:
   :show-inheritance:

Overview
--------

The ``hash`` module provides utilities for creating stable hashes of objects and files. These functions are useful for:

- Caching results based on input parameters
- Generating unique identifiers for objects
- Checking file integrity

Examples
--------

Creating a stable hash for an object::

    from jinnang import hash
    
    data = {"name": "John", "age": 30}
    hash_value = hash.stable_hash(data)
    print(hash_value)  # Will always produce the same hash for the same data

Calculating an MD5 hash::

    from jinnang import hash
    
    text = "Hello, world!"
    md5_hash = hash.md5(text)
    print(md5_hash)

Generating a partial file hash::

    from jinnang import hash
    
    file_path = "path/to/large/file.txt"
    file_hash = hash.partial_file_hash(file_path)
    print(file_hash)  # Hash based on portions of the file