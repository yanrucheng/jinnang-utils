from jinnang.common.patterns import Singleton

class MySingleton(Singleton):
    """
    An example of a Singleton class.
    The `__init__` method needs to be idempotent because it's called
    every time `MySingleton()` is invoked.
    """
    def __init__(self, value=None):
        # Pass arguments to the parent class to enable re-initialization checks.
        super().__init__(value=value)
        
        # The hasattr check ensures that the instance's state is set only once.
        # Without this, `s2 = MySingleton()` would reset `self.value` to `None`.
        if not hasattr(self, '_initialized_once'):
            self.value = value
            self._initialized_once = True

# --- Correct Usage ---
# 1. First call initializes the singleton instance with a value.
print("Initializing singleton...")
s1 = MySingleton(value="Hello, Singleton!")
print(f"Instance 1 value: {s1.value}")

# 2. Subsequent calls return the same instance without re-initializing.
print("\nRetrieving existing singleton...")
s2 = MySingleton.get_instance()
print(f"Instance 2 value: {s2.value}")
assert s1 is s2, "s1 and s2 should be the same instance"
print("s1 and s2 are the same instance.")


# --- Incorrect Usage (will raise TypeError) ---
# 1. Attempting to re-initialize with new parameters is not allowed.
print("\nAttempting to re-initialize with new parameters...")
try:
    MySingleton(value="New Value")
except TypeError as e:
    print(f"Caught expected error: {e}")

# 2. Calling get_instance() with parameters is not allowed.
print("\nAttempting to call get_instance() with parameters...")
try:
    MySingleton.get_instance(value="Another Value")
except TypeError as e:
    print(f"Caught expected error: {e}")