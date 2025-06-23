from jinnang.common.patterns import Singleton

print("--- Minimal Singleton Example ---")

class MySingleton(Singleton):
    def __init__(self, value=None):
        # The __init__ method is called every time, but we only initialize once.
        if not hasattr(self, '_initialized'):
            print(f"Initializing MySingleton with value: {value}")
            self.value = value
            self._initialized = True

# 1. First instantiation with a parameter. This is the correct way to initialize.
print("\n1. Initializing singleton instance:")
s1 = MySingleton(value="Initial Value")
print(f"s1.value: {s1.value}")

# 2. Get the existing instance using get_instance(). No parameters are allowed.
print("\n2. Retrieving existing instance:")
s2 = MySingleton.get_instance()
print(f"s2.value: {s2.value}")
print(f"s1 is s2: {s1 is s2}")

# 3. Attempting to re-initialize with a new parameter will raise a TypeError.
print("\n3. Attempting to re-initialize with new parameters (will raise TypeError):")
try:
    MySingleton(value="New Value")
except TypeError as e:
    print(f"Caught expected error: {e}")

# 4. Attempting to call get_instance() with parameters will also raise a TypeError.
print("\n4. Attempting to get_instance() with parameters (will raise TypeError):")
try:
    MySingleton.get_instance(value="Another Value")
except TypeError as e:
    print(f"Caught expected error: {e}")

print("\n--- Example Finished ---")